from src import Criteria

def get_strategy():
    print("Select your strategy:")
    print("1) Random")
    print("2) Entropy")
    print("3) Expected Value")
    
    criteria_choice = input("> ")
    while criteria_choice not in ["1", "2", "3"]:
        print("Try again.")
        criteria_choice = input("> ")

    if criteria_choice == "1":
        criteria = Criteria.RANDOM
    elif criteria_choice == "2":
        criteria = Criteria.ENTROPY
    elif criteria_choice == "3":
        criteria = Criteria.EXPECTED_MOVES
    else:
        raise ValueError("Invalid Criteria Selection")

    return criteria