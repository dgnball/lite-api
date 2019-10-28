from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from applications.models import BaseApplication
from test_helpers.clients import DataTestClient


class DeleteApplication(DataTestClient):
    def setUp(self):
        super().setUp()

    def test_delete_draft_application_as_exporter_user_success(self):
        draft = self.create_standard_application(self.organisation)
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse('applications:application', kwargs={'pk': draft.id})

        response = self.client.delete(url, **self.exporter_headers)

        self.assertTrue(response.status_code, HTTP_200_OK)
        self.assertEqual(number_of_applications - 1, BaseApplication.objects.all().count())

    def test_delete_draft_application_as_gov_user_failure(self):
        draft = self.create_standard_application(self.organisation)
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse('applications:application', kwargs={'pk': draft.id})

        response = self.client.delete(url, **self.gov_headers)

        self.assertTrue(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(number_of_applications, BaseApplication.objects.all().count())

    def test_delete_application_as_exporter_user_failure(self):
        application = self.create_standard_application(self.organisation)
        self.submit_application(application)
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse('applications:application', kwargs={'pk': application.id})

        response = self.client.delete(url, **self.exporter_headers)

        self.assertTrue(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_applications, BaseApplication.objects.all().count())
