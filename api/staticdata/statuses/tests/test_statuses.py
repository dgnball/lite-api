import pytest
from parameterized import parameterized

from api.staticdata.statuses.libraries.get_case_status import get_case_status_by_status
from api.applications.libraries.case_status_helpers import get_case_statuses


@pytest.mark.django_db
class TestCaseStatus:
    @parameterized.expand(get_case_statuses(read_only=True))
    def test_read_only_case_statuses(self, status):
        read_only_case_status = get_case_status_by_status(status)
        assert read_only_case_status.is_read_only is True

    @parameterized.expand(get_case_statuses(read_only=False))
    def test_editable_case_statuses(self, status):
        editable_case_status = get_case_status_by_status(status)
        assert editable_case_status.is_read_only is False
