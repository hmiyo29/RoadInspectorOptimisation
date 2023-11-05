import streamlit as st
import pandas as pd
import os

path_image = ""

st.title("Methodology")

tab1, tab2, tab3 = st.tabs(["Data processing", "Model", "Sensitivity Analysis"])


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
tab2.markdown('''<p style="font-size: 18px;">\
                <b> Variables </b> </p>''', unsafe_allow_html=True)
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
tab2.markdown('''<p style="font-size: 18px;">\
                <b> Constraints </b> </p>''', unsafe_allow_html=True)
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
tab2.markdown("\n")
tab2.caption("Concept of the second constraint")
tab2.image(path_image + "capacity.png", use_column_width=True)
              
tab2.markdown("Mathematically, this constraint is defined as follows:")
tab2.latex(r'''
\sum_{j \in J} x_{ij} \leq 10 \cdot c_i \quad \forall i \in I
''')
tab2.markdown("\n")
tab2.markdown("The third constraint is to limit the number of road inspectors. \
              The number of inspectors on the network are limited. \
              This constraint is defined as follows:")
tab2.latex(r'''
\sum_{i \in I} c_i \leq N
''')
tab2.markdown("\n")
latext = r'''
Where
$N$
is the maximum number of road inspectors.
'''
tab2.write(latext)
tab2.markdown("The number of maximum road inspectors are one of the parameters that can be flexible.\
              The impact of this parameter will be discussed later.")
tab2.markdown("\n")
tab2.markdown('''<p style="font-size: 18px;">\
                <b> Objective functions </b></p>''', unsafe_allow_html=True)
tab2.markdown("\n")
tab2.markdown("The objective function of the model should be defined to indicate the optimality of the solution. \
              For this model, the objective function is defined as minimising the total travel distance. \
              Minimising the total travel distance will result in minimising the average travel distance of the road inspectors, \
              and thus the average response time of the road inspectors will be minimised as well. \
              This is based on the assumption that the road inspectors are able to travel on a constant speed.")
tab2.markdown("\n")
tab2.markdown("Mathematically, the objective function is defined as follows:")
tab2.latex(r'''
\min \sum_{i \in I} \sum_{j \in J} x_{ij} \cdot d_{ij}
''')
tab2.markdown("\n")
latext = r'''
Where
$d_{ij}$
is the driving distance between the candidate point $i$ and the incident $j$.
'''
tab2.write(latext)
tab2.markdown("\n")
tab2.markdown("The mathematical formulation of the model were implemented in Python using Gurobi package. \
              Gurobi package is a package that specialises in solving optimisation problems. \
              It is known as one of the most powerful and fastest optimisation solver in Python.")
# ---------------------------------------- Aggregation of results ------------------------------------------------------------------------------------
tab2.subheader("Aggregation of results")
tab2.markdown("\n")
tab2.markdown("The optimal locations of the road inspectors were obtained for each scenario, and the results were aggregated to obtain the global optimal locations. \
              The aggregation process is explained in this section.")
tab2.markdown("\n")
tab2.markdown("Our group decided to consider the frequency of the scenario occurring in the aggregation process. \
              Each day has different number of incidents occurring. Our group believe that the scenarios with more likelihood to occur should be \
              considered more important than the scenarios with less likelihood to occur.")
tab2.markdown("\n")
tab2.markdown("The figure below shows the histogram of the number of incidents per day in the incident dataset. \
              It can be observed that the distribution of the number of incidents fits well with the normal distribution. \
              This fitted normal distribution uses the average and standard deviation of the number of incidents per day from the incident dataset.")
tab2.caption("Histogram of the number of incidents per day")
tab2.image(path_image + "histogram_incidents.png", use_column_width=True)
tab2.markdown("\n")
tab2.write(r'''For each day, the probability of the number of incidents occurring was calculated using the fitted normal distribution.
           Then, this probability was used as the weight of the day, and the optimal locations of inspectors of the day were assigned with the weight (score)
            and summed up. As a result, the global optimal locations of the road inspectors will be the $N$ locations with the highest score.''')
