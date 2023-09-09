import os 

def main():
    print("Running planting survey...")
    os.system("python code/cassava_sos/planting_survey.py")
    print("\n\n")
    print("Running germination survey...")
    os.system("python code/cassava_sos/germination_survey.py")
    print("\n\n")
    print("Running farm visit survey...")
    os.system("python code/cassava_sos/farm_visit_survey.py")
    print("\n\n")
    print("Running canopy survey...")
    os.system("python code/cassava_sos/canopy_measurement.py")
    print("\n\n")
    print("Running disease score survey...")
    os.system("python code/cassava_sos/disease_monitoring.py")
    print("\n\n")   
    print("Running severity image survey...")
    os.system("python code/cassava_sos/severity_monitoring.py")
    print("\n\n")
    print("Running whitefly survey...")
    os.system("python code/cassava_sos/whitefly_monitoring.py")
    


if __name__ == "__main__":
    main()