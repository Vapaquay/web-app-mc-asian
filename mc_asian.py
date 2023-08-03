#This code give multiple functions to compute different options prices by using different model
#The objective is to use it for an App to show how to price an arithmetic Asian option using MC
#SOURCES:
#MC using vectorization is inspired from https://quantpy.com.au/
#Theoretical equations come from: 
#Slides from Pr. Vrins in LLSMS2225 at the Louvain School Of Management
#Monte Carlo in Financial Engineering from Paul Glasserman, editor: Springer

#The way the seed is managed follows the metholodogy of the V1 app developed by Michel Vanderhulst

#Import packages
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plot


#### Closed form equation for european option ####
def BS_eur(S0, K, T, vol, r, type):
    d1 = (1/(vol*np.sqrt(T)))*(np.log(S0/K)+(r+0.5*vol**2)*T)
    d2 = d1 - vol*np.sqrt(T)
    if type == "Call":
        price= S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    else: 
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S0*norm.cdf(-d1)
    return price

#### Closed form equation for geometric asian option ####
def BS_geo(S0,K,T,vol,r,n,type): 
    varbis = vol**2 * (((n+1)*(2*n+1))/(6*(n**2))) #We need to compute another the specific volatility and risk-free rate for the geometric asian option
    rbis = (varbis/2) + (r-((vol**2)/2)) * ((n+1)/(2*n))
    d1 = (np.log(S0/K) + (rbis+0.5*varbis)*T) / np.sqrt(varbis)*np.sqrt(T)
    d2 = d1 - (np.sqrt(varbis)*np.sqrt(T))
    if type == "Call":
        price = np.exp(-r*T) * (S0*np.exp(rbis*T)*norm.cdf(d1)-K*norm.cdf(d2))
    else:
        price = np.exp(-r*T) * (K*norm.cdf(-d2) - S0*np.exp(rbis*T)*norm.cdf(-d1))
    return price

#### Classical Monte Carlo simulation ####
def MC_AsianClass(S0,K,T,r,vol,N,M,Type,seed):
    #Seed management
    b = seed
    if type(b) is list:
        b=b[0]  
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)

    #Computing time steps
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    #Vectors for precomputed constants
    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
    ####### Monte Carlo Method
    #We generate a matrix N*M of r.v. following the Normal(0,1) and we generate all the stock paths
    Z = np.random.normal(size=(N, M)) 
    delta_St1 = nudt + volsdt*Z
    ST1 = S0*np.cumprod( np.exp(delta_St1), axis=0)
    AT1 = np.cumsum(ST1, axis=0)/N #[N*M] average of S(t)

    if Type == "Call":
        Payoff = np.maximum(0, AT1[-1] - K) #reduction to [1*M]
    else:
        Payoff = np.maximum(0, K - AT1[-1]) #reduction to [1*M]
    Price = np.exp(-r*T)*Payoff
    AvgPrice = np.mean(Price)
    SEavg = np.std(Price)/np.sqrt(M)
    #print("Call value is ${0} with SE +/- {1}".format(np.round(AvgPrice,3),np.round(SEavg,4)))
    return AvgPrice, SEavg, b #Return price, SE and stock paths  ST1[:,1]

