from rest_framework.fields import UUIDField

from conf.serializers import PrimaryKeyRelatedSerializerField
from lite_content.lite_api import strings
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueValidator

from gov_users.enums import GovUserStatuses
from organisations.models import Organisation
from queues.constants import SYSTEM_QUEUES
from queues.models import Queue
from queues.serializers import TinyQueueSerializer
from static.statuses.models import CaseStatus
from static.statuses.serializers import CaseStatusSerializer
from teams.models import Team
from teams.serializers import TeamSerializer
from users.enums import UserType
from users.models import GovUser, GovNotification
from users.models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
        )


class RoleSerializer(serializers.ModelSerializer):
    permissions = PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)
    organisation = PrimaryKeyRelatedField(queryset=Organisation.objects.all(), required=False, allow_null=True)
    type = serializers.ChoiceField(choices=UserType.non_system_choices())
    name = serializers.CharField(max_length=30, error_messages={"blank": strings.Roles.BLANK_NAME},)
    statuses = PrimaryKeyRelatedSerializerField(
        queryset=CaseStatus.objects.all(), many=True, required=False, serializer=CaseStatusSerializer
    )

    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "permissions",
            "type",
            "organisation",
            "statuses",
        )


class RoleListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, read_only=True)
    permissions = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "permissions",
        )


class RoleListStatusesSerializer(RoleListSerializer):
    statuses = PrimaryKeyRelatedSerializerField(
        queryset=CaseStatus.objects.all(), many=True, required=False, serializer=CaseStatusSerializer
    )

    class Meta:
        model = Role
        fields = ("id", "name", "permissions", "statuses")


class GovUserListSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)


class GovUserViewSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    role = RoleListStatusesSerializer()
    default_queue = serializers.SerializerMethodField()

    class Meta:
        model = GovUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "status",
            "team",
            "role",
            "default_queue",
        )

    def get_default_queue(self, instance):
        queue_id = str(instance.default_queue)

        if queue_id in SYSTEM_QUEUES.keys():
            return {"id": queue_id, "name": SYSTEM_QUEUES[queue_id]}
        else:
            return TinyQueueSerializer(Queue.objects.get(pk=queue_id)).data


class GovUserCreateSerializer(GovUserViewSerializer):
    status = serializers.ChoiceField(choices=GovUserStatuses.choices, default=GovUserStatuses.ACTIVE)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=GovUser.objects.all())],
        error_messages={"blank": strings.Users.INVALID_EMAIL, "invalid": strings.Users.INVALID_EMAIL},
    )
    team = PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        error_messages={"null": strings.Users.NULL_TEAM, "invalid": strings.Users.NULL_TEAM},
    )
    role = PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        error_messages={"null": strings.Users.NULL_ROLE, "invalid": strings.Users.NULL_ROLE},
    )
    default_queue = UUIDField(
        error_messages={"null": strings.Users.NULL_DEFAULT_QUEUE, "invalid": strings.Users.NULL_DEFAULT_QUEUE},
    )

    class Meta:
        model = GovUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "status",
            "team",
            "role",
            "default_queue",
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        default_queue = str(validated_data.get("default_queue") or self.instance.default_queue)
        team = validated_data.get("team") or self.instance.team

        is_system_queue = default_queue in SYSTEM_QUEUES.keys()
        is_work_queue = Queue.objects.filter(id=default_queue).exists()

        if not is_system_queue and not is_work_queue:
            raise serializers.ValidationError({"default_queue": [strings.Users.NULL_DEFAULT_QUEUE]})

        if is_work_queue and not Queue.objects.values_list("team_id", flat=True).get(id=default_queue) == team.id:
            raise serializers.ValidationError({"default_queue": [strings.Users.INVALID_DEFAULT_QUEUE % team.name]})

        return validated_data


class GovUserSimpleSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = GovUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "team",
        )

    def get_team(self, instance):
        return instance.team.name


class GovUserNotificationSerializer(serializers.ModelSerializer):
    audit_id = serializers.SerializerMethodField()

    class Meta:
        model = GovNotification
        fields = ("audit_id",)

    def get_audit_id(self, obj):
        return obj.object_id
