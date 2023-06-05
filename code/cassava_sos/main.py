import os 

def main():
    print("Running planting survey....")
    os.system("python code/cassava_sos/planting_survey.py")
    print("\n\n")
    print("Running germination survey...")
    os.system("python code/cassava_sos/germination_survey.py")
    print("\n\n")
    print("Running farm visit survey...")
    os.system("python code/cassava_sos/farm_visit_survey.py")


if __name__ == "__main__":
    main()