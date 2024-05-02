from gurobipy import Model, GRB, quicksum
import networkx as nx


def solve_shortest_path(graph, start_node, end_node):
    # Ensure reverse edges are present
    # for (i, j), data in list(graph['edges'].items()):
    #     reverse_edge = (j, i)
    #     if reverse_edge not in graph['edges']:
    #         graph['edges'][reverse_edge] = {'weight': data['weight'], 'duration': data['duration']}

    # créer un nouvel model
    model = Model('shortest_path')

    # Definir les variables de decision pour les arcs
    x = model.addVars(graph['edges'].keys(), vtype=GRB.BINARY, name="x")

    # Definir les variables de decision pour le temps
    t = model.addVars(graph['nodes'].keys(), vtype=GRB.CONTINUOUS, name="t")

    # Definir les variables de decision pour le debut ( cette variable permet l'attente devant un noaed si on ne peut pas accéder )
    start = {}

    # mettre le temps de depart du noeud de depart a 0
    model.addConstr(t[start_node] == 0, name='start_time')

    # Ajouter les contraintes pour les noeuds
    for node, (a, b) in graph['nodes'].items():
        start[node] = model.addVar(
            vtype=GRB.CONTINUOUS, name=f'slack_start_{node}')

        
        model.addConstr(t[node] >= a - start[node], name=f'time_start_{node}')
        model.addConstr(t[node] <= b, name=f'time_end_{node}')

    # Ajouter les contraintes pour les arcs
    for (i, j), data in graph['edges'].items():
        # Obtenir la durée de l'arc
        tij = data.get('duration', 0)

        # Contrainte pour les variables de temps basée sur les arcs et la variable de décision
        model.addConstr(t[j] >= t[i] + tij - (1 - x[i, j])
                        * 1e5, name=f'arc_{i}_{j}')
        model.addConstr(t[i] >= t[j] + tij - (1 - x[j, i])
                        * 1e5, name=f'arc_{j}_{i}')

    # Ajouter les contraintes de flux pour chaque noeud
    for node in graph['nodes']:
        in_edges = quicksum(x[i, node]
                            for (i, j) in graph['edges'] if j == node)
        out_edges = quicksum(x[node, j]
                            for (i, j) in graph['edges'] if i == node)
        if node == start_node:
            model.addConstr(out_edges - in_edges == 1, name=f'flux_{node}')
        elif node == end_node:
            model.addConstr(in_edges - out_edges == 1, name=f'flux_{node}')
        else:
            model.addConstr(in_edges == out_edges, name=f'flux_{node}')

    # Définir la fonction objective ( minimiser total weight )
    model.setObjective(quicksum(graph['edges'][(
        i, j)]['weight'] * x[i, j] for (i, j) in graph['edges']), GRB.MINIMIZE)

    # Optimiser le model
    model.optimize()

    # voir si une solution optimale existe
    if model.status == GRB.OPTIMAL:
        # recuperer optimal path and total cost
        shortest_path = []
        current_node = start_node
        while current_node != end_node:
            for (i, j), var in x.items():
                if i == current_node and var.X > 0.5:
                    print("hello", var.X)
                    shortest_path.append((i, j))
                    current_node = j
                    break
        total_cost = model.objVal
        return shortest_path, total_cost
    else:
        print("No optimal solution found.")
        return None


def validate_graph(graph, labels):
    # variable pour stocker le message d'erreur
    error_message = ""

    # Valider chaque noeud dans le graphe
    for i, data in graph['nodes'].items():
        # Obtenir la durée de l'arc
        ai, bi = graph['nodes'][i]

        # Vérifier les valeurs négatives
        if ai < 0 or bi < 0:
            error_message += f"Erreur : Le noeud {labels[i]} a une entrée ou sortie négative. \n"
            print(error_message)
            return False, error_message

    # Valider chaque arc dans le graphe
    for (i, j), data in graph['edges'].items():
        # Obtenir la durée de l'arc
        tij = data.get('duration', 0)
        wij = data.get('weight', 0)

        # Vérifier les valeurs négatives
        if tij < 0:
            error_message += f"Erreur : L'arc ({labels[i]}, {labels[j]}) a une durée négative : {tij}.\n"
            print(error_message)
            return False, error_message
        if wij < 0:
            error_message += f"Erreur : L'arc ({labels[i]}, {labels[j]}) a un poids négatif : {wij}.\n"
            print(error_message)
            return False, error_message

    # Vérifier les nœuds isolés
    all_nodes = set(graph['nodes'].keys())
    arc_nodes = set()

    for (i, j) in graph['edges']:
        arc_nodes.add(i)
        arc_nodes.add(j)

    isolated_nodes = all_nodes - arc_nodes
    isolated_nodes = [labels[node] for node in isolated_nodes]
    if isolated_nodes:
        error_message += f"Erreur : Les nœuds isolés suivants ont été détectés : {isolated_nodes}\n"
        print(error_message)
        return False, error_message

    # Si toutes les contraintes sont respectées, renvoyer True
    return True, ""
