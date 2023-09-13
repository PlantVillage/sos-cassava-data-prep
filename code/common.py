def farm_id(county: str, id: int) -> str:
    """Return a standardized Farm ID"""
    county_abbreviations = {
        "baringo": "BAR",
        "bungoma": "BUN",
        "busia": "BUS",
        "homabay": "HOM",
        "kilifi": "KIL",
        "migori": "MIG"
        "siaya": "SIA",
    }

    abbrev = county_abbreviations[county.lower()]
    return f"{abbrev}:{id:02}"


def farm_num_id(id: str) -> int:
    """Return the numeric ID of a farm"""
    return int(id.split(":")[1])


def days_after_planting(survey_date, planting_date) -> int:
    """Return the number of days after planting"""
    return (survey_date - planting_date).days


def standardize_farm_id(farm_id: str) -> str:
    """Standardize the farm ID to lower case"""
    return farm_id.lower()


def unique_farm_id(county: str, field_id: int) -> str:
    """Generate a unique ID for the farm"""
    try:
        return f"{county.lower()}:{field_id:02}"
    except:
        return "Unknown"