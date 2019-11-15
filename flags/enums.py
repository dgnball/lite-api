class FlagLevels:
    CASE = "Case"
    ORGANISATION = "Organisation"
    GOOD = "Good"
    DESTINATION = "Destination"

    choices = [
        (CASE, "Case"),
        (ORGANISATION, "Organisation"),
        (GOOD, "Good"),
        (DESTINATION, "Destination"),
    ]


class FlagStatuses:
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"

    choices = [
        (ACTIVE, "Active"),
        (DEACTIVATED, "Deactivated"),
    ]


class SystemFlags:
    REFUSAL_FLAG_ID = "00000000-0000-0000-0000-000000000001"
