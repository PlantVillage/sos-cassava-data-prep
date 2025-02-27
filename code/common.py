import pandas as pd

def farm_id(county: str, id: int) -> str:
    """Return a standardized Farm ID"""
    county_abbreviations = {
        "baringo": "BAR",
        "bungoma": "BUN",
        "busia": "BUS",
        "homabay": "HOM",
        "kilifi": "KIL",
        "migori": "MIG",
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
        field_id = int(field_id)
        return f"{county.lower()}:{field_id:02}"
    except:
        return "Unknown"


def load_aez(data: pd.DataFrame) -> pd.DataFrame:
    """Load Agroecological zones for each farm."""
    try:
        df = pd.read_csv("output/cassava_sos_planting_survey.csv")
    except:
        subprocess.run(["python3", "./planting_survey.py"], check=True)
        df = pd.read_csv("output/cassava_sos_planting_survey.csv")

    df["num_id"] = df["farm_id"].apply(farm_num_id)
    df["farm_id"] = df.apply(lambda x: farm_id(x['county'], x['num_id']), axis=1)

    # get zone data from planting report survey
    aez = {}
    for id in df["farm_id"].unique().tolist():
        zone = df.query(f" farm_id == '{id}'")["zones"].unique().tolist()[0]
        aez[id] = zone
    
    data["zones"] = data["farm_id"].apply(lambda x: aez[x])
    return data