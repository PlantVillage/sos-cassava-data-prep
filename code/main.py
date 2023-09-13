#!/usr/bin/env python3

import os 

def main():
    print("Running planting survey...")
    os.system("python3 planting_survey.py")
    print("\n\n")
    print("Running germination survey...")
    os.system("python3 germination_survey.py")
    print("\n\n")
    print("Running farm visit survey...")
    os.system("python3 farm_visit_survey.py")
    print("\n\n")
    print("Running canopy survey...")
    os.system("python3 canopy_measurement.py")
    print("\n\n")
    print("Running disease score survey...")
    os.system("python3 disease_monitoring.py")
    print("\n\n")   
    print("Running severity image survey...")
    os.system("python3 severity_monitoring.py")
    print("\n\n")
    print("Running whitefly survey...")
    os.system("python3 whitefly_monitoring.py")
    


if __name__ == "__main__":
    main()