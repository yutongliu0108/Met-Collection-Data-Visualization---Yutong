##Project Overview
-Visualizations using data from the Met Museum Collection.
-3 main visualizations:
(1)Network Graph: Artist connections based on shared mediums.
(2)Animated Bar Chart: Number of objects by artist over time.
(3)Heatmap: Correlation between object dimensions and dates.

##Installation
Please intall all necessary libraries
Step 1. Create a Virtual Environment
python -m venv venv
Step 2. Activate the Virtual Environment
Windows: venv\Scripts\activate
Mac:source venv/bin/activate
step 3: install the followings manually:
pip install requests
pip install pandas
pip install plotly
pip install streamlit
pip install networkx
pip install seaborn
pip install matplotlib

##Usage
-Open terminal and go to the project folder.
run "streamlit run visualization_all.py" and "python visualization_1_plotly"

##Data Source
-From the Metropolitan Museum of Art Collection API (url: "https://metmuseum.github.io/)
-Data: https://collectionapi.metmuseum.org/public/collection/v1/objects

  
