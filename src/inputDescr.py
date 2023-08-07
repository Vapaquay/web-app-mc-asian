#Note: this code has been taken from Michel Vanderhulst's thesis code to ensure the consistency of the app if another student want
#implement new features. Small changes have been done to adapt the code for the purpose of this thesis. 

list_input = {"-": "-",
              "Spot price": "Current market price at which asset is bought or sold.",

              "Strike": 'The price at which a put or call option can be exercised.',

              "Risk-free rate": 'The risk-free interest rate is the rate of return of a hypothetical investment with no'
                                ' risk of financial loss, over a given period of time.',

              "Volatility": 'Standard deviation of the underlying asset stock price, in other words the degree of'
                            ' variation of the price.',

              "Maturity": 'Date on which the option will cease to exist, and when the investor will be able to exercise'
                          ' his right to buy or sell the underlying asset.',

              "Discretization step": 'Used in the pricing model of the underlying asset, its mathematical definition is'
                                     ' the step at which the continuous period (i.e. from t = 0 to t = maturity) is'
                                     ' discretized. Financially speaking, it is time between each pricing of the asset.',

              "Number of simulations": "Number of Monte Carlo simulations used to calculate the price.",

              "Seed": "The simulations are based on a random number generation. Currently, the generation is fixed, ie the Brownian motion behind"
                     " the stock random dynamics is fixed, therefore allowing for sensitivity analysis. Clicking on this button will generate a new Brownian motion, thus changing the stoch trajectory.",
              
              "Number of MC": "To display the graphs, we need to use a price vector, which involves running the MC model several times. "
              }
