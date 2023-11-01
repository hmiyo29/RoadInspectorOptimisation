import streamlit as st
import pandas as pd
import os

path_image = ""

st.title("Methodology")

tab1, tab2 = st.tabs(["Data processing", "Model"])


# ---------------------------------------------------------------------- TAB 1 ------------------------------------------------------------------------

# ---------------------------------------- Intro of data processing -----------------------------------------------------------------------------
# Tab 1: Data processing
tab1.header("Data processing")
tab1.markdown("In this section, the procedure of the data processing is introduced. \
                The process is divided into 3 parts.\n 1. Cleaning data \n 2. Assigning incident data to road network \n 3. Selecting candidate points for road inspectors\n")

tab1.subheader("Cleaning data")
tab1.markdown("For this project, the highway network of the Netherlands in shapefile, and the incident record data were provided. \
                The overview of the data are shown below:")
tab1.markdown("\n")


# ---------------------------------------- Overview of data ------------------------------------------------------------------------------------
# Screenshot of the dataframes
tab1.caption("The overview of the incident record data")    
tab1.image(path_image + "df_incident_image.png", use_column_width=True)
tab1.markdown("\n")
text_incident = ("The incident record data consists of the type of incidents, start time and end time, the location and the road number. \
                    The duration was simply calculated by subtracting the starting time from the end time.")
tab1.markdown(text_incident)
tab1.caption("The overview of the highway network data")
folium_map_html = open("map.html", "r", encoding="utf-8").read()
tab1._html(folium_map_html, height=600)
text_network = ("The road network data was provided in shapefile. \
                Each geometry of the data information such as road number, direction, \
                and the location of the points that compose the linestring.")
tab1.markdown(text_network)

# ---------------------------------------- Data cleaning ------------------------------------------------------------------------------------

# Overview
text_process = """
**The data cleaning process is as follows:**\n
"""
tab1.markdown(text_process)
text_step = '''
1. Editting road network to assure connectivity in the network \n
2. Incident data filtering  
'''
tab1.markdown(text_step, unsafe_allow_html=True)
tab1.markdown("\n")
# Editting road network
tab1.markdown('''<p style="font-size: 18px;">\
1. Editting road network to assure connectivity in the network </p>''', unsafe_allow_html=True)
tab1.markdown("\n")
tab1.markdown("The road network data had some road segments that did not have connectivity. \
              These road segments are connected by adding edges between the end point and the begin point of the road segments. \
              The driving direction of the road segments were also considered when selecting the end and begin points. \
              When the road has a # in the attribute, edges were added in both directions.\
              After creating the edges, the number of edges entering the node and leaving the node were counted and stored as attributes. \
              This network was translated into a directed graph using NetworkX package in Python. \
              This will be used for the candidate selection process.")
tab1.image(path_image + "ani_network_clean.gif", use_column_width=True)

# Incident data filtering
tab1.markdown("\n")
tab1.markdown('''<p style="font-size: 18px;">\
                2. Incident data filtering </p>''', unsafe_allow_html=True)
tab1.markdown("\n")
tab1.markdown("Some incident data were not reliable to apply for the project. \
               Each incident has the start time and end time, thus the duration of the incident. \
               Some incidents have extremely long duration, as it lasted for the whole 3 months. \
               These incidents were removed from the data.")
tab1.markdown("\n")


# ---------------------------------------- Incident data to network ------------------------------------------------------------------------------------
tab1.subheader("Assigning incident data to road network")
tab1.write("Some incidents' locations were not exactly located on the highway network. \
           This can be because of the coverage area of the incident data and also the measurement accuracy of the locations.\
           As the GIF below shows, the incidents were relocated to the closest node of the road network that was found by Euclidian distance.\
           By this process, each node on the road network will have certain number of incidents being assinged.")
tab1.write("Through this process, all incidents were relocated on the road network, \
           and by this process it will be possible to calculate the distance between the incident and the inspectors location nodes.\
           For the driving distance calculation, the euclidian distances between the new position and the original position were taken into account \
           so that the driving distance would not be underestimating too much compared to the actual distance before the relocation.\n")
tab1.caption("Concept of the relocation of the incidents")
tab1.image(path_image + "ani_incident_node.gif", use_column_width=True)
tab1.markdown("\n")


# ---------------------------------------- Candidate points selection ------------------------------------------------------------------------------------
tab1.subheader("Selecting candidate points for road inspectors\n")
tab1.markdown("In order to identify the optimal location of the inspectors, \
              the candidate locations were selected from the nodes of the road network so that it will be possible to apply \
              optimisation and also remove irrational locations from candidates. \
              \n \
              Firstly, the intersections on the road network were selected as candidates. \
              Intersection points were selected because the road inspectors would be able to drive to multiple directions and this would cover the road network more efficiently\
              compared to locating the inspectors in the middle of a road segment. This is possible by referring to the number of edges entering and leaving the nodes.\
              After this, a location which has another location within 500 meters range was removed. \
              This is to prevent multiple road inspectors being located too close to each other.\
              The figure below shows the overview and a zoomed-in example of the candidate points. The green cross points are the candidate points.\
              After the candidate point selection, 1936 candidate locations for the road inspectors were set, and these locations were used for the optimisation process.")
tab1.caption("Overview of the candidate points")
tab1.image(path_image + "candidate_point_new.png", use_column_width=True)
tab1.markdown("\n")
tab1.caption("Zoomed-in example of the candidate points")
tab1.image(path_image + "candidate_point_zoom_new.png", use_column_width=True)


