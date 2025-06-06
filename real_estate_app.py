import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the dataset
real_estate_data = pd.read_csv("Real_Estate.csv",parse_dates=False)  # <-- Replace with your actual path if needed

# Selecting features and target variable
features = ['Distance to the nearest MRT station', 'Number of convenience stores', 'Latitude', 'Longitude']
target = 'House price of unit area'

X = real_estate_data[features]
y = real_estate_data[target]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Real Estate Price Predictor"

# Define the layout
app.layout = html.Div([
    html.H1("🏠 Real Estate Price Prediction", style={'text-align': 'center', 'color': '#007BFF'}),

    html.Div([
        dcc.Input(id='distance_to_mrt', type='number', placeholder='Distance to BUS Station (meters)',
                  style={'margin': '10px', 'padding': '10px'}),
        dcc.Input(id='num_convenience_stores', type='number', placeholder='Number of Convenience Stores',
                  style={'margin': '10px', 'padding': '10px'}),
        dcc.Input(id='latitude', type='number', placeholder='Latitude',
                  style={'margin': '10px', 'padding': '10px'}),
        dcc.Input(id='longitude', type='number', placeholder='Longitude',
                  style={'margin': '10px', 'padding': '10px'}),

        html.Button('Predict Price', id='predict_button', n_clicks=0,
                    style={'margin': '10px', 'padding': '10px',
                           'background-color': '#007BFF', 'color': 'white', 'border': 'none'}),
    ], style={'text-align': 'center'}),

    html.Div(id='prediction_output',
             style={'text-align': 'center', 'font-size': '20px', 'margin-top': '20px'})
], style={
    'width': '50%',
    'margin': '0 auto',
    'border': '2px solid #007BFF',
    'padding': '30px',
    'border-radius': '15px',
    'font-family': 'Arial'
})


# Define the callback
@app.callback(
    Output('prediction_output', 'children'),
    Input('predict_button', 'n_clicks'),
    State('distance_to_mrt', 'value'),
    State('num_convenience_stores', 'value'),
    State('latitude', 'value'),
    State('longitude', 'value')
)
def update_output(n_clicks, distance_to_mrt, num_convenience_stores, latitude, longitude):
    if n_clicks > 0:
        if None in (distance_to_mrt, num_convenience_stores, latitude, longitude):
            return "❗ Please enter all the values to make a prediction."

        # Create DataFrame for prediction
        features_input = pd.DataFrame([[distance_to_mrt, num_convenience_stores, latitude, longitude]],
                                      columns=features)

        prediction = model.predict(features_input)[0]
        return f"💰 Predicted House Price of Unit Area: {prediction:.2f}"

    return ""

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
