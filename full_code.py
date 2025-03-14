import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

# API URL
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

# Fetch data from the API
response = requests.get(url)
data = response.json()

# Parse data if valid response
if response.status_code == 200:
    if 'objectIDs' in data:
        object_ids = data['objectIDs'][:200]
        # Sampling Methodology: I use the first 200 object IDs as a sample for the analysis

# Fetch detailed data for each object
objects_data = []
for obj_id in object_ids:
    obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
    obj_response = requests.get(obj_url)
    if obj_response.status_code == 200:
        obj_data = obj_response.json()
        
        # Data Cleaning: Check if the data is valid and contains required fields
        # Skip invalid or missing data
        objects_data.append({
            'objectID': obj_data.get('objectID'),
            'title': obj_data.get('title'),
            'artist': obj_data.get('artistDisplayName'),
            'date': obj_data.get('objectDate'),
            'medium': obj_data.get('medium'),
            'dimensions': obj_data.get('dimensions'),
            'classification': obj_data.get('classification')
        })

# Create a DataFrame
df = pd.DataFrame(objects_data)

# Display a big title
st.title("Exploring The Met Museum Art Collection")

# Display subtitle for the table
st.subheader("Showing the First 5 Artworks from the Collection")

# Display first 5 rows in Streamlit app
st.write(df.head())

# --- Visualization 1: Network Graph ---

# Create artist-medium network graph
G = nx.Graph()
for _, row in df.iterrows():
    artist = row['artist']
    if artist:
        G.add_node(artist)
    if row['medium']:
        mediums = row['medium'].split(', ') if isinstance(row['medium'], str) else []
        for medium in mediums:
            G.add_edge(artist, medium)

# Position nodes using spring layout and plot
pos = nx.spring_layout(G)
x_vals = [pos[node][0] for node in G.nodes()]
y_vals = [pos[node][1] for node in G.nodes()]
node_labels = list(G.nodes())

trace_nodes = go.Scatter(x=x_vals, y=y_vals, mode='markers', text=node_labels, hoverinfo='text', 
                         marker=dict(color='blue', size=12, line=dict(color='black', width=1)))

trace_edges = go.Scatter(x=[], y=[], mode='lines', line=dict(width=0.5, color='#888'), hoverinfo='none')
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    trace_edges['x'] += (x0, x1, None)
    trace_edges['y'] += (y0, y1, None)

fig_network = go.Figure(data=[trace_edges, trace_nodes])
fig_network.update_layout(title="Artist Connections Network", showlegend=False, hovermode='closest')

# Display network graph in Streamlit
st.plotly_chart(fig_network)

# --- Visualization 2: Animated Bar Chart ---

fig_animation = px.bar(df, x="artist", y="objectID", title="Number of Objects by Artist Over Time", 
                       animation_frame="date", animation_group="artist", hover_data=["artist", "title", "date", "medium"])
fig_animation.update_layout(title="Artist Object Count Over Time", xaxis_title="Artist", yaxis_title="Object Count")

# Display animated chart in Streamlit
st.plotly_chart(fig_animation)

# --- Visualization 3: Scatter Plot ---

# Extract the first number from the dimension string
def clean_dimensions(dim):
    try:
        if isinstance(dim, str):
            dimensions_list = [float(s) for s in dim.split() if s.replace('.', '', 1).isdigit()]
            return dimensions_list[0] if dimensions_list else None
        return None
    except Exception as e:
        return None

# Clean date data: Extract the year
def extract_year(date):
    try:
        year = pd.to_datetime(date, errors='coerce').year
        return year if pd.notnull(year) else None
    except:
        return None

# Apply cleaning functions
df['dimensions_numeric'] = df['dimensions'].apply(clean_dimensions)
df['date_numeric'] = df['date'].apply(extract_year)

# Remove rows with missing data
df_clean = df.dropna(subset=['dimensions_numeric', 'date_numeric'])

# If there is valid data, create the scatter plot
if len(df_clean) > 0:
    fig_scatter = px.scatter(df_clean, x="date_numeric", y="dimensions_numeric", 
                             title="Dimensions vs. Date of Artwork", 
                             labels={"date_numeric": "Year", "dimensions_numeric": "Dimensions (numeric)"}, 
                             hover_data=["title", "artist", "date", "medium"])

    fig_scatter.update_layout(title="Dimensions vs. Date of Artwork", xaxis_title="Year", yaxis_title="Dimensions")

    st.plotly_chart(fig_scatter)
else:
    st.write("No valid data for the scatter plot.")