# ---------------------------------------------------------------------- END TAB 1 ------------------------------------------------------------------------
# ---------------------------------------------------------------------- TAB 2 ----------------------------------------------------------------------------
tab2.header("Model")
tab2.markdown("In this section, the model set up for obtaining the optimal locations of road inspectors is introduced. \
              Through this process, the optimal locations of the road inspectors will be obtained for each scenario and also the global optimal locations.\
              The model is divided into 3 parts.\n 1. Calculation of cost-matrix \n 2. Optmisation model  \n 3. Aggregation of results")
tab2.markdown("\n")
tab2.markdown("The first part calculates the driving distance between the road inspectors' candidate locations and the incidents. By applying this cost-matrix, \
              the optimisation model was build in the second part. \
              Lastly, the thrid part shows how we aggregated the results of the optimisation model to obtain the global optimal locations.\
              Each step will be explained below.")
tab2.markdown("\n")

# ---------------------------------------- Calculation of cost-matrix ---------------------------------------------------------------------------
tab2.subheader("Calculation of cost-matrix")
tab2.markdown("\n")
tab2.markdown("The cost-matrix is the matrix that contains the driving distance between the candidate locations and the incidents. \
              The road inspectors are expected to be located as close as possible to the incidents to respond to the incidents as fast as possible. \
              The driving distance will indicate how close the road inspectors locations are to the incidents.")
tab2.markdown("\n")
tab2.markdown("In the data processing, the road network and the incident data were implemented into a graph by NetworkX package in Python. \
              Each edges in the graph has the distance as an attribute, and these distances will be applied to calculate the distance between two points in the network. \n \
              For the path finding, the 'shortest_path_length' function in NetworkX was used. \
              This function calculates the shortest path between two nodes in the graph and returns the distance of the path. \
              This function applies dijkstra algorithm to find the shortest path between two nodes.")
tab2.caption("Concept of Dijkstra algorithm")
tab2.image(path_image + "dijkstra.gif", use_column_width=True)
tab2.markdown("\n")
tab2.markdown("However, since there are externsive amount of candidate points and on average around 800 incidents per day, \
              the pair of nodes to calculate the driving distance were limited in advance. \
              The path betwenn a pair of candidate points and incident points with a euclidian distance of more than 50 km was not calculated \
              because it is not possible for the road inspectors to reach an incident that far in a short time, and that incident should be handled by a closer inspector. \
              For these pairs, a value of 1E9 meters. In addition, some pairs did not have possible path available because of the imcompleteness of the road network. \
              For these pairs, a value of 2E9 meters were assigned. These large values will prevent from these pairs being chosen (= an inspector handling an incindent) \
              later in the optimisation.")
tab2.markdown("\n")
tab2.markdown("The figure below shows the concept of the cost-matrix.")
tab2.caption("Cost-matrix")
tab2.image(path_image + "cost-matrix.png", use_column_width=True)
                
# ---------------------------------------- Optmisation model ------------------------------------------------------------------------------------
tab2.subheader("Optmisation model")
tab2.markdown("\n")
tab2.markdown("So far, the candidate points for the road inspectors and the method to calculate the cost-matrix were introduced.\
              In this section, the optimisation model to obtain the optimal locations of the road inspectors for a given incident dataset is explained.")
tab2.markdown("\n")
tab2.markdown("For the formulation of the model, the variables, constraints, and the objective function are defined.")
tab2.markdown("\n")
tab2.markdown("**Variables**")
tab2.markdown("\n")
tab2.markdown("The variables of the model should be defined to indicate the optimal locations of the road inspectors. \
              For this, a binary variable is defined.")
tab2.latex(r"x_{ij} = {0, 1} \quad \forall  i \in I, j \in J")
tab2.markdown("\n")
latext = r'''
Where  
$I$ 
is the set of candidate points, and 
$J$
is the set of incidents. If the variable 
$x_{ij}$
is 1, it means that the road inspector located at the candidate point
$i$
is assigned to the incident
$j$.
Otherwise the variable would be 0.
'''
tab2.write(latext)
tab2.markdown("\n")
tab2.markdown("In addition, another binary variable is defined to indicate whether the candidate point is selected or not.")
tab2.latex(r"c_{i} = {0, 1} \quad \forall  i \in I")
tab2.markdown("\n")
latext = r'''
$c_{i}$ will be 1 if the candidate point $i$ is selected, and 0 otherwise.
'''
tab2.write(latext)
tab2.markdown("\n")
tab2.markdown("**Constraints**")
tab2.markdown("\n")
tab2.markdown("The constraints of the model should be defined to assure the rationality of the solution and have some assumptions implemented. \
              There are three constraints defined for this model.")
tab2.markdown("\n")
tab2.markdown("1. Each incident should be handled by exactly one road inspector. \n 2. Road inspector has a capacity of 10 incidents to handle. \n 3. The number of road inspectors are limited.")
tab2.markdown("\n")
tab2.markdown("The first constraint is to assure that each incident is handled by exactly one road inspector. Of course every incident must be handled, \
              and in reality it is possible that multiple road inspectors handle one incident together.\
              However, for simplicity of the model, it is assumed that each incident is handled by exactly one road inspector. ")
tab2.markdown("\n")
tab2.caption("Concept of the first constraint")
tab2.image(path_image + "1by1rule.png", use_column_width=True)
tab2.markdown("\n")
tab2.markdown("Mathematically, this constraint is defined as follows:")
tab2.latex(r"\sum_{i \in I} x_{ij} = 1 \quad \forall j \in J")
tab2.markdown("\n")
tab2.markdown("The second constraint is to assure that each road inspector can handle up to 10 incidents.")

              
tab2.markdown("Mathematically, this constraint is defined as follows:")
tab2.latex(r'''
\sum_{j \in J} x_{ij} \leq 10 \cdot c_i \quad \forall i \in I
''')


