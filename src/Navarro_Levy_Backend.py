"""
----------------------------IMPORTACIÓN DE LAS LIBRERÍAS ORTOOLS (ES NECESARIO INSTALARLAS, NO SON NATIVAS DE PYTHON)----------------------------
"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import networkx as nx
import matplotlib.pyplot as plt
import time

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
    #Matriz de demandas asociadas a cada nodo
    data["demands"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     #Creación de los vehículos con su capacidad respectiva
    data["vehicle_capacities"] = [12, 17]
    #Devolución del diccionario
    return data

"""
----------------------------------------------------IMPRESIÓN DE LA SOLUCIÓN EN LA CONSOLA----------------------------------------------------
"""
def print_solution(data, manager, routing, solution, original_packages, routes_info):
    #Se inicializa la distancia máxima
    max_route_distance = 0
    #Ciclo for que itera sobre cada vehículo
    for vehicle_id in range(data["num_vehicles"]):
        #Se obtiene el índice del inicio para el vehículo actual
        index = routing.Start(vehicle_id)
        #Se inicia una cadena de texto empezando por el identificador del vehículo
        plan_output = f"Ruta del vehículo {vehicle_id}:\n"
        #Se inicializa la disntancia recorrida
        route_distance = 0
        #Lista para almacenar los paquetes llevados por este vehículo
        packages_carried = []  

        #Verificar si hay información adicional sobre la ruta del vehículo actual
        if vehicle_id in routes_info:
            route = routes_info[vehicle_id]
            for node_index in route:
                plan_output += f" {node_index} -> "
                route_distance += routing.GetArcCostForVehicle(
                    index, manager.NodeToIndex(node_index), vehicle_id
                )
                
                # Si el nodo tiene un paquete asignado, se agrega a la lista de paquetes llevados
                if node_index in original_packages:
                    packages_carried.append((node_index, original_packages[node_index]))

                index = manager.NodeToIndex(node_index)
        else:
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                plan_output += f" {node_index} -> "
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

                # Si el nodo tiene un paquete asignado, se agrega a la lista de paquetes llevados
                if node_index in packages:
                    packages_carried.append((node_index, packages[node_index]))

            node_index = manager.IndexToNode(index)
            plan_output += f"{node_index}\n"

        plan_output += f"Distancia de la ruta: {route_distance}m\n"
        
        # Imprime los paquetes llevados por este vehículo
        if packages_carried:
            plan_output += "Paquetes llevados:\n"
            for package, demand in packages_carried:
                plan_output += f"  Paquete {package} - Demanda: {demand}\n"

        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)


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
def main(packages):
    #Creación de la instancia para recibir el diccionario
    data = create_data_model()

    #Creación de un índice de gestión de rutas
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    #Se crea un modelo de enrutamiento y se asocia con el índice de gestión de rutas creado arriba
    routing = pywrapcp.RoutingModel(manager)

    #Suma de las demandas
    total_demand = sum(packages.values())
    #Suma de la capacidad de los vehículos
    total_capacity = sum(data["vehicle_capacities"])

    # Verificar si la demanda total supera la capacidad inicial de los vehículos
    if total_demand > total_capacity:
        print("La capacidad inicial de los vehículos es insuficiente para cargar todos los paquetes. Los paquetes se dividirán en varios viajes.")

        # Ordenar los paquetes por demanda de menor a mayor
        sorted_packages = dict(sorted(packages.items(), key=lambda item: item[1]))

        #Inicializar variables para separar los paquetes en packages y waiting_packages
        current_capacity = data["vehicle_capacities"][0]  # Capacidad del primer vehículo
        packages = {}
        waiting_packages = {}

        # Separar los paquetes en packages y waiting_packages según la capacidad de los vehículos
        for node, demand in sorted_packages.items():
            if current_capacity >= demand:
                packages[node] = demand
                current_capacity -= demand
            else:
                waiting_packages[node] = demand

        print("Paquetes a llevar: ",packages)
        print("Paquetes en espera: ",waiting_packages)

        #Modificación de la matriz de demandas según los paquetes ingresados por el usuario
        for node, demand in packages.items():
            data["demands"][node] = demand

        #Función dedicada a tomar dos indices y devolver la distancia que los separa
        def distance_callback(from_index, to_index):
            #Retorna la distancia entre dos nodos
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        #Se registra la función de devolución de llamada como un callback de tránsito en el modelo de enrutamiento
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        #Definir una función que se utilizará como callback para las capacidades de los vehículos
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]
        
        # Registrar el callback de demanda como una restricción de capacidad en el modelo de enrutamiento
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # No se inicia la capacidad en cada nodo, se maneja acumulativamente
        data["vehicle_capacities"],  # Capacidades de los vehículos
        True,  # True para tener en cuenta la capacidad restante
        "Capacity"
        )
        
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
            # Copia de seguridad de los paquetes originales
            original_packages = packages.copy()
            # Recopilar información sobre la solución actual
            routes_info = {}
            for vehicle_id in range(data["num_vehicles"]):
                index = routing.Start(vehicle_id)
                route = []
                last_package_node = -1  # Nodo del último paquete entregado por el vehículo
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))

                    # Verificar si el nodo tiene un paquete asignado
                    if node_index in packages:
                        last_package_node = node_index  # Actualizar el nodo del último paquete entregado

                route.append(manager.IndexToNode(index))
                routes_info[vehicle_id] = route

                # Obtener los paquetes llevados por cada vehículo
                packages_carried = []
                for node_index in route:
                    if node_index in packages:
                        packages_carried.append((node_index, packages[node_index]))

                # Actualizar la información de los paquetes y capacidades de los vehículos
                for node_index, demand in packages_carried:
                    del packages[node_index]

                # Verificar si el vehículo entregó algún paquete y actualizar la ruta
                if last_package_node != -1:
                    # Construir la ruta solo hasta el último paquete entregado
                    route = route[:route.index(last_package_node) + 1]
                    routes_info[vehicle_id] = route
                    route.append(data["depot"])

            print_solution(data, manager, routing, solution, original_packages, routes_info)
            #Llamada recursiva a la función main con los waiting_packages
            main(waiting_packages)
        
        #De no ser así, se imprime que no se encontró una solución
        else:
            # Si el vehículo no entregó ningún paquete, simplemente conservar la ruta actual
            route = route[:]
            print("No se encontró una solución")
    
    #Si la capacidad de carga de los vehículos no se ve superada por la demanda de los paquetes
    else:
        #Función dedicada a tomar dos indices y devolver la distancia que los separa
        def distance_callback(from_index, to_index):
            #Retorna la distancia entre dos nodos
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        #Se registra la función de devolución de llamada como un callback de tránsito en el modelo de enrutamiento
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        #Definir una función que se utilizará como callback para las capacidades de los vehículos
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]
        
        # Registrar el callback de demanda como una restricción de capacidad en el modelo de enrutamiento
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # No se inicia la capacidad en cada nodo, se maneja acumulativamente
        data["vehicle_capacities"],  # Capacidades de los vehículos
        True,  # True para tener en cuenta la capacidad restante
        "Capacity"
        )

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
        solution = routing.SolveWithParameters(search_parameters) #Justo aquí se traba el programa

        #Verificación si se encontró solución
        #De ser encontrada, se imprime la solución
        if solution:
            # Copia de seguridad de los paquetes originales
            original_packages = packages.copy()
            # Recopilar información sobre la solución actual
            routes_info = {}
            for vehicle_id in range(data["num_vehicles"]):
                index = routing.Start(vehicle_id)
                route = []
                last_package_node = -1  # Nodo del último paquete entregado por el vehículo
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))

                    # Verificar si el nodo tiene un paquete asignado
                    if node_index in packages:
                        last_package_node = node_index  # Actualizar el nodo del último paquete entregado

                route.append(manager.IndexToNode(index))
                routes_info[vehicle_id] = route

                # Obtener los paquetes llevados por cada vehículo
                packages_carried = []
                for node_index in route:
                    if node_index in packages:
                        packages_carried.append((node_index, packages[node_index]))

                # Actualizar la información de los paquetes y capacidades de los vehículos
                for node_index, demand in packages_carried:
                    del packages[node_index]

                # Verificar si el vehículo entregó algún paquete y actualizar la ruta
                if last_package_node != -1:
                    # Construir la ruta solo hasta el último paquete entregado
                    route = route[:route.index(last_package_node) + 1]
                    routes_info[vehicle_id] = route
                    route.append(data["depot"])

            print_solution(data, manager, routing, solution, original_packages, routes_info)
        
        #De no ser así, se imprime que no se encontró una solución
        else:
            # Si el vehículo no entregó ningún paquete, simplemente conservar la ruta actual
            route = route[:]
            print("No se encontró una solución")




"""
------------------------------------------------------LLAMADO DEL MAIN Y DIBUJADO DEL GRAFO------------------------------------------------------
"""

if __name__ == "__main__":
    #Paquetes con sus respectivas demandas para cada nodo
    packages = {5: 6, 2: 8, 10: 1, 16: 5, 7: 4, 14: 4, 12: 2, 1: 12}  
    #Invocación de la función que encuentra e imprime la solución
    main(packages)
    #Declaración de la variable que recibe el diccionario de datos que contiene los vehículos, los nodos y el depósito
    data = create_data_model()
    #Guarda en la variable distance_matrix el elemento de las distancias de la matriz contenida en el diccionario previamente recibido
    distance_matrix = data["distance_matrix"]
    #Se llama a la función que dibuja el grafo
    draw_graph(distance_matrix)