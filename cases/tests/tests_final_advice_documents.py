from django.urls import reverse
from rest_framework import status

from cases.enums import AdviceType, CaseTypeEnum, AdviceLevel
from cases.models import Advice
from licences.tests.factories import LicenceFactory
from test_helpers.clients import DataTestClient


class AdviceDocumentsTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.case = self.create_standard_application_case(self.organisation)
        self.licence = LicenceFactory(application=self.case)
        self.template = self.create_letter_template(name="Template", case_types=[CaseTypeEnum.SIEL.id])
        self.url = reverse("cases:final_advice_documents", kwargs={"pk": self.case.id})

    def test_get_final_advice_no_documents(self):
        self.create_advice(self.gov_user, self.case, "good", AdviceType.APPROVE, AdviceLevel.FINAL)
        self.create_advice(self.gov_user, self.case, "end_user", AdviceType.REFUSE, AdviceLevel.FINAL)

        expected_format = {
            AdviceType.APPROVE: {"value": AdviceType.get_text(AdviceType.APPROVE)},
            AdviceType.REFUSE: {"value": AdviceType.get_text(AdviceType.REFUSE)},
        }

        response = self.client.get(self.url, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["documents"], expected_format)

    def test_get_final_advice_with_document(self):
        self.create_advice(self.gov_user, self.case, "good", AdviceType.APPROVE, AdviceLevel.FINAL)
        self.create_advice(self.gov_user, self.case, "end_user", AdviceType.REFUSE, AdviceLevel.FINAL)

        document_one = self.create_generated_case_document(
            self.case, self.template, advice_type=AdviceType.APPROVE, licence=self.licence
        )
        document_two = self.create_generated_case_document(
            self.case, self.template, advice_type=AdviceType.REFUSE, licence=self.licence
        )

        response = self.client.get(self.url, **self.gov_headers)
        response_data = response.json()["documents"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[AdviceType.APPROVE]["value"], AdviceType.get_text(AdviceType.APPROVE))
        self.assertEqual(
            list(response_data[AdviceType.APPROVE]["document"].keys()), ["id", "advice_type", "user", "created_at"]
        )
        self.assertEqual(response_data[AdviceType.APPROVE]["document"]["id"], str(document_one.pk))

        self.assertEqual(response_data[AdviceType.REFUSE]["value"], AdviceType.get_text(AdviceType.REFUSE))
        self.assertEqual(
            list(response_data[AdviceType.REFUSE]["document"].keys()), ["id", "advice_type", "user", "created_at"]
        )
        self.assertEqual(response_data[AdviceType.REFUSE]["document"]["id"], str(document_two.pk))

    def test_get_final_advice_with_document_proviso(self):
        # Proviso advice should match up with approve document
        self.create_advice(self.gov_user, self.case, "good", AdviceType.PROVISO, AdviceLevel.FINAL)
        document = self.create_generated_case_document(
            self.case, self.template, advice_type=AdviceType.APPROVE, licence=self.licence
        )

        response = self.client.get(self.url, **self.gov_headers)
        response_data = response.json()["documents"][AdviceType.APPROVE]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["value"], AdviceType.get_text(AdviceType.APPROVE))
        self.assertEqual(response_data["document"]["id"], str(document.pk))