#### Monte Carlo simulation with antithetic variate ####
def MC_SimAnti(S0,K,T,r,vol,N,M,Type,seed): 
    #seed management
    b = seed
    if type(b) is list:
        b=b[0]
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)

    #Compute time steps
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    #Generate matrix for precomputed constants
    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
    # Monte Carlo Method
    Z = np.random.normal(size=(N, M)) 
    delta_St1 = nudt + volsdt*Z
    delta_St2 = nudt - volsdt*Z #computing the antithetic variable
    ST1 = S0*np.cumprod( np.exp(delta_St1), axis=0) #first path
    ST2 = S0*np.cumprod( np.exp(delta_St2), axis=0) #second path
    AT1 = np.cumsum(ST1, axis=0)/N #first payoff
    AT2 = np.cumsum(ST2, axis=0)/N #second payoff

    if Type == "Call":
        Payoff = 0.5 * ( np.maximum(0, AT1[-1] - K) + np.maximum(0, AT2[-1] - K) ) #average of both payoff (see antithetic variate in theory)
    else:
        Payoff = 0.5 * ( np.maximum(0, K - AT1[-1]) + np.maximum(0, K - AT2[-1]) )
    Price = np.exp(-r*T)*Payoff
    AvgPrice = np.mean(Price)
    SE = np.std(Price)/np.sqrt(M)
    #print("Call value with antithetic variate is ${0} with SE +/- {1}".format(np.round(AvgPrice,3),np.round(SE,4)))
    return AvgPrice, SE, b

#### MC with european option as control variate ####
def MC_Sim_CV_EUR(S0,K,T,r,vol,N,M,Type,seed): 
    #seed management
    b = seed
    if type(b) is list:
        b=b[0]
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)
    
    #computing time steps
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
    BSprice = BS_eur(S0,K,T,vol,r,Type) #Black-Scholes price
    # Monte Carlo Method 
    Z = np.random.normal(size=(N, M)) 
    delta_St = nudt + volsdt*Z
    ST = S0*np.cumprod( np.exp(delta_St), axis=0)

    #Computing asian price vector
    AT = np.cumsum(ST, axis=0)/N #[N*M] for the payoff
    if Type == "Call":
        PayoffAsian = np.maximum(0, AT[-1] - K) #[1*M] 
    else:
        PayoffAsian = np.maximum(0, K - AT[-1]) #[1*M]
    AsianPrice = np.exp(-r*T)*PayoffAsian #Computing price vector for asian 

    #Computing euro price
    if Type == "Call":
        PayoffEuro = np.maximum(0, ST[-1] - K) #Computing payoff from stock's final price
    else:
        PayoffEuro = np.maximum(0, K - ST[-1])
    EuroPrice = np.exp(-r*T)*PayoffEuro 

    #Estimating alpha
    cov = np.cov(AsianPrice, EuroPrice)
    alpha = cov[0,1]/cov[1,1]

    #Final price and SE
    Price=AsianPrice - alpha*(EuroPrice - BSprice)
    SEavg = np.std(Price)/np.sqrt(M)
    AvgPrice = np.mean(Price)
    #print("Call value with control variate is ${0} with SE +/- {1}".format(np.round(np.mean(Price),3),np.round(SEavg,4)))
    return AvgPrice, SEavg, b

#### MC with european option as control variate AND antithetic variate####
def MC_Sim_CV_EUR_ANTI(S0,K,T,r,vol,N,M,Type,seed): 
    b = seed
    if type(b) is list:
        b=b[0]
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)
    
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
    BSprice = BS_eur(S0,K,T,vol,r,Type) #Black-Scholes price
    # Monte Carlo Method 
    Z = np.random.normal(size=(N, M)) 
    delta_St = nudt + volsdt*Z 
    delta_St2 = nudt - volsdt*Z 
    ST = S0*np.cumprod( np.exp(delta_St), axis=0) #first stock path
    ST_anti = S0*np.cumprod( np.exp(delta_St2), axis=0) #antithetic path

    #Computing asian price
    AT = np.cumsum(ST, axis=0)/N #[N*M]
    AT_anti = np.cumsum(ST_anti, axis=0)/N
    if Type == "Call":
        PayoffAsian = 0.5 * (np.maximum(0, AT[-1] - K) + np.maximum(0, AT_anti[-1] - K))#[1*M]
    else:
        PayoffAsian = 0.5 * (np.maximum(0, K - AT[-1]) + np.maximum(0, K - AT_anti[-1]))#[1*M]
    AsianPrice = np.exp(-r*T)*PayoffAsian #Computing price vector for asian 

    #Computing euro price
    if Type == "Call":
        PayoffEuro = np.maximum(0, ST[-1] - K) #Computing payoff from stock's final price
    else: 
        PayoffEuro = np.maximum(0, K - ST[-1]) #Computing payoff from stock's final price
    EuroPrice = np.exp(-r*T)*PayoffEuro 

    #Estimating alpha
    cov = np.cov(AsianPrice, EuroPrice)
    alpha = cov[0,1]/cov[1,1]

    #Final price and SE
    Price=AsianPrice - alpha*(EuroPrice - BSprice)
    SEavg = np.std(Price)/np.sqrt(M)
    AvgPrice = np.mean(Price)
    #print("Call value with control variate is ${0} with SE +/- {1}".format(np.round(np.mean(Price),3),np.round(SEavg,4)))
    return AvgPrice, SEavg, b

