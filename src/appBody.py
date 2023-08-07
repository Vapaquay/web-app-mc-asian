# Dash app libraries
from dash import dcc, Dash
from dash import html
import dash_bootstrap_components as dbc
import base64

from inputDescr import list_input

def body():
    return html.Div(children=[
                html.Div(id = 'leftCol', children=[
                    dcc.Tabs(
                        id = 'tabs', value='About this app',
                        children=[
                            dcc.Tab( #What is this App ?
                                label='About this app',
                                value='About this app',
                                children=html.Div(children=[
                                    html.Br(),
                                    html.H4('What is this app?', style={"text-align":"center"}),
                                    html.P(
                                        """
                                        This app computes the price of an arithmetic Asian option \(V_0\) for a certain set of parameters, using Monte Carlo simulation. 
                                        """),
                                    html.P(     
                                        """This app has two main goals: """    
                                    ),
                                    html.Ul([   html.Li("Show that the price of an Asian option can be computed with the Monte-Carlo simulation"), 
                                                html.Li('Simulation variance can be reduced (i.e. certain methods allow for greater precision)')
                                        ]),
                                    html.Hr(),
                                    html.H4("Type of options", style={"text-align":"center"}),
                                    html.P([
                                    """
                                  The considered options are arithmetic Asian options paying \(\psi(A(S))\) at maturity \(T\) where \(\psi(X)\) is the payoff function
                                  and \(A(S)\) the arithmetic mean of the stock until maturity.
                                  For a call, the payoff function is \(\psi(A(S))=max(0,A(S)-K)\) and for a put \(\psi(A(S))=max(0,K-A(S))\) where \(K\) is the strike price.
                                  """]),
                                    html.Hr(),
                                    html.P(
                                    """
                                    Read more about Asian options : 
                                    https://en.wikipedia.org/wiki/Asian_option
                                    """
                                      ),
                                    
                                    
                                ])
                            ),
                            dcc.Tab( #Model
                                label='Model',
                                value='Model',
                                children=html.Div(children=[
                                    html.Br(),
                                    html.H4('Model assumptions', style={"text-align":"center"}),
                                    html.P("""
                                        The stochastic differential equation (SDE) of a stock is a geometric Brownian motion (GBM):
                                        $$dS_t = \mu S_tdt+\sigma S_tdW_t$$ Where \(\mu\) is the drift, \(\sigma\) the volatility, and \(dW_t\) the increment of a Brownian motion."""
                                    ),
                                    html.P(
                                        """We make the following assumptions:"""
                                    ),
                                    html.Ul([   html.Li("We do not consider any dividends"), 
                                                html.Li('We consider that the risk-free rate \(r\) and the volatility \(\sigma\) are constant')
                                        ]),
                                    html.Hr(),
                                    html.H4('Derivative pricing', style={"text-align":"center"}),
                                    html.P('''The unique price that prevents arbitrage opportunities is found
                                                using the risk-neutral expectation:
                                           $$V_0 = \mathbb{E}^{\\mathbb{Q}} \Big[\\frac{\psi(X)}{\\beta_T} \Big] $$
                                           
                                           where \(V_0\) the derivative price at time 0, \(\psi(X)\) the derivative's payoff and \(\\beta_T\) the discounting factor at maturity \(T\).'''),
                                    html.Hr(),
                                    html.H4('Monte-Carlo simulation', style={"text-align":"center"}),
                                    html.P('Monte-Carlo simulation (MC) is used to estimate an expectation using a large number of simulations. '),
                                    html.P('''Let's assume we want to estimate $$\\theta = \\mathbb{E}[g(X)]$$  where \(g(X)\) is an arbitrary function 
                                           of the random variable \(X\). The following estimators can be constructed using different methods, for \(m\) simulations: '''),
                                    html.Ul([   html.Li("""Classical estimator: $$\\hat{\\theta}^{Cl} = \\frac{1}{m} \\sum_{i=1}^{m} g(X_i)$$ where \(i \\in \{1,...,m\}\)"""), 
                                                html.Li("""Antithetic variate estimator: 
                                                        $$\\hat{\\theta}^{AV} = \\frac{1}{m} \\sum_{i=1}^{m} \Big[\\frac{g(X_i) + g(-X_i)}{2}\Big] $$ 
                                                        where \(-X_i\) is the opposite of \(X\) and \(X\) must be symmetrical in \(0\)"""),
                                                html.Li('''Control variate estimator: $$\\hat{\\theta}^{CV} = \\frac{1}{m} \\sum_{i=1}^{m} 
                                                        \Big[g(X_i) - \\alpha [h(X_i) - \\mathbb{E}[h(X)] \Big]$$ 
                                                        where \(h(X)\) is another arbitrary function of \(X\) for which its expectation is known and \(\\alpha\) is the coefficient
                                                        used to minimize the variance.''')        
                                        ]),
                                    html.P('The purpose of the last 2 methods is to reduce the variance of the first, without increasing the number of simulations.'),
                                    html.Hr(),
                                    html.H4("Academical references", style={"text-align":"center"}),
                                     html.Ul([html.Li("Glasserman, P. (2003). Monte carlo methods in financial engineering. Springer"), 
                                            html.Li("Hull, J. (2008). Options, futures and other derivatives. Pearson"),
                                            html.Li("Vrins, F. (2021). Derivatives pricing [Retrieved from Louvain School of Managemen LLSM2225 Derivatives Pricing].")])

                                ]   
                                    
                                )
                            ),
                            dcc.Tab( #Approach
                                label='Appro-ach',
                                value='Appro-ach',
                                children=html.Div(children=[
                                    html.Br(),
                                    html.H4("Methodology followed", style={"text-align":"center"}),
                                    html.P("Using Monte Carlo simulation, we are able to estimate the price of an arithmetic Asian option. "),
                                    html.P("""The graphs illustrate that by using variance reduction methods, it is possible to improve the accuracy
                                            of the simulation. Each estimated price displayed corresponds to \(1\) complete simulation. """),
                                    html.P("""Example: If \(10\) estimated prices are displayed, they are each obtained from an MC simulation
                                            simulating the share path \(m\) times (i.e. \(10\)x a run of \(m\) simulations)."""),
                                    html.Hr(),
                                    html.H4("Stock simulation", style={"text-align":"center"}),
                                    html.P([
                                    """
                                    We use the analytical solution to the GBM SDE, using Îto: \(S_t=S_0exp((\mu-\\frac{\sigma^2}{2})t+\sigma W_t)\). Then, suppose that the stock price
                                    observations are equally spaced: \(t_j=j\delta, i \in \{1,2,\dots,n\}, n=T/\delta\)\(,\\forall \delta>0\)
                                    This corresponds to $$S_{t+\delta}=S_texp((\mu-\\frac{\sigma^2}{2})\delta+\sigma\sqrt{\delta}Z), Z\sim \mathcal{N}(0,1)$$
                                    """]),
                                    html.Hr(),
                                    html.H4("Estimating the price", style={"text-align":"center"}),
                                    html.P(),
                                    html.Label("Step 1", style={'font-weight': 'bold'}),
                                    html.P([
                                    """
                                    Using the SDE analytical solution, we simulate \(m\) times the stock path discretized between \(n\) time steps. 
                                    """]),
                                    html.Label("Step 2", style={'font-weight': 'bold'}),
                                    html.P([
                                    """
                                    For each path, we calculate the average share price and the payoff \(\\psi(A(S))\).
                                    """]),

                                    html.Label("Step 3", style={'font-weight': 'bold'}),
                                    html.P([
                                    """
                                    If we use the antithetic method: we simulate a mirrored trajectory using the opposite sign for each \(Z\) and calculate the payoff \(\\psi(A^{AV}(S))\) where 
                                    \(A^{AV}(S)\)  is the average share price calculated using this mirror trajectory. It is important to note that even if the average is expressed 
                                    as a function of \(S\), we are working on the random variable \(Z\), as this method only works if the random variable is symmetrical in \(0\).
                                    We retain this notation for the sake of clarity.  
                                    """]),
                                    html.P([
                                    """
                                    We combine the payoff of the normal trajectory and the payoff of the antithetic trajectory and we divide each pair by 2 to get our estimator.
                                    """]),
                                    html.P([
                                    """
                                    If we use the control variable method, we calculate this control variable from \(S\) and calculate the error using the analytical form of its expectation.
                                    Then, we estimate the \(\\alpha\) coefficient using the simulation values. Finally, we correct our estimator by subtracting this error. 
                                    """]),
                                    html.Label("Step 4", style={'font-weight': 'bold'}),
                                    html.P([
                                    """
                                    We discount the estimated payoff of each simulation by \(e^{-rT}\) to get the estimated price for each simulation.
                                    """]),
                                    html.Label("Step 5", style={'font-weight': 'bold'}),
                                    html.P([
                                    """
                                    We calculate the average of the estimated prices to find our price estimator. 
                                    """]),
                                    #dbc.Button("List of implemented models", id="model-list", color="primary", className="mr-1",),
                                                    #dbc.Popover(children=[dbc.PopoverHeader("List of implemented models"),
                                                    #dbc.PopoverBody([html.Img(src="data:image/png;base64,{}".format(base64.b64encode(open("./pictures/ListModels.png",'rb').read()).decode()), style={"width": "250%"})]),
                                                  #],
                                                    #id="list",
                                                    #is_open=False,
                                                    #target="model-list",)
                                ]   
                                )
                            ),
                            dcc.Tab( #Inputs
                                label='Inputs',
                                value='Inputs',
                                children=html.Div(children=[
                                    html.Br(),
                                    html.P(
                                            """
                                            Place your mouse over any input to get its definition. 
                                            """
                                             ),
                                    html.Br(),
                                    html.H5("Model selector", style={"text-align":"center"}),
                                    html.P("""
                                           Choose 2 models to compare
                                           """),
                                    dcc.Dropdown(id='ModelSel',
                                                   options=[{'label':'Classical MC', 'value':"Classical MC"}, 
                                                            {'label':'MC with antithetic', 'value':"MC with antithetic"},
                                                            {'label':'MC with european as CV', 'value':"MC with european as CV"},
                                                            {'label':'MC with antithetic and european as CV', 'value':"MC with antithetic and european as CV"},
                                                            {'label':'MC with average of european as CV','value':"MC with average of european as CV"},
                                                            {'label':'MC with geometric as CV','value':"MC with geometric as CV"}],
                                                   value='Classical MC'),
                                    html.Div(children=[html.Label("Price", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="PriceMod1", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Standard error", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="SEMod1", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Conf. interval 95%", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="ConfIntMod1", style={'display': 'inline-block'}),]
                                    ),
                                    
                                    html.Br(),
                                    dcc.Dropdown(id='ModelSel2',
                                                   options=[{'label':'Classical MC', 'value':"Classical MC"}, 
                                                            {'label':'MC with antithetic', 'value':"MC with antithetic"},
                                                            {'label':'MC with european as CV', 'value':"MC with european as CV"},
                                                            {'label':'MC with antithetic and european as CV', 'value':"MC with antithetic and european as CV"},
                                                            {'label':'MC with average of european as CV','value':"MC with average of european as CV"},
                                                            {'label':'MC with geometric as CV','value':"MC with geometric as CV"}],
                                                   value='MC with geometric as CV'), 
                                    html.Div(children=[html.Label("Price", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="PriceMod2", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Standard error", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="SEMod2", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Conf. interval 95%", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="ConfIntMod2", style={'display': 'inline-block'}),]
                                    ),
                                                  
                                    html.Br(),
                                    html.H5("Option parameters", style={"text-align":"center"}),
                                    ####### Call or put value
                                    dcc.Dropdown(id='CallOrPut',
                                                   options=[{'label':'Asian Call option', 'value':"Call"}, 
                                                            {'label':'Asian Put option', 'value':"Put"}],
                                                   value='Call'),
                                    html.Br(),

                                    ####### Spot price
                                    html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="S", value=100, debounce=True, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                               html.P("",id="message_S", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),
                                    ####### Strike
                                    html.Div(children=[html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="K", value=105, debounce=True, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                               html.P("",id="message_K", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ],
                                    ),
                                    ####### Risk free rate
                                    html.Div(children=[html.Label("Risk-free rate", title=list_input["Risk-free rate"], style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="Risk-free", style={'display': 'inline-block'}),]
                                    ),
                                    dcc.Slider(id='rf', min=-0.50, max=0.50, value=0.05, step=0.01, marks={-0.50: '-50%', -0.25: '-25%',0:"0%", 0.25: '25%',  0.50: '50%'}),

                                    ####### Volatility
                                    html.Div([html.Label('Volatility', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
                                                html.Label(id="sigma", style={"display":"inline-block"}),]
                                                ),  
                                    dcc.Slider(id='vol', min=0, max=0.50, step=0.01, value=0.25, marks={0:"0%", 0.25:"25%",  0.50:"50%"}),

                                    ####### Maturity
                                    html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
                                                html.Label(id="matu", style={"display":"inline-block"}),]),                    
                                    dcc.Slider(id='T', min=0.25, max=5,
                                        marks={0.25:"3 months", 1: "1 year", 3:"3 years", 5:"5 years"}, step=0.25, value=3),

                                    html.Br(),
                                    html.H5("Simulation parameters", style={"text-align":"center"}),
                                    ####### Time steps
                                    html.Div(children=[html.Label('Number of time step', title=list_input["Discretization step"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="TS", value=252, debounce=True, type='number', style={"width":"16%", 'display': 'inline-block'},min=1,max=507),
                                               html.P("",id="message_TS", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),  
                                    ####### Number of simulations
                                    html.Div(children=[html.Label('Number of simulations', title=list_input["Number of simulations"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="M", value=1000, debounce=True, type='number', style={"width":"20%", 'display': 'inline-block'},min=1,max=1000001),
                                               html.P("",id="message_M", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),
                                    ####### Number of time the simulation is run
                                    html.Div(children=[html.Label('Number of prices to plot', title=list_input["Number of MC"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="MC", value=50, debounce=True, type='number', style={"width":"20%", 'display': 'inline-block'},min=1,max=101),
                                               html.P("",id="message_MC", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),
                                    html.Br(),
                                    html.Label(children=[dbc.Button("Change stock trajectory", id="ButtonChangeStockTrajectory", color="primary", class_name="mr-1")],
                                     title=list_input["Seed"]),
                                    html.Br(),
                                    html.Div(children=[html.Label("You can input a specific seed: ", style={'display': 'inline-block', "padding":5}),
                                             dcc.Input(id='seed', readOnly=False, debounce=True, value=1, min=1,max=500000, type='number',  style={"width":"20%", 'display': 'inline-block'})
                                             ]      #stockScenario
                                    ),
                                ]
                                )   
                            )
                        ]
                    )
                ], style={'float': 'left', 'width': '25%', 'margin':"30px"})
    ])
def graphs():
  return html.Div(id='right-column', 
          children=[
            html.Br(),
            html.Div(children=[dcc.Markdown(children=''' #### Boxplot'''),
                            dcc.Graph(id='boxplot'),],
                       style={"float":"right", "width":"100%", "display":"inline-block"}),
                html.Div([
                  html.Div(children=[dcc.Markdown(children=''' #### Second model distribution'''),
                             dcc.Graph(id='density2'),],
                       style={"float":"right", "width":"50%", "display":"inline-block"}),
                  html.Div(children=[dcc.Markdown(children=''' #### First model distribution'''),
                             dcc.Graph(id='density1'),],
                       style={"float":"right", "width":"50%", "display":"inline-block"}),
                        ]),
                   ], 
          style={'float': 'right', 'width': '70%'})