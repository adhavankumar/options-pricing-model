from black_scholes import *
import matplotlib.pyplot as plt

# Range of S values
S_range = np.linspace(50, 150, 200)

# The greek values for each S value and the test values for other variables
deltaC_values = delta_call(S_range, K_t, T_t, r_t, sigma_t)
deltaP_values = delta_put(S_range, K_t, T_t, r_t, sigma_t)
vega_values = vega(S_range, K_t, T_t, r_t, sigma_t)
thetaC_values = theta_call(S_range, K_t, T_t, r_t, sigma_t)
thetaP_values = theta_put(S_range, K_t, T_t, r_t, sigma_t)
gamma_values = gamma(S_range, K_t, T_t, r_t, sigma_t)

# Plotting S_range and each greek assuming for calls
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Greeks vs. Underlying price')
ax1, ax2, ax3, ax4 = axes.flat

ax1.plot(S_range, deltaC_values)
ax1.set_title('Delta vs Underlying Price')
ax1.set_xlabel('Stock Price')
ax1.set_ylabel('Delta')

ax2.plot(S_range, gamma_values)
ax2.set_title('Gamma vs Underlying Price')
ax2.set_xlabel('Stock Price')
ax2.set_ylabel('Gamma')

ax3.plot(S_range, thetaC_values)
ax3.set_title('Theta vs Underlying Price')
ax3.set_xlabel('Stock Price')
ax3.set_ylabel('Theta')

ax4.plot(S_range, vega_values)
ax4.set_title('Vega vs Underlying Price')
ax4.set_xlabel('Stock Price')
ax4.set_ylabel('Vega')

plt.tight_layout()
fig.savefig('images/greeks_vs_price.png')
plt.show()

# Range of T values
T_range = np.linspace(0.01, 1, 200)

# The greek values for each T value and the test values for other variables
deltaC_values = delta_call(S_t, K_t, T_range, r_t, sigma_t)
deltaP_values = delta_put(S_t, K_t, T_range, r_t, sigma_t)
vega_values = vega(S_t, K_t, T_range, r_t, sigma_t)
thetaC_values = theta_call(S_t, K_t, T_range, r_t, sigma_t)
thetaP_values = theta_put(S_t, K_t, T_range, r_t, sigma_t)
gamma_values = gamma(S_t, K_t, T_range, r_t, sigma_t)

# Plotting T_range and each greek assuming for calls
fig1, axes1 = plt.subplots(2, 2, figsize=(12, 8))
fig1.suptitle('Greeks vs. Time to expiry')
ax11, ax12, ax13, ax14 = axes1.flat

ax11.plot(T_range, deltaC_values)
ax11.set_title('Delta vs Time to expiry')
ax11.set_xlabel('Time to expiry')
ax11.set_ylabel('Delta')

ax12.plot(T_range, gamma_values)
ax12.set_title('Gamma vs Time to expiry')
ax12.set_xlabel('Time to expiry')
ax12.set_ylabel('Gamma')

ax13.plot(T_range, thetaC_values)
ax13.set_title('Theta vs Time to expiry')
ax13.set_xlabel('Time to expiry')
ax13.set_ylabel('Theta')

ax14.plot(T_range, vega_values)
ax14.set_title('Vega vs Time to expiry')
ax14.set_xlabel('Time to expiry')
ax14.set_ylabel('Vega')

plt.tight_layout()
fig1.savefig('images/greeks_vs_TimetoExpiry.png')
plt.show()

# Long Call P&L
call_premium = C(S_t, K_t, T_t, r_t, sigma_t)
call_pnl = np.maximum(S_range - K_t, 0) - call_premium

# Long put P&L
put_premium = P(S_t, K_t, T_t, r_t, sigma_t)
put_pnl = np.maximum(K_t - S_range, 0) - put_premium

# Iron condor
K_bp = 90
K_sp = 95
K_sc = 105
K_bc = 110

net_premium = (C(S_t, K_sc, T_t, r_t, sigma_t) + P(S_t, K_sp, T_t, r_t, sigma_t)
               - C(S_t, K_bc, T_t, r_t, sigma_t) - P(S_t, K_bp, T_t, r_t, sigma_t))

ic_pnl = (-np.maximum(S_range - K_sc, 0)
          + np.maximum(S_range - K_bc, 0)
          - np.maximum(K_sp - S_range, 0)
          + np.maximum(K_bp - S_range, 0)
          + net_premium)

fig2, ax = plt.subplots(figsize=(10, 6))
ax.plot(S_range, call_pnl, label='Long Call (K=100)')
ax.plot(S_range, put_pnl, label='Long Put (K=100)')
ax.plot(S_range, ic_pnl, label='Iron Condor (90/95/105/110)')
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.set_title('P&L at Expiration')
ax.set_xlabel('Stock Price')
ax.set_ylabel('Profit / Loss')
ax.legend()
plt.tight_layout()
fig2.savefig('images/pnl_diagram.png')
plt.show()