from rest_framework import serializers
from django.db.models import Min, Case, When, BinaryField
from rest_framework.fields import CharField

from applications.enums import ApplicationExportType, GoodsTypeCategory
from applications.libraries.goodstype_category_helpers import set_goods_and_countries_for_open_media_application
from applications.models import OpenApplication
from applications.serializers.generic_application import (
    GenericApplicationCreateSerializer,
    GenericApplicationUpdateSerializer,
    GenericApplicationViewSerializer,
)
from applications.serializers.serializer_helper import validate_field
from cases.enums import CaseTypeEnum
from conf.serializers import KeyValueChoiceField
from goodstype.serializers import GoodsTypeViewSerializer
from licences.models import Licence
from licences.serializers.view_licence import CaseLicenceViewSerializer
from lite_content.lite_api import strings
from static.countries.models import Country
from static.countries.serializers import CountryWithFlagsSerializer
from static.trade_control.enums import TradeControlProductCategory, TradeControlActivity


class OpenApplicationViewSerializer(GenericApplicationViewSerializer):
    goods_types = serializers.SerializerMethodField()
    destinations = serializers.SerializerMethodField()
    additional_documents = serializers.SerializerMethodField()
    licence = serializers.SerializerMethodField()
    proposed_return_date = serializers.DateField(required=False)
    trade_control_activity = serializers.SerializerMethodField()
    trade_control_product_categories = serializers.SerializerMethodField()
    goodstype_category = serializers.SerializerMethodField()

    class Meta:
        model = OpenApplication
        fields = GenericApplicationViewSerializer.Meta.fields + (
            "activity",
            "usage",
            "goods_types",
            "destinations",
            "additional_documents",
            "is_military_end_use_controls",
            "military_end_use_controls_ref",
            "is_informed_wmd",
            "informed_wmd_ref",
            "is_suspected_wmd",
            "suspected_wmd_ref",
            "intended_end_use",
            "licence",
            "is_shipped_waybill_or_lading",
            "non_waybill_or_lading_route_details",
            "temp_export_details",
            "is_temp_direct_control",
            "temp_direct_control_details",
            "proposed_return_date",
            "trade_control_activity",
            "trade_control_product_categories",
            "goodstype_category",
        )

    def get_goods_types(self, application):
        goods_types = application.goods_type.all().prefetch_related("countries")
        default_countries = Country.objects.filter(countries_on_application__application=application)

        return GoodsTypeViewSerializer(goods_types, default_countries=default_countries, many=True).data

    def get_goodstype_category(self, instance):
        key = instance.goodstype_category
        value = GoodsTypeCategory.get_text(key)
        return {"key": key, "value": value}

    def get_destinations(self, application):
        """ Get destinations for the open application, ordered based on flag priority and alphabetized by name."""
        if "user_type" in self.context and self.context["user_type"] == "exporter":
            countries = Country.objects.filter(countries_on_application__application=application)
        else:
            countries = (
                Country.objects.prefetch_related("flags")
                .filter(countries_on_application__application=application)
                .annotate(
                    highest_flag_priority=Min("flags__priority"),
                    contains_flags=Case(When(flags__isnull=True, then=0), default=1, output_field=BinaryField()),
                )
                .order_by("-contains_flags", "highest_flag_priority", "name")
            )

        serializer = CountryWithFlagsSerializer(countries, many=True, context={"active_flags_only": True})
        return {"type": "countries", "data": serializer.data}

    def get_licence(self, instance):
        licence = Licence.objects.filter(application=instance).first()
        return CaseLicenceViewSerializer(licence).data

    def get_trade_control_activity(self, instance):
        key = instance.trade_control_activity
        value = (
            instance.trade_control_activity_other
            if key == TradeControlActivity.OTHER
            else TradeControlActivity.get_text(key)
        )
        return {"key": key, "value": value}

    def get_trade_control_product_categories(self, instance):
        trade_control_product_categories = (
            sorted(instance.trade_control_product_categories) if instance.trade_control_product_categories else []
        )
        return [
            {"key": tc_product_category, "value": TradeControlProductCategory.get_text(tc_product_category)}
            for tc_product_category in trade_control_product_categories
        ]


