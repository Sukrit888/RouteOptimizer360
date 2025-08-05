import streamlit as st
import pandas as pd
import pydeck as pdk
from generate_sample_data import generate_delivery_data, HUB_COORDS
from route_optimizer import naive_route, nearest_neighbor_route, calculate_total_distance

# Streamlit UI
st.title("RouteOptimizer360 - Milestone 2")
st.sidebar.header("Settings")
num_points = st.sidebar.slider("Number of delivery points", 5, 50, 10)
algorithm = st.sidebar.selectbox("Select Route Algorithm", ["Naive Route", "Nearest Neighbor"])

# Generate data
df = generate_delivery_data(num_points)
df_points = df.copy()
df_points["type"] = "delivery"
hub = pd.DataFrame([{"latitude": HUB_COORDS[0], "longitude": HUB_COORDS[1], "type": "hub"}])
df_all = pd.concat([hub, df_points], ignore_index=True)

# Optimize route
if algorithm == "Naive Route":
    route = naive_route(df)
elif algorithm == "Nearest Neighbor":
    route = nearest_neighbor_route(HUB_COORDS, df)

total_distance = calculate_total_distance(HUB_COORDS, route)
st.sidebar.markdown(f"**Total Route Distance:** {total_distance:.2f} units")

# Map display
route_df = pd.DataFrame(route, columns=["latitude", "longitude"])
layers = [
    pdk.Layer(
        "ScatterplotLayer",
        data=df_all,
        get_position="[longitude, latitude]",
        get_color="[200, 30, 0, 160]",
        get_radius=100,
    ),
    pdk.Layer(
        "LineLayer",
        data=route_df,
        get_source_position="[-1] if index == 0 else [route_df.longitude[index-1], route_df.latitude[index-1]]",
        get_target_position="[longitude, latitude]",
        get_color=[0, 100, 255],
        get_width=3,
        pickable=True,
        auto_highlight=True
    )
]

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=HUB_COORDS[0],
        longitude=HUB_COORDS[1],
        zoom=12,
        pitch=0,
    ),
    layers=layers,
))