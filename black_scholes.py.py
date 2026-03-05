import numpy as np
from scipy.stats import norm
# Test Values
S_t = 100 # Underlying Price
K_t = 100 # Strike price
T_t = 1.0 # Time to expiry (years)
r_t = 0.05 # Risk-free rate
sigma_t = 0.2 # Annualized volatility

# Defining d1 and d2 functions, Black-Scholes intermediate terms
d1 = lambda S, K, T, r, sigma: (np.log(S/K) + T*(r + (sigma**2)/2))/(sigma*np.sqrt(T))
d2 = lambda S, K, T, r, sigma: d1(S, K, T, r, sigma) - (sigma*np.sqrt(T))

# Value Check
#print (d1(S_t, K_t, T_t, r_t, sigma_t))
#print (d2(S_t, K_t, T_t, r_t, sigma_t))

# Defining the Black Scholes closed form pricing 
# Call
C = lambda S, K, T, r, sigma: (S*norm.cdf(d1(S, K, T, r, sigma))) - (K*np.exp(-r*T)*norm.cdf(d2(S, K, T, r, sigma)))
# Put
P = lambda S, K, T, r, sigma: (K*np.exp(-r*T)*norm.cdf(-d2(S, K, T, r, sigma))) - (S*norm.cdf(-d1(S, K, T, r, sigma)))
# Put call parity check: C - P = S - K*e^(-rT)
Parity_Check = lambda S, K, T, r, sigma: S - (K*np.exp(-r*T))

# Value Check
print(C(S_t, K_t, T_t, r_t, sigma_t))
print(P(S_t, K_t, T_t, r_t, sigma_t))
print(C(S_t, K_t, T_t, r_t, sigma_t) - P(S_t, K_t, T_t, r_t, sigma_t))
print(Parity_Check(S_t, K_t, T_t, r_t, sigma_t))

# Defining the Greeks
# Defining call delta - how much the option price moves per 1$ move in the stock
# Formula -> N(d1)
delta_call = lambda S, K, T, r, sigma: norm.cdf(d1(S, K, T, r, sigma))
# Defining put delta - ""
# Formula -> N(d1) - 1
delta_put = lambda S, K, T, r, sigma: delta_call(S, K, T, r, sigma) - 1
# Defining gamma - how fast delta changes
# Formula -> n(d1) / (S * σ * sqrt(T))
gamma = lambda S, K, T, r, sigma: norm.pdf(d1(S, K, T, r, sigma))/(S*sigma*np.sqrt(T))
# Defining theta - time decay per year 
# Formula -> −[S * n(d1) * σ] / (2*srt(T)) − r * K * e^(−rT) * N(d2)
theta_call = lambda S, K, T, r, sigma: (-(S*norm.pdf(d1(S, K, T, r, sigma))*sigma)/(2*np.sqrt(T))) - ((r*K*np.exp(-r*T)*norm.cdf(d2(S, K, T, r, sigma))))
# Formula -> −[S * n(d1) * σ] / (2*srt(T)) + r * K * e^(−rT) * N(-d2)
theta_put = lambda S, K, T, r, sigma: (-(S*norm.pdf(d1(S, K, T, r, sigma))*sigma)/(2*np.sqrt(T))) + ((r*K*np.exp(-r*T)*norm.cdf(-d2(S, K, T, r, sigma))))
# Defining vega - sensitivity to volatility
# Formula -> S * n(d1) * sqrt(T)
vega = lambda S, K, T, r, sigma: S*norm.pdf(d1(S, K, T, r, sigma))*np.sqrt(T)
# Defining rho - sensitivity to interest rates
# Formula -> K * T * e^(−rT) * N(d2)  
rho_call = lambda S, K, T, r, sigma: K * T * np.exp(-r*T) * norm.cdf(d2(S, K, T, r, sigma))
# Formula -> -K * T * e^(−rT) * N(-d2)
rho_put = lambda S, K, T, r, sigma: - K * T * np.exp(-r*T) * norm.cdf(-d2(S, K, T, r, sigma))

# Value Check
#print(delta_call(S_t, K_t, T_t, r_t, sigma_t))
#print(delta_put(S_t, K_t, T_t, r_t, sigma_t))
#print(gamma(S_t, K_t, T_t, r_t, sigma_t))
#print(theta_call(S_t, K_t, T_t, r_t, sigma_t) / 365)
#print(theta_put(S_t, K_t, T_t, r_t, sigma_t) / 365)
#print(vega(S_t, K_t, T_t, r_t, sigma_t))
#print(rho_call(S_t, K_t, T_t, r_t, sigma_t))
#print(rho_put(S_t, K_t, T_t, r_t, sigma_t))

# Implied Volatility Solver using Newton Raphson
def implied_vol(S, K, T, r, market_price, option_type):
    sigma = 0.2 # starting guess
    tol_err = 1e-6 # tolerance for error check
    tol_zero = 1e-10 # tolerance for near zero values

    for i in range(100): # makximum 100 iterations, Newton Raphson
        if(option_type == "call"):
            price = C(S, K, T, r, sigma) # price (for a call) based on guessed volatility sigma
        elif(option_type == "put"):
            price = P(S, K, T, r, sigma) # price calculation for put
        error = price - market_price # error compared to market price
        Vega = vega(S, K, T, r, sigma)
        if(abs(error) < tol_err): # check if error is within tolerance, if it is we have found sigma
            return sigma
        if(abs(Vega) < tol_zero): # check is vego is close to zero, if it is stop Newton Raphson
            break
        sigma = sigma - (error/Vega)

    sigma_low = 0.01 # lower bound for bisection
    sigma_high = 3.0 # higher bound for bisection
    for j in range(100):# max 100 iterations, Bisection
        sigma_mid = (sigma_low + sigma_high)/2
        if(option_type == "call"):
            price = C(S, K, T, r, sigma_mid)
        elif(option_type == "put"):
            price = P(S, K, T, r, sigma_mid)
        error = price - market_price
        if(abs(error) < tol_err):
            return sigma_mid
        if (error < 0): # volatility should be higher
            sigma_low = sigma_mid # lower bound is increased, the true volatility is in the upper half
        elif (error > 0): # volatility should be lower
            sigma_high = sigma_mid # upper bound is decreased, the true volatility is in the lower half

    print("Could not find implied volatility within reasonable error at " + str(K))    
    return sigma_mid

# Value Check
# print(implied_vol(S_t, K_t, T_t, r_t, 10.450583572185565, "call"))