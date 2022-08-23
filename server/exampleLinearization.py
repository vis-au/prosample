from pipeline import *

# Requires file mountainPeaksData.csv to be in the datasets folder
# Linearizes file by 3 attributes (columns 2,3 and 4, since the first one is the ID)
linearization = LinearizationZOrderKD(
    "spotify",
    12,
    exclude_attributes=[
        "name",
        "artists",
        "id_artists",
        "release_date",
        "key",
        "mode",
        "time_signature",
    ],
)
linearization.linearize()


# ["name", "artists", "id_artists", "release_date", "key", "mode", "time_signature"]
