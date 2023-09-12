def farm_id(county: str, id: int) -> str:
    """Return a standardized Farm ID"""
    county_abbreviations = {
        "baringo": "BAR",
        "siaya": "SIA",
        "homabay": "HOM",
        "bungoma": "BUN",
        "busia": "BUS",
        "migori": "MIG",
        "kilifi": "KIL"
    }

    abbrev = county_abbreviations[county]
    return f"{abbrev}:{id:02}"

