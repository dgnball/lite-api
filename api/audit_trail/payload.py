from string import Formatter

from api.audit_trail.enums import AuditType
from api.audit_trail import formatters
from lite_content.lite_api import strings


class DefaultValueParameterFormatter(Formatter):
    """String formatter that allows strings to specify a default value
    for substitution parameters. The default is used when the parameter
    is not found in the substitution parameters dictionary (payload).

    Example: "the sky is {colour|blue}"
    Without default: "the sky is {colour}"
    """

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                try:
                    key, val = key.split("|")
                    try:
                        return kwds[key.strip()]
                    except KeyError:
                        return val.strip()
                except ValueError:
                    raise KeyError(f"Payload does not contain parameter '{key}' and message specifies no default value")
        else:
            return Formatter.get_value(key, args, kwds)


def format_payload(audit_type, payload):
    fmt = DefaultValueParameterFormatter()

    if callable(audit_type_format[audit_type]):
        text = audit_type_format[audit_type](**payload)
    else:
        text = fmt.format(audit_type_format[audit_type], **payload)
        if text[-1] not in [":", ".", "?"]:
            return f"{text}."

    return text


audit_type_format = {
    AuditType.OGL_CREATED: strings.Audit.CREATED_OGL,
    AuditType.OGL_FIELD_EDITED: strings.Audit.UPDATED_OGL,
    AuditType.OGL_MULTI_FIELD_EDITED: strings.Audit.UPDATED_MULTI_OGL_FIELD,
    AuditType.CREATED: strings.Audit.CREATED,
    AuditType.ADD_FLAGS: strings.Audit.ADD_FLAGS,
    AuditType.REMOVE_FLAGS: strings.Audit.REMOVE_FLAGS,
    AuditType.GOOD_REVIEWED: strings.Audit.GOOD_REVIEWED,
    AuditType.GOOD_ADD_FLAGS: strings.Audit.GOOD_ADD_FLAGS,
    AuditType.GOOD_REMOVE_FLAGS: strings.Audit.GOOD_REMOVE_FLAGS,
    AuditType.GOOD_ADD_REMOVE_FLAGS: strings.Audit.GOOD_ADD_REMOVE_FLAGS,
    AuditType.DESTINATION_ADD_FLAGS: strings.Audit.DESTINATION_ADD_FLAGS,
    AuditType.DESTINATION_REMOVE_FLAGS: strings.Audit.DESTINATION_REMOVE_FLAGS,
    AuditType.ADD_GOOD_TO_APPLICATION: strings.Audit.ADD_GOOD_TO_APPLICATION,
    AuditType.REMOVE_GOOD_FROM_APPLICATION: strings.Audit.REMOVE_GOOD_FROM_APPLICATION,
    AuditType.ADD_GOOD_TYPE_TO_APPLICATION: strings.Audit.ADD_GOOD_TYPE_TO_APPLICATION,
    AuditType.REMOVE_GOOD_TYPE_FROM_APPLICATION: strings.Audit.REMOVE_GOOD_TYPE_FROM_APPLICATION,
    AuditType.UPDATE_APPLICATION_END_USE_DETAIL: strings.Audit.UPDATE_APPLICATION_END_USE_DETAIL,
    AuditType.UPDATE_APPLICATION_TEMPORARY_EXPORT: strings.Audit.UPDATE_APPLICATION_TEMPORARY_EXPORT,
    AuditType.REMOVED_SITES_FROM_APPLICATION: strings.Audit.REMOVED_SITES_FROM_APPLICATION,
    AuditType.ADD_SITES_TO_APPLICATION: strings.Audit.ADD_SITES_TO_APPLICATION,
    AuditType.REMOVED_EXTERNAL_LOCATIONS_FROM_APPLICATION: strings.Audit.REMOVED_EXTERNAL_LOCATIONS_FROM_APPLICATION,
    AuditType.ADD_EXTERNAL_LOCATIONS_TO_APPLICATION: strings.Audit.ADD_EXTERNAL_LOCATIONS_TO_APPLICATION,
    AuditType.REMOVED_COUNTRIES_FROM_APPLICATION: strings.Audit.REMOVED_COUNTRIES_FROM_APPLICATION,
    AuditType.ADD_COUNTRIES_TO_APPLICATION: strings.Audit.ADD_COUNTRIES_TO_APPLICATION,
    AuditType.ADD_ADDITIONAL_CONTACT_TO_CASE: strings.Audit.ADD_ADDITIONAL_CONTACT_TO_CASE,
    AuditType.MOVE_CASE: strings.Audit.MOVE_CASE,
    AuditType.ASSIGN_CASE: strings.Audit.ASSIGN_CASE,
    AuditType.ASSIGN_USER_TO_CASE: strings.Audit.ASSIGN_USER_TO_CASE,
    AuditType.REMOVE_CASE: strings.Audit.REMOVE_CASE,
    AuditType.REMOVE_CASE_FROM_ALL_QUEUES: strings.Audit.REMOVE_CASE_FROM_ALL_QUEUES,
    AuditType.REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS: strings.Audit.REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS,
    AuditType.CLC_RESPONSE: strings.Audit.CLC_RESPONSE,
    AuditType.PV_GRADING_RESPONSE: strings.Audit.PV_GRADING_RESPONSE,
    AuditType.CREATED_CASE_NOTE: strings.Audit.CREATED_CASE_NOTE,
    AuditType.ECJU_QUERY: strings.Audit.ECJU_QUERY,
    AuditType.UPDATED_STATUS: strings.Audit.UPDATED_STATUS,
    AuditType.UPDATED_APPLICATION_NAME: strings.Audit.UPDATED_APPLICATION_NAME,
    AuditType.UPDATE_APPLICATION_LETTER_REFERENCE: strings.Audit.UPDATE_APPLICATION_LETTER_REFERENCE,
    AuditType.UPDATE_APPLICATION_F680_CLEARANCE_TYPES: strings.Audit.UPDATE_APPLICATION_F680_CLEARANCE_TYPES,
    AuditType.ADDED_APPLICATION_LETTER_REFERENCE: strings.Audit.ADDED_APPLICATION_LETTER_REFERENCE,
    AuditType.REMOVED_APPLICATION_LETTER_REFERENCE: strings.Audit.REMOVED_APPLICATION_LETTER_REFERENCE,
    AuditType.ASSIGNED_COUNTRIES_TO_GOOD: strings.Audit.ASSIGNED_COUNTRIES_TO_GOOD,
    AuditType.REMOVED_COUNTRIES_FROM_GOOD: strings.Audit.REMOVED_COUNTRIES_FROM_GOOD,
    AuditType.CREATED_FINAL_ADVICE: "added a decision",
    AuditType.CLEARED_FINAL_ADVICE: "cleared their decision",
    AuditType.CREATED_TEAM_ADVICE: strings.Audit.CREATED_TEAM_ADVICE,
    AuditType.CLEARED_TEAM_ADVICE: strings.Audit.CLEARED_TEAM_ADVICE,
    AuditType.REVIEW_COMBINE_ADVICE: "reviewed and combined {department} recommendations",
    AuditType.CREATED_USER_ADVICE: "added a recommendation",
    AuditType.CLEARED_USER_ADVICE: "cleared their recommendation",
    AuditType.ADD_PARTY: formatters.add_party,
    AuditType.REMOVE_PARTY: formatters.remove_party,
    AuditType.UPLOAD_PARTY_DOCUMENT: formatters.upload_party_document,
    AuditType.DELETE_PARTY_DOCUMENT: strings.Audit.DELETE_PARTY_DOCUMENT,
    AuditType.UPLOAD_APPLICATION_DOCUMENT: strings.Audit.UPLOAD_APPLICATION_DOCUMENT,
    AuditType.DELETE_APPLICATION_DOCUMENT: strings.Audit.DELETE_APPLICATION_DOCUMENT,
    AuditType.UPLOAD_CASE_DOCUMENT: strings.Audit.UPLOAD_CASE_DOCUMENT,
    AuditType.GENERATE_CASE_DOCUMENT: strings.Audit.GENERATE_CASE_DOCUMENT,
    AuditType.ADD_CASE_OFFICER_TO_CASE: strings.Audit.ADD_CASE_OFFICER_TO_CASE,
    AuditType.REMOVE_CASE_OFFICER_FROM_CASE: strings.Audit.REMOVE_CASE_OFFICER_FROM_CASE,
    AuditType.GRANTED_APPLICATION: strings.Audit.GRANTED_APPLICATION,
    AuditType.REINSTATED_APPLICATION: strings.Audit.REINSTATED_APPLICATION,
    AuditType.FINALISED_APPLICATION: strings.Audit.FINALISED_APPLICATION,
    AuditType.UNASSIGNED_QUEUES: strings.Audit.UNASSIGNED_QUEUES,
    AuditType.UNASSIGNED: strings.Audit.UNASSIGNED,
    AuditType.CREATED_DOCUMENT_TEMPLATE: strings.Audit.CREATED_DOCUMENT_TEMPLATE,
    AuditType.UPDATED_LETTER_TEMPLATE_NAME: strings.Audit.UPDATED_LETTER_TEMPLATE_NAME,
    AuditType.ADDED_LETTER_TEMPLATE_CASE_TYPES: strings.Audit.ADDED_LETTER_TEMPLATE_CASE_TYPES,
    AuditType.UPDATED_LETTER_TEMPLATE_CASE_TYPES: strings.Audit.UPDATED_LETTER_TEMPLATE_CASE_TYPES,
    AuditType.REMOVED_LETTER_TEMPLATE_CASE_TYPES: strings.Audit.REMOVED_LETTER_TEMPLATE_CASE_TYPES,
    AuditType.ADDED_LETTER_TEMPLATE_DECISIONS: strings.Audit.ADDED_LETTER_TEMPLATE_DECISIONS,
    AuditType.UPDATED_LETTER_TEMPLATE_DECISIONS: strings.Audit.UPDATED_LETTER_TEMPLATE_DECISIONS,
    AuditType.REMOVED_LETTER_TEMPLATE_DECISIONS: strings.Audit.REMOVED_LETTER_TEMPLATE_DECISIONS,
    AuditType.UPDATED_LETTER_TEMPLATE_PARAGRAPHS: strings.Audit.UPDATED_LETTER_TEMPLATE_PARAGRAPHS,
    AuditType.REMOVED_LETTER_TEMPLATE_PARAGRAPHS: strings.Audit.REMOVED_LETTER_TEMPLATE_PARAGRAPHS,
    AuditType.ADDED_LETTER_TEMPLATE_PARAGRAPHS: strings.Audit.ADDED_LETTER_TEMPLATE_PARAGRAPHS,
    AuditType.UPDATED_LETTER_TEMPLATE_LAYOUT: strings.Audit.UPDATED_LETTER_TEMPLATE_LAYOUT,
    AuditType.UPDATED_LETTER_TEMPLATE_PARAGRAPHS_ORDERING: strings.Audit.UPDATED_LETTER_TEMPLATE_PARAGRAPHS_ORDERING,
    AuditType.UPDATED_LETTER_TEMPLATE_INCLUDE_DIGITAL_SIGNATURE: strings.Audit.UPDATED_LETTER_TEMPLATE_INCLUDE_DIGITAL_SIGNATURE,
    AuditType.CREATED_PICKLIST: strings.Audit.CREATED_PICKLIST,
    AuditType.UPDATED_PICKLIST_TEXT: strings.Audit.UPDATED_PICKLIST_TEXT,
    AuditType.UPDATED_PICKLIST_NAME: strings.Audit.UPDATED_PICKLIST_NAME,
    AuditType.DEACTIVATE_PICKLIST: strings.Audit.DEACTIVATE_PICKLIST,
    AuditType.REACTIVATE_PICKLIST: strings.Audit.REACTIVATE_PICKLIST,
    AuditType.UPDATED_EXHIBITION_DETAILS_TITLE: strings.Audit.UPDATED_EXHIBITION_DETAILS_TITLE,
    AuditType.UPDATED_EXHIBITION_DETAILS_START_DATE: strings.Audit.UPDATED_EXHIBITION_DETAILS_START_DATE,
    AuditType.UPDATED_EXHIBITION_DETAILS_REQUIRED_BY_DATE: strings.Audit.UPDATED_EXHIBITION_DETAILS_REQUIRED_BY_DATE,
    AuditType.UPDATED_EXHIBITION_DETAILS_REASON_FOR_CLEARANCE: strings.Audit.UPDATED_EXHIBITION_DETAILS_REASON_FOR_CLEARANCE,
    AuditType.UPDATED_ROUTE_OF_GOODS: strings.Audit.UPDATED_ROUTE_OF_GOODS,
    AuditType.RERUN_ROUTING_RULES: strings.Audit.RERUN_ROUTING_RULES,
    AuditType.UPDATED_ORGANISATION: strings.Audit.UPDATED_ORGANISATION,
    AuditType.CREATED_ORGANISATION: strings.Audit.CREATED_ORGANISATION,
    AuditType.REGISTER_ORGANISATION: strings.Audit.REGISTER_ORGANISATION,
    AuditType.REJECTED_ORGANISATION: strings.Audit.REJECTED_ORGANISATION,
    AuditType.APPROVED_ORGANISATION: strings.Audit.APPROVED_ORGANISATION,
    AuditType.REMOVED_FLAG_ON_ORGANISATION: strings.Audit.REMOVED_FLAG_ON_ORGANISATION,
    AuditType.ADDED_FLAG_ON_ORGANISATION: strings.Audit.ADDED_FLAG_ON_ORGANISATION,
    AuditType.ENFORCEMENT_CHECK: "exported the case for enforcement checks",
    AuditType.UPDATED_SITE: strings.Audit.UPDATED_SITE,
    AuditType.CREATED_SITE: strings.Audit.CREATED_SITE,
    AuditType.UPDATED_SITE_NAME: strings.Audit.UPDATED_SITE_NAME,
    AuditType.COMPLIANCE_SITE_CASE_CREATE: strings.Audit.COMPLIANCE_SITE_CASE_CREATE,
    AuditType.COMPLIANCE_SITE_CASE_NEW_LICENCE: strings.Audit.COMPLIANCE_SITE_CASE_NEW_LICENCE,
    AuditType.ADDED_NEXT_REVIEW_DATE: strings.Audit.ADDED_NEXT_REVIEW_DATE,
    AuditType.EDITED_NEXT_REVIEW_DATE: strings.Audit.EDITED_NEXT_REVIEW_DATE,
    AuditType.REMOVED_NEXT_REVIEW_DATE: strings.Audit.REMOVED_NEXT_REVIEW_DATE,
    AuditType.COMPLIANCE_VISIT_CASE_CREATED: strings.Audit.COMPLIANCE_VISIT_CASE_CREATED,
    AuditType.COMPLIANCE_VISIT_CASE_UPDATED: strings.Audit.COMPLIANCE_VISIT_CASE_UPDATED,
    AuditType.COMPLIANCE_PEOPLE_PRESENT_CREATED: strings.Audit.COMPLIANCE_PEOPLE_PRESENT_CREATED,
    AuditType.COMPLIANCE_PEOPLE_PRESENT_UPDATED: strings.Audit.COMPLIANCE_PEOPLE_PRESENT_UPDATED,
    AuditType.COMPLIANCE_PEOPLE_PRESENT_DELETED: strings.Audit.COMPLIANCE_PEOPLE_PRESENT_DELETED,
    AuditType.UPDATED_GOOD_ON_DESTINATION_MATRIX: strings.Audit.UPDATED_GOOD_ON_DESTINATION_MATRIX,
    AuditType.LICENCE_UPDATED_GOOD_USAGE: strings.Audit.LICENCE_UPDATED_GOOD_USAGE,
    AuditType.OGEL_REISSUED: strings.Audit.OGEL_REISSUED,
    AuditType.LICENCE_UPDATED_STATUS: strings.Audit.LICENCE_UPDATED_STATUS,
    AuditType.DOCUMENT_ON_ORGANISATION_CREATE: "added {document_type} '{file_name}' to organization",
    AuditType.DOCUMENT_ON_ORGANISATION_DELETE: "removed {document_type} '{file_name}' from organization",
    AuditType.DOCUMENT_ON_ORGANISATION_UPDATE: "updated {document_type} '{file_name}' from organization",
    AuditType.REPORT_SUMMARY_UPDATED: "updated ARS for {good_name} from {old_report_summary} to {report_summary}",
    AuditType.COUNTERSIGN_ADVICE: "countersigned all {department|} recommendations",
    AuditType.UPDATED_SERIAL_NUMBERS: "updated serial numbers on '{good_name}'",
}
