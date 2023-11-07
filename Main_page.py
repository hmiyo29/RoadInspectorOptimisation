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
N = tab1_intro.slider("Number of inscpectors", min_value=100, max_value=120, step=10)
tab1_intro.write("Optimal locations for road inspectors when there are {} road inspectors".format(N))
tab1_intro.markdown("\n")
# MAP WITH LOCATION COME HERE
dict_loc = {100: open("maps\location_100.html", "r", encoding="utf-8").read(), 
            110: open("maps\location_110.html", "r", encoding="utf-8").read(), 
            120: open("maps\location_100.html", "r", encoding="utf-8").read()}
tab1_intro._html(dict_loc[N], height=600, scrolling=True)

tab1_intro.markdown("As an example, the matching of the solutions of road inspectors' locations and random days are shown below. The first figure shows the locations of the road inspectors and the incidents on a random day. \
                    The second figure shows the locations of the road inspectors and the incidents on the same day, but now the road inspectors are located at the locations of the global solution.")
tab1_intro.markdown("\n")
N2 = tab1_intro.slider("Number of inscpectors ", min_value=100, max_value=120, step=10)
days = tab1_intro.selectbox("Days", ["2019-08-02", "2019-09-16", "2019-10-03"])
# MAP WITH LOCATION AND INCIDENTS COME HERE
dict_match = {100: {"2019-08-02": open("maps\matching_2019-08-02_100.html", "r", encoding="utf-8").read(),
                    "2019-09-16": open("maps\matching_2019-09-16_100.html", "r", encoding="utf-8").read(),
                    "2019-10-03": open("maps\matching_2019-10-03_100.html", "r", encoding="utf-8").read()},
              110: {"2019-08-02": open("maps\matching_2019-08-02_110.html", "r", encoding="utf-8").read(),
                    "2019-09-16": open("maps\matching_2019-09-16_110.html", "r", encoding="utf-8").read(),
                    "2019-10-03": open("maps\matching_2019-10-03_110.html", "r", encoding="utf-8").read()},
              120: {"2019-08-02": open("maps\matching_2019-08-02_120.html", "r", encoding="utf-8").read(),
                    "2019-09-16": open("maps\matching_2019-09-16_120.html", "r", encoding="utf-8").read(),
                    "2019-10-03": open("maps\matching_2019-10-03_120.html", "r", encoding="utf-8").read()}}
tab1_intro._html(dict_match[N2][days], height=600, scrolling=True)
tab1_intro.markdown("\n")
tab1_intro.markdown("The boxplot and histrogram below show the distribution of the response times of the road inspectors \
                    in each number of road inspectors scenario for the days used for the valudation of the optimal locations.")
tab1_intro.markdown("\n")
# BOX PLOT AND HISTOGRAM COME HERE
tab1_intro.image("validation.jpg", use_column_width=True)
tab1_intro.markdown("\n")
tab1_intro.markdown("The distribution of the average response time of the road inspectors in each number of road inspectors scenario\
                    shows that the response time for each day has an average of less than 18 minutes. \
                    This means that new locations of road inspectors are likely to be able to reach the incidents on average less than 18 minutes in most days. \
                    It can also be seen that the average response time decreases when the number of inspectors increases. \
                    This is plausible because the road inspector will need to cover larger area when there are less road inspectors, \
                    and needs more time to reach the incidents further away.")

# CONCLUSION AND RECOMMENDATION
tab1_intro.subheader("Conclusion")
tab1_intro.markdown("This project was aimed to find the optimal locations of road inspectors so that the average response time to incidents are less than 18 minutes. \
                    Our group was able to determine the optimal locations of road inspectors given the incident data in 3 scenarios, \
                    which are 100, 110, and 120 road inspectors. In any scenario, the average response time was validated to be less than 18 minutes.")
