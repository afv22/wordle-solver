from src import Criteria


def get_strategy():
    print("Select your strategy:")
    options = {"1": "Random", "2": "Entropy", "3": "Expected Value"}
    criteria_choice = get_input(options)

    if criteria_choice == "1":
        criteria = Criteria.RANDOM
    elif criteria_choice == "2":
        criteria = Criteria.ENTROPY
    elif criteria_choice == "3":
        criteria = Criteria.EXPECTED_MOVES

    return criteria


def get_input(options: dict):
    for key in options:
        print(f"{key}: {options[key]}")

    selection = input("> ")
    while selection not in options.keys():
        print("Oops! Try again.")
        selection = input("> ")

    return selection
