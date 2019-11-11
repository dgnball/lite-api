class CaseType:
    APPLICATION = 'application'
    CLC_QUERY = 'clc_query'
    END_USER_ADVISORY_QUERY = 'end_user_advisory_query'

    choices = [
        (APPLICATION, 'Application'),
        (CLC_QUERY, 'CLC Query'),
        (END_USER_ADVISORY_QUERY, 'End User Advisory Query'),
    ]

    @classmethod
    def get_text(cls, choice):
        for key, value in cls.choices:
            if key == choice:
                return value

    @classmethod
    def as_list(cls):
        return [
            {
                'value': choice[0],
                'title': choice[1],
            } for choice in cls.choices
        ]


class AdviceType:
    APPROVE = 'approve'
    PROVISO = 'proviso'
    REFUSE = 'refuse'
    NO_LICENCE_REQUIRED = 'no_licence_required'
    NOT_APPLICABLE = 'not_applicable'
    CONFLICTING = 'conflicting'

    choices = [
        (APPROVE, 'Approve'),
        (PROVISO, 'Proviso'),
        (REFUSE, 'Refuse'),
        (NO_LICENCE_REQUIRED, 'No Licence Required'),
        (NOT_APPLICABLE, 'Not Applicable'),
        (CONFLICTING, 'Conflicting')
    ]
