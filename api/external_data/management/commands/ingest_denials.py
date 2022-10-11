import logging
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework import serializers

from elasticsearch_dsl import connections

from api.documents.libraries import s3_operations
from api.external_data import documents, models
from api.external_data.serializers import DenialSerializer

log = logging.getLogger(__name__)


def get_json_content():
    with open("export.json") as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    required_headers = [
        "reference",
        "name",
        "address",
        "notifying_government",
        "country",
        "item_list_codes",
        "item_description",
        "consignee_name",
        "end_use",
    ]

    def add_arguments(self, parser):
        parser.add_argument("--rebuild", default=False, action="store_true")

    def rebuild_index(self):
        connection = connections.get_connection()
        connection.indices.delete(index=settings.ELASTICSEARCH_DENIALS_INDEX_ALIAS, ignore=[404])
        documents.DenialDocumentType.init()

    @staticmethod
    def add_bulk_errors(errors, row_number, line_errors):
        for key, values in line_errors.items():
            errors.append(f"[Row {row_number}] {key}: {','.join(values)}")

    def handle(self, *args, **options):
        if options["rebuild"]:
            self.rebuild_index()
        self.load_denials()

    @transaction.atomic
    def load_denials(self):
        data = get_json_content()
        errors = []
        valid_serializers = []
        for i, row in enumerate(data, start=1):
            serializer = DenialSerializer(
                data={
                    "data": row,
                    **{field: row.pop(field, None) for field in self.required_headers},
                }
            )
            if serializer.is_valid():
                valid_serializers.append(serializer)
            else:
                self.add_bulk_errors(errors=errors, row_number=i + 1, line_errors=serializer.errors)

        if errors:
            log.exception(
                "Error loading denials -> %s",
                errors,
            )
            raise serializers.ValidationError(errors)
        else:
            # only save if no errors
            for serializer in valid_serializers:
                serializer.save()
            log.info(
                "denials record saved -> %s",
                len(valid_serializers),
            )
