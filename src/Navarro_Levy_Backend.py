"""
----------------------------IMPORTACIÓN DE LAS LIBRERÍAS ORTOOLS (ES NECESARIO INSTALARLAS, NO SON NATIVAS DE PYTHON)----------------------------
"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import networkx as nx
import matplotlib.pyplot as plt

"""
---------------------------CREACIÓN DE DATOS DE ENTRADA (VEHÍCULOS, DISNTANCIAS ENTRE NODOS Y UBICACIÓN DEL DEPOSITO)---------------------------
"""

#Función que cre la matriz con los nodos propuestos
def create_data_model():
    #Almacenamiento de los datos para el problema
    data = {}
    #Distancia entre las ubicaciones
    data["distance_matrix"] = [
      [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
      [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
      [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
      [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
      [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
      [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
      [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
      [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
      [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
      [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
      [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
      [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
      [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
      [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
      [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
      [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
      [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
    ]
    #Creación de los vehículos
    data["num_vehicles"] = 2
    #Ubicación del deposito (inicio y fin de la ruta) en la posición 0
    data["depot"] = 0
    #Devolución del diccionario
    return data

"""
----------------------------------------------------IMPRESIÓN DE LA SOLUCIÓN EN LA CONSOLA----------------------------------------------------
"""
def print_solution(data, manager, routing, solution):
    #Impresión del valor de la solución, es decir, la distancia recorrida por todos los vehículos
    print(f"Sumatoria de las rutas: {solution.ObjectiveValue()}")
    #Inicialización de la variable que hace un seguimiento de la distancia máxima de las rutas de los vehículos
    max_route_distance = 0
    #Ciclo for que itera sobre cada vehículo
    for vehicle_id in range(data["num_vehicles"]):
        #Se obtiene el índice del inicio para el vehículo actual
        index = routing.Start(vehicle_id)
        #Se inicia una cadena de texto empezando por el identificador del vehículo
        plan_output = f"Ruta del vehículo {vehicle_id}:\n"
        #Se inicializa la disntancia recorrida
        route_distance = 0
        #Bucle while para recorrer todos los nodos de la ruta hasta llegar al final
        while not routing.IsEnd(index):
            #Agrega el nodo actual a la cadena de salida
            plan_output += f" {manager.IndexToNode(index)} -> "
            #Se almacena el índice actual como el índice anterior para calcular la distancia del arco en la siguiente iteración
            previous_index = index
            #Obtención del siguiente índice en la ruta
            index = solution.Value(routing.NextVar(index))
            #Se agrega el costo del costo del arco actual a la distancia total de la ruta del vehículo
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        #Adición del nodo final de la ruta a la cadena de salida
        plan_output += f"{manager.IndexToNode(index)}\n"
        #Adición de la distancia total de la ruta del vehículo a la cadena de salida
        plan_output += f"Distancia de la ruta: {route_distance}m\n"
        #Impresión de la información de la ruta del vehículo en le consola
        print(plan_output)
        #Actualización de la distancia máxima de las rutas de los vehículos
        max_route_distance = max(route_distance, max_route_distance)
    #Imprime la distancia máxima de todas las rutas de los vehículos al final
    print(f"Distancia máxima recorrida en ruta: {max_route_distance}m")

"""
----------------------------------------------------FUNCIÓN ENCARGADA DEL DIBUJADO DEL GRAFO----------------------------------------------------
"""

def draw_graph(distance_matrix):
    #Se crea un nuevo grafo vacío utilizando NetworkX
    G = nx.Graph()

    #Se determina el número de nodos en el grafo basado en la longitud de la matriz de distancias
    num_nodes = len(distance_matrix)
    #Se agregan los nodos al grafo. Se utilizan los índices del rango de nodos (0 a num_nodes - 1) como etiquetas para los nodos
    G.add_nodes_from(range(num_nodes))

    #Definición de las coordenadas de los nodos 
    node_positions = {
        0: (8.5, 9.5),
        1: (13, 6),
        2: (9, 0),
        3: (1, 13),
        4: (1, 1),
        5: (10.5, 4),
        6: (10.5, 17.5),
        7: (16, 8),
        8: (14, 16),
        9: (3, 17.5),
        10: (7.5, 4),
        11: (5, 5),
        12: (13, 13),
        13: (3, 1.5),
        14: (7, 14),
        15: (3.5, 8),
        16: (15.5, 0),
    }

    #Adición las coordenadas de los nodos al grafo
    nx.set_node_attributes(G, node_positions, "pos")

    #Bucle anidado para agregar aristas y sus respectivas distancias
    #Bucle que itera en cada nodo del grafo
    for i in range(num_nodes):
        #Bucle encargado de ierar sobre los nodos restantes para evitar duplicar la creación de aristas
        for j in range(i+1, num_nodes):
            #Verificación si la distancia es distinta de cero la dibuja
            if distance_matrix[i][j] != 0: 
                #Adición de las aristas entre los nodos "i" y "j" con su respectiva distancia utilizando la matriz de distancias
                G.add_edge(i, j, weight=distance_matrix[i][j])
    
    #Obtención de las posiciones de los nodos del atributo 'pos'
    pos = nx.get_node_attributes(G, "pos")

    #Obtención de los atributos de las aristas del grafo (weight)
    labels = nx.get_edge_attributes(G, 'weight')

    #Dibujo del grafo utilizando las posiciones de los nodos (with_labels=True hace que se muestren las etiquetas)
    nx.draw(G, pos, with_labels=True)
    #Adición de las etiquetas de las distancias a las aristas del gráfico
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    #Muestra el gráfico utilizando matplotlib
    plt.show()

"""
---------------------------------------------------------------FUNCIÓN PRINCIPAL---------------------------------------------------------------
"""
def main():
    #Creación de la instancia para recibir el diccionario
    data = create_data_model()

    #Creación de un índice de gestión de rutas
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    #Se crea un modelo de enrutamiento y se asocia con el índice de gestión de rutas creado arriba
    routing = pywrapcp.RoutingModel(manager)

    #Función dedicada a tomar dos indices y devolver la distancia que los separa
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    #Se registra la función de devolución de llamada como un callback de tránsito en el modelo de enrutamiento
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    #Se define el costo de cada arco (ruta entre dos nodos), utilizando el callback de tránsito
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    dimension_name = "Distance"

    #Se agrega una dimensión al modelo para representar la distancia total recorrida en cada ruta (estableciendo un limite superior de 3000 unidades de distancia y se inicia la acumulación desde 0)
    routing.AddDimension(
        transit_callback_index,
        0,  
        3000,  
        True,  
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)

    #Se establece un coeficiente de costo global para la dimensión de distancia (este coeficiente influye en la prioridad de minimizar la distancia total en comparación con otros objetivos)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    #Se configuran los parámetros de búsqueda predeterminados para el modelo de enrutamiento
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    #Elección de la estrategia de búsqueda de la primera solución (en este caso la estrategia es seleccionar la ruta más barata debido a la función "PATH_CEHAPEST_ARC")
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    #Resolución del problema de enrutamiento utilizando los parámetros de búsqueda configurados y se obtiene la solución
    solution = routing.SolveWithParameters(search_parameters)

    #Verificación si se encontró solución

    #De ser encontrada, se imprime la solución
    if solution:
        print_solution(data, manager, routing, solution)
    #De no ser así, se imprime que no se encontró una solución
    else:
        print("No se encontró una solución")


"""
------------------------------------------------------LLAMADO DEL MAIN Y DIBUJADO DEL GRAFO------------------------------------------------------
"""

if __name__ == "__main__":
    #Invocación de la función que encuentra e imprime la solución
    main()
    #Declaración de la variable que recibe el diccionario de datos que contiene los vehículos, los nodos y el depósito
    data = create_data_model()
    #Guarda en la variable distance_matrix el elemento de las distancias de la matriz contenida en el diccionario previamente recibido
    distance_matrix = data["distance_matrix"]
    #Se llama a la función que dibuja el grafo
    draw_graph(distance_matrix)