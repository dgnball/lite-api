from api.audit_trail import service as audit_trail_service
from api.audit_trail.enums import AuditType
from api.cases.enums import AdviceLevel, AdviceType, CountersignOrder
from api.cases.models import CountersignAdvice
from api.flags.models import Flag
from api.flags.enums import FlagStatuses
from api.teams.enums import TeamIdEnum
from api.teams.models import Team

from lite_routing.routing_rules_internal.enums import FlagsEnum


class CounterSignatureIncompleteError(Exception):
    """
    Exception raised if we countersignatures are incomplete
     - When required countersignatures are missing
     - When required countersignatures are present but if atleast one of them is rejected
    """

    pass


class CountersignInvalidAdviceTypeError(Exception):
    """
    Exception raised if we encounter invalid Advice types for countersigning, eg REFUSE type
    """

    pass


def lu_countersigning_flags_all():
    return Flag.objects.filter(
        id__in=[
            FlagsEnum.LU_COUNTER_REQUIRED,
            FlagsEnum.LU_SENIOR_MANAGER_CHECK_REQUIRED,
            FlagsEnum.MANPADS,
            FlagsEnum.AP_LANDMINE,
        ],
        status=FlagStatuses.ACTIVE,
    )


def lu_sr_mgr_countersigning_flags():
    return Flag.objects.filter(
        id__in=[
            FlagsEnum.LU_SENIOR_MANAGER_CHECK_REQUIRED,
            FlagsEnum.MANPADS,
        ],
        status=FlagStatuses.ACTIVE,
    )


def get_lu_required_countersign_orders(case):
    countersign_orders = []

    all_case_flags = {item for item in case.parameter_set() if isinstance(item, Flag)}
    countersign_flags = all_case_flags.intersection(lu_countersigning_flags_all())
    if not countersign_flags:
        return countersign_orders

    # We are here means atleast first countersign is required so
    # check if second countersign is also required
    countersign_orders = [CountersignOrder.FIRST_COUNTERSIGN]
    lu_sr_mgr_countersign_required = countersign_flags.intersection(lu_sr_mgr_countersigning_flags())
    if lu_sr_mgr_countersign_required:
        countersign_orders = [CountersignOrder.FIRST_COUNTERSIGN, CountersignOrder.SECOND_COUNTERSIGN]

    return countersign_orders


def check_lu_refused_outcome_exists(case, team, countersign_orders):
    # If a Case is being refused then it won't reach countersigning queues but
    # if it is routed unexpectedly then we need to catch and raise error
    return CountersignAdvice.objects.filter(
        order__in=countersign_orders,
        valid=True,
        case=case,
        advice__user__team=team,
        advice__level=AdviceLevel.FINAL,
        advice__type=AdviceType.REFUSE,
    ).exists()