tab1_intro.markdown("**Check the maps above again for the final results!**")
tab1_intro.markdown("As expected, the number of road inspectors affects the average response time to incidents. The more inspectors are available, \
                    the less time it takes to reach the incidents. Also, there are some regional bias in the distribution of the optimal locations. \
                    It can be seen that the Randstad area has more inspectors being located than the other areas. \
                    This is because incidents occur in this area more frequently than other areas, and that has been taken into account in the model by\
                    obtaining the optimal locations of each day, and aggregating the results of all days in the incident dataset.")

tab1_intro.markdown("The optimal locations were determined by formulating a linear programming model that minimizes the total travel time of the road inspectors given a set of incidents. \
                    As an input of the model, the set of candidate points of road inspectors were selected in rational way, \
                    and the incident data was cleaned to be assigned onto the road network in the data processing step. \
                    The mathematical model was formulated to satisfy the conditions of the problem, \
                    and the variables were optimised to minimise the total travel distance of the road inspectors, \
                    so that the average response time will be minimised as well. The model was solved using Gurobi in Python.")

tab1_intro.markdown("Each result of the optimisation model was aggregated by applying a weight to each result (day) \
                    based on the number of incidents in each day. By summing the weighted results, \
                    the global optimal locations of road inspectors were obtained.\
                    In addition, sensitivity analyses were conducterd to capture the influence of the parameters to obtain the global optimal locations. \
                    These analyses helped to understand what role each parameter plays in the model, and gave the best parameter settings to obtain the best global solution.\
                    After the calibration, the validation was conducted with the calibrated parameters settings and it was validated that the average response time is less than 18 minutes.")
tab1_intro.markdown("The advantade of the approach we took is that it is simple, and it is able to update the optimal locations of road inspectors \
                    by adding data of the incident sets and adjusting the parameters of the model based on the new dataset.")
                    

tab1_intro.subheader("Recommendations")
tab1_intro.markdown("Even though optimal locations of road inspectors had been obtained, there are still some recommendations that can be made to improve the model. \
                    The first recommendation is to consider the time domain of the incidents and the road inspectors. \
                    Because the incidents have its duration and road inspectors requires time to travel to the location of the incidents, \
                    the time domain of the incidents and the road inspectors should be considered to have a more realistic model. \
                    The second recommendation is to consider the traffic conditions when calculating the travel time of the road inspectors. \
                    In this model, the road inspectors were assumed to travel at a constant speed of 100 km/h. \
                    However, in reality the speed of the road inspectors is affected by the traffic conditions, especially when it is near an incident. \
                    Therefore, to estimate the travel time more accurately, the traffic conditions should be considered. \
                    Lastly, in this project, there were not any aspects to lower the number of inspectors. In general, the average response time would \
                    keep improving if the number of inspectors increases. However, in reality there is a limitation to the number of inspectors. \
                    This can be because of the budget, for instance. Therefore, it is important to consider the trade-off between the cost of the road inspectors \
                    and the benefit of shortening the average response time, and decide the extent of how well the average response time should be improved.")


tab2_intro.subheader("Project motivation")
tab2_intro.markdown("Rijkswaterstaat has recently develop a new model to determine what the best locations are for the road inspectors that Rijkswaterstaat employs. The reason why this is so important is that the response time of the road inspectors needs to be as short as possible. The quicker a road inspector is at the locations of an incident or some kind of obstruction, the less disturbance there is for the other road users. A couple of factors are important here: \n \
- The traffic safety needs to be as high as possible. With an incident there are most likely people on the side of the road and they need to be brought to safety by removing the incident. \n \
- An obstruction might lead to another incident and this must be prevented by removing it as quick as possible. \n \
- The traffic flow needs to be as smooth as possible to prevent delays. An incident and also an obstruction can disturb this flow.")
tab2_intro.markdown("\n")
tab2_intro.markdown("The new model Rijkswaterstaat has developed has led to a reduce in response time from 18 to 14 minutes. This is a significant reduce, however the new positioning of road inspectors might not be the only factor that has reduced the response time. Another factor might be that Rijkswaterstaat has improved the communication with other road inspectors, which means that the number of road inspectors going to one incident is more efficient now. Another factor could be that the characteristics of certain roads have changed.")
tab2_intro.markdown("\n")
tab2_intro.markdown("\n")