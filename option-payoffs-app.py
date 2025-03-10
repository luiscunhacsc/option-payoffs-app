import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import exp

st.set_page_config(page_title="Options & Derivatives Explorer", layout="wide")

st.title("Options & Derivatives Explorer")
st.markdown("""
This app helps you understand the key concepts of options and derivatives through interactive visualizations.
Explore option payoffs, strategies, and factors affecting prices.

*Created by Luís Simões da Cunha*
""")

# Add license and disclaimer information
with st.expander("License & Disclaimer"):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png", width=120)
    with col2:
        st.markdown("""
        ### CC BY-NC License
        This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
        
        ### Disclaimer
        - This application is for educational purposes only.
        - The author is not a licensed financial advisor, and this content should not be taken as financial advice.
        - Information provided is simplified for educational purposes and may not reflect all market complexities.
        - Options trading involves significant risk and potential for loss.
        - Accuracy of models and calculations is not guaranteed.
        - Users should consult with qualified professionals before making investment decisions.
        """)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Basic Options", "Option Strategies", "Put-Call Parity", "Factors Affecting Price"])

# Basic function to calculate payoffs
def call_payoff(S, K):
    return np.maximum(S - K, 0)

def put_payoff(S, K):
    return np.maximum(K - S, 0)

def binary_call_payoff(S, K):
    return (S > K).astype(int)

def binary_put_payoff(S, K):
    return (S < K).astype(int)

