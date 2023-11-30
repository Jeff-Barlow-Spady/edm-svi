
import streamlit as st
st.set_page_config(
    layout="wide", 
    page_title="Neighborhood Scoring System: Statistical Analysis and Model Development Report",
    page_icon="📊",
    theme="auto"  # Set theme to "auto" to use system setting for light or dark mode
)
# Title
st.title("Neighborhood Scoring System: Statistical Analysis and Model Development Report")
st.markdown("""Analysis by Jeff Barlow-Spady""")    # Markdown text
st.markdown("""This report details the methodology, analysis, and outcomes of the Neighborhood Scoring System project.""")
st.divider()
st.header("Objective")
st.markdown(
"""
The primary goal of this analysis was to develop a comprehensive understanding of neighbourhood vulnerability using various socio-economic, 
demographic, and environmental metrics. The aim was to distil these complex datasets into a single, 
interpretable vulnerability score for each neighbourhood.
""")
# Executive Summary
st.header("Executive Summary")
st.markdown(
"""
In this project, I embarked on an ambitious project to create a comprehensive scoring system for neighborhood evaluation. 
Through the application of factor analysis, machine learning optimization, and meticulous visual data exploration,
I developed a model that not only accurately assesses neighborhood characteristics but also provides a statistically sound benchmark for comparison. 
This report encapsulates the detailed analytical processes and presents the project's impactful outcomes.
""")
st.header("Data Sources")

st.markdown("The analysis utilized three primary data sources:")

st.markdown("### 2021 Federal Census - Long Form:")
st.markdown("There were over 2000 characteristics measured for each neighbourhood. After reviewing the documentation with the dataset I chose the following possible indicators of exposure to social vulnerability:")
st.markdown("- total_population")
st.markdown("- homeowners_core_housing_need")
st.markdown("- total_core_housing_need")
st.markdown("- tennants_in_core_housing_need")
st.markdown("- owners_30%*or_more")
st.markdown("- total_30%plus_shelter")
st.markdown("- tennants_30%plus_shelter_cost")
st.markdown("- tennants_subs_housing")
st.markdown("- Low_Income_Measure_18_to_64_years(%)")
st.markdown("- Low_Income_Cutoff_18_to_64_years(%)")
st.markdown("- housing_stock_1960_and_earlier")
st.markdown("- housing_stock_61_to_80")
st.markdown("- New LIM 65 years and over")
st.markdown("- new LICO 65 plus")
st.markdown("- proportion_children")
st.markdown("- total sum Gini index on adjusted household after-tax income")
st.markdown("- in_single_parent_families")
st.markdown("- bottom_decile*%")
st.markdown("- bottom_half_dist")
st.markdown("- second_decile_prop")
st.markdown("- Living alone 42 34")
st.markdown("- less_than_hs")
st.markdown("- non_perm_resident")
st.markdown("- non_citizens")
st.markdown("- unsuitable_housing")
st.markdown("- Low-income cut-offs, after tax (LICO-AT) (%)")
st.markdown("- Low-income measure, after tax (LIM-AT) (%)")
st.markdown("- Renters")
st.markdown("- visible_minority_population")
st.markdown("- unemployed")

st.markdown("### Edmonton Neighbourhoods 2021 Dataset:")
st.markdown("From City of Edmonton Open Data Portal - used to match neighbourhood names, geometry and lat/long to the 2021 Federal Census.")

st.markdown("### Shrubscriber Canopy Coverage vs Population Density:")
st.markdown("I used this data to get average temperature, canopy information, confirmation of land area, and trees per square kilometre.")
st.markdown("Key steps in data preparation included merging these datasets on neighborhood names, normalizing the data, and calculating additional metrics such as population density. Used to create:")
st.markdown("- Lacking_canopy - the compliment of the land area per neighbourhood without measured canopy")
st.markdown("- Population Density (People/sq. km)")

st.header("Data Preparation")

st.markdown("All data was cleaned, validated and then combined into a single dataset using Excel and Python.")

st.markdown("All numeric columns were converted to proportions of the population, made uni-directional so that a higher number denotes increased risk of vulnerability.")

st.markdown("Data Normalization: For this analysis I used Z-Score Normalization. Z-score normalization is a statistical technique used to standardize data by transforming it to a common scale. It calculates the z-score for each data point, which represents the number of standard deviations that data point is away from the mean. This normalization process allows for easier comparison and interpretation of data across different variables or datasets.")

st.markdown("Building score categories was the next step. I used the method similar to the one described in this paper:")
st.markdown("Reid, C., O’Neill, M., Gronlund, C., Brines, S., Brown, D., Diez-Roux, A., Schwartz, J. (2009). Mapping community determinants of heat vulnerability. Environmental Health Perspectives, 117(11), 1730–1736.")
st.markdown("[http://doi.org/10.1289/ehp.0900683](http://doi.org/10.1289/ehp.0900683)")
st.code(
"""
#Calculate 'VI' columns/Index scores based on the method from Reid et all 2009
def calculate_index(x):
    if x <= -2:
        return 1
    elif -2 < x <= -1:
        return 2
    elif -1 < x <= 0:
        return 3
    elif 0 < x <= 1:
        return 4
    elif 1 < x <= 2:
        return 5
    elif x > 2:
        return 6
    else:
        return 7
#insert into current dataframe
for column in ind_columns:
    subset_df[column + '_VI'] = subset_df[column].apply(calculate_index)
""", language="python")

