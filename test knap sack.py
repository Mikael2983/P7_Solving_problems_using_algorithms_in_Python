# A naive recursive implementation
# of 0-1 Knapsack Problem
import csv
# CSV_PATH = "data/liste_actions.csv"
CSV_PATH = "data/dataset3.csv"


class Action:
    def __init__(self, name: str, cost: str, profit: str):
        self.name = name
        self.cost = float(cost)
        self.profit = float(cost)*float(profit.strip('%')) / 100


def knapsack(max_budget, actions, n, selected_actions):
    # Base Case
    if n == 0 or max_budget == 0:
        return 0, []

    # If the cost of the nth action is more than Knapsack of max_budget,
    # then this item cannot be included in the optimal solution
    if actions[n - 1].cost > max_budget:
        print(n, actions[n - 1].cost, max_budget )
        return knapsack(max_budget, actions, n - 1, selected_actions)

    profit_included, actions_included = knapsack(
        max_budget - actions[n - 1].cost, actions, n - 1, selected_actions
    )
    profit_included += actions[n - 1].profit
    actions_included = actions_included + [actions[n - 1].name]

    profit_excluded, actions_excluded = knapsack(max_budget, actions, n - 1,
                                                 selected_actions)
    print(selected_actions)
    return max((profit_included, actions_included), (profit_excluded, actions_excluded), key=lambda x: x[0])

# This code is contributed by Nikhil Kumar Singh


def extract_actions_from_csv(path: str):
    """
    extracts the list of actions and their characteristics from the csv file
    :param path: path to the data file
    :type path: str
    :return: a list of dictionaries of actions with their name, cost and profitability
    """
    actions = []

    with open(path, 'r', encoding='utf-8', newline='') as actions_file:
        reader = csv.reader(actions_file)
        next(reader)  # Ignore l'en-tête

        for row in reader:
            if float(row[1])>0:
                action = Action(row[0], row[1], row[2])
                actions.append(action)

    return actions


def run():
    actions = extract_actions_from_csv(CSV_PATH)

    max_budget = 500
    n = len(actions)
    max_profit, selected_actions = knapsack(max_budget, actions, n, [])
    print(max_profit, selected_actions)


if __name__ == '__main__':
    run()
