import streamlit as st

tab1, tab2, tab3 = st.tabs(['dummy', 'dummy', 'Sensitivity analysis'])

tab3.header('Sensitivity analysis')
tab3.markdown("In this section the sensitivity analysis of the final model will be discussed. The purpose of this sensitivity analysis is to see how sensitive the results are to changes in the parameters of the model. Four different parameters have been chosen for this analysis, these are: \n\
1. The weights used for combining the solutions from the training \n\
As explained earlier, after the optimised locations of the inspectors for the 60 training days were in these locations needed to be combined into a final solution. This was done by assigning a weight to the solutions based on how likely that day was to occur. Here this method is compared to the results from using no weights, or in other words, with all weights set to 1. \n\
2. The total number of inspectors in the network \n\
In the gurobi optimisation there is no disadvantage to adding more inspectors to the network, which means that the best result will almost always be the maximum number of inspectors. Here the maximum number of inspectors that can be assigned to the network is reduced to 110 and 100 to see how well these solutions compare to the standard of 120 inspectors. \n\
3. The minimum euclidian distance between inspectors \n\
After combining the results from the training the 120 locations with the highest scores were picked. But these locations were often close together, so by introducing a minimum euclidian distance between inspectors the algorithm was forced to spread them out more. The default value used for this was 5000 meter, this was tested against the values of: 0, 1000, 2000, 3000, 4000, 6000, 7000 meter. \n\
4. The minimum path distance between inspectors \n\
Another way of spreading out the inspectors over the network was by adding a minimum path distance. Here the default value was 15000 meter which was tested against the values of: 0, 2500, 5000, 7500, 10000, 12500, 17500 meter. \n\
It should be noted that in order to reduce calculation time the values of point 3 and 4 were paired up with each other in increasing order instead of testing them against all other values. The pairs used for the analysis were: [0, 0], [1000, 2500], [2000, 5000] etc.")

tab3.subheader('Results sensitivity analysis')
tab3.markdown('After running the analysis for all parameters described above the results were analysed by calculating the average response time on 20 different days. These results are displayed in boxplots below. There are 6 different boxplots for the 6 possible combinations from parameters 1 and 2. Paremeter 4 is displayed on the y-axis, keep in mind that these are paired up with parameter 3.')

st.image(['./Boxplots_with_weight_120.png', './Boxplots_without_weight_120.png'], caption=['120 inspectors with weights', '120 inspectors without weights'])
st.image(['./Boxplots_with_weight_110.png', './Boxplots_without_weight_110.png'], caption=['110 inspectors with weights', '110 inspectors without weights'])
st.image(['./Boxplots_with_weight_100.png', './Boxplots_without_weight_100.png'], caption=['100 inspectors with weights', '100 inspectors without weights'])

tab3.markdown('There are several conclusion which can be made from those boxplots. The first which is very obvious is that in all cases it holds true that the fewer inspectors there are in the network the slower the average response time will be. The second is that the average response times for the different ranges from a crescent shape which indicates an optimum of a minimum path distance between 7500-10000 meter and a minimum euclidian distance between 3000-4000 meter. A third interesting observation is that when the minimum distance between the inspectors is either large or small the variation in response times increases. The weights (parameter 1) do not seem to have a significant influence on the response times.')

