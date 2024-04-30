from gurobipy import Model, GRB, quicksum
import networkx as nx


def solve_shortest_path(graph, start_node, end_node):
    # Ensure reverse edges are present
    # for (i, j), data in list(graph['edges'].items()):
    #     reverse_edge = (j, i)
    #     if reverse_edge not in graph['edges']:
    #         graph['edges'][reverse_edge] = {'weight': data['weight'], 'duration': data['duration']}

    # Create a new model
    model = Model('shortest_path')

    # Define decision variables for edges
    x = model.addVars(graph['edges'].keys(), vtype=GRB.BINARY, name="x")

    # Define decision variables for time at each node
    t = model.addVars(graph['nodes'].keys(), vtype=GRB.CONTINUOUS, name="t")

    start = {}
    # Set the start time of the start node
    model.addConstr(t[start_node] == 0, name='start_time')

    # Add time window constraints for each node
    for node, (a, b) in graph['nodes'].items():
        start[node] = model.addVar(
            vtype=GRB.CONTINUOUS, name=f'slack_start_{node}')

        model.addConstr(t[node] >= a - start[node], name=f'time_start_{node}')
        model.addConstr(t[node] <= b, name=f'time_end_{node}')

    # Add constraints for the edges
    for (i, j), data in graph['edges'].items():
        # Duration for the edge
        tij = data.get('duration', 0)
        # Constraint for time variables based on the edges and the decision variable
        model.addConstr(t[j] >= t[i] + tij - (1 - x[i, j])
                        * 1e5, name=f'arc_{i}_{j}')
        model.addConstr(t[i] >= t[j] + tij - (1 - x[j, i])
                        * 1e5, name=f'arc_{j}_{i}')

    # Add flow constraints for each node
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

    # Define the objective function (minimize total weight)
    model.setObjective(quicksum(graph['edges'][(
        i, j)]['weight'] * x[i, j] for (i, j) in graph['edges']), GRB.MINIMIZE)

    # Optimize the model
    model.optimize()

    # Check if an optimal solution was found
    if model.status == GRB.OPTIMAL:
        # Retrieve the optimal path and total cost
        shortest_path = []
        current_node = start_node
        while current_node != end_node:
            for (i, j), var in x.items():
                if i == current_node and var.X > 0.5:
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

# # Testing the function with the provided graph, start node, and end node
# graph = {
#     'nodes': {
#         '1': (1, 1),
#         '2': (1, 2),
#         '3': (1, 20),
#         '4': (1, 20),
#         # '5': (1,20)
#     },
#     'edges': {
#         ('1', '2'): {'weight': 2.5, 'duration': 3},
#         ('2', '3'): {'weight': 3.5, 'duration': 3.5},
#         # ('2', '4'): {'weight': 10.5, 'duration': 1.5},
#         ('1', '4'): {'weight': 10, 'duration': 1},
#         ('3', '4'): {'weight': 10, 'duration': 1},
#     },
# }

# start_node = '2'
# end_node = '4'

# is_valid, error_message = validate_graph(graph)
# if not is_valid:
#     error_message = "le graphe n'est pas valide.\n" + error_message
# else:
#     print(solve_shortest_path(graph, start_node, end_node))
#     shortest_path, total_cost = solve_shortest_path(graph, start_node, end_node)
#     print(f"Chemin le plus court: {shortest_path}")
#     print(f"Coût total: {total_cost}")