# Basic Options page
if page == "Basic Options":
    st.header("Basic Option Types")
    
    st.markdown("""
    ### Key Concepts
    
    - **Call Option**: The right to buy an asset at an agreed strike price on a specified date
    - **Put Option**: The right to sell an asset at an agreed strike price on a specified date
    - **Strike Price**: The price at which the option can be exercised
    - **Intrinsic Value**: The payoff if exercised immediately
    - **Time Value**: Any value above intrinsic value due to future potential
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option Parameters")
        S0 = st.slider("Current Asset Price ($)", 50, 150, 100)
        K = st.slider("Strike Price ($)", 50, 150, 100)
        premium = st.slider("Option Premium ($)", 0, 20, 5)
        
        # Generate price range
        S_range = np.linspace(50, 150, 100)
        
        option_type = st.radio("Option Type", ["Call", "Put", "Binary Call", "Binary Put"])
        
        if option_type == "Call":
            payoff = call_payoff(S_range, K)
            profit = call_payoff(S_range, K) - premium
            title = f"Call Option (K=${K})"
            formula = r"Call Payoff = max(S - K, 0)"
        elif option_type == "Put":
            payoff = put_payoff(S_range, K)
            profit = put_payoff(S_range, K) - premium
            title = f"Put Option (K=${K})"
            formula = r"Put Payoff = max(K - S, 0)"
        elif option_type == "Binary Call":
            payoff = binary_call_payoff(S_range, K)
            profit = binary_call_payoff(S_range, K) - premium
            title = f"Binary Call Option (K=${K})"
            formula = r"Binary Call Payoff = 1 if S > K, 0 otherwise"
        else:  # Binary Put
            payoff = binary_put_payoff(S_range, K)
            profit = binary_put_payoff(S_range, K) - premium
            title = f"Binary Put Option (K=${K})"
            formula = r"Binary Put Payoff = 1 if S < K, 0 otherwise"
    
    with col2:
        st.subheader("Payoff Diagram")
        st.markdown(f"**Formula**: {formula}")

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot payoff and profit lines
        ax.plot(S_range, payoff, 'b-', linewidth=2, label='Payoff at Expiry')
        ax.plot(S_range, profit, 'g--', linewidth=2, label='Profit (after premium)')
        
        # Add the breakeven point
        if option_type == "Call":
            breakeven = K + premium
            if breakeven <= 150:
                ax.axvline(x=breakeven, color='r', linestyle=':', label=f'Breakeven (${breakeven})')
        elif option_type == "Put":
            breakeven = K - premium
            if breakeven >= 50:
                ax.axvline(x=breakeven, color='r', linestyle=':', label=f'Breakeven (${breakeven})')
        
        # Add the strike price
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        # Current price marker
        ax.axvline(x=S0, color='purple', linestyle='-', label=f'Current Price (${S0})')
        
        # Highlight zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        ax.set_title(title)
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff/Profit ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Value summary
        st.subheader("Current Value Summary")
        current_intrinsic = 0
        if option_type == "Call":
            current_intrinsic = max(S0 - K, 0)
        elif option_type == "Put":
            current_intrinsic = max(K - S0, 0)
        elif option_type == "Binary Call":
            current_intrinsic = 1 if S0 > K else 0
        else:  # Binary Put
            current_intrinsic = 1 if S0 < K else 0
            
        time_value = max(0, premium - current_intrinsic)
        
        value_data = {
            "Component": ["Intrinsic Value", "Time Value", "Total Premium"],
            "Value ($)": [current_intrinsic, time_value, premium]
        }
        
        st.table(pd.DataFrame(value_data))
        
        # In-the-money/out-of-the-money status
        status = ""
        if option_type in ["Call", "Binary Call"]:
            if S0 > K:
                status = "In-the-money"
            elif S0 < K:
                status = "Out-of-the-money"
            else:
                status = "At-the-money"
        else:  # Put options
            if S0 < K:
                status = "In-the-money"
            elif S0 > K:
                status = "Out-of-the-money"
            else:
                status = "At-the-money"
                
        st.markdown(f"**Status**: {status}")
    
    st.markdown("""
    ### Understanding Option Payoffs
    - The **blue line** shows the payoff of the option at expiry
    - The **green dashed line** shows the profit after accounting for the premium paid
    - **Breakeven point** is where the profit becomes positive
    """)

# Option Strategies page
elif page == "Option Strategies":
    st.header("Option Strategies")
    
    st.markdown("""
    Option strategies involve combining options with different strikes, expiries, or types to 
    create specific payoff profiles for different market views.
    """)
    
    strategy = st.selectbox("Select Strategy", [
        "Bull Spread", "Bear Spread", "Straddle", "Strangle", 
        "Butterfly Spread", "Risk Reversal"
    ])
    
    S_range = np.linspace(50, 150, 100)
    
    if strategy == "Bull Spread":
        st.subheader("Bull Spread")
        st.markdown("""
        A **Bull Spread** is created by buying a call option with a lower strike price 
        and selling a call option with a higher strike price. This strategy:
        - Benefits from moderate price increases
        - Limits both potential profit and loss
        - Reduces the cost compared to just buying a call option
        """)
        
        K1 = st.slider("Lower Strike Price ($)", 70, 100, 90)
        K2 = st.slider("Higher Strike Price ($)", K1, 130, 110)
        
        long_call = call_payoff(S_range, K1)
        short_call = -call_payoff(S_range, K2)
        spread_payoff = long_call + short_call
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, long_call, 'b--', label=f'Long Call (K=${K1})')
        ax.plot(S_range, short_call, 'r--', label=f'Short Call (K=${K2})')
        ax.plot(S_range, spread_payoff, 'g-', linewidth=3, label='Bull Spread Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.set_title(f"Bull Spread (K1=${K1}, K2=${K2})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: ${K2-K1} (when asset price ≥ ${K2})  
        **Maximum Loss**: Cost of the spread (premium paid for K1 call minus premium received for K2 call)  
        **Breakeven**: Lower strike + net premium paid
        
        **Formula**: Bull Spread Payoff = max(S-K1, 0) - max(S-K2, 0)
        """)
    
    elif strategy == "Bear Spread":
        st.subheader("Bear Spread")
        st.markdown("""
        A **Bear Spread** is created by buying a put option with a higher strike price 
        and selling a put option with a lower strike price. This strategy:
        - Benefits from moderate price decreases
        - Limits both potential profit and loss
        - Reduces the cost compared to just buying a put option
        """)
        
        K1 = st.slider("Lower Strike Price ($)", 70, 100, 90)
        K2 = st.slider("Higher Strike Price ($)", K1, 130, 110)
        
        long_put = put_payoff(S_range, K2)
        short_put = -put_payoff(S_range, K1)
        spread_payoff = long_put + short_put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, long_put, 'b--', label=f'Long Put (K=${K2})')
        ax.plot(S_range, short_put, 'r--', label=f'Short Put (K=${K1})')
        ax.plot(S_range, spread_payoff, 'g-', linewidth=3, label='Bear Spread Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.set_title(f"Bear Spread (K1=${K1}, K2=${K2})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: ${K2-K1} (when asset price ≤ ${K1})  
        **Maximum Loss**: Cost of the spread (premium paid for K2 put minus premium received for K1 put)  
        **Breakeven**: Higher strike - net premium paid
        
        **Formula**: Bear Spread Payoff = max(K2-S, 0) - max(K1-S, 0)
        """)
    
    elif strategy == "Straddle":
        st.subheader("Straddle")
        st.markdown("""
        A **Straddle** involves buying both a call and a put option with the same strike price 
        and expiration date. This strategy:
        - Benefits from large price movements in either direction
        - Used when expecting significant volatility or a major news announcement
        - Profitable if the price moves more than the combined premiums
        """)
        
        K = st.slider("Strike Price ($)", 70, 130, 100)
        
        call = call_payoff(S_range, K)
        put = put_payoff(S_range, K)
        straddle_payoff = call + put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call, 'b--', label=f'Call (K=${K})')
        ax.plot(S_range, put, 'r--', label=f'Put (K=${K})')
        ax.plot(S_range, straddle_payoff, 'g-', linewidth=3, label='Straddle Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax.set_title(f"Straddle (K=${K})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: Unlimited (increases as price moves away from strike)  
        **Maximum Loss**: Combined premium of call and put (occurs if price = strike at expiry)  
        **Breakeven Points**: Strike + combined premium OR Strike - combined premium
        
        **Formula**: Straddle Payoff = max(S-K, 0) + max(K-S, 0) = |S-K|
        """)
    
    elif strategy == "Strangle":
        st.subheader("Strangle")
        st.markdown("""
        A **Strangle** involves buying an out-of-the-money call and an out-of-the-money put. This strategy:
        - Benefits from large price movements in either direction
        - Cheaper than a straddle but requires larger price movement to be profitable
        - Used when expecting significant volatility but with higher risk tolerance
        """)
        
        K1 = st.slider("Put Strike Price ($)", 70, 100, 90)
        K2 = st.slider("Call Strike Price ($)", K1, 130, 110)
        
        call = call_payoff(S_range, K2)
        put = put_payoff(S_range, K1)
        strangle_payoff = call + put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call, 'b--', label=f'Call (K=${K2})')
        ax.plot(S_range, put, 'r--', label=f'Put (K=${K1})')
        ax.plot(S_range, strangle_payoff, 'g-', linewidth=3, label='Strangle Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle='--', label=f'Put Strike (${K1})')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'Call Strike (${K2})')
        
        ax.set_title(f"Strangle (K1=${K1}, K2=${K2})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: Unlimited (increases as price moves far from strikes)  
        **Maximum Loss**: Combined premium of call and put (occurs if price between strikes at expiry)  
        **Breakeven Points**: Lower strike - combined premium OR Higher strike + combined premium
        
        **Formula**: Strangle Payoff = max(S-K2, 0) + max(K1-S, 0)
        """)
    
    elif strategy == "Butterfly Spread":
        st.subheader("Butterfly Spread")
        st.markdown("""
        A **Butterfly Spread** involves buying one call at a lower strike, selling two calls at a middle strike,
        and buying one call at a higher strike. This strategy:
        - Benefits when price remains near the middle strike
        - Has limited risk and limited profit potential
        - Used when expecting low volatility or a stable price
        """)
        
        K1 = st.slider("Lowest Strike Price ($)", 70, 90, 80)
        K2 = st.slider("Middle Strike Price ($)", K1+10, 110, 100)
        K3 = st.slider("Highest Strike Price ($)", K2+10, 130, 120)
        
        call1 = call_payoff(S_range, K1)
        call2 = -2 * call_payoff(S_range, K2)
        call3 = call_payoff(S_range, K3)
        butterfly_payoff = call1 + call2 + call3
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call1, 'b--', label=f'Long Call (K=${K1})')
        ax.plot(S_range, call2, 'r--', label=f'Short 2 Calls (K=${K2})')
        ax.plot(S_range, call3, 'y--', label=f'Long Call (K=${K3})')
        ax.plot(S_range, butterfly_payoff, 'g-', linewidth=3, label='Butterfly Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle=':', label=f'K1=${K1}')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'K2=${K2}')
        ax.axvline(x=K3, color='gray', linestyle=':', label=f'K3=${K3}')
        
        ax.set_title(f"Butterfly Spread (K1=${K1}, K2=${K2}, K3=${K3})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: ${K2-K1} (occurs if price = middle strike at expiry)  
        **Maximum Loss**: Net premium paid (limited)  
        **Breakeven Points**: Lower strike + net premium OR Higher strike - net premium
        
        **Formula**: Butterfly Payoff = max(S-K1, 0) - 2*max(S-K2, 0) + max(S-K3, 0)
        """)
    
    elif strategy == "Risk Reversal":
        st.subheader("Risk Reversal")
        st.markdown("""
        A **Risk Reversal** involves selling an out-of-the-money put and buying an out-of-the-money call.
        This strategy:
        - Creates a position similar to holding the underlying asset
        - Benefits from rising prices and is hurt by falling prices
        - Can be structured to be zero-cost (premiums offset each other)
        """)
        
        K1 = st.slider("Put Strike Price ($)", 70, 95, 90)
        K2 = st.slider("Call Strike Price ($)", 105, 130, 110)
        
        short_put = -put_payoff(S_range, K1)
        long_call = call_payoff(S_range, K2)
        risk_reversal_payoff = short_put + long_call
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, short_put, 'r--', label=f'Short Put (K=${K1})')
        ax.plot(S_range, long_call, 'b--', label=f'Long Call (K=${K2})')
        ax.plot(S_range, risk_reversal_payoff, 'g-', linewidth=3, label='Risk Reversal Payoff')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle='--', label=f'Put Strike (${K1})')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'Call Strike (${K2})')
        
        ax.set_title(f"Risk Reversal (K1=${K1}, K2=${K2})")
        ax.set_xlabel('Asset Price at Expiry ($)')
        ax.set_ylabel('Payoff ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Maximum Profit**: Unlimited (increases as price rises above call strike)  
        **Maximum Loss**: Limited but potentially large (increases as price falls below put strike)  
        
        **Formula**: Risk Reversal Payoff = max(S-K2, 0) - max(K1-S, 0)
        """)

# Put-Call Parity page
elif page == "Put-Call Parity":
    st.header("Put-Call Parity")
    
    st.markdown("""
    Put-Call Parity is a fundamental relationship that connects the prices of European put options, 
    call options, the underlying asset, and a risk-free bond.
    
    ### The Formula
    
    $$ C - P = S - K e^{-r(T-t)} $$
    
    Where:
    - $C$ is the call price
    - $P$ is the put price
    - $S$ is the underlying asset price
    - $K$ is the strike price
    - $r$ is the risk-free interest rate
    - $T-t$ is the time to expiry in years
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parameters")
        S0 = st.slider("Current Asset Price ($)", 50, 150, 100)
        K = st.slider("Strike Price ($)", 50, 150, 100)
        r = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0) / 100
        T = st.slider("Time to Expiry (years)", 0.1, 2.0, 1.0, 0.1)
        
        # Calculate theoretical prices (using very basic model for illustration)
        vol = 0.2  # Assumed volatility
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        from scipy.stats import norm
        call_price = S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        put_price = K * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
        
        st.markdown(f"""
        ### Theoretical Prices
        - Call Option Price: **${call_price:.2f}**
        - Put Option Price: **${put_price:.2f}**
        - Present Value of Strike: **${K*np.exp(-r*T):.2f}**
        """)
        
        # Check put-call parity
        left_side = call_price - put_price
        right_side = S0 - K * np.exp(-r*T)
        
        st.markdown(f"""
        ### Verification of Put-Call Parity
        - Left Side (C - P): **${left_side:.2f}**
        - Right Side (S - Ke^(-rT)): **${right_side:.2f}**
        - Difference: **${left_side - right_side:.4f}** (should be close to zero)
        """)
        
    with col2:
        st.subheader("Visual Representation")
        
        # Generate price range
        S_range = np.linspace(50, 150, 100)
        
        # Calculate payoffs at expiry
        call_payoff_values = call_payoff(S_range, K)
        put_payoff_values = put_payoff(S_range, K)
        stock_minus_bond = S_range - K  # At expiry, bond value is just K
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(S_range, call_payoff_values, 'b-', label='Call Payoff')
        ax.plot(S_range, -put_payoff_values, 'r-', label='-Put Payoff')
        ax.plot(S_range, call_payoff_values - put_payoff_values, 'g-', linewidth=3, 
                label='Call - Put')
        ax.plot(S_range, stock_minus_bond, 'k--', label='Stock - Strike')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax.set_title("Put-Call Parity at Expiry")
        ax.set_xlabel('Asset Price ($)')
        ax.set_ylabel('Value ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown("""
        The green line (Call - Put) overlaps perfectly with the black dashed line (Stock - Strike) at expiry,
        demonstrating put-call parity.
        
        ### Arbitrage Opportunity
        If put-call parity doesn't hold in the market, an arbitrage opportunity exists:
        1. If C - P > S - Ke^(-rT), sell the call, buy the put, short the stock, and invest Ke^(-rT)
        2. If C - P < S - Ke^(-rT), buy the call, sell the put, buy the stock, and borrow Ke^(-rT)
        """)

# Factors Affecting Price page
elif page == "Factors Affecting Price":
    st.header("Factors Affecting Option Prices")
    
    st.markdown("""
    The price of an option is influenced by several key factors. Understanding these relationships
    is crucial for options trading and risk management.
    """)
    
    factor = st.selectbox("Select Factor to Explore", [
        "Underlying Asset Price", "Time to Expiry", "Volatility", 
        "Interest Rate", "Strike Price"
    ])
    
    if factor == "Underlying Asset Price":
        st.subheader("Effect of Underlying Asset Price")
        st.markdown("""
        The price of the underlying asset is one of the most important factors affecting option prices:
        - **Call options** increase in value when the underlying asset price increases
        - **Put options** decrease in value when the underlying asset price increases
        
        Near the strike price, option values are most sensitive to changes in the underlying.
        """)
        
        # Parameters
        K = 100
        r = 0.05
        T = 1.0
        vol = 0.2
        
        # Generate price range
        S_range = np.linspace(70, 130, 100)
        
        # Calculate theoretical prices using Black-Scholes approximation
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        from scipy.stats import norm
        call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(S_range, call_prices, 'b-', linewidth=2, label='Call Option')
        ax.plot(S_range, put_prices, 'r-', linewidth=2, label='Put Option')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax.set_title(f"Option Prices vs. Underlying Asset Price (Strike=${K})")
        ax.set_xlabel('Underlying Asset Price ($)')
        ax.set_ylabel('Option Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Add delta curve
        st.subheader("Delta: Rate of Change with Asset Price")
        
        # Calculate delta
        call_delta = norm.cdf(d1)
        put_delta = call_delta - 1
        
        # Plot delta
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(S_range, call_delta, 'b-', linewidth=2, label='Call Delta')
        ax2.plot(S_range, put_delta, 'r-', linewidth=2, label='Put Delta')
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax2.set_title(f"Option Delta vs. Underlying Asset Price (Strike=${K})")
        ax2.set_xlabel('Underlying Asset Price ($)')
        ax2.set_ylabel('Delta')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        **Delta** measures the rate of change of option price with respect to changes in the underlying asset price:
        - Call delta ranges from 0 to 1
        - Put delta ranges from -1 to 0
        - At-the-money options have deltas around 0.5 (calls) or -0.5 (puts)
        
        Delta is important for hedging and understanding the option's exposure to price movements.
        """)
        
    elif factor == "Time to Expiry":
        st.subheader("Effect of Time to Expiry")
        st.markdown("""
        Time to expiry affects option prices through time value:
        
        - Options lose value as they approach expiry (time decay)
        - The rate of time decay (theta) accelerates as expiry approaches
        - At-the-money options are most affected by time decay
        - Time value is greatest for at-the-money options
        """)
        
        # Parameters
        S0 = 100
        K = 100
        r = 0.05
        vol = 0.2
        
        # Time ranges
        T_values = [2.0, 1.0, 0.5, 0.25, 0.1, 0.01]
        
        # Price range
        S_range = np.linspace(70, 130, 100)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for T in T_values:
            # Calculate call prices
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            ax.plot(S_range, call_prices, linewidth=2, label=f'T = {T} years')
        
        # Add the payoff function
        payoff = np.maximum(S_range - K, 0)
        ax.plot(S_range, payoff, 'k--', linewidth=1, label='Payoff at expiry')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax.set_title(f"Call Option Prices vs. Time to Expiry (Strike=${K})")
        ax.set_xlabel('Underlying Asset Price ($)')
        ax.set_ylabel('Call Option Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Time decay illustration
        st.subheader("Time Decay Illustration")
        
        # Fixed price
        atm_call_prices = []
        otm_call_prices = []
        itm_call_prices = []
        days = np.linspace(365, 0, 100)
        years = days/365
        
        for T in years:
            if T == 0:
                # At expiry
                atm_call = max(S0 - K, 0)
                otm_call = max(S0*0.9 - K, 0)
                itm_call = max(S0*1.1 - K, 0)
            else:
                # Calculate call prices
                # At-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                atm_call = S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
                
                # Out-of-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0*0.9/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                otm_call = S0*0.9 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
                
                # In-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0*1.1/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                itm_call = S0*1.1 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            atm_call_prices.append(atm_call)
            otm_call_prices.append(otm_call)
            itm_call_prices.append(itm_call)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(days, atm_call_prices, 'b-', linewidth=2, label='At-the-money Call')
        ax2.plot(days, otm_call_prices, 'r-', linewidth=2, label='Out-of-the-money Call')
        ax2.plot(days, itm_call_prices, 'g-', linewidth=2, label='In-the-money Call')
        
        ax2.set_title("Option Price vs. Days to Expiry")
        ax2.set_xlabel('Days to Expiry')
        ax2.set_ylabel('Call Option Price ($)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        The graph shows how option prices converge to their intrinsic value as expiry approaches:
        
        - **At-the-money options** (blue line) lose all time value at expiry
        - **Out-of-the-money options** (red line) become worthless at expiry if they remain out-of-the-money
        - **In-the-money options** (green line) retain their intrinsic value but lose time value
        
        This time decay is known as **theta** in the Greeks.
        """)
        
    elif factor == "Volatility":
        st.subheader("Effect of Volatility")
        st.markdown("""
        Volatility measures the expected magnitude of price movements of the underlying asset:
        
        - Higher volatility increases option prices (both calls and puts)
        - Volatility is the only factor in option pricing that is not directly observable
        - Implied volatility is derived from market prices of options
        - Volatility tends to increase during market stress
        """)
        
        # Parameters
        S0 = 100
        K = 100
        r = 0.05
        T = 1.0
        
        # Volatility values
        vol_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        # Price range
        S_range = np.linspace(70, 130, 100)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for vol in vol_values:
            # Calculate call prices
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            ax.plot(S_range, call_prices, linewidth=2, label=f'σ = {vol*100:.0f}%')
        
        # Add the payoff function
        payoff = np.maximum(S_range - K, 0)
        ax.plot(S_range, payoff, 'k--', linewidth=1, label='Payoff at expiry')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Strike (${K})')
        
        ax.set_title(f"Call Option Prices vs. Volatility (Strike=${K})")
        ax.set_xlabel('Underlying Asset Price ($)')
        ax.set_ylabel('Call Option Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Volatility smile illustration
        st.subheader("Volatility Smile")
        
        # Create synthetic implied volatility data for visualization
        strikes = np.linspace(80, 120, 9)
        atm_vol = 0.2
        
        # Synthetic volatility smile
        def vol_smile(k):
            return atm_vol + 0.001 * (k-K)**2
        
        implied_vols = [vol_smile(k) for k in strikes]
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(strikes, implied_vols, 'b-o', linewidth=2)
        
        ax2.axvline(x=S0, color='gray', linestyle='--', label=f'Current Price (${S0})')
        
        ax2.set_title("Implied Volatility Smile")
        ax2.set_xlabel('Strike Price ($)')
        ax2.set_ylabel('Implied Volatility')
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig2)
        
        st.markdown("""
        ### Volatility Smile
        
        In practice, implied volatility varies across different strike prices, creating a "smile" pattern:
        
        - Lower strikes (OTM puts/ITM calls) often have higher implied volatility
        - Higher strikes (ITM puts/OTM calls) often have higher implied volatility
        - This pattern contradicts the constant volatility assumption in Black-Scholes
        - The volatility smile reflects market concerns about extreme price movements
        
        Vega (sensitivity to volatility) is highest for at-the-money options.
        """)
        
    elif factor == "Interest Rate":
        st.subheader("Effect of Interest Rate")
        st.markdown("""
        Interest rates affect option prices in several ways:
        
        - Higher interest rates generally increase call option prices
        - Higher interest rates generally decrease put option prices
        - The effect is usually less significant than other factors
        - Interest rates impact the present value of the strike price
        - The effect relates to the time value of money and cost of carrying the underlying asset
        """)
        
        # Parameters
        S0 = 100
        K = 100
        T = 1.0
        vol = 0.2
        
        # Interest rate values
        r_values = [0.01, 0.03, 0.05, 0.07, 0.10]
        
        # Price range
        S_range = np.linspace(70, 130, 100)
        
        # Plot for call options
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        for r in r_values:
            # Calculate call prices
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
            
            ax1.plot(S_range, call_prices, linewidth=2, label=f'r = {r*100:.0f}%')
            ax2.plot(S_range, put_prices, linewidth=2, label=f'r = {r*100:.0f}%')
        
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=K, color='gray', linestyle='--')
        ax1.set_title("Call Option Prices vs. Interest Rate")
        ax1.set_xlabel('Underlying Asset Price ($)')
        ax1.set_ylabel('Call Option Price ($)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=K, color='gray', linestyle='--')
        ax2.set_title("Put Option Prices vs. Interest Rate")
        ax2.set_xlabel('Underlying Asset Price ($)')
        ax2.set_ylabel('Put Option Price ($)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig)
        
        # Present value illustration
        st.subheader("Present Value of Strike Price")
        
        r_range = np.linspace(0.01, 0.10, 100)
        pv_strike = [K * np.exp(-r*T) for r in r_range]
        
        fig2, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.plot(r_range*100, pv_strike, 'b-', linewidth=2)
        
        ax3.set_title(f"Present Value of Strike (K=${K}, T={T} year)")
        ax3.set_xlabel('Interest Rate (%)')
        ax3.set_ylabel('Present Value of Strike ($)')
        ax3.grid(True, alpha=0.3)
        
        st.pyplot(fig2)
        
        st.markdown("""
        The present value of the strike price decreases as interest rates increase. This explains why:
        
        - Call options become more valuable with higher rates (lower present value of strike)
        - Put options become less valuable with higher rates (lower present value of strike)
        
        In put-call parity: C - P = S - Ke^(-rT)
        """)
        
    elif factor == "Strike Price":
        st.subheader("Effect of Strike Price")
        st.markdown("""
        The strike price is a fundamental parameter in options:
        
        - Call options decrease in value as strike price increases
        - Put options increase in value as strike price increases
        - At-the-money options (strike ≈ current price) have the most time value
        - Deep in-the-money options behave similarly to the underlying asset
        - Deep out-of-the-money options have low delta and are most sensitive to volatility
        """)
        
        # Parameters
        S0 = 100
        r = 0.05
        T = 1.0
        vol = 0.2
        
        # Strike values
        K_values = [80, 90, 100, 110, 120]
        
        # Price range
        S_range = np.linspace(70, 130, 100)
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        for K in K_values:
            # Calculate prices
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
            
            ax1.plot(S_range, call_prices, linewidth=2, label=f'K = ${K}')
            ax2.plot(S_range, put_prices, linewidth=2, label=f'K = ${K}')
        
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=S0, color='gray', linestyle='--', label=f'Current Price (${S0})')
        ax1.set_title("Call Option Prices vs. Strike Price")
        ax1.set_xlabel('Underlying Asset Price ($)')
        ax1.set_ylabel('Call Option Price ($)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=S0, color='gray', linestyle='--', label=f'Current Price (${S0})')
        ax2.set_title("Put Option Prices vs. Strike Price")
        ax2.set_xlabel('Underlying Asset Price ($)')
        ax2.set_ylabel('Put Option Price ($)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig)
        
        # Plot of option price vs. strike
        K_range = np.linspace(70, 130, 100)
        
        # Calculate prices
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K_range) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        call_prices = S0 * norm.cdf(d1) - K_range * np.exp(-r*T) * norm.cdf(d2)
        put_prices = K_range * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
        
        fig2, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.plot(K_range, call_prices, 'b-', linewidth=2, label='Call Option')
        ax3.plot(K_range, put_prices, 'r-', linewidth=2, label='Put Option')
        
        ax3.axvline(x=S0, color='gray', linestyle='--', label=f'Current Price (${S0})')
        
        ax3.set_title(f"Option Prices vs. Strike Price (S=${S0})")
        ax3.set_xlabel('Strike Price ($)')
        ax3.set_ylabel('Option Price ($)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        The graphs show how option prices vary with strike price:
        
        - For calls: the lower the strike, the higher the value
        - For puts: the higher the strike, the higher the value
        - At-the-money options (S ≈ K) have the most time value and highest vega
        
        Strike price selection is critical in options strategies.
        """)

# Footer
st.markdown("---")
st.markdown("""
### Summary
This app demonstrates the fundamental concepts of options trading:

1. Options give rights without obligations
2. The primary factors affecting option prices are:
   - Underlying asset price
   - Time to expiry
   - Volatility
   - Interest rates
   - Strike price

3. Option strategies can be constructed for different market views:
   - Directional views (bull/bear spreads)
   - Volatility views (straddles/strangles)
   - Range-bound views (butterflies/condors)

4. Put-call parity provides a fundamental relationship between call and put prices

### About the Author
Luís Simões da Cunha is a financial educator specializing in derivatives and quantitative finance. This tool was developed to help students and practitioners visualize key options concepts for educational purposes.

### Contact
For questions, suggestions, or educational inquiries, please contact the author.

---
*© 2025 Luís Simões da Cunha. All rights reserved except as granted under CC BY-NC license.*
""")