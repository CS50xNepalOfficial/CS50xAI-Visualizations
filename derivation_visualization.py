import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COLORS = {
    'background': '#ffffff',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#2ecc71',
    'accent': '#e74c3c',
    'highlight': '#f39c12'
}

def get_function_and_derivative(func_name):
    functions = {
        'x²': (lambda x: x**2, lambda x: 2*x, 'f(x) = x²', "f'(x) = 2x"),
        'x³': (lambda x: x**3, lambda x: 3*x**2, 'f(x) = x³', "f'(x) = 3x²"),
        'sin(x)': (lambda x: np.sin(x), lambda x: np.cos(x), 'f(x) = sin(x)', "f'(x) = cos(x)"),
        'e^x': (lambda x: np.exp(x), lambda x: np.exp(x), 'f(x) = e^x', "f'(x) = e^x"),
        'ln(x)': (lambda x: np.log(np.abs(x)), lambda x: 1/x, 'f(x) = ln(x)', "f'(x) = 1/x"),
        'cos(x)': (lambda x: np.cos(x), lambda x: -np.sin(x), 'f(x) = cos(x)', "f'(x) = -sin(x)"),
        'tan(x)': (lambda x: np.tan(x), lambda x: 1/np.cos(x)**2, 'f(x) = tan(x)', "f'(x) = sec²(x)"),
    }
    return functions.get(func_name, functions['x²'])  # Default to x² if invalid function

app = Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Interactive Derivative Explorer',
                style={'color': COLORS['text'], 'textAlign': 'center', 'marginBottom': 30}),
        html.H4('Visualize and understand derivatives in real-time',
                style={'color': COLORS['primary'], 'textAlign': 'center'})
    ]),

    # Educational Content
    html.Div([
        # Concept Card
        html.Div([
            html.H3("Understanding Derivatives", style={'color': COLORS['primary']}),
            html.P("""
                The derivative represents the instantaneous rate of change of a function.
                It helps us understand how quickly a quantity is changing at any point.
            """)
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '15px', 'margin': '10px 0'}),

        # Formula and Common Derivatives
        html.Div([
            html.H4("Limit Definition:", style={'color': COLORS['text']}),
            html.Div([
                "f'(x) = lim[h→0] [f(x+h) - f(x)] / h"
            ], style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'fontFamily': 'monospace'}),
            
            html.H4("Common Derivatives:", style={'color': COLORS['text']}),
            html.Ul([
                html.Li("d/dx(x²) = 2x"),
                html.Li("d/dx(x³) = 3x²"),
                html.Li("d/dx(sin x) = cos x"),
                html.Li("d/dx(eˣ) = eˣ"),
            ])
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '15px', 'margin': '10px 0'}),

        # Real-world Applications
        html.Div([
            html.H4("Why Do We Need Derivatives? 🤔", style={'color': COLORS['secondary']}),
            html.Div([
            # Practical examples in everyday life
            html.H5("Derivatives in Daily Life:", style={'color': COLORS['text']}),
            html.Ul([
                html.Li("📈 Stock Market: Track how fast prices are changing to make trading decisions"),
                html.Li("🚗 Speed & Acceleration: Your car's speedometer shows position's derivative"),
                html.Li("🌡️ Temperature Change: How quickly temperature rises or falls per hour"),
                html.Li("📱 Population Growth: Rate of increase in social media users")
            ]),
            
            # Simple example with visualization
            html.H5("Simple Example: Car Motion", style={'color': COLORS['text']}),
            html.P([
                "A car drives along a straight road:",
                html.Br(),
                "• Position = where the car is",
                html.Br(),
                "• Velocity (1st derivative) = how fast it's moving",
                html.Br(),
                "• Acceleration (2nd derivative) = how quickly speed changes"
            ]),
            
            # Interactive note
            html.Div([
                "👉 Use the slider above to see how derivatives work!",
                html.Br(),
                "The steeper the curve, the larger the derivative."
            ], style={'backgroundColor': '#e8f4f8', 'padding': '10px', 'borderRadius': '5px', 'marginTop': '10px'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '15px'})
        ], style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '15px', 'margin': '10px 0', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'width': '80%', 'margin': 'auto'}),

    # Interactive Controls
    html.Div([
        dcc.Dropdown(
            id='function-selector',
            options=[{'label': k, 'value': k} for k in ['x²', 'x³', 'sin(x)', 'e^x', 'ln(x)', 'cos(x)', 'tan(x)']],
            value='x²',
            style={'width': '50%', 'margin': '20px auto'}
        ),
        dcc.Slider(
            id='x-slider',
            min=-5,
            max=5,
            step=0.1,
            value=0,
            marks={i: str(i) for i in range(-5, 6)},
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'width': '80%', 'margin': 'auto'}),

    # Graph
    dcc.Graph(id='derivative-plot', style={'height': '800px'})

], style={'padding': '20px', 'backgroundColor': COLORS['background']})

@app.callback(
    Output('derivative-plot', 'figure'),
    [Input('function-selector', 'value'),
     Input('x-slider', 'value')]
)
def update_graph(func_name, x_point):
    try:
        x = np.linspace(-5, 5, 500)
        f, f_prime, f_label, f_prime_label = get_function_and_derivative(func_name)
        
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=(f'Function ({f_label}) and Tangent Line', 
                                        f'Derivative ({f_prime_label})'),
                           vertical_spacing=0.15)
        
        # Original function and tangent line
        y = f(x)
        y_prime = f_prime(x)
        tangent = f(x_point) + f_prime(x_point) * (x - x_point)
        
        # Add traces with improved styling
        fig.add_trace(go.Scatter(x=x, y=y, name=f_label, line=dict(color='#2ecc71')), row=1, col=1)
        fig.add_trace(go.Scatter(x=[x_point], y=[f(x_point)], 
                                mode='markers', name='Point',
                                marker=dict(size=10, color='#e74c3c')), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=tangent, name='Tangent', 
                                line=dict(dash='dash', color='#3498db')), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=y_prime, name=f_prime_label,
                                line=dict(color='#9b59b6')), row=2, col=1)
        
        # Update layout with better styling
        fig.update_layout(
            height=800,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#2c3e50',
                borderwidth=1
            )
        )
        
        # Add grid and improve axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1',
                        zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1',
                        zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50')
        
        return fig
    except Exception as e:
        # Return empty figure with error message if something goes wrong
        return go.Figure().add_annotation(text=f"Error: {str(e)}", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

if __name__ == '__main__':
    app.run_server(debug=True)