from api.data_workspace.serializers import EcjuQuerySerializer, CaseAssignmentSerializer
from api.cases.tests.factories import EcjuQueryFactory, CaseAssignmentFactory


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
