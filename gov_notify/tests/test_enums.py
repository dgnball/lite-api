from unittest import mock

from parameterized import parameterized
from rest_framework.test import APITestCase

from gov_notify.enums import TemplateType


class TemplateTypeTests(APITestCase):
    @parameterized.expand(
        [
            (TemplateType.ECJU_COMPLIANCE_CREATED, "b23f4c55-fef0-4d8f-a10b-1ad7f8e7c672"),
            (TemplateType.APPLICATION_STATUS, "b9c3403a-8d09-416e-acd3-99baabf5b043"),
            (TemplateType.EXPORTER_REGISTERED_NEW_ORG, "6096c45e-0cbb-4ecd-a7a9-0ad674e1d2c0"),
            (TemplateType.EXPORTER_USER_ADDED, "c9b67dca-0916-453a-99c0-70ba563e1bdd"),
        ]
    )
    def test_template_id(self, template_type, expected_template_id):
        assert template_type.template_id == expected_template_id