class OpenApplicationCreateSerializer(GenericApplicationCreateSerializer):
    goodstype_category = KeyValueChoiceField(
        choices=GoodsTypeCategory.choices,
        error_messages={"required": strings.Applications.Generic.OIEL_GOODSTYPE_CATEGORY_ERROR},
    )
    export_type = KeyValueChoiceField(
        choices=ApplicationExportType.choices, error_messages={"required": strings.Applications.Generic.NO_EXPORT_TYPE},
    )
    trade_control_activity = KeyValueChoiceField(
        choices=TradeControlActivity.choices,
        error_messages={"required": strings.Applications.Generic.TRADE_CONTROL_ACTIVITY_ERROR},
    )
    trade_control_activity_other = CharField(
        error_messages={
            "blank": strings.Applications.Generic.TRADE_CONTROL_ACTIVITY_OTHER_ERROR,
            "required": strings.Applications.Generic.TRADE_CONTROL_ACTIVITY_OTHER_ERROR,
        }
    )
    trade_control_product_categories = serializers.MultipleChoiceField(
        choices=TradeControlProductCategory.choices,
        error_messages={"required": strings.Applications.Generic.TRADE_CONTROl_PRODUCT_CATEGORY_ERROR},
    )

    class Meta:
        model = OpenApplication
        fields = GenericApplicationCreateSerializer.Meta.fields + (
            "export_type",
            "trade_control_activity",
            "trade_control_activity_other",
            "trade_control_product_categories",
            "goodstype_category",
        )

    def __init__(self, case_type_id, **kwargs):
        super().__init__(case_type_id, **kwargs)
        self.trade_control_licence = case_type_id in [str(CaseTypeEnum.SICL.id), str(CaseTypeEnum.OICL.id)]

        # Remove fields from serializer depending on the application being for a Trade Control Licence
        if self.trade_control_licence:
            self.fields.pop("export_type")
            self.fields.pop("goodstype_category")

            if not self.initial_data.get("trade_control_activity") == TradeControlActivity.OTHER:
                self.fields.pop("trade_control_activity_other")
        else:
            self.fields.pop("trade_control_activity")
            self.fields.pop("trade_control_activity_other")
            self.fields.pop("trade_control_product_categories")

        if case_type_id == str(CaseTypeEnum.HMRC.id):
            self.fields.pop("goodstype_category")

        self.media_application = (
            True if self.initial_data.get("goodstype_category") == GoodsTypeCategory.MEDIA else False
        )
        if self.media_application:
            self.fields.pop("export_type")
            self.media_application = True

    def create(self, validated_data):
        # Trade Control Licences are always permanent
        if self.trade_control_licence:
            validated_data["export_type"] = ApplicationExportType.PERMANENT
        elif self.media_application:
            validated_data["export_type"] = ApplicationExportType.TEMPORARY

        application = super().create(validated_data)

        if validated_data.get("goodstype_category") == GoodsTypeCategory.MEDIA:
            set_goods_and_countries_for_open_media_application(application)

        return application


class OpenApplicationUpdateSerializer(GenericApplicationUpdateSerializer):
    class Meta:
        model = OpenApplication
        fields = GenericApplicationUpdateSerializer.Meta.fields + (
            "is_shipped_waybill_or_lading",
            "non_waybill_or_lading_route_details",
        )

    def __init__(self, *args, **kwargs):
        super(OpenApplicationUpdateSerializer, self).__init__(*args, **kwargs)

        if self.get_initial().get("is_shipped_waybill_or_lading") == "True":
            if hasattr(self, "initial_data"):
                self.initial_data["non_waybill_or_lading_route_details"] = None

    def validate(self, data):
        validate_field(
            data,
            "is_shipped_waybill_or_lading",
            strings.Applications.Generic.RouteOfGoods.IS_SHIPPED_AIR_WAY_BILL_OR_LADING,
        )
        if data.get("is_shipped_waybill_or_lading") == False:
            validate_field(
                data, "non_waybill_or_lading_route_details", strings.Applications.Generic.RouteOfGoods.SHIPPING_DETAILS
            )
        return super().validate(data)
