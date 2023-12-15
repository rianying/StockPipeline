import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from collections import deque  # Import deque
from datetime import datetime, timedelta  # Import datetime for date handling

# Set the start time for the actual data
start_time_actual = datetime.strptime('05:00:01', '%H:%M:%S')
time_interval = .5  # Update frequency in seconds

# Existing data (replace this with your actual data)
existing_actual_data = [25, 27, 30, 28, 32, 35, 38, 40, 42, 45]  # Example: Existing actual data
existing_predicted_data = [None] * len(existing_actual_data)  # Existing predicted data (initially empty)

# Initialize deque for actual and predicted prices with appropriate lengths
max_data_points = 100  # Adjust the window size as needed
actual_data_length = 75  # Half for actual data
predicted_data_length = 25  # Remaining for predicted data

actual_prices = deque(existing_actual_data[:actual_data_length], maxlen=actual_data_length)  # Actual stock prices as a rolling window
predicted_prices = deque([], maxlen=predicted_data_length)  # Predicted stock prices as a rolling window

# Create Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='stock-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*100,  # in milliseconds (change as needed for update frequency)
        n_intervals=0
    )
])

# Define callback to update graph
@app.callback(
    Output('stock-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    global start_time_actual
    
    # Generate timestamps for actual and predicted data
    timestamp_range_actual = [start_time_actual + timedelta(seconds=i*time_interval) for i in range(len(actual_prices))]
    timestamp_range_predicted = [timestamp_range_actual[-1] + timedelta(seconds=(i+1)*time_interval) for i in range(len(predicted_prices))]
    
    # Update start time for the next iteration
    start_time_actual += timedelta(seconds=time_interval)
    
    # Fetch or generate new actual data (for demonstration)
    # For illustration, let's generate some random data as new incoming data
    new_data_point_actual = generate_random_data_point()  # Replace with your data source
    
    # Update deque for actual prices
    actual_prices.append(new_data_point_actual)
    
    # Check if halfway point is reached and add predicted data
    if len(actual_prices) == actual_data_length:
        # Only randomize the last value of predicted prices after the initial batch
        if len(predicted_prices) == 0:
            # Randomize the initial batch of predicted data
            for _ in range(predicted_data_length):
                predicted_prices.append(generate_random_data_point())  # Example: Append a random data point
        else:
            # Only randomize the last value of predicted prices
            predicted_prices.append(generate_random_data_point())  # Example: Append a random data point
            predicted_prices.popleft()  # Remove the oldest predicted value
    
    # Create traces for the plot
    # Create traces for the plot with improved aesthetics
    trace_actual = go.Scatter(
        x=timestamp_range_actual,
        y=list(actual_prices),
        mode='lines+markers',
        name='Actual Prices',
        line=dict(color='blue', width=2)  # Adjust line color and width
    )

    trace_predicted = go.Scatter(
        x=timestamp_range_predicted,
        y=list(predicted_prices),
        mode='lines+markers',
        name='Predicted Prices',
        line=dict(color='gray', width=2, dash='dash'),  # Change line color to gray
        marker=dict(size=8, color='gray')  # Change marker color to gray
    )

    # Create an appealing layout
    layout = dict(
        title='Real-time Stock Prices',
        xaxis=dict(title='Time', tickformat='%H:%M:%S', showgrid=True, gridcolor='lightgrey'),  # Show gridlines and modify color
        yaxis=dict(title='Stock Price', showgrid=True, gridcolor='lightgrey'),  # Show gridlines and modify color
        plot_bgcolor='rgba(240,240,240,0.9)',  # Set plot background color with transparency
        paper_bgcolor='rgba(240,240,240,0.7)',  # Set paper background color with transparency
        font=dict(family='Arial, sans-serif', size=12, color='black'),  # Adjust font style, size, and color
        legend=dict(x=0, y=1.1),  # Adjust legend position
        margin=dict(l=40, r=40, t=80, b=40),  # Adjust margins for better display
    )

    # Return updated graph
    return {'data': [trace_actual, trace_predicted], 'layout': layout}
# Function to generate random data (for simulation purposes)
def generate_random_data_point():
    # Replace this with your actual method of fetching or generating new data
    import random
    return random.uniform(10, 50)  # Example: Generate random data between 10 and 50

if __name__ == '__main__':
    app.run_server(debug=True)
