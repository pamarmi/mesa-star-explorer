def get_history_quantities(data):
    """
    Extract common stellar quantities.
    """

    return {

        "age":
        data["star_age"],

        "luminosity":
        data["log_L"],

        "temperature":
        data["log_Teff"],

        "radius":
        data["log_R"]

    }