import csv

CSV_PATH = "liste_actions.csv"


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
            action = Action(row[0], row[1], row[2])
            actions.append(action)
            # cost est utilisé comme indice de table dans la fonction knapsack
            # il doit donc impérativement être entier
            # Vérifie si un coût non entier est détecté
            if action.cost != int(action.cost):
                scale = 100  # Active la mise à l'échelle

    return actions, scale


def knapsack(actions, max_budget, scale=1):
    """
    Solves the 0/1 knapsack problem to maximize profitability while respecting a budget constraint.

    :param actions: List of Action objects
    :param max_budget: Maximum budget
    :param scale: Scaling factor (1 if all costs are integers, otherwise 100 for decimal handling)
    :return: Maximum achievable profit and the list of selected actions
    """

    costs = [int(action.cost * scale) for action in actions]
    profits = [action.cost * action.profitability for action in
               actions]
    max_budget = int(max_budget * scale)

    number_of_actions = len(actions)
    max_profit_at_budget = [0] * (max_budget + 1)

    selected = [[False] * number_of_actions for _ in range(
        max_budget + 1)]  # Tableau pour récupérer les actions choisies

    for i in range(number_of_actions):
        for j in range(max_budget, costs[i] - 1, -1):
            if max_profit_at_budget[j] < max_profit_at_budget[j - costs[i]] + profits[i]:
                max_profit_at_budget[j] = max_profit_at_budget[j - costs[i]] + profits[i]
                selected[j] = selected[j - costs[i]][
                              :]  # Copier la sélection précédente
                selected[j][i] = True  # Ajouter l'action actuelle

    # Récupération des actions sélectionnées
    max_profit = max_profit_at_budget[max_budget]
    selected_actions = [actions[i] for i in range(number_of_actions) if
                        selected[max_budget][i]]

    return max_profit, selected_actions


def run():
    actions, scale = extract_actions_from_csv(CSV_PATH)
    budget_max = 500

    max_profit, selected_actions = knapsack(actions, budget_max,
                                                       scale)

    print(f"Meilleure rentabilité obtenue : {max_profit:.2f} €")
    print("Actions sélectionnées :")
    for action in selected_actions:
        print(
            f"- {action.name} (Coût : {action.cost} €, Rentabilité : {action.profitability * 100:.0f}%)")


run()
