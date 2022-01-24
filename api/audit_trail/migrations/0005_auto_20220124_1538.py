# Generated by Django 3.1.13 on 2022-01-24 15:38

import api.audit_trail.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit_trail", "0004_auto_20211101_1242"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audit",
            name="verb",
            field=models.CharField(
                choices=[
                    (api.audit_trail.enums.AuditType["CREATED"], "created"),
                    (api.audit_trail.enums.AuditType["OGL_CREATED"], "ogl_created"),
                    (api.audit_trail.enums.AuditType["OGL_FIELD_EDITED"], "ogl_field_edited"),
                    (api.audit_trail.enums.AuditType["OGL_MULTI_FIELD_EDITED"], "ogl_multi_field_edited"),
                    (api.audit_trail.enums.AuditType["ADD_FLAGS"], "add_flags"),
                    (api.audit_trail.enums.AuditType["REMOVE_FLAGS"], "remove_flags"),
                    (api.audit_trail.enums.AuditType["GOOD_REVIEWED"], "good_reviewed"),
                    (api.audit_trail.enums.AuditType["GOOD_ADD_FLAGS"], "good_add_flags"),
                    (api.audit_trail.enums.AuditType["GOOD_REMOVE_FLAGS"], "good_remove_flags"),
                    (api.audit_trail.enums.AuditType["GOOD_ADD_REMOVE_FLAGS"], "good_add_remove_flags"),
                    (api.audit_trail.enums.AuditType["DESTINATION_ADD_FLAGS"], "destination_add_flags"),
                    (api.audit_trail.enums.AuditType["DESTINATION_REMOVE_FLAGS"], "destination_remove_flags"),
                    (api.audit_trail.enums.AuditType["ADD_GOOD_TO_APPLICATION"], "add_good_to_application"),
                    (api.audit_trail.enums.AuditType["REMOVE_GOOD_FROM_APPLICATION"], "remove_good_from_application"),
                    (api.audit_trail.enums.AuditType["ADD_GOOD_TYPE_TO_APPLICATION"], "add_good_type_to_application"),
                    (
                        api.audit_trail.enums.AuditType["REMOVE_GOOD_TYPE_FROM_APPLICATION"],
                        "remove_good_type_from_application",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATE_APPLICATION_END_USE_DETAIL"],
                        "update_application_end_use_detail",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATE_APPLICATION_TEMPORARY_EXPORT"],
                        "update_application_temporary_export",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_SITES_FROM_APPLICATION"],
                        "removed_sites_from_application",
                    ),
                    (api.audit_trail.enums.AuditType["ADD_SITES_TO_APPLICATION"], "add_sites_to_application"),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_EXTERNAL_LOCATIONS_FROM_APPLICATION"],
                        "removed_external_locations_from_application",
                    ),
                    (
                        api.audit_trail.enums.AuditType["ADD_EXTERNAL_LOCATIONS_TO_APPLICATION"],
                        "add_external_locations_to_application",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_COUNTRIES_FROM_APPLICATION"],
                        "removed_countries_from_application",
                    ),
                    (api.audit_trail.enums.AuditType["ADD_COUNTRIES_TO_APPLICATION"], "add_countries_to_application"),
                    (
                        api.audit_trail.enums.AuditType["ADD_ADDITIONAL_CONTACT_TO_CASE"],
                        "add_additional_contact_to_case",
                    ),
                    (api.audit_trail.enums.AuditType["MOVE_CASE"], "move_case"),
                    (api.audit_trail.enums.AuditType["ASSIGN_CASE"], "assign_case"),
                    (api.audit_trail.enums.AuditType["ASSIGN_USER_TO_CASE"], "assign_user_to_case"),
                    (api.audit_trail.enums.AuditType["REMOVE_CASE"], "remove_case"),
                    (api.audit_trail.enums.AuditType["REMOVE_CASE_FROM_ALL_QUEUES"], "remove_case_from_all_queues"),
                    (
                        api.audit_trail.enums.AuditType["REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS"],
                        "remove_case_from_all_user_assignments",
                    ),
                    (api.audit_trail.enums.AuditType["CLC_RESPONSE"], "clc_response"),
                    (api.audit_trail.enums.AuditType["PV_GRADING_RESPONSE"], "pv_grading_response"),
                    (api.audit_trail.enums.AuditType["CREATED_CASE_NOTE"], "created_case_note"),
                    (api.audit_trail.enums.AuditType["ECJU_QUERY"], "ecju_query"),
                    (api.audit_trail.enums.AuditType["UPDATED_STATUS"], "updated_status"),
                    (api.audit_trail.enums.AuditType["UPDATED_APPLICATION_NAME"], "updated_application_name"),
                    (
                        api.audit_trail.enums.AuditType["UPDATE_APPLICATION_LETTER_REFERENCE"],
                        "update_application_letter_reference",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATE_APPLICATION_F680_CLEARANCE_TYPES"],
                        "update_application_f680_clearance_types",
                    ),
                    (
                        api.audit_trail.enums.AuditType["ADDED_APPLICATION_LETTER_REFERENCE"],
                        "added_application_letter_reference",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_APPLICATION_LETTER_REFERENCE"],
                        "removed_application_letter_reference",
                    ),
                    (api.audit_trail.enums.AuditType["ASSIGNED_COUNTRIES_TO_GOOD"], "assigned_countries_to_good"),
                    (api.audit_trail.enums.AuditType["REMOVED_COUNTRIES_FROM_GOOD"], "removed_countries_from_good"),
                    (api.audit_trail.enums.AuditType["CREATED_FINAL_ADVICE"], "created_final_advice"),
                    (api.audit_trail.enums.AuditType["CLEARED_FINAL_ADVICE"], "cleared_final_advice"),
                    (api.audit_trail.enums.AuditType["CREATED_TEAM_ADVICE"], "created_team_advice"),
                    (api.audit_trail.enums.AuditType["CLEARED_TEAM_ADVICE"], "cleared_team_advice"),
                    (api.audit_trail.enums.AuditType["REVIEW_COMBINE_ADVICE"], "review_combine_advice"),
                    (api.audit_trail.enums.AuditType["CREATED_USER_ADVICE"], "created_user_advice"),
                    (api.audit_trail.enums.AuditType["CLEARED_USER_ADVICE"], "cleared_user_advice"),
                    (api.audit_trail.enums.AuditType["ADD_PARTY"], "add_party"),
                    (api.audit_trail.enums.AuditType["REMOVE_PARTY"], "remove_party"),
                    (api.audit_trail.enums.AuditType["UPLOAD_PARTY_DOCUMENT"], "upload_party_document"),
                    (api.audit_trail.enums.AuditType["DELETE_PARTY_DOCUMENT"], "delete_party_document"),
                    (api.audit_trail.enums.AuditType["UPLOAD_APPLICATION_DOCUMENT"], "upload_application_document"),
                    (api.audit_trail.enums.AuditType["DELETE_APPLICATION_DOCUMENT"], "delete_application_document"),
                    (api.audit_trail.enums.AuditType["UPLOAD_CASE_DOCUMENT"], "upload_case_document"),
                    (api.audit_trail.enums.AuditType["GENERATE_CASE_DOCUMENT"], "generate_case_document"),
                    (api.audit_trail.enums.AuditType["ADD_CASE_OFFICER_TO_CASE"], "add_case_officer_to_case"),
                    (api.audit_trail.enums.AuditType["REMOVE_CASE_OFFICER_FROM_CASE"], "remove_case_officer_from_case"),
                    (api.audit_trail.enums.AuditType["GRANTED_APPLICATION"], "granted_application"),
                    (api.audit_trail.enums.AuditType["REINSTATED_APPLICATION"], "reinstated_application"),
                    (api.audit_trail.enums.AuditType["FINALISED_APPLICATION"], "finalised_application"),
                    (api.audit_trail.enums.AuditType["UNASSIGNED_QUEUES"], "unassigned_queues"),
                    (api.audit_trail.enums.AuditType["UNASSIGNED"], "unassigned"),
                    (api.audit_trail.enums.AuditType["CREATED_DOCUMENT_TEMPLATE"], "created_document_template"),
                    (api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_NAME"], "updated_letter_template_name"),
                    (
                        api.audit_trail.enums.AuditType["ADDED_LETTER_TEMPLATE_CASE_TYPES"],
                        "added_letter_template_case_types",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_CASE_TYPES"],
                        "updated_letter_template_case_types",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_LETTER_TEMPLATE_CASE_TYPES"],
                        "removed_letter_template_case_types",
                    ),
                    (
                        api.audit_trail.enums.AuditType["ADDED_LETTER_TEMPLATE_DECISIONS"],
                        "added_letter_template_decisions",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_DECISIONS"],
                        "updated_letter_template_decisions",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_LETTER_TEMPLATE_DECISIONS"],
                        "removed_letter_template_decisions",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_PARAGRAPHS"],
                        "updated_letter_template_paragraphs",
                    ),
                    (
                        api.audit_trail.enums.AuditType["REMOVED_LETTER_TEMPLATE_PARAGRAPHS"],
                        "removed_letter_template_paragraphs",
                    ),
                    (
                        api.audit_trail.enums.AuditType["ADDED_LETTER_TEMPLATE_PARAGRAPHS"],
                        "added_letter_template_paragraphs",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_LAYOUT"],
                        "updated_letter_template_layout",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_PARAGRAPHS_ORDERING"],
                        "updated_letter_template_paragraphs_ordering",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_LETTER_TEMPLATE_INCLUDE_DIGITAL_SIGNATURE"],
                        "updated_letter_template_include_digital_signature",
                    ),
                    (api.audit_trail.enums.AuditType["CREATED_PICKLIST"], "created_picklist"),
                    (api.audit_trail.enums.AuditType["UPDATED_PICKLIST_TEXT"], "updated_picklist_text"),
                    (api.audit_trail.enums.AuditType["UPDATED_PICKLIST_NAME"], "updated_picklist_name"),
                    (api.audit_trail.enums.AuditType["DEACTIVATE_PICKLIST"], "deactivate_picklist"),
                    (api.audit_trail.enums.AuditType["REACTIVATE_PICKLIST"], "reactivate_picklist"),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_EXHIBITION_DETAILS_TITLE"],
                        "updated_exhibition_details_title",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_EXHIBITION_DETAILS_START_DATE"],
                        "updated_exhibition_details_start_date",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_EXHIBITION_DETAILS_REQUIRED_BY_DATE"],
                        "updated_exhibition_details_required_by_date",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_EXHIBITION_DETAILS_REASON_FOR_CLEARANCE"],
                        "updated_exhibition_details_reason_for_clearance",
                    ),
                    (api.audit_trail.enums.AuditType["UPDATED_ROUTE_OF_GOODS"], "updated_route_of_goods"),
                    (api.audit_trail.enums.AuditType["UPDATED_ORGANISATION"], "updated_organisation"),
                    (api.audit_trail.enums.AuditType["CREATED_ORGANISATION"], "created_organisation"),
                    (api.audit_trail.enums.AuditType["REGISTER_ORGANISATION"], "register_organisation"),
                    (api.audit_trail.enums.AuditType["REJECTED_ORGANISATION"], "rejected_organisation"),
                    (api.audit_trail.enums.AuditType["APPROVED_ORGANISATION"], "approved_organisation"),
                    (api.audit_trail.enums.AuditType["REMOVED_FLAG_ON_ORGANISATION"], "removed_flag_on_organisation"),
                    (api.audit_trail.enums.AuditType["ADDED_FLAG_ON_ORGANISATION"], "added_flag_on_organisation"),
                    (api.audit_trail.enums.AuditType["RERUN_ROUTING_RULES"], "rerun_routing_rules"),
                    (api.audit_trail.enums.AuditType["ENFORCEMENT_CHECK"], "enforcement_check"),
                    (api.audit_trail.enums.AuditType["UPDATED_SITE"], "updated_site"),
                    (api.audit_trail.enums.AuditType["CREATED_SITE"], "created_site"),
                    (api.audit_trail.enums.AuditType["UPDATED_SITE_NAME"], "updated_site_name"),
                    (api.audit_trail.enums.AuditType["COMPLIANCE_SITE_CASE_CREATE"], "compliance_site_case_create"),
                    (
                        api.audit_trail.enums.AuditType["COMPLIANCE_SITE_CASE_NEW_LICENCE"],
                        "compliance_site_case_new_licence",
                    ),
                    (api.audit_trail.enums.AuditType["ADDED_NEXT_REVIEW_DATE"], "added_next_review_date"),
                    (api.audit_trail.enums.AuditType["EDITED_NEXT_REVIEW_DATE"], "edited_next_review_date"),
                    (api.audit_trail.enums.AuditType["REMOVED_NEXT_REVIEW_DATE"], "removed_next_review_date"),
                    (api.audit_trail.enums.AuditType["COMPLIANCE_VISIT_CASE_CREATED"], "compliance_visit_case_created"),
                    (api.audit_trail.enums.AuditType["COMPLIANCE_VISIT_CASE_UPDATED"], "compliance_visit_case_updated"),
                    (
                        api.audit_trail.enums.AuditType["COMPLIANCE_PEOPLE_PRESENT_CREATED"],
                        "compliance_people_present_created",
                    ),
                    (
                        api.audit_trail.enums.AuditType["COMPLIANCE_PEOPLE_PRESENT_UPDATED"],
                        "compliance_people_present_updated",
                    ),
                    (
                        api.audit_trail.enums.AuditType["COMPLIANCE_PEOPLE_PRESENT_DELETED"],
                        "compliance_people_present_deleted",
                    ),
                    (
                        api.audit_trail.enums.AuditType["UPDATED_GOOD_ON_DESTINATION_MATRIX"],
                        "updated_good_on_destination_matrix",
                    ),
                    (api.audit_trail.enums.AuditType["LICENCE_UPDATED_GOOD_USAGE"], "licence_updated_good_usage"),
                    (api.audit_trail.enums.AuditType["OGEL_REISSUED"], "ogel_reissued"),
                    (api.audit_trail.enums.AuditType["LICENCE_UPDATED_STATUS"], "licence_updated_status"),
                    (
                        api.audit_trail.enums.AuditType["DOCUMENT_ON_ORGANISATION_CREATE"],
                        "document_on_organisation_create",
                    ),
                    (api.audit_trail.enums.AuditType["REPORT_SUMMARY_UPDATED"], "report_summary_updated"),
                    (api.audit_trail.enums.AuditType["COUNTERSIGN_ADVICE"], "countersign_advice"),
                ],
                db_index=True,
                max_length=255,
            ),
        ),
    ]
