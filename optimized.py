import csv

CSV_PATH = "data/liste_actions.csv"
# CSV_PATH = "data/dataset1.csv"


class Action:
    def __init__(self, name: str, cost: str, profitability: str):
        self.name = name
        self.cost = float(cost)
        self.profitability = float(profitability.strip('%')) / 100


def extract_actions_from_csv(path: str):
    """
    extracts the list of actions and their characteristics from the csv file
    :param path: path to the data file
    :type path: str
    :return: a list of dictionaries of actions with their name, cost and profitability
    """
    actions = []
    scale = 1  # Valeur par défaut

    with open(path, 'r', encoding='utf-8', newline='') as actions_file:
        reader = csv.reader(actions_file)
        next(reader)  # Ignore l'en-tête

        for row in reader:
            if float(row[1]) > 0:
                action = Action(row[0], row[1], row[2])
                actions.append(action)
                # cost est utilisé comme indice de table dans la fonction knapsack,
                # il doit donc impérativement être entier
                # Vérifie si un coût non entier est détecté
                if action.cost != int(action.cost):
                    scale = 100  # Active la mise à l'échelle

    return actions, scale


def knapsack(actions, max_budget, scale=1):
    """
    Solves the 0/1 knapsack problem to maximize profitability while respecting
    a budget constraint.

    :param actions: List of Action objects
    :param max_budget: Maximum budget
    :param scale: Scaling factor (1 if all action.cost are integers, otherwise 100 for decimal handling)
    :return: Maximum achievable profit and the list of selected actions
    """

    # Convert costs to integers if necessary
    costs = [int(action.cost * scale) for action in actions]
    profits = [action.cost * action.profitability for action in actions]
    max_budget = int(max_budget * scale)

    max_profit_table = [[0] * (max_budget + 1) for _ in
                        range(len(actions) + 1)]

    for i in range(1, len(actions) + 1):
        for j in range(max_budget + 1):
            if costs[i - 1] <= j:
                max_profit_table[i][j] = max(
                    max_profit_table[i - 1][j],
                    max_profit_table[i - 1][j - costs[i - 1]] + profits[i - 1]
                )
            else:
                max_profit_table[i][j] = max_profit_table[i - 1][j]

    # Save the transposed max_profit_table to a CSV file
    # with open('table_transposed.csv', mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Budget"] + [0] + [f"{action.name}" for action in actions])
    #     for j in range(max_budget + 1):
    #         writer.writerow([j] + [profit_table[i][j] for i in range(n + 1)])

    budget_remaining = max_budget
    selected_actions = []

    for i in range(len(actions), 0, -1):
        if (max_profit_table[i][budget_remaining] !=
                max_profit_table[i - 1][budget_remaining]):
            selected_actions.append(actions[i - 1])
            budget_remaining -= costs[i - 1]
    selected_actions.reverse()
    return max_profit_table[-1][-1], selected_actions


def run():
    actions, scale = extract_actions_from_csv(CSV_PATH)
    budget_max = 500

    max_profit, selected_actions = knapsack(actions, budget_max,
                                            scale)

    print(f"Meilleure rentabilité obtenue : {max_profit:.2f} €")
    print("Actions sélectionnées :")
    actions_cost = 0
    for action in selected_actions:
        actions_cost += action.cost
        print(
            f"- {action.name} (Coût : {action.cost} €, Rentabilité : "
            f"{action.profitability * 100:.0f}%)")
    print(f"coût total de l'investissement : {actions_cost:.2f} €")


run()