def ensure_lu_countersign_complete(application):
    """
    If a Case requires LU countersigning then it ensure necessary countersignatures
    are present and approved.

    Certain cases need double countersigning so it checks for countersignatures
    of both orders (FIRST_COUNTERSIGN, SECOND_COUNTERSIGN) where applicable.

    Once the countersignatures are valid then it removes the flags that blocks
    finalising the Case.
    """
    case = application.get_case()
    lu_team = Team.objects.get(id=TeamIdEnum.LICENSING_UNIT)

    all_case_flags = {item for item in case.parameter_set() if isinstance(item, Flag)}
    countersign_flags = all_case_flags.intersection(lu_countersigning_flags_all())
    countersign_orders = get_lu_required_countersign_orders(case)

    if check_lu_refused_outcome_exists(case, lu_team, countersign_orders):
        raise CountersignInvalidAdviceTypeError(
            "This application cannot be finalised as the countersigning has been refused"
        )

    # check countersignatures for the required orders
    for order in countersign_orders:
        countersign_advice = CountersignAdvice.objects.filter(
            order=order,
            valid=True,
            case=case,
            advice__user__team=lu_team,
            advice__level=AdviceLevel.FINAL,
            advice__type__in=[AdviceType.APPROVE, AdviceType.PROVISO],
        )
        if not (countersign_advice and all(advice.outcome_accepted for advice in countersign_advice)):
            raise CounterSignatureIncompleteError(
                "This applications requires countersigning and the required countersignatures are not completed"
            )

    # Remove countersigning flags that block finalising
    # MANPADS and AP_LANDMINE are also countersigning flags but they are related
    # to product attributes and we want to retain them, they also don't
    # block finalising the case but if they are applied then we need to ensure
    # necessary countersignatures are present before finalising the Case
    countersign_process_flags = Flag.objects.filter(
        id__in=[
            FlagsEnum.LU_COUNTER_REQUIRED,
            FlagsEnum.LU_SENIOR_MANAGER_CHECK_REQUIRED,
        ],
        status=FlagStatuses.ACTIVE,
    )
    flags_to_remove = countersign_flags.intersection(countersign_process_flags)
    for party_on_application in application.parties.all():
        if not flags_to_remove.intersection(party_on_application.party.flags.all()):
            continue

        party_on_application.party.flags.remove(*flags_to_remove)
        audit_trail_service.create_system_user_audit(
            verb=AuditType.DESTINATION_REMOVE_FLAGS,
            action_object=party_on_application.party,
            target=case,
            payload={
                "removed_flags": [flag.name for flag in flags_to_remove],
                "destination_name": party_on_application.party.name,
                "additional_text": "Removing flags as required countersignatures present and approved",
            },
        )


def mark_lu_rejected_countersignatures_as_invalid(case):
    """
    When countersigning is rejected and sent back then caseworkers edit their outcome before
    moving the case forward again for countersigning. This is now considered as if it has
    come for the first time and possibly by a different officer so we can mark them as invalid.
    They are still available on the case for the officer to check previous history but to prevent
    using the same (eg by editing) these are marked as invalid.

    Countersigning officers will provide new countersignatures to move it forward.

    This is only done if there is a rejected countersignature. If all are approved it will go
    back to caseworker for finalising.
    """
    lu_team = Team.objects.get(id=TeamIdEnum.LICENSING_UNIT)
    countersign_orders = get_lu_required_countersign_orders(case)

    # If the original outcome is refused then they don't get routed to countersigning queues
    # but if something is routed unintentionally then guard against those cases
    if check_lu_refused_outcome_exists(case, lu_team, countersign_orders):
        raise CountersignInvalidAdviceTypeError("Cannot invalidate countersignatures as the outcome is refused")

    # check if any rejected countersignatures present
    countersign_orders_to_invalidate = []
    for order in countersign_orders:
        countersign_advice = CountersignAdvice.objects.filter(
            order=order,
            valid=True,
            case=case,
            outcome_accepted=False,
            advice__user__team=lu_team,
            advice__level=AdviceLevel.FINAL,
            advice__type__in=[AdviceType.APPROVE, AdviceType.PROVISO],
        )
        if countersign_advice.exists():
            countersign_orders_to_invalidate.append(order)

    # nothing to invalidate if all countersignatures are approved
    if not countersign_orders_to_invalidate:
        return

    # Mark countersignatures as invalid in the required orders
    # Usually either first or second countersign is rejected but not both because
    # routing engine would've moved the Case back when first countersign is rejected
    # But in the case where second countersign is rejected, then we also need to
    # invalidate first countersign hence take the max_order
    max_order = max(countersign_orders_to_invalidate)
    for order in range(1, max_order + 1):  # +1 because the end is not included
        countersign_advice = CountersignAdvice.objects.filter(
            order=order,
            valid=True,
            case=case,
            advice__user__team=lu_team,
            advice__level=AdviceLevel.FINAL,
            advice__type__in=[AdviceType.APPROVE, AdviceType.PROVISO],
        )
        countersign_advice.update(valid=False)
