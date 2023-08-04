import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# st.set_page_config(layout="wide", page_icon=":house_with_garden:")


def calculate_owning_scenario(home_value, mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, years, loan_term, down_payment_pct):
    mortgage_rate /= 100
    maintenance_rate /= 100
    property_tax_rate /= 100
    home_growth_rate /= 100
    down_payment = home_value * down_payment_pct
    monthly_mortgage_payment = (mortgage_rate / 12) * (home_value - down_payment) / (1 - (1 + mortgage_rate / 12) ** (-loan_term * 12))
    net_worth_owning = [down_payment]
    owning_costs = [0]
    outstanding_mortgage = home_value - down_payment
    for i in range(1, years + 1):
        annual_mortgage_payment = monthly_mortgage_payment * 12 * (1 if i <= loan_term else 0)
        annual_ownership_costs = annual_mortgage_payment + home_value * (maintenance_rate + property_tax_rate)
        owning_costs.append(annual_ownership_costs)
        outstanding_mortgage -= annual_mortgage_payment - (outstanding_mortgage * mortgage_rate)
        home_value *= (1 + home_growth_rate)
        net_worth_owning.append(home_value - outstanding_mortgage)
    owning_costs += [0] * (years - loan_term)
    return net_worth_owning, owning_costs

def calculate_renting_scenario(monthly_mortgage_payment, home_value, property_tax_rate, maintenance_rate, rent, rent_growth_rate, investment_return_rate, years, down_payment_pct):
    property_tax_rate /= 100
    maintenance_rate /= 100
    rent_growth_rate /= 100
    investment_return_rate /= 100
    renting_costs = [0]  # Initializing with 0 for year 0
    net_worth_renting = [home_value * 0.15]
    investment_fund_renting = home_value * down_payment_pct
    for i in range(1, years + 1):
        owning_total_costs = monthly_mortgage_payment * 12 + home_value * property_tax_rate + home_value * maintenance_rate
        annual_rent = rent * 12 * (1 + rent_growth_rate) ** (i - 1)
        renting_costs.append(annual_rent)
        savings = owning_total_costs - annual_rent
        investment_fund_renting += savings
        investment_fund_renting *= (1 + investment_return_rate)
        net_worth_renting.append(investment_fund_renting)
    return net_worth_renting, renting_costs

def plot_scenarios(owning_data, renting_data, loan_term):
    palette = ['#ff0000', '#ff69b4']  # Red and pink
    df = pd.DataFrame({
        'Year': list(range(loan_term + 1)),
        'Net Worth Owning': owning_data,
        'Net Worth Renting': renting_data
    })
    fig = px.line(df, x='Year', y=df.columns[1:], line_dash_sequence=['solid', 'solid'], color_discrete_map={'Net Worth Owning': palette[0], 'Net Worth Renting': palette[1]})
    fig.update_layout(
        title={"text": "Net Worth Projection", "x": 0.5, "xanchor": "center"},
        xaxis_title="Years",
        yaxis_title="Net Worth ($)",
        showlegend=True,
        yaxis_tickprefix="$",
        legend=dict(x=0.7, y=0.1, title=""),
        hovermode='x unified'
    )
    fig.update_traces(hoverinfo="x+y")
    return fig

def plot_costs(owning_costs, renting_costs, loan_term):
    palette = ['#ff0000', '#ff69b4']  # Red and pink
    df_costs = pd.DataFrame({
        'Year': list(range(loan_term + 1)),
        'Owning Costs': owning_costs,
        'Rent Costs': renting_costs
    })
    fig = px.line(df_costs, x='Year', y=df_costs.columns[1:], line_dash_sequence=['solid', 'solid'], color_discrete_map={'Owning Costs': palette[0], 'Rent Costs': palette[1]})
    fig.update_layout(
        title={"text": "Owning Costs vs Rent Costs", "x": 0.5, "xanchor": "center"},
        xaxis_title="Years",
        yaxis_title="Costs ($)",
        showlegend=True,
        margin=dict(l=20, r=20, b=20, t=20),
        yaxis_tickprefix="$",
        legend=dict(x=0.7, y=0.1, title=""),
        hovermode='x unified'
    )
    fig.update_traces(hoverinfo="x+y")
    return fig




col1, colx, col2, coly, col3 = st.columns([2,1.2,5,1,2])


with col1:
    st.markdown("<h2 style='text-align:center;'> Mortgage </h2>", unsafe_allow_html=True)
    home_value = st.number_input('Home Value', min_value=50000, max_value=1000000, value=500000, step=50000)
    home_growth_rate = st.slider('Home Growth Rate (%)', min_value=0.0, max_value=20.0, step=0.1, value=8.0)
    down_payment_pct = st.slider('Down Payement (%)', 0, 100, 15)
    mortgage_rate = st.slider('Mortgage Rate (%)', min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    loan_term_options = [15, 20, 25, 30]
    loan_term = st.selectbox('Loan Term (years)', options=loan_term_options, index=2)
    maintenance_rate = st.slider('Maintenance Rate (%)', min_value=0.0, max_value=3.0, step=0.1, value=1.0)
    property_tax_rate = st.slider('Property Tax Rate (%)', min_value=0.0, max_value=3.0, step=0.1, value=1.0)

with col3:
    st.markdown("<h2 style='text-align:center;'> Rent & Invest </h2>", unsafe_allow_html=True)
    rent = st.number_input('Monthly Rent', min_value=500, max_value=5000, value=2000, step=100)
    rent_growth_rate = st.slider('Rent Growth Rate (%)', min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    investment_return_rate = st.slider('Investment Return Rate (%)', min_value=0.0, max_value=100.0, step=0.1, value=8.0)

with col2:
    st.markdown("<h1 style='text-align:center;'>Mortgage VS. Rent & Invest </h1>", unsafe_allow_html=True)
    down_payment_pct= down_payment_pct/100
    down_payment = home_value * down_payment_pct
    mortgage_rate_percent = mortgage_rate / 100
    monthly_mortgage_payment = (mortgage_rate_percent / 12) * (home_value - down_payment) / (1 - (1 + mortgage_rate_percent / 12) ** (-loan_term * 12))
    owning_data, owning_costs = calculate_owning_scenario(home_value, mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, loan_term, loan_term, down_payment_pct)
    renting_data, renting_costs = calculate_renting_scenario(monthly_mortgage_payment, home_value, property_tax_rate, maintenance_rate, rent, rent_growth_rate, investment_return_rate, loan_term, down_payment_pct)
    if len(owning_data) != len(renting_data):
        owning_data = owning_data[:len(renting_data)]
        renting_data = renting_data[:len(owning_data)]
    fig_networth = plot_scenarios(owning_data, renting_data, loan_term)

    tab1, tab2 = st.tabs(["📈 Net Worth","🏠 Costs"])

    with tab1:
        with st.container():
            st.write("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.plotly_chart(fig_networth, config={'displaylogo': False, 'modeBarButtonsToRemove': ['toggleFullscreen']}, use_container_width=True)
            st.write("</div>", unsafe_allow_html=True)
        fig_costs = plot_costs(owning_costs, renting_costs, loan_term)

    with tab2:
        with st.container():
            st.write("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.plotly_chart(fig_costs, config={'displaylogo': False, 'modeBarButtonsToRemove': ['toggleFullscreen']}, use_container_width=True)
            st.write("</div>", unsafe_allow_html=True)