import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

def create_surface(x_range=(-5, 5), y_range=(-5, 5), step=0.1):
    x = np.arange(x_range[0], x_range[1], step)
    y = np.arange(y_range[0], y_range[1], step)
    X, Y = np.meshgrid(x, y)
    # Hill-shaped function: f(x,y) = x²/2 + y² + sin(x)*cos(y)
    Z = X**2/2 + Y**2 + np.sin(X)*np.cos(Y)
    return X, Y, Z

def gradient_descent(start_x, start_y, learning_rate, n_steps):
    path_x, path_y, path_z = [start_x], [start_y], []
    current_x, current_y = start_x, start_y
    
    for _ in range(n_steps):
        # Gradient of f(x,y) = x²/2 + y² + sin(x)*cos(y)
        grad_x = current_x + np.cos(current_y)*np.cos(current_x)
        grad_y = 2*current_y - np.sin(current_y)*np.sin(current_x)
        
        current_x = current_x - learning_rate * grad_x
        current_y = current_y - learning_rate * grad_y
        current_z = current_x**2/2 + current_y**2 + np.sin(current_x)*np.cos(current_y)
        
        path_x.append(current_x)
        path_y.append(current_y)
        path_z.append(current_z)
    
    return path_x, path_y, path_z

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gradient Descent Visualization"),
    html.Div([
        html.Div([
            html.Label("Learning Rate (α):"),
            dcc.Slider(
                id='learning-rate',
                min=0.01, max=0.5, value=0.1, step=0.01,
                marks={i/10: f'{i/10:.1f}' for i in range(1, 6)},
            ),
            html.Label("Starting X:"),
            dcc.Slider(
                id='start-x',
                min=-4, max=4, value=3, step=0.5,
                marks={i: f'{i}' for i in range(-4, 5)},
            ),
            html.Label("Starting Y:"),
            dcc.Slider(
                id='start-y',
                min=-4, max=4, value=3, step=0.5,
                marks={i: f'{i}' for i in range(-4, 5)},
            ),
            html.Button('Run Gradient Descent', id='run-button'),
            html.Div([
                html.H4("Mathematical Background:"),
                dcc.Markdown('''
                    **Objective Function:**
                    ```
                    f(x,y) = x²/2 + y² + sin(x)cos(y)
                    ```
                    
                    **Gradient Descent Update Rule:**
                    ```
                    x = x - α * ∂f/∂x
                    y = y - α * ∂f/∂y
                    ```
                    where α is the learning rate
                    
                    **Partial Derivatives:**
                    ```
                    ∂f/∂x = x + cos(y)cos(x)
                    ∂f/∂y = 2y - sin(y)sin(x)
                    ```
                ''')
            ], style={'margin-top': '20px'})
        ], style={'width': '30%', 'padding': '20px'}),
        dcc.Graph(id='3d-plot', style={'width': '70%', 'height': '800px'})
    ], style={'display': 'flex'})
])

@app.callback(
    Output('3d-plot', 'figure'),
    [Input('run-button', 'n_clicks')],
    [State('learning-rate', 'value'),
     State('start-x', 'value'),
     State('start-y', 'value')]
)
def update_graph(n_clicks, learning_rate, start_x, start_y):
    X, Y, Z = create_surface()
    path_x, path_y, path_z = gradient_descent(start_x, start_y, learning_rate, 50)
    
    fig = go.Figure(data=[
        go.Surface(x=X, y=Y, z=Z, colorscale='viridis', opacity=0.8),
        go.Scatter3d(x=path_x, y=path_y, z=path_z, 
                     mode='lines+markers',
                     line=dict(color='red', width=4),
                     marker=dict(size=4, color='red'))
    ])
    
    fig.update_layout(
        title=dict(text='Gradient Descent on Hill Surface', font=dict(size=24)),
        scene=dict(
            xaxis=dict(title='X', titlefont=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(title='Y', titlefont=dict(size=18), tickfont=dict(size=14)),
            zaxis=dict(title='f(X,Y)', titlefont=dict(size=18), tickfont=dict(size=14)),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=800
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)