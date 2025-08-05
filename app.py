import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(layout="wide")
st.title("🚛 RouteOptimizer360 – Real-Time Vehicle Routing Optimization")

# Sidebar input
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload Distance Matrix (CSV)", type=["csv"])
num_vehicles = st.sidebar.number_input("Number of Vehicles", min_value=1, max_value=10, value=3)
depot_index = st.sidebar.number_input("Depot Index (starting point)", min_value=0, value=0)

def solve_vehicle_routing(distance_matrix, num_vehicles, depot=0):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_idx, to_idx):
        return int(distance_matrix[manager.IndexToNode(from_idx)][manager.IndexToNode(to_idx)])
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)

    if not solution:
        return None

    routes = []
    total_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))  # Add depot/end
        routes.append((route, route_distance))
        total_distance += route_distance

    return routes, total_distance

def plot_routes(routes):
    fig, ax = plt.subplots(figsize=(10, 6))
    for idx, (route, dist) in enumerate(routes):
        y = [idx] * len(route)
        ax.plot(route, y, marker='o', label=f'Vehicle {idx+1} | Distance: {dist}')
    ax.set_xlabel("Node Index")
    ax.set_ylabel("Vehicle")
    ax.set_title("Optimized Routes per Vehicle")
    ax.legend()
    st.pyplot(fig)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, header=None)
        distance_matrix = df.values.tolist()
        st.success("✅ Distance matrix uploaded successfully!")
        if st.sidebar.button("Run Optimization"):
            result = solve_vehicle_routing(distance_matrix, num_vehicles, depot_index)
            if result is None:
                st.error("❌ No solution found. Try reducing the number of vehicles or fixing your data.")
            else:
                routes, total_distance = result
                st.subheader("📍 Optimized Routes")
                for i, (route, dist) in enumerate(routes):
                    st.markdown(f"**Vehicle {i+1}:** {' → '.join(map(str, route))} (Distance: {dist})")
                st.markdown(f"### 🧮 Total Distance: {total_distance}")
                plot_routes(routes)
    except Exception as e:
        st.error(f"Error reading the distance matrix: {e}")
else:
    st.info("📤 Please upload a CSV file containing the distance matrix.")
