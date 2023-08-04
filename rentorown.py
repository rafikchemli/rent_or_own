import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center;'>Mortgage VS. Rent & Invest </h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'> What's Your Move? </h4>", unsafe_allow_html=True)

def convert_rates_to_decimal(*rates):
    return [rate / 100 for rate in rates]

def calculate_scenarios(home_value, mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, rent, rent_growth_rate, investment_return_rate, years, loan_term, down_payment_pct):
    years = loan_term
    down_payment = home_value * down_payment_pct
    monthly_payment_factor = mortgage_rate / 12
    monthly_mortgage_payment = monthly_payment_factor * (home_value - down_payment) / (1 - (1 + monthly_payment_factor) ** (-loan_term * 12))

    owning_costs = [0]
    net_worth_owning = [down_payment]
    outstanding_mortgage = home_value - down_payment

    renting_costs = [0]
    net_worth_renting = [home_value * down_payment_pct]
    investment_fund_renting = home_value * down_payment_pct

    for i in range(1, years + 1):
        annual_mortgage_payment = monthly_mortgage_payment * 12 * (1 if i <= loan_term else 0)
        outstanding_mortgage -= annual_mortgage_payment - (outstanding_mortgage * mortgage_rate)
        annual_ownership_costs = annual_mortgage_payment + (home_value - outstanding_mortgage) * (maintenance_rate + property_tax_rate)
        owning_costs.append(annual_ownership_costs)
        home_value *= (1 + home_growth_rate)
        net_worth_owning.append(home_value - outstanding_mortgage)

        annual_rent = rent * 12 * (1 + rent_growth_rate) ** (i - 1)
        renting_costs.append(annual_rent)
        owning_total_costs = annual_ownership_costs
        savings = owning_total_costs - annual_rent
        investment_fund_renting += savings
        investment_fund_renting *= (1 + investment_return_rate)
        net_worth_renting.append(investment_fund_renting)

    owning_costs += [0] * (years - loan_term)

    return (net_worth_owning, owning_costs), (net_worth_renting, renting_costs)


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



col1, colx, col2, coly, col3 = st.columns([2,0.5,5,0.5,2])


