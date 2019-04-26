from django.urls import path, include
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from applications.models import Application, GoodOnApplication
from applications.libraries.ValidateFormFields import ValidateFormFields
from drafts.models import Draft, GoodOnDraft
from cases.models import Case
from goods.models import Good
from queues.models import Queue
from reversion.models import Version
from drafts.tests import DraftTestHelpers


class ApplicationsTests(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('drafts/', include('drafts.urls')),
        path('applications/', include('applications.urls')),
        path('organisations/', include('organisations.urls'))
    ]

    client = APIClient()

    def setUp(self):
        self.draft_test_helper = DraftTestHelpers(name='name')
        self.headers = {'HTTP_USER_ID': str(self.draft_test_helper.user.id)}

    def test_that_goods_are_added_to_application_when_submitted(self):
        draft = DraftTestHelpers.complete_draft('test', self.draft_test_helper.organisation)
        good = DraftTestHelpers.create_controlled_good('test good', self.draft_test_helper.organisation)
        good_on_draft_1 = GoodOnDraft(draft=draft, good=good, quantity=20, unit='kg', value=400)
        good_on_draft_2 = GoodOnDraft(draft=draft, good=good, quantity=90, unit='kg', value=500)
        good_on_draft_1.save()
        good_on_draft_2.save()

        url = '/applications/'
        data = {'id': draft.id}
        response = self.client.post(url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GoodOnApplication.objects.count(), 2)
        application = Application.objects.get()
        self.assertEqual(GoodOnApplication.objects.filter(application=application).count(), 2)

    def test_create_application_case_and_addition_to_queue(self):
        """
            Test whether we can create a draft first and then submit it as an application
        """

        draft = DraftTestHelpers.complete_draft(name='test', org=self.draft_test_helper.organisation)
        draft_id = draft.id
        self.assertEqual(Queue.objects.get(pk='00000000-0000-0000-0000-000000000001').cases.count(), 0)
        url = '/applications/'
        data = {'id': draft_id}
        response = self.client.post(url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.get(pk=draft_id).status.name, "submitted")
        self.assertEqual(Case.objects.get(application=Application.objects.get(pk=draft_id)).application,
                         Application.objects.get(pk=draft_id))
        self.assertEqual(Queue.objects.get(pk='00000000-0000-0000-0000-000000000001').cases.count(), 1)

    def test_create_application_with_invalid_id(self):
        """
            Ensure we cannot create a new application object with an invalid draft id.
        """
        draft_id = '90D6C724-0339-425A-99D2-9D2B8E864EC7'

        draft = DraftTestHelpers.complete_draft(name='test', org=self.draft_test_helper.organisation)

        url = '/applications/'
        data = {'id': draft_id}
        response = self.client.post(url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_application_without_id(self):
        """
            Ensure we cannot create a new application object without a draft id.
        """
        complete_draft = Application(id='90D6C724-0339-425A-99D2-9D2B8E864EC7',
                                     name='Test',
                                     destination='Poland',
                                     activity='Trade',
                                     usage='Fun')
        complete_draft.save()

        url = '/applications/'
        response = self.client.post(url, {}, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(Application.objects.filter(id='90D6C724-0339-425A-99D2-9D2B8E864EC7')), 1)

    def test_reject_submit_if_usage_data_is_missing(self):
        incomplete_draft = Application(id='90D6C724-0339-425A-99D2-9D2B8E864EC7',
                                       name='Test',
                                       destination='Poland',
                                       activity='Trade')

        self.assertEqual(ValidateFormFields(incomplete_draft).usage, "Usage cannot be blank")
        self.assertEqual(ValidateFormFields(incomplete_draft).ready_for_submission, False)

    def test_reject_submit_if_activity_data_is_missing(self):
        incomplete_draft = Application(id='90D6C724-0339-425A-99D2-9D2B8E864EC7',
                                       name='Test',
                                       destination='Poland')

        self.assertEqual(ValidateFormFields(incomplete_draft).activity, "Activity cannot be blank")
        self.assertEqual(ValidateFormFields(incomplete_draft).ready_for_submission, False)

    def test_reject_submit_if_destination_data_is_missing(self):
        incomplete_draft = Application(id='90D6C724-0339-425A-99D2-9D2B8E864EC7',
                                       name='Test',
                                       activity='Trade')

        self.assertEqual(ValidateFormFields(incomplete_draft).destination, "Destination cannot be blank")
        self.assertEqual(ValidateFormFields(incomplete_draft).ready_for_submission, False)



    def test_accept_submit_if_form_is_ready_for_submission(self):
        complete_draft = Application(id='90D6C724-0339-425A-99D2-9D2B8E864EC7',
                                     name='Test',
                                     destination='Poland',
                                     activity='Trade',
                                     usage='Trade')

        self.assertEqual(ValidateFormFields(complete_draft).ready_for_submission, True)

    def test_reject_submit_if_all_fields_missing(self):
        empty_draft = Application()
        self.assertEqual(ValidateFormFields(empty_draft).destination, 'Destination cannot be blank')
        self.assertEqual(ValidateFormFields(empty_draft).activity, 'Activity cannot be blank')
        self.assertEqual(ValidateFormFields(empty_draft).usage, 'Usage cannot be blank')
        self.assertEqual(ValidateFormFields(empty_draft).ready_for_submission, False)

    def test_update_status_of_an_application(self):
        application = Application(id='90d6c724-0339-425a-99d2-9d2b8e864ec7',
                                  name='Test',
                                  destination='Poland',
                                  activity='Trade',
                                  usage='Trade')
        application.save()
        url = '/applications/' + str(application.id) + '/'
        data = {'id': application.id, 'status': 'withdrawn'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.get(pk=application.id).status.name, "withdrawn")


class ApplicationTestHelpers:
    urlpatterns = [
        path('drafts/', include('drafts.urls')),
        path('applications/', include('applications.urls')),
        path('organisations/', include('organisations.urls'))
    ]

    client = APIClient()

    def __init__(self, name):
        self.name = name
        self.eori_number = "GB123456789000"
        self.sic_number = "2765"
        self.vat_number = "123456789"
        self.registration_number = "987654321"
        self.address = "London"
        self.admin_user_email = "trinity@" + name + ".com"

        url = reverse('organisations:organisations')
        data = {'name': self.name, 'eori_number': self.eori_number, 'sic_number': self.sic_number,
                'vat_number': self.vat_number,
                'registration_number': self.registration_number, 'address': self.address,
                'admin_user_email': self.admin_user_email}
        self.client.post(url, data, format='json')

        self.organisation = Organisation.objects.get(name=name)
        self.user = User.objects.filter(organisation=self.organisation)[0]
#
#     @staticmethod
#     def complete_draft(name, org):
#         return Draft(name=name,
#                      destination='Poland',
#                      activity='Trade',
#                      usage='Fun',
#                      organisation=org)