# Factor Analysis
st.header("Factor Analysis")
st.markdown(
"""
I commenced with a detailed factor analysis on the standardized variables, which was instrumental in unraveling the fundamental factors hidden within the dataset. 
This approach was critical in uncovering latent patterns and structures that are not immediately apparent.
""")
st.subheader("Figure 1: Scree Plot for 5 Factors")
st.image("data/Scree.png") # Replace with actual image path


# Identification of Significant Factors
st.header("Identification of Significant Factors")
st.markdown(
    """
Utilizing scree plots, I meticulously identified the significant factors. 
This step was crucial in ensuring that the core characteristics of the dataset were captured efficiently and accurately.
""")
st.subheader("Figure 2: Cumulative Explained Variance by PCA Components")
st.image("data/PCA.png")  # Replace with actual image path

# Extraction of Feature Importances
st.header("Extraction of Feature Importances")
st.markdown(
"""
I harnessed the power of machine learning models to extract feature importances. 
This process was key in pinpointing the variables that have the most substantial impact on the scoring system.
""")

# Machine Learning Optimization
st.header("Machine Learning Optimization")
st.subheader("Hyperparameter Tuning")
st.markdown(
"""
I performed an exhaustive grid search for XGBoost and Random Forest models. 
This rigorous optimization of hyperparameters was aimed at enhancing the accuracy and efficiency of the models.
""")

# Model Evaluation
st.subheader("Model Evaluation")
st.markdown(
"""
The models were evaluated using a variety of metrics such as mean squared error, explained variance, and R². 
This diverse range of metrics provided a comprehensive view of the model's performance and robustness.
""")

# Optimization and Weight Assignment
st.subheader("Optimization and Weight Assignment")
st.markdown(
"""
The culmination of this phase was identifying the optimal models and isolating their feature importances. 
This led to the development of a composite weight for each feature, culminating in a final, weighted score for each neighborhood.
""")
st.subheader("Figure 3: Feature Importances from Best XGBoost Model")
st.image("data/XGB.png")  # Replace with actual image path
st.subheader("Figure 4: Feature Importances from Random Forest Model")
st.image("data/RF.png")  # Replace with actual image path

# Visual Data Exploration
st.header("Visual Data Exploration")
st.subheader("Histograms and Density Plots")
st.markdown(
"""
I delved into histograms and density plots of z-score standardized variables, which gave a clear picture of the data point distributions and their nuances.
""")
st.image("data/Density.png")  # Replace with actual image path

# Pairwise Scatter Plots Analysis
st.subheader("Pairwise Scatter Plots Analysis")
st.markdown(
"""
An analysis of pairwise scatter plots shed light on correlations and trends. 
These insights were pivotal in shaping the composite score and understanding the interplay between different variables.
""")
st.image("data/Pairplot.png")  # Replace with actual image path

# Project Impact
st.header("Project Impact")
st.subheader("Statistically Sound Benchmarking")
st.markdown(
"""
The project's outcome is a set of weighted scores that provide a statistically sound benchmark for comparing neighborhoods.
""")
st.subheader("Commitment to Data Integrity")
st.markdown("""
My thorough and detailed approach highlights my unwavering commitment to data integrity and analytical precision.
""")
st.subheader("Highlighting Data-Driven Insights")
st.markdown(
"""
The project showcases the significant impact of data-driven insights. 
The combination of visual and quantitative analyses solidifies the statistical significance of our scoring method and provides a reliable metric for stakeholders.
This not only enhances the decision-making process but also underscores the value of meticulous data analysis in real-world applications.
""")

# Score Analysis
st.header("Score Analysis")

# Summary Statistics
st.subheader("Summary Statistics")

st.markdown("""
- **Unweighted Score**:
    - Count: 274 entries
    - Mean: ~118.89
    - Standard Deviation: ~17.35
    - Min: 74
    - 25th Percentile: 108
    - Median: 119
    - 75th Percentile: 130
    - Max: 170
- **Weighted Score**:
    - Count: 274 entries
    - Mean: ~10.04
    - Standard Deviation: ~1.87
    - Min: ~5.15
    - 25th Percentile: ~8.95
    - Median: ~10.03
    - 75th Percentile: ~11.18
    - Max: ~15.51
- **Quartiles**: Both unweighted and weighted scores are divided into quartiles ranging from 0 to 3, where a higher quartile represents a higher score range.
""")

# Visualizations
st.subheader("Visualizations")
st.image("data/histo.png")
st.image("data/b_plot.png")
st.markdown(
"""
- **Histograms**: Both unweighted and weighted scores appear to be approximately normally distributed,
with a single peak around the mean.
- **Boxplots**: The boxplots show that the unweighted scores have a wider range and higher median compared to the weighted scores. 
There are no obvious outliers in either distribution, which suggests that scores are relatively evenly distributed across neighbourhoods.
- **Scatter Plot**: The scatter plot of weighted vs. unweighted scores indicates a positive relationship between the two,
 as would be expected since they are based on the same data
""")
st.image("data/weighted_corr.png")
# Observations
st.subheader("Observations")
st.markdown("""
- The distributions of scores are roughly symmetric, and the presence of a single peak suggests that most neighbourhoods cluster around the mean score.
- The quartile information shows that the data is evenly split across the quartile ranges.
- The positive correlation between unweighted and weighted scores indicates consistency in scoring across the two methods.
""")
