import streamlit as st

st.title("Project Overview")

# Page name: Project introduction
tab1_intro, tab2_intro = st.tabs(["Overview", "Motivation"])
tab1_intro.subheader("Project description")
tab1_intro.markdown("In this project a model is developed for Rijkswaterstaat in order to reduce the average response times of road inspectors to incidents. \
                    The current model that Rijkswaterstaat uses to determine the positions of the road inspectors results in an average response time to incidents of 18 minutes. \
                    The goal is to develop and optimise a model that has an average response time that is less than these 18 minutes.")
tab1_intro.markdown("\n")

tab1_intro.subheader("Research question")
tab1_intro.markdown("The research question that is answered in this project is: ")
tab1_intro.markdown('''<p style="font-size: 18px;">\
At which locations do the road inspectors need to be placed in order to optimize the response time to incidents? </p>''', unsafe_allow_html=True)
tab1_intro.markdown("\n")

tab1_intro.subheader("Approach")
tab1_intro.markdown("In order to develop a model and get results that answer the research question, the following approach were taken. \
                    These approaches are explained in detail in Methodology page. \n\
1. Cleaning the data \n\
2. Selecting candidate locations for inspectors \n\
3. Calculating a cost-matrix \n\
4. Formulating the optimisation model \n\
5. Combining the results for a global solution \n\
6. Calibration and validation")
tab1_intro.markdown("\n")
# tab1_intro.markdown("First the data is cleaned. This is done to make sure that all the data that is not needed or not suitable for the model are removed. In this step also the incidents are connected to a location on the highway network. In the second step candidate locations for inspectors are selected. This are all the locations were a car can change direction on the road network, so at the intersections. Having a limited number of potential locations for the road inspectors means that the number of shortest path calculations is not too large. Next a cost-matrix is calculated. Here a weight is given to each candidate note in combination with each incident based on the distance between them. The next step is to formulate the optimisation model, where each of the first three steps are input. In the final step the results are combined for a global solution. This global solution is based on a set of solutions for a specified number of days.")

tab1_intro.subheader("Results")
tab1_intro.markdown("The result is a global solution where the locations are selected that have the highest score. The map below shows the location of them.")
tab1_intro.markdown("\n")
# MAP ONLY LOCATION COME HERE
tab1_intro.markdown("As an example, the matching of the solutions of road inspectors' locations and random days are shown below. The first figure shows the locations of the road inspectors and the incidents on a random day. The second figure shows the locations of the road inspectors and the incidents on the same day, but now the road inspectors are located at the locations of the global solution.")
# MAP WITH LOCATION AND INCIDENTS COME HERE


tab1_intro.subheader("Recommendations")
tab1_intro.markdown("Even though optimal locations of road inspectors had been obtained, there are still some recommendations that can be made. \
                    The first recommendation is to consider the time domain of the incidents and the road inspectors. \
                    Because the incidents have its duration and road inspectors requires time to travel to the location of the incidents, \
                    the time domain of the incidents and the road inspectors should be considered to have a more realistic model. \
                    The second recommendation is to consider the traffic conditions when calculating the travel time of the road inspectors. \
                    In this model, the road inspectors were assumed to travel at a constant speed of 100 km/h. \
                    However, in reality the speed of the road inspectors is affected by the traffic conditions, especially when it is near an incident. \
                    Therefore, to estimate the travel time more accurately, the traffic conditions should be considered. ")


tab2_intro.subheader("Project motivation")
tab2_intro.markdown("Rijkswaterstaat has recently develop a new model to determine what the best locations are for the road inspectors that Rijkswaterstaat employs. The reason why this is so important is that the response time of the road inspectors needs to be as short as possible. The quicker a road inspector is at the locations of an incident or some kind of obstruction, the less disturbance there is for the other road users. A couple of factors are important here: \n \
- The traffic safety needs to be as high as possible. With an incident there are most likely people on the side of the road and they need to be brought to safety by removing the incident. \n \
- An obstruction might lead to another incident and this must be prevented by removing it as quick as possible. \n \
- The traffic flow needs to be as smooth as possible to prevent delays. An incident and also an obstruction can disturb this flow.")
tab2_intro.markdown("\n")
tab2_intro.markdown("The new model Rijkswaterstaat has developed has led to a reduce in response time from 18 to 14 minutes. This is a significant reduce, however the new positioning of road inspectors might not be the only factor that has reduced the response time. Another factor might be that Rijkswaterstaat has improved the communication with other road inspectors, which means that the number of road inspectors going to one incident is more efficient now. Another factor could be that the characteristics of certain roads have changed.")
tab2_intro.markdown("\n")
tab2_intro.markdown("\n")