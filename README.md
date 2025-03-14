## Project Overview
- Visualizations using data from the Met Museum Collection:
The project visualizes the connections between artists and the mediums they use, utilizing data from the Metropolitan Museum of Art's API. 3 visualizations are created using Plotly and Streamlit to represent these relationships.
- 3 main visualizations:
  1. **Network Graph**: Artist connections based on shared mediums.
  2. **Animated Bar Chart**: Number of objects by artist over time.
  3. **Heatmap**: Correlation between object dimensions and dates.

## Installation

Please install all necessary libraries:

-Step 1: Create a Virtual Environment
python -m venv venv

-Step 2: Activate the Virtual Environment
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

-Step 3: Install the Following Manually:
pip install requests
pip install pandas
pip install plotly
pip install streamlit
pip install networkx
pip install seaborn
pip install matplotlib

## Usage

- Open terminal and go to the project folder.
- Run the following command to start the Streamlit app:
streamlit run visualization_all.py
for the one using plotly:
python visualization_1_plotly

## Data Source

From the Metropolitan Museum of Art Collection API (https://metmuseum.github.io/)
Data: https://collectionapi.metmuseum.org/public/collection/v1/objects
