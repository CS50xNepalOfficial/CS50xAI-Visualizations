import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

def get_function(func_name):
    functions = {
        'x²': (lambda x: x**2, 'f(x) = x²'),
        'x³': (lambda x: x**3, 'f(x) = x³'),
        'sin(x)': (lambda x: np.sin(x), 'f(x) = sin(x)'),
        'e^x': (lambda x: np.exp(x), 'f(x) = e^x'),
    }
    return functions.get(func_name, functions['x²'])

def calculate_riemann_sum(f, a, b, n, method='left'):
    x = np.linspace(a, b, n+1)
    dx = (b - a) / n
    
    if method == 'left':
        x_sample = x[:-1]
    elif method == 'right':
        x_sample = x[1:]
    else:  # midpoint
        x_sample = (x[:-1] + x[1:]) / 2
        
    return x, dx, x_sample, np.sum(f(x_sample) * dx)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Understanding Integration through Riemann Sums', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Add educational content
    html.Div([
        html.H3("What is Integration?"),
        html.P("""
            Integration helps us find the area under a curve. Think of it as adding up infinitely many 
            tiny rectangles to approximate the total area. Here's how it works:
        """),
        html.Ul([
            html.Li("1. We divide the area into rectangles (more rectangles = better approximation)"),
            html.Li("2. Each rectangle's height is determined by the function value"),
            html.Li("3. The sum of rectangle areas approximates the integral"),
            html.Li("4. As rectangles approach infinity, we get the exact area")
        ]),
        html.H4("Step-by-Step Calculation (n=4 rectangles):"),
            html.P([
                "1. Divide interval [0,2] into 4 parts:",
                html.Br(),
                "   Δx = (2-0)/4 = 0.5",
                html.Br(),
                "2. Left endpoints: x = 0, 0.5, 1.0, 1.5",
                html.Br(),
                "3. Calculate areas of rectangles:",
                html.Br(),
                "   • At x=0: (0)² × 0.5 = 0",
                html.Br(),
                "   • At x=0.5: (0.5)² × 0.5 = 0.125",
                html.Br(),
                "   • At x=1.0: (1)² × 0.5 = 0.5",
                html.Br(),
                "   • At x=1.5: (1.5)² × 0.5 = 1.125",
                html.Br(),
                "4. Total Area ≈ 0 + 0.125 + 0.5 + 1.125 = 1.75",
                html.Br(),
                html.Br(),
                "Note: Actual integral = 8/3 ≈ 2.67"
            ]),
        
        html.H4("Methods of Approximation:"),
        html.Ul([
            html.Li("Left Riemann Sum: Uses function value at left endpoint"),
            html.Li("Right Riemann Sum: Uses function value at right endpoint"),
            html.Li("Midpoint Rule: Uses function value at middle of each interval")
        ]),
        
        html.H4("Try It Yourself:"),
        html.P("""
            Experiment with different functions, number of rectangles, and methods to see how 
            the approximation improves!
        """)
    ], style={'width': '80%', 'margin': 'auto', 'marginBottom': '30px'}),

    
    html.Div([
        html.Div([
            html.Label('Select Function:'),
            dcc.Dropdown(
                id='function-selector',
                options=[{'label': k, 'value': k} for k in ['x²', 'x³', 'sin(x)', 'e^x']],
                value='x²',
                style={'width': '200px'}
            ),
        ], style={'margin': '10px'}),
        
        html.Div([
            html.Label('Number of Rectangles:'),
            dcc.Slider(
                id='n-slider',
                min=1,
                max=50,
                step=1,
                value=10,
                marks={i: str(i) for i in range(0, 51, 10)},
            ),
        ], style={'margin': '10px'}),
        
        html.Div([
            html.Label('Riemann Sum Method:'),
            dcc.RadioItems(
                id='method-selector',
                options=[
                    {'label': 'Left', 'value': 'left'},
                    {'label': 'Right', 'value': 'right'},
                    {'label': 'Midpoint', 'value': 'midpoint'}
                ],
                value='left',
                inline=True
            ),
        ], style={'margin': '10px'}),
    ], style={'width': '80%', 'margin': 'auto'}),
    
    dcc.Graph(id='riemann-plot'),
    
    html.Div(id='area-display', 
             style={'textAlign': 'center', 'fontSize': '20px', 'marginTop': '20px'})
], style={'padding': '20px'})

@app.callback(
    [Output('riemann-plot', 'figure'),
     Output('area-display', 'children')],
    [Input('function-selector', 'value'),
     Input('n-slider', 'value'),
     Input('method-selector', 'value')]
)
def update_graph(func_name, n, method):
    f, f_label = get_function(func_name)
    a, b = 0, 2  # integration limits
    x = np.linspace(a, b, 1000)
    y = f(x)
    
    # Calculate Riemann sum
    x_rect, dx, x_sample, area = calculate_riemann_sum(f, a, b, n, method)
    
    # Create rectangles
    shapes = []
    for i in range(len(x_sample)):
        x_pos = x_rect[i]
        y_pos = f(x_sample[i])
        
        shapes.append(dict(
            type="rect",
            x0=x_pos,
            x1=x_pos + dx,
            y0=0,
            y1=y_pos,
            line=dict(color="#3498db", width=1),
            fillcolor="rgba(52, 152, 219, 0.3)"
        ))
    
    fig = go.Figure()
    
    # Add function curve
    fig.add_trace(go.Scatter(x=x, y=y, name=f_label, line=dict(color='#2ecc71')))
    
    # Update layout with shapes and styling
    fig.update_layout(
        shapes=shapes,
        showlegend=True,
        title=f'Riemann Sum Approximation using {method.capitalize()} Method',
        xaxis_title='x',
        yaxis_title='y',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1',
                     zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1',
                     zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50')
    
    area_text = f"Approximate Area = {area:.4f}"
    
    return fig, area_text

if __name__ == '__main__':
    app.run_server(debug=True)