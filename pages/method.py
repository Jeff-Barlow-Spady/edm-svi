
import streamlit as st
st.set_page_config(
    layout="wide", 
    page_title="Neighborhood Scoring System: Statistical Analysis and Model Development Report",
    page_icon="📊"
)
# Title
st.title("Neighborhood Scoring System: Statistical Analysis and Model Development Report")

# Executive Summary
st.header("Executive Summary")
st.markdown(
"""
In this project, I embarked on a statistical journey to create a comprehensive scoring system for neighborhood evaluation. 
Through the application of factor analysis, machine learning optimization, and meticulous visual data exploration,
I developed a model that not only accurately assesses neighborhood characteristics but also provides a statistically sound benchmark for comparison. 
This report encapsulates the detailed analytical processes and presents the project's impactful outcomes.
""")

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
st.markdown("[Score Analysis Link Placeholder](#)")  # Replace with actual link

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