with col1:
    st.markdown("<h4 style='text-align:center;'> Mortgage </h4>", unsafe_allow_html=True)
    home_value = st.number_input('Home Value', min_value=1, max_value=1000000000, value=500000, step=50000)
    home_growth_rate = st.slider('Home Growth Rate (%)', min_value=0.0, max_value=20.0, step=0.1, value=5.0)
    down_payment_pct = st.slider('Down Payement (%)', 0, 100, 15)
    mortgage_rate = st.slider('Mortgage Rate (%)', min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    
    with st.expander("Advanced Options", expanded=False):
        loan_term_options = [15, 20, 25, 30]
        loan_term = st.selectbox('Loan Term (years)', options=loan_term_options, index=2)
        maintenance_rate = st.slider('Maintenance Rate (%)', min_value=0.0, max_value=3.0, step=0.1, value=1.0)
        property_tax_rate = st.slider('Property Tax Rate (%)', min_value=0.0, max_value=3.0, step=0.1, value=1.25)

with col3:
    st.markdown("<h4 style='text-align:center;'> Rent & Invest </h4>", unsafe_allow_html=True)
    rent = st.number_input('Monthly Rent', min_value=1, max_value=1000000, value=2000, step=100)
    rent_growth_rate = st.slider('Rent Growth Rate (%)', min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    investment_return_rate = st.slider('Investment Return Rate (%)', min_value=0.0, max_value=100.0, step=0.1, value=8.0)
    st.markdown(""" """)
    st.markdown("""
        <div style='background-color: #1111; padding: 20px; border-radius: 10px; text-align: justify;'>
            The decision between putting your money into a mortgage or renting and investing the rest is multifaceted. This dashboard is designed to make that decision clearer by providing a transparent, side-by-side comparison of both options.
        </div>
        """, unsafe_allow_html=True)
    
with col2:
    mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, rent_growth_rate, investment_return_rate, down_payment_pct = convert_rates_to_decimal(
        mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, rent_growth_rate, investment_return_rate, down_payment_pct
    )

    down_payment = home_value * down_payment_pct
    monthly_payment_factor = mortgage_rate / 12
    monthly_mortgage_payment = monthly_payment_factor * (home_value - down_payment) / (1 - (1 + monthly_payment_factor) ** (-loan_term * 12))
    
    (owning_data, owning_costs), (renting_data, renting_costs) = calculate_scenarios(
        home_value, mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, rent, rent_growth_rate, investment_return_rate, loan_term, loan_term, down_payment_pct
    )

    # Ensure owning_data and renting_data have the same length
    min_length = min(len(owning_data), len(renting_data))
    owning_data = owning_data[:min_length]
    renting_data = renting_data[:min_length]

    fig_networth = plot_scenarios(owning_data, renting_data, loan_term)

    tab1, tab2, tab3, tab4= st.tabs(["📈 Net Worth", "🏠 Costs", "💻 Code", " Other"])

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
    with tab3:
        with st.container():
            st.code("""
                        def calculate_scenarios(home_value, mortgage_rate, maintenance_rate, property_tax_rate, home_growth_rate, rent, rent_growth_rate, investment_return_rate, years, loan_term, down_payment_pct):
                            # Initial setup for owning
                            down_payment = home_value * down_payment_pct
                            monthly_payment_factor = mortgage_rate / 12
                            monthly_mortgage_payment = monthly_payment_factor * (home_value - down_payment) / (1 - (1 + monthly_payment_factor) ** (-loan_term * 12))
                            owning_costs = [0]
                            net_worth_owning = [down_payment]
                            outstanding_mortgage = home_value - down_payment

                            # Initial setup for renting
                            renting_costs = [0]
                            net_worth_renting = [home_value * down_payment_pct]
                            investment_fund_renting = home_value * down_payment_pct

                            # Calculations for each year
                            for i in range(1, years + 1):
                                # Owning calculations
                                annual_mortgage_payment = monthly_mortgage_payment * 12 * (1 if i <= loan_term else 0)
                                outstanding_mortgage -= annual_mortgage_payment - (outstanding_mortgage * mortgage_rate)
                                annual_ownership_costs = annual_mortgage_payment + (home_value - outstanding_mortgage) * (maintenance_rate + property_tax_rate)
                                owning_costs.append(annual_ownership_costs)
                                home_value *= (1 + home_growth_rate)
                                net_worth_owning.append(home_value - outstanding_mortgage)

                                # Renting calculations
                                annual_rent = rent * 12 * (1 + rent_growth_rate) ** (i - 1)
                                renting_costs.append(annual_rent)
                                savings = annual_ownership_costs - annual_rent
                                investment_fund_renting += savings
                                investment_fund_renting *= (1 + investment_return_rate)
                                net_worth_renting.append(investment_fund_renting)

                            return (net_worth_owning, owning_costs), (net_worth_renting, renting_costs)
                        """)
    with tab4:
        with st.container():

            st.markdown("""
            <div style="text-align: justify;">
            When considering the decision between owning a home or renting and investing, 
            it's essential to look beyond just the financial numbers. Here's a comparison 
            of the unique intangible aspects that may influence your choice:
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            # Owning a Home
            with col1:
                st.markdown("### Owning a Home")
                st.markdown("- Full control and creative freedom over property.")
                st.markdown("- Access to financial tools like HELOCs, home equity loans, and refinancing.")
                st.markdown("- Potential for home value appreciation through improvements and market growth.")
                st.markdown("- Opportunity for potential tax deductions related to mortgage interest and improvements.")
                st.markdown("- Building equity in the property.")

            # Renting & Investing
            with col2:
                st.markdown("### Renting & Investing")
                st.markdown("- Flexibility to move, making it easy to adapt to lifestyle changes.")
                st.markdown("- Limited control over property, with no commitment to maintenance.")
                st.markdown("- Opportunity to invest in diverse assets, not tied to real estate.")
                st.markdown("- Low responsibility for property maintenance, freeing up time and resources.")
                st.markdown("- Frees up capital that might otherwise be tied to a mortgage, allowing for greater investment opportunities.")

                        

            


## By DashDesigndev.inc