#### MC with averaged sum of european option as control variate####
def MC_Sim_CV_EuroSum(S0,K,T,r,vol,N,M,Type,seed):
    b = seed
    if type(b) is list:
        b=b[0]
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)
    
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    #to get the option price for each time t, we need to discount it by e^{-rt_j} 
    ActrateMatrix = np.full(shape=(N,M), fill_value=0.0) 
    actrate = np.exp(-r*T)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
        ActrateMatrix[i,:] = np.exp(-r*TS[i+1])
    # Monte Carlo Method 
    Z = np.random.normal(size=(N, M)) 
    delta_St = nudt + volsdt*Z
    ST = S0*np.cumprod( np.exp(delta_St), axis=0)

    #Computing asian option price
    AT = np.cumsum(ST, axis=0)/N #Arithmetic average [N*M]
    if(Type=="Call"):
        PayoffAsian = np.maximum(0, AT[-1] - K) #Payoff [1*M]
    else:
        PayoffAsian = np.maximum(0, K - AT[-1]) #Payoff [1*M]
    AsianPrice = PayoffAsian * actrate #Price [1*M]
    
    #Computing european average 
    if(Type=="Call"):
        PO = np.maximum(0,ST-K) #Payoff for each simulation, at each time step[N*M]
    else:
        PO = np.maximum(0,K-ST) #[N*M]
    PriceMatrix = PO*ActrateMatrix #[N*M]
    SumEuroPrice = np.sum(PriceMatrix, axis=0)/N #Average payoff for each time step[1*M]

    #Computing average of cumulative BS prices
    dataBS = BS_eur(S0,K,TS[1:],vol,r,Type)#get the vector of BS prices for each time step
    cumBS = np.cumsum(dataBS)
    AvgBS = cumBS[-1]/N

    #Estimating alpha
    cov = np.cov(AsianPrice,SumEuroPrice)
    alpha = cov[0,1]/cov[1,1]

    Price = AsianPrice - alpha*(SumEuroPrice - AvgBS)
    SEavg = np.std(Price)/np.sqrt(M)
    AvgPrice = np.mean(Price)

    #print("Price: {0}, SE: {1}".format(AvgPrice, SEavg))
    return AvgPrice, SEavg, b

