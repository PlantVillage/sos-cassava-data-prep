#!/usr/bin/env python3

import subprocess

def main():
    print("Running planting survey...")
    subprocess.run(["python3", "./planting_survey.py"], check=True)
    
    print("Running germination survey...")
    subprocess.run(["python3", "./germination_survey.py"], check=True)
    
    print("Running farm visit survey...")
    subprocess.run(["python3", "./farm_visit_survey.py"], check=True)
    
    print("Running canopy survey...")
    subprocess.run(["python3", "./canopy_measurement.py"], check=True)
    
    print("Running disease score survey...")
    subprocess.run(["python3", "./disease_monitoring.py"], check=True)
    
    print("Running severity image survey...")
    subprocess.run(["python3", "./severity_monitoring.py"], check=True)
    
    print("Running whitefly survey...")
    subprocess.run(["python3", "./whitefly_monitoring.py"], check=True)
    

if __name__ == "__main__":
    main()