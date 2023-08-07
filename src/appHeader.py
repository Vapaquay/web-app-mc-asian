# Dash app libraries
import dash
from dash import html
import dash_bootstrap_components as dbc
import base64

# Author parameters
bg_color="#506784",
font_color="#F3F6FA"
author = "Valentin Paquay"
emailAuthor = "valentin.paquay1@gmail.com"
supervisor = "Prof. Frédéric Vrins"
emailSupervisor = "frederic.vrins@uclouvain.be"
logo1path = "./Logo_LSM.png"
logo1URL  = "https://uclouvain.be/en/faculties/lsm"

# Creating the app header
def header():
    return html.Div(
                id='app-page-header',
                children=[
                    html.Div(children=[#html.A(id='lsm-logo', 
                                              #children=[html.Img(style={'height':'6%', 'width':'6%'}, src='data:image/png;base64,{}'.format(base64.b64encode(open(logo1path, 'rb').read()).decode()))],
                                              #href=f"{logo1URL}",
                                              #target="_blank", #open link in new tab
                                              #style={"margin-left":"10px"}
                                              #),
                                       html.Div(children=[html.H5("Asian option pricing app"),
                                                          html.H6("Monte Carlo simulation model")
                                                          ],
                                                 style={"display":"inline-block", "font-family":'sans-serif','transform':'translateY(+32%)', "margin-left":"10px"}),

                                     html.Div(children=[dbc.Button("About", id="popover-target", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
                                                          dbc.Popover(children=[dbc.PopoverHeader("About"),
                                                                                dbc.PopoverBody([f"Author: {author}",                             
                                                                                             f"\n {emailAuthor}", 
                                                                                               html.Hr(), 
                                                                                             f"This app was built for my Master's Thesis, under the supervision of {supervisor} ({emailSupervisor})."]),],
                                                                       id="popover",
                                                                       is_open=False,
                                                                       target="popover-target"),
                                                          ],
                                                 style={"display":"inline-block","font-family":"sans-serif","marginLeft":"80%", "margin-right":"10px"})                                       
                                      ]
                             ,style={"display":"inline-block"}),  
                         ],
                style={
                    'background': bg_color,
                    'color': font_color,
                    "padding-bottom": "10px",
                    "padding-top":"-10px"
                }
            )