# ---------------------------------------------------------------------- END TAB 2 ------------------------------------------------------------------------
# ---------------------------------------------------------------------- TAB 3 ----------------------------------------------------------------------------
tab3.header('Sensitivity analysis')
tab3.markdown("In this section the sensitivity analysis of the final model will be discussed. The purpose of this sensitivity analysis is to see how sensitive the results are to changes in the parameters of the model. Four different parameters have been chosen for this analysis, these are: \n\
1. The weights used for combining the solutions from the training")
tab3.markdown("\n")
tab3.markdown("As explained earlier, after the optimised locations of the inspectors for the 60 training days were in these locations needed to be combined into a final solution. This was done by assigning a weight to the solutions based on how likely that day was to occur. Here this method is compared to the results from using no weights, or in other words, with all weights set to 1. \n")
tab3.markdown("\n")
tab3.markdown("2. The total number of inspectors in the network")
tab3.markdown("\n")
tab3.markdown("In the gurobi optimisation there is no disadvantage to adding more inspectors to the network, which means that the best result will almost always be the maximum number of inspectors. Here the maximum number of inspectors that can be assigned to the network is reduced to 110 and 100 to see how well these solutions compare to the standard of 120 inspectors. \n")
tab3.markdown("\n")
tab3.markdown("3. The minimum euclidian distance between inspectors")
tab3.markdown("\n")
tab3.markdown("After combining the results from the training the 120 locations with the highest scores were picked. But these locations were often close together, so by introducing a minimum euclidian distance between inspectors the algorithm was forced to spread them out more. The default value used for this was 5000 meter, this was tested against the values of: 0, 1000, 2000, 3000, 4000, 6000, 7000 meter. \n")
tab3.markdown("\n")
tab3.markdown("4. The minimum path distance between inspectors")
tab3.markdown("\n")
tab3.markdown("Another way of spreading out the inspectors over the network was by adding a minimum path distance. Here the default value was 15000 meter which was tested against the values of: 0, 2500, 5000, 7500, 10000, 12500, 17500 meter. \n")
tab3.markdown("\n")
tab3.markdown("It should be noted that in order to reduce calculation time the values of point 3 and 4 were paired up with each other in increasing order instead of testing them against all other values. The pairs used for the analysis were: [0, 0], [1000, 2500], [2000, 5000] etc.")

tab3.subheader('Results sensitivity analysis')
tab3.markdown('After running the analysis for all parameters described above the results were analysed by calculating the average response time on 20 different days. These results are displayed in boxplots below. There are 6 different boxplots for the 6 possible combinations from parameters 1 and 2. Paremeter 4 is displayed on the y-axis, keep in mind that these are paired up with parameter 3.')

tab3.image('./All boxplots.png', use_column_width=True)

# tab3.caption('120 inspectors with weights')
# tab3.image('./Boxplots_with_weight_120.png', width=500)
# tab3.markdown("\n")
# tab3.caption('120 inspectors without weights')
# tab3.image('./Boxplots_without_weight_120.png', width=500)
# tab3.markdown("\n")
# tab3.caption('110 inspectors with weights')
# tab3.image('./Boxplots_with_weight_110.png', width=500)
# tab3.markdown("\n")
# tab3.caption('110 inspectors without weights')
# tab3.image('./Boxplots_without_weight_110.png', width=500)
# tab3.markdown("\n")
# tab3.caption('100 inspectors with weights')
# tab3.image('./Boxplots_with_weight_100.png', width=500)
# tab3.markdown("\n")
# tab3.caption('100 inspectors without weights')
# tab3.image('./Boxplots_without_weight_100.png', width=500)
# tab3.markdown("\n")
# tab3.markdown('There are several conclusion which can be made from those boxplots. The first which is very obvious is that in all cases it holds true that the fewer inspectors there are in the network the slower the average response time will be. The second is that the average response times for the different ranges from a crescent shape which indicates an optimum of a minimum path distance between 7500-10000 meter and a minimum euclidian distance between 3000-4000 meter. A third interesting observation is that when the minimum distance between the inspectors is either large or small the variation in response times increases. The weights (parameter 1) do not seem to have a significant influence on the response times.')
