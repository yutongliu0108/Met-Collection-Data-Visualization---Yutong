import requests
import networkx as nx
import pandas as pd
import plotly.graph_objects as go

# Fetch data from the API
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
response = requests.get(url)
data = response.json()

# Check if the response is valid and contains objectIDs
if response.status_code == 200 and 'objectIDs' in data:
# Get the first 200 object IDs
# Sampling Methodology: I use the first 200 object IDs as a sample
    object_ids = data['objectIDs'][:200]  

# Store object data
    objects_data = []

# Fetch detailed data for each object
    for obj_id in object_ids:
        obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
        obj_response = requests.get(obj_url)

        if obj_response.status_code == 200:
            obj_data = obj_response.json()
            
# Data Cleaning: Ensure the object contains valid artist and medium data before appending
# Only add objects where both 'artist' and 'medium' are present
            artist = obj_data.get('artistDisplayName')
            medium = obj_data.get('medium')
            if artist and medium:
                objects_data.append({
                    'objectID': obj_data.get('objectID'),
                    'title': obj_data.get('title'),
                    'artist': artist,
                    'medium': medium
                })

 # Create a DataFrame
    df = pd.DataFrame(objects_data)

# Create a network graph
    G = nx.Graph()

# Add artist and medium nodes and connect them
    for _, row in df.iterrows():
        artist = row['artist']
        medium = row['medium']
        if artist:
            G.add_node(artist, type='artist')
        if medium:
            mediums = medium.split(', ') if isinstance(medium, str) else []
            for m in mediums:
                G.add_node(m, type='medium')
                G.add_edge(artist, m)

# Set node positions
    pos = nx.spring_layout(G, k=0.1, iterations=50)
    x_vals = [pos[node][0] for node in G.nodes()]
    y_vals = [pos[node][1] for node in G.nodes()]
    node_labels = list(G.nodes())

# Create coordinates for edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

 # Create node scatter plot
    node_trace = go.Scatter(
        x=x_vals, y=y_vals, mode='markers', text=node_labels, hoverinfo='text',
        marker=dict(showscale=True, colorscale='YlGnBu', color='blue', size=10, line=dict(color='black', width=1))
    )

# Create edge scatter plot
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='#888'), hoverinfo='none'
    )

# Set layout for the graph
    layout = go.Layout(
        title="Artist Connections Network", title_font_size=16, showlegend=False,
        hovermode='closest', xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False)
    )

# Display the graph
    fig_network = go.Figure(data=[edge_trace, node_trace], layout=layout)
    fig_network.show()

else:
    print("Failed to fetch data.")
