# Dash app libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64

from inputDescr import list_input

def body():
    return html.Div(children=[
                html.Div(id = 'leftCol', children=[
                    dcc.Tabs(
                        id = 'tabs', value='About this app',
                        children=[
                            dcc.Tab(
                                label='About this app',
                                value='About this app',
                                children=html.Div(children=[
                                    #html.Br(
                                    html.H4('What is this app?', style={"text-align":"center"}),
                                    html.P("Insérer l'explication de l'app avec les différents modèles")
                                    #)
                                ])
                            ),
                            dcc.Tab(
                                label='Model',
                                value='Model',
                                children=html.Div(children=[
                                    html.H4('What is the model?')
                                ]
                                    
                                )
                            ),
                            dcc.Tab(
                                label='Appro-ach',
                                value='Appro-ach',
                                children=html.Div(children=[
                                    html.H4('What is the model?')
                                ]
                                    
                                )
                            ),
                            dcc.Tab(
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
                                                            {'label':'MC with antithetic', 'value':"McAnti"},
                                                            {'label':'MC with european as CV', 'value':"McEuro"},
                                                            {'label':'MC with antithetic and european as CV', 'value':"McEuroAnti"},
                                                            {'label':'MC with sum of european as CV','value':"McSumEuro"},
                                                            {'label':'MC with geometric as CV','value':"McGeo"}],
                                                   value='Classical MC'),
                                    html.Div(children=[html.Label("Price", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="PriceMod1", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Standard error", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="SEMod1", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Confidence interval", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="ConfIntMod1", style={'display': 'inline-block'}),]
                                    ),
                                    
                                    html.Br(),
                                    dcc.Dropdown(id='ModelSel2',
                                                   options=[{'label':'Classical MC', 'value':"Classical MC"}, 
                                                            {'label':'MC with antithetic variate', 'value':"McAnti"},
                                                            {'label':'MC with european option as CV', 'value':"McEuro"},
                                                            {'label':'MC with antithetic variate and european option as CV', 'value':"McEuroAnti"},
                                                            {'label':'MC with sum of european option as CV','value':"McSumEuro"},
                                                            {'label':'MC with geometric asian option as CV','value':"McGeo"}],
                                                   value='McGeo'), 
                                    html.Div(children=[html.Label("Price", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="PriceMod2", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Standard error", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                             html.Label(id="SEMod2", style={'display': 'inline-block'}),]
                                    ),
                                    html.Div(children=[html.Label("Confidence interval", style={'font-weight': 'bold', 'display': 'inline-block'}),
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
                                               dcc.Input(id="M", value=1000, debounce=True, type='number', style={"width":"20%", 'display': 'inline-block'},min=1,max=100001),
                                               html.P("",id="message_M", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                              ]
                                    ),
                                    ####### Number of time the simulation is run
                                    html.Div(children=[html.Label('Number of MC', title=list_input["Number of MC"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                               dcc.Input(id="MC", value=10, debounce=True, type='number', style={"width":"20%", 'display': 'inline-block'},min=1,max=101),
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
            html.Div(children=[dcc.Markdown(children=''' #### Boxplot for each model'''),
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