import streamlit as st
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(page_title="RouteOptimizer360", layout="centered")

st.title("🚛 RouteOptimizer360 – Real-Time Vehicle Routing Optimization")

uploaded_file = st.file_uploader("📤 Upload your Distance Matrix CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, index_col=0)
        st.success("✅ Distance matrix uploaded successfully!")
        st.dataframe(df)

        # Ensure square matrix
        if df.shape[0] != df.shape[1]:
            st.error("❌ The distance matrix must be square (NxN).")
        else:
            # Convert DataFrame to nested list
            distance_matrix = df.values.tolist()
            locations = df.index.tolist()

            # Ask user for number of vehicles and depot index
            num_vehicles = st.number_input("🚚 Number of Vehicles", min_value=1, max_value=10, value=1)
            depot_index = st.selectbox("🏢 Select Depot", locations, index=0)
            depot = locations.index(depot_index)

            if st.button("🚀 Optimize Route"):
                try:
                    # OR-Tools model
                    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
                    routing = pywrapcp.RoutingModel(manager)

                    def distance_callback(from_index, to_index):
                        from_node = manager.IndexToNode(from_index)
                        to_node = manager.IndexToNode(to_index)
                        return distance_matrix[from_node][to_node]

                    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

                    solution = routing.SolveWithParameters(search_parameters)

                    if solution:
                        st.success("✅ Route optimized successfully!")
                        for vehicle_id in range(num_vehicles):
                            index = routing.Start(vehicle_id)
                            route = []
                            route_distance = 0
                            while not routing.IsEnd(index):
                                node = manager.IndexToNode(index)
                                route.append(locations[node])
                                previous_index = index
                                index = solution.Value(routing.NextVar(index))
                                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                            route.append(locations[manager.IndexToNode(index)])

                            st.markdown(f"### 🚚 Vehicle {vehicle_id + 1}")
                            st.write(" → ".join(route))
                            st.write(f"📏 Total Distance: {route_distance}")
                    else:
                        st.error("❌ No solution found.")
                except Exception as e:
                    st.error(f"❌ Optimization failed: {e}")

    except Exception as e:
        st.error(f"Error reading the distance matrix: {e}")
