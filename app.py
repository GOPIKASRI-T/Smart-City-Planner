import pandas as pd
from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__)


print("Current Working Directory:", os.getcwd())


df = pd.read_csv('DATASETnew.csv')


@app.route('/')
def home():
    return render_template('index.html')

# Traffic Analysis route
@app.route('/traffic')
def traffic_analysis():
    # Plot the traffic analysis (vehicle count by hour)
    fig = px.line(df, x='hour', y='vehicle_count', title='Traffic Analysis: Vehicle Count by Hour')
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('traffic.html', graph_html=graph_html)

# Energy Consumption route
@app.route('/energy')
def energy_consumption():
    # Plot the energy consumption by zone
    fig = px.bar(df, x='zone', y='energy_usage', title='Energy Consumption by Zone')
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('energy.html', graph_html=graph_html)

# Environmental Conditions route
@app.route('/environment')
def environmental_conditions():
    try:
        # Ensure 'hour' and 'PM2.5' are in the dataset for plotting Air Quality
        if 'hour' in df.columns and 'PM2.5' in df.columns:
            fig1 = px.scatter(
                df, 
                x='hour', 
                y='PM2.5', 
                title='PM2.5 Levels Over Time', 
                labels={'hour': 'Hour', 'PM2.5': 'PM2.5 Concentration'},
                template='plotly_dark'
            )
            graph_html1 = pio.to_html(fig1, full_html=False)
        else:
            graph_html1 = "<div>Data for PM2.5 levels not available.</div>"
        
        # Ensure 'temperature' and 'vehicle_count' are available for plotting Temperature vs Vehicle Count
        if 'temperature' in df.columns and 'vehicle_count' in df.columns:
            fig2 = px.scatter(
                df, 
                x='temperature', 
                y='vehicle_count', 
                title='Temperature vs Vehicle Count', 
                labels={'temperature': 'Temperature (°C)', 'vehicle_count': 'Vehicle Count'},
                color='zone',
                template='plotly_dark'
            )
            graph_html2 = pio.to_html(fig2, full_html=False)
        else:
            graph_html2 = "<div>Data for Temperature and Vehicle Count not available.</div>"

    except Exception as e:
        # Log the error and provide a user-friendly message
        print(f"Error: {e}")
        graph_html1 = "<div>An error occurred while generating the PM2.5 plot.</div>"
        graph_html2 = "<div>An error occurred while generating the Temperature vs Vehicle Count plot.</div>"

    return render_template('environmental.html', graph_html1=graph_html1, graph_html2=graph_html2)


if __name__ == '__main__':
    app.run(debug=True)

