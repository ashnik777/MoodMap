import streamlit as st
from plots import CustomPieChart
import pandas as pd
import numpy as np



def dashboard():
    st.title("Dashboard")


    # Filters block
    st.sidebar.divider()
    primary_btn = st.sidebar.button(label="Filter", type="primary")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    st.sidebar.divider()
    start_emotion = st.sidebar.selectbox("Costumer Start emotion", options=['All','Happy','Neutral','Sad','Angry'], index=0)
    end_emotion = st.sidebar.selectbox("Costumer End emotion", options=['All','Happy','Neutral','Sad','Angry'], index=0)
    st.sidebar.divider()
    satisfaction_level = st.sidebar.selectbox("Costumer satisfaction level", options=['All','(0-25)%','(25-50)%','(50-75)%','(75-100)%'], index=0)
    st.sidebar.divider()
    performance_level = st.sidebar.selectbox("Agent performance level", options=['All','(0-25)%','(25-50)%','(50-75)%','(75-100)%'], index=0)
    st.sidebar.divider()
    agent_id = st.sidebar.selectbox("Agent", options=['All','John','Arsen','David','Karen'], index=0)


    col1, col2, col3 = st.columns(3)

    col1.metric(label="Total Calls", value=50)
    col2.metric(label="Satisfied calls", value=30, delta=10)
    col3.metric(label="Not Satisfied calls", value=20, delta=-10,delta_color="inverse")

    st.divider()
    # Call count block

    chart = CustomPieChart()
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Costumers Satisfactions Levels")
        chart.create_custom_pie_chart(progress=60, hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agents Performance Rate")
        chart.create_custom_pie_chart(progress=70, hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Costumer Care")
        chart.create_custom_pie_chart(progress=60, hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

    st.divider()
    col1, col2= st.columns(2)

    with col1:
        st.caption("Share of voice emotional moments")
        tab1, tab2 = st.tabs(["Costumers", "Agents"])
        with tab1:
            chart.create_bar_chart([20,30,59,20],['Happy','Neutral','Sad','Angry'])
        with tab2:
            chart.create_bar_chart([30,40,60,10],['Happy','Neutral','Sad','Angry'])

    with col2:
        st.caption("Share of text emotional moments")
        tab1, tab2 = st.tabs(["Costumers", "Agents"])
        with tab1:
            chart.create_bar_chart([20,30,59],['Positive','Neutral','Negative'])
        with tab2:
            chart.create_bar_chart([30,40,60],['Positive','Neutral','Negative'])

    st.divider()


    col1, col2= st.columns(2)
    with col1:
        st.caption("Share of voice emotional moments based on the time")
        tab1, tab2 = st.tabs(["Costumers", "Agents"])
        with tab1:
            chart.create_grouped_bar_chart(Happy = [20,30,40],Neutral=[10,50,20],Sad=[35,25,55],Angry=[14,43,23])
        with tab2:
            chart.create_grouped_bar_chart(Happy = [10,30,50],Neutral=[60,30,25],Sad=[34,23,66],Angry=[23,12,54])

    with col2:
        st.caption("Share of text emotional moments based on the time")
        tab1, tab2 = st.tabs(["Costumers", "Agents"])
        with tab1:
            chart.create_grouped_bar_chart(Happy = [23,54,76],Neutral=[87,45,23],Sad=[34,25,55],Angry=[65,43,23])
        with tab2:
            chart.create_grouped_bar_chart(Happy = [35,34,40],Neutral=[10,56,20],Sad=[35,86,55],Angry=[14,43,23])

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Top Call Aspects")
        df = pd.read_csv('Call_topics.csv',index_col=0)
        st.write(df)
    with col2:
        st.caption("Analysis of irony across calls")
        chart.create_pie_chart_ironic_ornot(ironic_count=15,non_ironic_count=60)
    with col3:
        st.caption("Hate speech analysis across calls")
        chart.create_hate_speech_pie_chart(hateful_count = 5, targeted_count = 12, aggressive_count = 6, not_hateful = 45)
    

def individual_call():
    st.title("Individual Call")

    # Your logic for individual call display goes here
    st.write("This is the individual call page.")

def main():
    st.set_page_config(page_title='Dashboard', layout='wide')

    page = st.sidebar.selectbox("Go to", ["Dashboard", "Individual Call"])

    if page == "Dashboard":
        dashboard()
    elif page == "Individual Call":
        individual_call()

if __name__ == "__main__":
    main()
