from api.audit_trail.models import AuditType
from api.audit_trail.tests.factories import AuditFactory
from api.data_workspace.serializers import (
    AuditMoveCaseSerializer,
    CaseAssignmentSerializer,
    EcjuQuerySerializer,
    AuditUpdatedCaseStatusSerializer,
    AuditUpdatedLicenceStatusSerializer,
    LicenceWithoutGoodsSerializer,
)
from api.cases.tests.factories import EcjuQueryFactory, CaseAssignmentFactory
from api.licences.tests.factories import LicenceFactory
from api.staticdata.statuses.models import CaseStatus


def test_EcjuQuerySerializer(db):
    ecju_query = EcjuQueryFactory()
    serialized = EcjuQuerySerializer(ecju_query)
    assert serialized.data
    assert "question" in serialized.data
    assert "response" in serialized.data


def test_CaseAssignmentSerializer(db):
    case_assignment = CaseAssignmentFactory()
    serialized = CaseAssignmentSerializer(case_assignment)
    expected_fields = {"case", "user", "id", "queue", "created_at", "updated_at"}
    assert set(serialized.data.keys()) == expected_fields


def test_AuditMoveCaseSerializer(db):
    audit = AuditFactory(verb=AuditType.MOVE_CASE, payload={"queues": ["test_queue_1", "test_queue_2"]})
    audit.queue = "test_queue_1"
    serialized = AuditMoveCaseSerializer(audit)
    expected_fields = {"created_at", "user", "case", "queue"}
    assert set(serialized.data.keys()) == expected_fields


def test_AuditUpdatedCaseStatusSerializer(db):
    audit = AuditFactory(
        verb=AuditType.UPDATED_STATUS, payload={"status": {"new": "finalised", "old": "under_final_review"}}
    )
    serialized = AuditUpdatedCaseStatusSerializer(audit)
    expected_fields = {"created_at", "user", "case", "status"}
    assert set(serialized.data.keys()) == expected_fields


def test_AuditUpdatedLicenceStatusSerializer(db):
    audit = AuditFactory(
        verb=AuditType.LICENCE_UPDATED_STATUS, payload={"status": "issued", "licence": "GBSIEL/2021/0000711/P"}
    )
    serialized = AuditUpdatedLicenceStatusSerializer(audit)
    expected_fields = {"created_at", "user", "case", "licence", "status"}
    assert set(serialized.data.keys()) == expected_fields


def test_LicenceWithoutGoodsSerializer(db):
    licence = LicenceFactory()
    serialized = LicenceWithoutGoodsSerializer(licence)
    expected_fields = {
        "id",
        "reference_code",
        "status",
        "application",
        "goods",
    }
    assert set(serialized.data) == expected_fields
    assert serialized.data["goods"] == []
