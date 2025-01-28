import csv
from itertools import combinations

CSV_PATH = "liste_actions.csv"
MAX_SPEND = 500

list_actions = []


def extract_actions_from_csv(path: str) -> list:
    """
    extracts the list of actions and their characteristics from the csv file
    :param path: path to the data file
    :type path: str
    :return: a list of dictionaries of actions with their name, cost and profitability
    """
    with open(path, 'r', encoding='utf-8', newline='') as actions_files:
        reader = csv.reader(actions_files)
        next(reader)
        for row in reader:
            action = {"name": row[0],
                      "cost": int(row[1]),
                      "profitability": float(row[2].strip('%')) / 100
                      }
            list_actions.append(action)
    return list_actions


def find_best_invest(actions: list[dict], max_cost:int) -> dict:
    """
    finds the most cost-effective combination of all possible combination
    choices from the Share Dictionary list for a given maximum amount
    :param actions: a list of dictionaries of actions with their name, cost
    and profitability
    :type actions: list[dict]
    :param max_cost: maximum amount to invest
    :type max_cost: int
    :return: a dictionary of the names of actions to buy, the total cost to
    invest and the total profitability
    """
    max_profitability = 0
    results = []
    for combinaison_size in range(1, len(actions) + 1):
        for combinaison in combinations(actions, combinaison_size):
            total_cost = sum(item["cost"] for item in combinaison)

            if total_cost <= max_cost:
                total_profitability = sum(
                    item["cost"] * item["profitability"] for item in combinaison)
                if total_profitability > max_profitability:
                    max_profitability = total_profitability
                    results = {
                        "actions": [item["name"] for item in combinaison],
                        "cost": total_cost, "profitability": total_profitability}

    return results


actions = extract_actions_from_csv(CSV_PATH)
best_invest = find_best_invest(actions, MAX_SPEND)
print(best_invest)
