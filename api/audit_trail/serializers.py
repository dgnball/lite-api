import logging
from copy import deepcopy

from rest_framework import serializers

from api.audit_trail.models import Audit
from api.audit_trail.enums import AuditType
from api.audit_trail.payload import format_payload
from api.users.enums import UserType


class AuditSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    additional_text = serializers.SerializerMethodField()

    class Meta:
        model = Audit
        fields = (
            "id",
            "created_at",
            "user",
            "text",
            "additional_text",
        )

    def get_user(self, instance: Audit):
        if instance.actor:
            return {
                "id": instance.actor.pk,
                "first_name": instance.actor.first_name,
                "last_name": instance.actor.last_name,
                "type": instance.actor.type,
                "team": instance.actor.team.name if instance.actor.type == UserType.INTERNAL else "",
            }
        else:
            # When an anonymous user is registering for an org,
            # we pass their email in the payload to use it as the actor later
            return {
                "first_name": instance.payload.get("email"),
                "last_name": "",
            }

    def get_text(self, instance):
        verb = AuditType(instance.verb)
        payload = deepcopy(instance.payload)

        if verb == AuditType.REGISTER_ORGANISATION:
            payload["email"] = ""

        for key in payload:
            # If value is a list, join by comma.
            try:
                if isinstance(payload[key], list):
                    payload[key] = ", ".join(payload[key])
            except KeyError as e:
                logging.error(f"Audit serialization exception skipped: {e}")

            # TODO: standardise payloads across all audits and remove below
            if key == "status" and "new" in payload[key]:
                # Handle new payload format
                payload[key] = payload[key]["new"]

        return format_payload(verb, payload)

    def get_additional_text(self, instance):
        return instance.payload.get("additional_text", "")
