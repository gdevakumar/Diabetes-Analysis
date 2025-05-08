import numpy as np
from preswald import Workflow, text, table, plotly, sidebar, RetryPolicy, connect, get_df
import pandas as pd
import plotly.express as px

# Set retry policy for the workflow
retry_policy = RetryPolicy(max_attempts=3, delay=1.0)

# Create a workflow instance
workflow = Workflow(default_retry_policy=retry_policy)

@workflow.atom()
def load_data():
    try:
        connect()
        df = get_df('sample_csv')
        return df
    except Exception as e:
        text(f"Error loading data: {str(e)}")
        return None

@workflow.atom(dependencies=["load_data"])
def analyze_data(load_data):
    df = load_data
    
    if df is None:
        text("No data available for analysis.")
        return
    
    # Display header for data analysis
    text("# CSV Data Analysis")
    
    # Section: Displaying Data
    text("## Displaying Data")
    table(df.head(10))  # Show first 10 rows

    # Call the visualization function
    visualize_data(df)

@workflow.atom(dependencies=["load_data"])
def visualize_data(data):
    if data is None:
        text("No data available for visualization.")
        return

    # Section: Recommended Visualizations

    # 1. Age Distribution
    fig1 = px.histogram(data, x='Age', title='Age Distribution')
    plotly(fig1)

    # 2. BMI vs. Cholesterol Scatter Plot
    fig2 = px.scatter(data, x='Age', y='Cholesterol_Total', color='Sex', title='Age vs Total Cholesterol')
    plotly(fig2)

    # 3. Blood Pressure Levels
    fig3 = px.box(data, y='Blood_Pressure_Systolic', title='Blood Pressure Systolic Levels')
    plotly(fig3)

    # 4. Cholesterol Levels by Sex
    fig4 = px.box(data, x='Sex', y='Cholesterol_Total', title='Cholesterol Levels by Sex')
    plotly(fig4)
    
    # 5. Waist Circumference by Physical Activity Level
    fig5 = px.box(data, x='Physical_Activity_Level',  y='Waist_Circumference', color='Physical_Activity_Level', title='Waist Circumference by Physical Activity Level')
    plotly(fig5)

# Execute the workflow
workflow.execute()

