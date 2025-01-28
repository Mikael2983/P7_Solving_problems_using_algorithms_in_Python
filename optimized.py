import csv
from itertools import combinations

CSV_PATH = "liste_actions.csv"
MAX_SPEND = 500


class Action:
    def __init__(self,name: str, cost: str, profitability: str):
        self.name = name
        self.cost = int(cost)
        self.profitability = round(int(cost)*float(profitability.strip('%')) / 100, 2)


def extract_actions_from_csv(path: str) -> list:
    """
    extracts the list of actions and their characteristics from the csv file
    :param path: path to the data file
    :type path: str
    :return: a list of dictionaries of actions with their name, cost and profitability
    """
    with open(path, 'r', encoding='utf-8', newline='') as actions_files:
        list_actions = []
        reader = csv.reader(actions_files)
        next(reader)
        for row in reader:
            action = Action(row[0],row[1],row[2])
            list_actions.append(action)
    return list_actions


def write_list_in_csv(data):
    filename = "matrice.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def sacADos_dynamique(capacite, elements):
    matrice = [[0 for x in range(capacite + 1)] for x in
               range(len(elements) + 1)]
    liste =[["name", "cost", "protability", 0]]
    for w in range(1, capacite + 1):
        liste[0].append(w)

    for i in range(1, len(elements) + 1):

        listerow = [elements[i-1].name, elements[i-1].cost,
                    elements[i-1].profitability,0]
        for w in range(1, capacite + 1):

            if elements[i - 1].cost <= w:
                matrice[i][w] = max(elements[i - 1].profitability + matrice[i - 1][w - elements[i - 1].cost],
                                    matrice[i - 1][w])
            else:
                matrice[i][w] = matrice[i - 1][w]
            listerow.append(matrice[i][w])
        liste.append(listerow)
    write_list_in_csv(liste)
    # Retrouver les éléments en fonction de la somme
    w = capacite
    n = len(elements)
    elements_selection = []

    while w >= 0 and n >= 0:
        e = elements[n - 1]
        if matrice[n][w] == matrice[n - 1][w - e.cost] + e.profitability:
            elements_selection.append(e.name)
            w -= e.cost

        n -= 1

    return matrice[-1][-1], elements_selection

def run():
    actions = extract_actions_from_csv(CSV_PATH)
    max_profitablity, selectionned_actions= sacADos_dynamique(MAX_SPEND, actions)
    print(max_profitablity,selectionned_actions)

run()





