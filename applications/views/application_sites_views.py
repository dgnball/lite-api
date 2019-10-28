from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from applications.libraries.case_activity import set_site_case_activity
from applications.models import SiteOnApplication, ExternalLocationOnApplication
from applications.serializers import SiteOnApplicationCreateSerializer
from conf.authentication import ExporterAuthentication
from conf.decorators import authorised_users
from organisations.libraries.get_external_location import has_previous_locations
from organisations.libraries.get_site import get_site
from organisations.models import Site
from organisations.serializers import SiteViewSerializer
from static.statuses.enums import CaseStatusEnum
from users.models import ExporterUser


class ApplicationSites(APIView):
    """
    View sites belonging to an application or add them
    """
    authentication_classes = (ExporterAuthentication,)

    @authorised_users(ExporterUser)
    def get(self, request, application):
        sites_ids = SiteOnApplication.objects.filter(application=application).values_list('site', flat=True)
        sites = Site.objects.filter(id__in=sites_ids)
        serializer = SiteViewSerializer(sites, many=True)
        return JsonResponse(data={'sites': serializer.data})

    @transaction.atomic
    @authorised_users(ExporterUser)
    def post(self, request, application):
        data = request.data
        site_ids = data.get('sites')

        # Validate that there are actually sites
        if not site_ids:
            return JsonResponse(data={'errors': {'sites': ['You have to pick at least one site']}},
                                status=status.HTTP_400_BAD_REQUEST)

        previous_sites = SiteOnApplication.objects.filter(application=application)
        previous_sites_ids = [str(previous_site_id) for previous_site_id in
                              previous_sites.values_list('site__id', flat=True)]

        if not application.status or application.status.status == CaseStatusEnum.APPLICANT_EDITING:
            new_sites = [get_site(site_id, request.user.organisation) for site_id in site_ids if site_id not in
                         previous_sites_ids]
        else:
            if has_previous_locations(application):
                return JsonResponse(data={'errors': {
                    'sites': [
                        "Go back and change your answer from ‘Change a site, or delete a good, third party or "
                        "country’ to ’Change something else’."]
                }}, status=status.HTTP_400_BAD_REQUEST)

            previous_site_countries = list(previous_sites.values_list('site__address__country_id', flat=True))
            new_sites = []

            for site_id in site_ids:
                new_site = get_site(site_id, request.user.organisation)

                if new_site.address.country.id not in previous_site_countries:
                    return JsonResponse(data={'errors': {
                        'sites': [
                            "Go back and change your answer from ‘Change a site, or delete a good, third party or "
                            "country’ to ’Change something else’."]
                    }}, status=status.HTTP_400_BAD_REQUEST)
                elif str(new_site.id) not in previous_sites_ids:
                    new_sites.append(new_site)

        # Update application activity
        application.activity = 'Trading'
        application.save()

        # Get sites to be removed
        removed_site_ids = list(set(previous_sites_ids) - set(site_ids))
        removed_sites = previous_sites.filter(site__id__in=removed_site_ids)

        # Append new SitesOnDrafts
        response_data = []
        for new_site in new_sites:
            serializer = SiteOnApplicationCreateSerializer(data={'site': new_site.id, 'application': application.id})

            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)
            else:
                return JsonResponse(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Get external locations to be removed if a site is being added
        removed_locations = ExternalLocationOnApplication.objects.filter(application=application)

        set_site_case_activity(removed_locations, removed_sites, new_sites, request.user, application)

        removed_sites.delete()
        removed_locations.delete()

        return JsonResponse(data={'sites': response_data}, status=status.HTTP_201_CREATED)