#### MC with geometric asian option as control variate####
def MC_Sim_CV_Geo(S0,K,T,r,vol,N,M,Type,seed):
    b = seed
    if type(b) is list:
        b=b[0]
    else:
        np.random.seed(b)

    # unless user wants new seed
    if seed == ["RandomSeed"]:
        np.random.seed(None)
        b = np.random.randint(low=1, high=500000)
        np.random.seed(b)
    
    TS = np.linspace(0,T,N+1)
    dt = np.diff(TS)

    nudt = np.full(shape=(N,M), fill_value=0.0)
    volsdt = np.full(shape=(N,M), fill_value=0.0)
    actrate = np.exp(-r*T)
    # Precompute constants
    for i in range(N):
        nudt[i,:] = (r - 0.5*vol**2)*dt[i]
        volsdt[i,:] = vol*np.sqrt(dt[i])
    # Monte Carlo Method 
    Z = np.random.normal(size=(N, M)) 
    delta_St = nudt + volsdt*Z
    ST = S0*np.cumprod( np.exp(delta_St), axis=0)

    #Computing asian option price
    AT = np.cumsum(ST, axis=0)/N #Arithmetic average [N*M]
    if(Type=="Call"):
        PayoffAsian = np.maximum(0, AT[-1] - K) #Payoff [1*M]
    else:
        PayoffAsian = np.maximum(0, K - AT[-1]) #Payoff [1*M]
    AsianPrice = PayoffAsian * actrate #Price [1]
    
    #Computing geometric average 
    GT = np.cumprod(ST**(1/N),axis=0)
    if(Type=="Call"):
        PayoffGeometric = np.maximum(0,GT[-1] - K) #Payoff for each simulation, at each time step[N*M]
    else:
        PayoffGeometric = np.maximum(0,K - GT[-1]) #[N*M]
    GeometricPrice = PayoffGeometric * actrate

    #Computing average of cumulative BS prices
    GeoBSPrice = BS_geo(S0, K,T,vol,r,N,Type)

    #Computing alpha
    Cov = np.cov(AsianPrice, GeometricPrice)
    alpha = Cov[0,1]/Cov[1,1]

    AsianPriceVec = (AsianPrice) - alpha*(GeometricPrice - GeoBSPrice)
    AvgPrice = np.mean(AsianPriceVec)
    SEavg = np.std(AsianPriceVec)/np.sqrt(M)

    #print("Price: {0}, SE: {1}".format(np.round(AvgPrice,4), np.round(SEavg,5)))
    return AvgPrice, SEavg, b

#Because we need to get multiples times the MC simulation to get a vector of option prices, we need to call the definition multiples times
#This function call the right function depending of the model selected 

def Model_provider(S0,K,T,r,vol,N,M,Type,seed, ModelSel, ModelSel2):
    if ModelSel == "Classical MC":
        Price, SE, seed = MC_AsianClass(S0,K,T,r,vol,N,M,Type,seed)
    elif ModelSel == "McAnti":
        Price, SE, seed = MC_SimAnti(S0,K,T,r,vol,N,M,Type,seed)
    elif ModelSel == "McEuro":
        Price, SE, seed = MC_Sim_CV_EUR(S0,K,T,r,vol,N,M,Type,seed)
    elif ModelSel == "McEuroAnti":
        Price, SE, seed = MC_Sim_CV_EUR_ANTI(S0,K,T,r,vol,N,M,Type,seed)
    elif ModelSel == "McSumEuro":
        Price, SE, seed = MC_Sim_CV_EuroSum(S0,K,T,r,vol,N,M,Type,seed)
    elif ModelSel == "McGeo":
        Price, SE, seed = MC_Sim_CV_Geo(S0,K,T,r,vol,N,M,Type,seed)

    if ModelSel2 == "Classical MC":
        Price2, SE2, seed2 = MC_AsianClass(S0,K,T,r,vol,N,M,Type,seed*2)
    elif ModelSel2 == "McAnti":
        Price2, SE2, seed2 = MC_SimAnti(S0,K,T,r,vol,N,M,Type,seed*2)
    elif ModelSel2 == "McEuro":
        Price2, SE2, seed2 = MC_Sim_CV_EUR(S0,K,T,r,vol,N,M,Type,seed*2)
    elif ModelSel2 == "McEuroAnti":
        Price2, SE2, seed2 = MC_Sim_CV_EUR_ANTI(S0,K,T,r,vol,N,M,Type,seed*2)
    elif ModelSel2 == "McSumEuro":
        Price2, SE2, seed2 = MC_Sim_CV_EuroSum(S0,K,T,r,vol,N,M,Type,seed*2)
    elif ModelSel2 == "McGeo":
        Price2, SE2, seed2 = MC_Sim_CV_Geo(S0,K,T,r,vol,N,M,Type,seed*2)

    return Price, Price2, SE, SE2, seed, seed2    

