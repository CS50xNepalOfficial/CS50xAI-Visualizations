from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.subplots as sp
import numpy as np
import plotly.express as px

app = Dash(__name__)

# Sample data
global X, y
np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 2 * X + 1 + np.random.normal(0, 1, (100, 1))

app.layout = html.Div([
    html.H1("Machine Learning Fundamentals", style={'textAlign': 'center'}),
    
    # Educational Content Section
    html.Div([
        html.H2("Key Concepts", style={'color': '#2c3e50'}),
        
        # Gradient Explanation
        html.Div([
            html.H3("Gradient", style={'color': '#34495e'}),
            html.P([
                "Gradient is the derivative (slope) showing direction of steepest ascent:",
                html.Br(),
                "• Tells us how to adjust parameters",
                html.Br(), 
                "• Negative gradient points to minimum",
                html.Br(),
                "Formula: ∂Loss/∂θ (partial derivative of loss with respect to parameter)"
            ]),
            html.Div([
                "Example:",
                html.Pre("""
                For MSE Loss = (1/2)(hθ(x) - y)²
                Gradient = (hθ(x) - y)x
                Where hθ(x) is prediction and y is actual
                """)
            ], style={'backgroundColor': '#f7f9fc', 'padding': '10px'})
        ]),

        # Learning Rate Explanation 
        html.Div([
            html.H3("Learning Rate (α)", style={'color': '#34495e'}),
            html.P([
                "Learning rate controls step size in gradient descent:",
                html.Br(),
                "• Small α (0.01): Slow but stable learning",
                html.Br(),
                "• Large α (0.5): Fast but might overshoot",
                html.Br(),
                "Formula: θ = θ - α * gradient"
            ]),
            html.Div([
                "Example calculation:",
                html.Pre("""
                If gradient = 2 and θ = 1:
                • α = 0.1: θ = 1 - 0.1 * 2 = 0.8
                • α = 0.5: θ = 1 - 0.5 * 2 = 0
                """)
            ], style={'backgroundColor': '#f7f9fc', 'padding': '10px'})
        ]),

        # Loss Function Explanation
        html.Div([
            html.H3("Loss Function (MSE)", style={'color': '#34495e'}),
            html.P([
                "Measures prediction error:",
                html.Br(),
                "MSE = (1/n) * Σ(y_pred - y_actual)²",
                html.Br(),
                "• Lower loss = better predictions",
                html.Br(),
                "• Gradient descent minimizes loss"
            ]),
            html.Div([
                "Sample calculation:",
                html.Pre("""
                For predictions [2,3] and actuals [1,4]:
                MSE = (1/2) * ((2-1)² + (3-4)²)
                MSE = (1/2) * (1 + 1) = 1
                """)
            ], style={'backgroundColor': '#f7f9fc', 'padding': '10px'})
        ]),
    ], style={'margin': '20px', 'padding': '20px'}),

    # Interactive Visualizations
    html.Div([
        # Left Panel - Original visualization
        html.Div([
            html.H3("Linear Regression with Gradient Descent"),
            dcc.Graph(id='regression-plot'),
            html.Label("Learning Rate:"),
            dcc.Slider(
                id='learning-rate',
                min=0.01,
                max=0.5,
                value=0.1,
                marks={i/10: f'{i/10:.2f}' for i in range(1, 6)},
            ),
            html.Label("Iterations:"),
            dcc.Slider(
                id='iterations',
                min=10,
                max=100,
                value=50,
                marks={i: str(i) for i in range(10, 101, 20)},
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Right Panel - Function derivatives
        html.Div([
            html.H3("Function Derivatives"),
            dcc.Dropdown(
                id='function-select',
                options=[
                    {'label': 'Quadratic (x²)', 'value': 'x2'},
                    {'label': 'Cubic (x³)', 'value': 'x3'},
                    {'label': 'Sine (sin x)', 'value': 'sin'}
                ],
                value='x2'
            ),
            dcc.Graph(id='derivative-plot')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # Impact Visualization
    html.Div([
        html.H3("Learning Rate Impact", style={'textAlign': 'center'}),
        dcc.Graph(id='learning-rate-impact')
    ]),
])

@app.callback(
    [Output('regression-plot', 'figure'),
     Output('derivative-plot', 'figure'),
     Output('learning-rate-impact', 'figure')],
    [Input('learning-rate', 'value'),
     Input('iterations', 'value'),
     Input('function-select', 'value')]
)
def update_graphs(learning_rate, iterations, function_select):
    global X, y
    
    # Original regression and derivative plots (keep existing code)
    theta0, theta1 = 0, 0
    m = len(X)
    loss_history = []
    parameter_history = []
    
    for i in range(int(iterations)):
        y_pred = theta0 + theta1 * X
        d_theta0 = -(2/m) * np.sum(y - y_pred)
        d_theta1 = -(2/m) * np.sum(X * (y - y_pred))
        theta0 = theta0 - learning_rate * d_theta0
        theta1 = theta1 - learning_rate * d_theta1
        loss = np.mean((y_pred - y) ** 2)
        loss_history.append(loss)
        parameter_history.append((theta0, theta1))

    # Regression plot
    reg_fig = sp.make_subplots(rows=1, cols=2)
    reg_fig.add_trace(
        go.Scatter(x=X.flatten(), y=y.flatten(), mode='markers', 
                  name='Data Points'),
        row=1, col=1
    )
    reg_fig.add_trace(
        go.Scatter(x=X.flatten(), y=(theta0 + theta1 * X).flatten(), 
                  name='Fitted Line'),
        row=1, col=1
    )
    reg_fig.add_trace(
        go.Scatter(x=list(range(int(iterations))), y=loss_history, 
                  name='Loss History'),
        row=1, col=2
    )
    reg_fig.update_layout(height=500, title_text="Model Training Progress")

    # Derivative plot
    x = np.linspace(-5, 5, 100)
    if function_select == 'x2':
        y = x**2
        dy = 2*x
        title = 'f(x) = x² and f\'(x) = 2x'
    elif function_select == 'x3':
        y = x**3
        dy = 3*x**2
        title = 'f(x) = x³ and f\'(x) = 3x²'
    else:
        y = np.sin(x)
        dy = np.cos(x)
        title = 'f(x) = sin(x) and f\'(x) = cos(x)'

    deriv_fig = go.Figure()
    deriv_fig.add_trace(go.Scatter(x=x, y=y, name='Function'))
    deriv_fig.add_trace(go.Scatter(x=x, y=dy, name='Derivative'))
    deriv_fig.update_layout(title=title, height=500)

    # Learning rate impact visualization
    impact_fig = go.Figure()
    learning_rates = [0.01, 0.1, 0.5]
    for lr in learning_rates:
        theta0, theta1 = 0, 0
        loss_hist = []
        for i in range(int(iterations)):
            y_pred = theta0 + theta1 * X
            d_theta0 = -(2/m) * np.sum(y - y_pred)
            d_theta1 = -(2/m) * np.sum(X * (y - y_pred))
            theta0 = theta0 - lr * d_theta0
            theta1 = theta1 - lr * d_theta1
            loss = np.mean((y_pred - y) ** 2)
            loss_hist.append(loss)
        impact_fig.add_trace(
            go.Scatter(x=list(range(int(iterations))), 
                      y=loss_hist, 
                      name=f'α = {lr}')
        )
    impact_fig.update_layout(
        title='Learning Rate Impact on Convergence',
        xaxis_title='Iteration',
        yaxis_title='Loss',
        height=400
    )

    return reg_fig, deriv_fig, impact_fig

if __name__ == '__main__':
    app.run_server(debug=True)