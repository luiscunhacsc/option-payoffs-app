import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Financial Derivatives Explorer", layout="wide")

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 28px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .subsection-header {
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .concept {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .formula {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        margin: 10px 0;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
    }
    .cc-license {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
    }
    .cc-license img {
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Financial Derivatives Explorer</p>', unsafe_allow_html=True)

st.write("""
This interactive application will help you understand the fundamental concepts of financial derivatives, 
with a focus on options. Explore different topics through the navigation menu and use the interactive 
tools to visualize key concepts.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a topic:",
    ["Introduction to Derivatives", 
     "Option Basics", 
     "Option Payoffs", 
     "Put-Call Parity",
     "Option Strategies",
     "Glossary"]
)

########################
# Introduction Page
########################
if page == "Introduction to Derivatives":
    st.markdown('<p class="section-header">Introduction to Financial Derivatives</p>', unsafe_allow_html=True)
    
    st.write("""
    Financial derivatives are financial instruments whose value is derived from the value of underlying assets. 
    These underlying assets can include stocks, bonds, commodities, currencies, interest rates, and market indexes.
    """)
    
    st.markdown('<p class="subsection-header">Key Characteristics of Derivatives</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="concept">', unsafe_allow_html=True)
    st.write("""
    Derivatives have several key characteristics:
    
    1. **Derived Value**: Their value comes from an underlying asset or benchmark
    2. **Future Settlement**: They typically settle at a future date
    3. **Leverage**: They often provide leverage, allowing for amplified gains or losses
    4. **Risk Management**: They are used for hedging and risk management
    5. **Speculation**: They can be used for speculative purposes
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="subsection-header">Types of Derivatives</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="concept">', unsafe_allow_html=True)
        st.write("""
        **Forwards and Futures**
        
        Contracts that obligate the parties to buy or sell an asset at a predetermined future date and price.
        - **Futures** are standardized contracts traded on exchanges
        - **Forwards** are customized contracts traded over-the-counter (OTC)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="concept">', unsafe_allow_html=True)
        st.write("""
        **Options**
        
        Contracts that give the buyer the right, but not the obligation, to buy or sell an asset at a specified price on or before a specified date.
        - **Call options** give the right to buy
        - **Put options** give the right to sell
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("""
    This application focuses primarily on options, which are one of the most commonly used derivatives in financial markets.
    """)
    
    st.markdown('<p class="subsection-header">Why Study Derivatives?</p>', unsafe_allow_html=True)
    
    st.write("""
    Understanding derivatives is essential for several reasons:
    
    1. **Risk Management**: Derivatives allow individuals and companies to manage price risks
    2. **Price Discovery**: They help in determining the price of the underlying asset
    3. **Market Efficiency**: They contribute to market efficiency and liquidity
    4. **Investment Opportunities**: They provide additional investment opportunities
    """)

########################
# Option Basics
########################
elif page == "Option Basics":
    st.markdown('<p class="section-header">Option Basics</p>', unsafe_allow_html=True)
    
    st.write("""
    Options are financial contracts that give the buyer the right, but not the obligation, to buy or sell an underlying 
    asset at a predetermined price within a specific time period.
    """)
    
    st.markdown('<p class="subsection-header">Key Elements of an Option Contract</p>', unsafe_allow_html=True)
    
    elements = {
        "Underlying Asset": "The financial instrument on which the option value depends (stocks, commodities, currencies, indices)",
        "Strike Price": "The price at which the option can be exercised (also called exercise price)",
        "Expiration Date": "The date after which the option ceases to exist or give the holder any rights",
        "Premium": "The price paid to acquire the option",
        "Option Type": "Call (right to buy) or Put (right to sell)"
    }
    
    for key, value in elements.items():
        st.markdown(f"**{key}**: {value}")
    
    st.markdown('<p class="subsection-header">Call Options vs. Put Options</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="concept">', unsafe_allow_html=True)
        st.subheader("Call Option")
        st.write("""
        A call option gives the holder the right to buy the underlying asset at the strike price before or at expiry.
        
        - **Buyer's View**: Expects the asset price to rise
        - **Seller's Position**: Obligated to deliver the asset if the option is exercised
        - **Payoff at Expiry**: max(S - E, 0) where S is the asset price and E is the strike price
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="concept">', unsafe_allow_html=True)
        st.subheader("Put Option")
        st.write("""
        A put option gives the holder the right to sell the underlying asset at the strike price before or at expiry.
        
        - **Buyer's View**: Expects the asset price to fall
        - **Seller's Position**: Obligated to buy the asset if the option is exercised
        - **Payoff at Expiry**: max(E - S, 0) where S is the asset price and E is the strike price
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="subsection-header">Option Styles</p>', unsafe_allow_html=True)
    
    option_styles = {
        "European Options": "Can only be exercised at expiration",
        "American Options": "Can be exercised at any time before or at expiration",
        "Bermudan Options": "Can be exercised on specified dates before expiration"
    }
    
    for key, value in option_styles.items():
        st.markdown(f"**{key}**: {value}")
    
    st.markdown('<p class="subsection-header">Options Terminology</p>', unsafe_allow_html=True)
    
    terminology = {
        "In-the-money (ITM)": "Call: Stock price > Strike price | Put: Stock price < Strike price",
        "At-the-money (ATM)": "Stock price ≈ Strike price",
        "Out-of-the-money (OTM)": "Call: Stock price < Strike price | Put: Stock price > Strike price",
        "Intrinsic Value": "The payoff if the option were exercised immediately: max(S - E, 0) for calls, max(E - S, 0) for puts",
        "Time Value": "Premium - Intrinsic Value"
    }
    
    for key, value in terminology.items():
        st.markdown(f"**{key}**: {value}")

########################
# Option Payoffs
########################
elif page == "Option Payoffs":
    st.markdown('<p class="section-header">Option Payoffs</p>', unsafe_allow_html=True)
    
    st.write("""
    The payoff of an option at expiration is determined by the relationship between the underlying asset's price and the option's strike price.
    """)
    
    st.markdown('<p class="subsection-header">Interactive Payoff Diagrams</p>', unsafe_allow_html=True)
    
    # User inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        option_type = st.selectbox("Option Type", ["Call", "Put"])
    
    with col2:
        position = st.selectbox("Position", ["Long", "Short"])
    
    with col3:
        strike_price = st.slider("Strike Price", 50, 150, 100)
    
    # Additional parameters
    premium = st.slider("Option Premium", 1, 30, 10)
    
    # Generate stock price range
    stock_prices = np.arange(40, 160, 1)
    
    # Calculate payoffs
    if option_type == "Call":
        if position == "Long":
            # Long call
            payoffs = np.maximum(stock_prices - strike_price, 0)
            profits = payoffs - premium
            title = "Long Call Option"
        else:
            # Short call
            payoffs = np.minimum(strike_price - stock_prices, 0)
            profits = -np.maximum(stock_prices - strike_price, 0) + premium
            title = "Short Call Option"
    else:  # Put
        if position == "Long":
            # Long put
            payoffs = np.maximum(strike_price - stock_prices, 0)
            profits = payoffs - premium
            title = "Long Put Option"
        else:
            # Short put
            payoffs = -np.maximum(strike_price - stock_prices, 0) + premium
            profits = -np.maximum(strike_price - stock_prices, 0) + premium
            title = "Short Put Option"
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_prices, payoffs, 'b-', linewidth=2, label='Payoff at Expiry')
    ax.plot(stock_prices, profits, 'r-', linewidth=2, label='Profit/Loss')
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.axvline(x=strike_price, color='green', linestyle='--', alpha=0.5, label='Strike Price')
    
    # Set labels and title
    ax.set_xlabel('Stock Price at Expiry')
    ax.set_ylabel('Payoff/Profit')
    ax.set_title(f'{title} (Strike={strike_price}, Premium={premium})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Display the plot
    st.pyplot(fig)
    
    # Payoff formulas
    st.markdown('<p class="subsection-header">Payoff Formulas</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="formula">', unsafe_allow_html=True)
    if option_type == "Call":
        st.latex(r"Call\ Payoff = \max(S - E, 0)")
        st.latex(r"Call\ Profit = \max(S - E, 0) - Premium")
    else:
        st.latex(r"Put\ Payoff = \max(E - S, 0)")
        st.latex(r"Put\ Profit = \max(E - S, 0) - Premium")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("""
    Where:
    - S is the stock price at expiry
    - E is the strike price
    - Premium is the initial cost of the option
    """)
    
    st.markdown('<p class="subsection-header">Analyzing Payoff Diagrams</p>', unsafe_allow_html=True)
    
    st.write("""
    The payoff diagram helps visualize:
    
    1. **Break-Even Point**: Where profit becomes positive
    2. **Maximum Profit/Loss**: The limits to potential gains and losses
    3. **Risk Profile**: How the option responds to changes in the underlying asset price
    
    For a long call, profit is unlimited as the stock price rises, while loss is limited to the premium paid.
    For a long put, profit increases as the stock price falls, while loss is limited to the premium paid.
    """)

########################
# Put-Call Parity
########################
elif page == "Put-Call Parity":
    st.markdown('<p class="section-header">Put-Call Parity</p>', unsafe_allow_html=True)
    
    st.write("""
    Put-Call Parity is a fundamental relationship between the prices of European put and call options with the same 
    strike price and expiration date. It establishes a link between call options, put options, the underlying asset, 
    and a risk-free bond.
    """)
    
    st.markdown('<p class="subsection-header">The Put-Call Parity Formula</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="formula">', unsafe_allow_html=True)
    st.latex(r"C - P = S - E \cdot e^{-r(T-t)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("""
    Where:
    - C is the price of the European call option
    - P is the price of the European put option
    - S is the current price of the underlying asset
    - E is the strike price
    - r is the risk-free interest rate
    - T-t is the time to expiration in years
    """)
    
    st.markdown('<p class="subsection-header">Interactive Put-Call Parity Demonstration</p>', unsafe_allow_html=True)
    
    # User inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        asset_price = st.slider("Current Asset Price (S)", 80, 120, 100)
    
    with col2:
        strike_price = st.slider("Strike Price (E)", 80, 120, 100, key="pcp_strike")
    
    with col3:
        interest_rate = st.slider("Risk-Free Rate (%)", 1.0, 10.0, 5.0) / 100
    
    time_to_expiry = st.slider("Time to Expiry (Years)", 0.0, 2.0, 1.0, 0.1)
    
    # Calculate the right side of put-call parity
    right_side = asset_price - strike_price * np.exp(-interest_rate * time_to_expiry)
    
    # Let the user input either call or put price
    option_choice = st.radio("Choose which option price to input:", ["Call", "Put"])
    
    if option_choice == "Call":
        call_price = st.slider("Call Option Price", 0.0, 50.0, 10.0, 0.5)
        put_price = call_price - right_side
        message = f"Based on Put-Call Parity, the Put Option should be priced at: ${put_price:.2f}"
    else:
        put_price = st.slider("Put Option Price", 0.0, 50.0, 10.0, 0.5)
        call_price = put_price + right_side
        message = f"Based on Put-Call Parity, the Call Option should be priced at: ${call_price:.2f}"
    
    st.markdown(f"<div style='background-color:#D4EDDA; padding:15px; border-radius:5px;'><b>{message}</b></div>", unsafe_allow_html=True)
    
    # Show a table with the values
    data = {
        "Component": ["Call Option (C)", "Put Option (P)", "Asset Price (S)", "Discounted Strike (E·e^(-rT))", "C - P", "S - E·e^(-rT)"],
        "Value": [
            f"${call_price:.2f}", 
            f"${put_price:.2f}", 
            f"${asset_price:.2f}", 
            f"${strike_price * np.exp(-interest_rate * time_to_expiry):.2f}",
            f"${call_price - put_price:.2f}",
            f"${right_side:.2f}"
        ]
    }
    
    st.table(pd.DataFrame(data))
    
    st.markdown('<p class="subsection-header">Implications of Put-Call Parity</p>', unsafe_allow_html=True)
    
    st.write("""
    Put-Call Parity has several important implications:
    
    1. **Arbitrage Opportunities**: If put-call parity is violated, arbitrage opportunities exist
    2. **Synthetic Positions**: You can create synthetic options using the other components:
        - Synthetic Call = Put + Stock - Risk-free Bond
        - Synthetic Put = Call - Stock + Risk-free Bond
    3. **Pricing Relationship**: It establishes a relationship that must hold for option prices to be consistent
    4. **Model Independence**: The relationship holds regardless of which option pricing model is used
    """)

########################
# Option Strategies
########################
elif page == "Option Strategies":
    st.markdown('<p class="section-header">Option Strategies</p>', unsafe_allow_html=True)
    
    st.write("""
    Option strategies involve combining multiple options and sometimes the underlying asset to create positions 
    with specific risk-reward characteristics. These strategies can be used for hedging, income generation, 
    speculation, or taking advantage of expected volatility changes.
    """)
    
    # Strategy selector
    strategy = st.selectbox(
        "Select a strategy to explore:",
        ["Bull Spread", "Bear Spread", "Straddle", "Strangle", "Butterfly Spread", "Risk Reversal"]
    )
    
    # Base parameters for all strategies
    col1, col2 = st.columns(2)
    with col1:
        stock_price = st.slider("Current Stock Price", 80, 120, 100)
    with col2:
        if strategy in ["Bull Spread", "Bear Spread", "Risk Reversal"]:
            lower_strike = st.slider("Lower Strike Price", 70, 100, 90)
            upper_strike = st.slider("Upper Strike Price", 100, 130, 110)
        elif strategy in ["Straddle", "Butterfly Spread"]:
            center_strike = st.slider("Strike Price", 80, 120, 100)
        elif strategy == "Strangle":
            put_strike = st.slider("Put Strike Price", 70, 100, 90)
            call_strike = st.slider("Call Strike Price", 100, 130, 110)
    
    # Generate stock price range
    stock_prices = np.arange(50, 150, 1)
    
    # Calculate payoffs based on strategy
    if strategy == "Bull Spread":
        # Bull Spread (Call Spread): Long a lower strike call, short a higher strike call
        long_call_payoff = np.maximum(stock_prices - lower_strike, 0)
        short_call_payoff = -np.maximum(stock_prices - upper_strike, 0)
        payoffs = long_call_payoff + short_call_payoff
        max_profit = upper_strike - lower_strike
        max_loss = -(upper_strike - lower_strike) * 0.3  # Estimated premium cost
        description = """
        A **Bull Spread** is created by buying a call option with a lower strike price and selling a call option with a higher strike price.
        
        - **Outlook**: Moderately bullish
        - **Maximum Profit**: Difference between strike prices minus net premium paid
        - **Maximum Loss**: Net premium paid
        - **Break-even**: Lower strike price plus net premium paid
        """
    
    elif strategy == "Bear Spread":
        # Bear Spread (Put Spread): Long a higher strike put, short a lower strike put
        long_put_payoff = np.maximum(upper_strike - stock_prices, 0)
        short_put_payoff = -np.maximum(lower_strike - stock_prices, 0)
        payoffs = long_put_payoff + short_put_payoff
        max_profit = upper_strike - lower_strike
        max_loss = -(upper_strike - lower_strike) * 0.3  # Estimated premium cost
        description = """
        A **Bear Spread** is created by buying a put option with a higher strike price and selling a put option with a lower strike price.
        
        - **Outlook**: Moderately bearish
        - **Maximum Profit**: Difference between strike prices minus net premium paid
        - **Maximum Loss**: Net premium paid
        - **Break-even**: Higher strike price minus net premium paid
        """
    
    elif strategy == "Straddle":
        # Straddle: Long a call and a put with the same strike
        call_payoff = np.maximum(stock_prices - center_strike, 0)
        put_payoff = np.maximum(center_strike - stock_prices, 0)
        payoffs = call_payoff + put_payoff
        premium_estimate = center_strike * 0.15  # Estimated total premium cost
        max_profit = "Unlimited"
        max_loss = f"${premium_estimate:.2f} (Premium paid)"
        description = """
        A **Straddle** is created by buying both a call option and a put option with the same strike price and expiration date.
        
        - **Outlook**: High volatility, significant price movement in either direction
        - **Maximum Profit**: Unlimited to the upside, limited to the strike price to the downside
        - **Maximum Loss**: Total premium paid for both options
        - **Break-even**: Strike price ± total premium paid
        """
    
    elif strategy == "Strangle":
        # Strangle: Long a call with higher strike and a put with lower strike
        call_payoff = np.maximum(stock_prices - call_strike, 0)
        put_payoff = np.maximum(put_strike - stock_prices, 0)
        payoffs = call_payoff + put_payoff
        premium_estimate = stock_price * 0.12  # Estimated total premium cost
        max_profit = "Unlimited"
        max_loss = f"${premium_estimate:.2f} (Premium paid)"
        description = """
        A **Strangle** is created by buying an out-of-the-money call option and an out-of-the-money put option.
        
        - **Outlook**: High volatility, significant price movement in either direction
        - **Maximum Profit**: Unlimited to the upside, limited to the lower strike price to the downside
        - **Maximum Loss**: Total premium paid for both options
        - **Break-even**: Lower strike price - premium paid OR Upper strike price + premium paid
        """
    
    elif strategy == "Butterfly Spread":
        # Butterfly Spread: Long 1 lower strike call, short 2 middle strike calls, long 1 higher strike call
        wing_width = 10
        lower_strike = center_strike - wing_width
        upper_strike = center_strike + wing_width
        
        lower_call_payoff = np.maximum(stock_prices - lower_strike, 0)
        middle_call_payoff = -2 * np.maximum(stock_prices - center_strike, 0)
        upper_call_payoff = np.maximum(stock_prices - upper_strike, 0)
        
        payoffs = lower_call_payoff + middle_call_payoff + upper_call_payoff
        max_profit = wing_width
        max_loss = wing_width * 0.2  # Estimated premium cost
        description = """
        A **Butterfly Spread** involves buying a low strike call, selling two middle strike calls, and buying a high strike call.
        
        - **Outlook**: Neutral, expecting price to be near the middle strike at expiration
        - **Maximum Profit**: Difference between adjacent strikes minus net premium paid
        - **Maximum Loss**: Net premium paid
        - **Break-even**: Lower strike + premium paid OR Upper strike - premium paid
        """
    
    elif strategy == "Risk Reversal":
        # Risk Reversal: Long a call with higher strike, short a put with lower strike
        call_payoff = np.maximum(stock_prices - upper_strike, 0)
        put_payoff = -np.maximum(lower_strike - stock_prices, 0)
        payoffs = call_payoff + put_payoff
        max_profit = "Unlimited"
        max_loss = "Potentially significant if price falls well below lower strike"
        description = """
        A **Risk Reversal** involves buying an out-of-the-money call and selling an out-of-the-money put.
        
        - **Outlook**: Strongly bullish
        - **Maximum Profit**: Unlimited to the upside
        - **Maximum Loss**: Potentially significant if the underlying price falls well below the put strike
        - **Break-even**: Call strike + net premium if paying for the strategy, or put strike - net premium if receiving credit
        """
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_prices, payoffs, 'b-', linewidth=2)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.axvline(x=stock_price, color='red', linestyle='--', alpha=0.5, label='Current Price')
    
    # Add strategy-specific lines
    if strategy in ["Bull Spread", "Bear Spread", "Risk Reversal"]:
        ax.axvline(x=lower_strike, color='green', linestyle='--', alpha=0.5, label='Lower Strike')
        ax.axvline(x=upper_strike, color='purple', linestyle='--', alpha=0.5, label='Upper Strike')
    elif strategy in ["Straddle", "Butterfly Spread"]:
        ax.axvline(x=center_strike, color='green', linestyle='--', alpha=0.5, label='Strike')
    elif strategy == "Strangle":
        ax.axvline(x=put_strike, color='green', linestyle='--', alpha=0.5, label='Put Strike')
        ax.axvline(x=call_strike, color='purple', linestyle='--', alpha=0.5, label='Call Strike')
    
    # Set labels and title
    ax.set_xlabel('Stock Price at Expiry')
    ax.set_ylabel('Payoff')
    ax.set_title(f'{strategy} Payoff Diagram')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Display the plot
    st.pyplot(fig)
    
    # Display strategy description
    st.markdown('<p class="subsection-header">Strategy Details</p>', unsafe_allow_html=True)
    st.markdown('<div class="concept">', unsafe_allow_html=True)
    st.write(description)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display profit/loss metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Maximum Profit", max_profit)
    with col2:
        st.metric("Maximum Loss", max_loss)
    
    st.markdown('<p class="subsection-header">When to Use This Strategy</p>', unsafe_allow_html=True)
    
    if strategy == "Bull Spread":
        st.write("""
        Consider using a Bull Spread when:
        - You're moderately bullish on the underlying asset
        - You want to reduce the cost of buying a call option
        - You're willing to cap your potential profit to reduce cost
        - You expect the price to rise but not dramatically
        """)
    
    elif strategy == "Bear Spread":
        st.write("""
        Consider using a Bear Spread when:
        - You're moderately bearish on the underlying asset
        - You want to reduce the cost of buying a put option
        - You're willing to cap your potential profit to reduce cost
        - You expect the price to decline but not collapse
        """)
    
    elif strategy == "Straddle":
        st.write("""
        Consider using a Straddle when:
        - You expect significant price movement but are unsure of the direction
        - You anticipate a major announcement or event that could impact the asset price
        - You expect volatility to increase
        - You want to profit from a large move in either direction
        """)
    
    elif strategy == "Strangle":
        st.write("""
        Consider using a Strangle when:
        - You expect significant price movement but are unsure of the direction
        - You want a cheaper alternative to a straddle
        - You're willing to need a larger price move to profit
        - You expect volatility to increase
        """)
    
    elif strategy == "Butterfly Spread":
        st.write("""
        Consider using a Butterfly Spread when:
        - You expect the asset price to remain stable near your target price
        - You want a position with limited risk
        - You're looking for a high reward-to-risk ratio
        - You expect low volatility
        """)
    
    elif strategy == "Risk Reversal":
        st.write("""
        Consider using a Risk Reversal when:
        - You're strongly bullish on the underlying asset
        - You're willing to take on significant downside risk
        - You want to create a position with little or no upfront cost
        - You want to profit from an expected increase in implied volatility skew
        """)

########################
# Glossary
########################
elif page == "Glossary":
    st.markdown('<p class="section-header">Glossary of Option Terms</p>', unsafe_allow_html=True)
    
    st.write("""
    This glossary provides definitions for common terms used in options trading and analysis.
    """)
   
    # Define the glossary terms and definitions
    # Create a search box for the glossary
    search_term = st.text_input("Search the glossary:", "")
    
    # Define the glossary terms and definitions
    glossary = {
        "Call Option": "A contract giving the holder the right, but not the obligation, to buy an underlying asset at a specified price within a specific time period.",
        
        "Put Option": "A contract giving the holder the right, but not the obligation, to sell an underlying asset at a specified price within a specific time period.",
        
        "Strike Price": "The price at which the holder can buy (for calls) or sell (for puts) the underlying asset when exercising an option.",
        
        "Premium": "The price paid by the buyer to the seller for an option contract.",
        
        "Expiration Date": "The date after which the option ceases to exist and can no longer be exercised.",
        
        "Intrinsic Value": "The value an option would have if it were exercised immediately. For calls: max(0, underlying price - strike price). For puts: max(0, strike price - underlying price).",
        
        "Time Value": "The portion of an option's premium that exceeds its intrinsic value, reflecting the probability of the option becoming more valuable before expiration.",
        
        "In-the-Money (ITM)": "A call option is ITM when the underlying price is above the strike price. A put option is ITM when the underlying price is below the strike price.",
        
        "At-the-Money (ATM)": "An option is ATM when the underlying price is approximately equal to the strike price.",
        
        "Out-of-the-Money (OTM)": "A call option is OTM when the underlying price is below the strike price. A put option is OTM when the underlying price is above the strike price.",
        
        "Volatility": "A measure of the amount of fluctuation in the price of the underlying asset, typically expressed as an annualized standard deviation.",
        
        "Exercise": "The act of converting an option into the underlying position (buying the asset for calls, selling it for puts).",
        
        "Assignment": "The obligation of the option writer to fulfill the terms of the contract when the buyer exercises the option.",
        
        "Bull Spread": "An options strategy involving the purchase of a call option with a lower strike price and the sale of a call option with a higher strike price, both with the same expiration date.",
        
        "Bear Spread": "An options strategy involving the purchase of a put option with a higher strike price and the sale of a put option with a lower strike price, both with the same expiration date.",
        
        "Straddle": "An options strategy involving the purchase of both a call and a put with the same strike price and expiration date.",
        
        "Strangle": "An options strategy involving the purchase of an out-of-the-money call and an out-of-the-money put with the same expiration date.",
        
        "Butterfly Spread": "An options strategy involving buying a call at one strike price, selling two calls at a higher strike price, and buying another call at an even higher strike price.",
        
        "Risk Reversal": "An options strategy involving buying an out-of-the-money call and selling an out-of-the-money put with the same expiration date.",
        
        "Put-Call Parity": "A relationship between the prices of European put and call options with the same strike price and expiration date: Call - Put = Stock - Present Value of Strike.",
        
        "Delta": "A measure of how much an option's price is expected to change for a $1 change in the price of the underlying asset.",
        
        "Theta": "A measure of the rate at which an option loses value as time passes (time decay).",
        
        "Vega": "A measure of an option's sensitivity to changes in the implied volatility of the underlying asset.",
        
        "Gamma": "A measure of the rate of change in an option's delta for a $1 change in the price of the underlying asset.",
        
        "Writer": "The seller of an option contract who receives the premium and assumes the obligation to sell (for calls) or buy (for puts) the underlying asset if the option is exercised.",
        
        "Covered Call": "A strategy in which an investor holds a long position in the underlying asset and sells a call option on that same asset.",
        
        "Naked Option": "An option position in which the writer does not hold an offsetting position in the underlying asset.",
        
        "LEAPS": "Long-term Equity Anticipation Securities, which are options with expiration dates longer than one year.",
        
        "Binary Option": "An option with a fixed payout if the underlying asset reaches or exceeds the strike price, and no payout otherwise."
    }
    
    # Filter the glossary based on the search term
    if search_term:
        filtered_glossary = {k: v for k, v in glossary.items() if search_term.lower() in k.lower() or search_term.lower() in v.lower()}
    else:
        filtered_glossary = glossary
    
    # Display the filtered glossary
    if filtered_glossary:
        for term, definition in filtered_glossary.items():
            st.markdown(f"<div style='margin-bottom:15px;'><b>{term}</b>: {definition}</div>", unsafe_allow_html=True)
    else:
        st.warning("No matching terms found. Try a different search term.")

# Footer with license information and disclaimer
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('<p class="footer">', unsafe_allow_html=True)
st.markdown("""
<div class="cc-license">
    <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">
        <img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png" width="88" height="31" alt="CC BY-NC">
    </a>
    <span>This work is licensed under a <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">Creative Commons Attribution-NonCommercial 4.0 International License</a>.</span>
</div>
""", unsafe_allow_html=True)

# Current year for copyright
current_year = datetime.now().year
st.markdown(f"""
<p>© {current_year} Luís Simões da Cunha</p>

<p><strong>Disclaimer:</strong> The information provided in this application is for educational purposes only and does not constitute financial advice. The author is not a financial advisor, and the content should not be considered as financial or investment advice. Options trading involves substantial risk and is not suitable for all investors. Past performance is not indicative of future results. Always consult with a qualified financial advisor before making investment decisions.</p>

<p>While efforts have been made to ensure the accuracy of the information provided, the author makes no guarantee of accuracy, completeness, or reliability. The author shall not be liable for any losses, damages, or errors resulting from the use of this information.</p>
""", unsafe_allow_html=True)
st.markdown('</p>', unsafe_allow_html=True)
        