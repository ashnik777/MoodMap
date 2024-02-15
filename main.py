import streamlit as st
from plots import CustomPieChart
import pandas as pd
import numpy as np
import json
import time
import threading
import psycopg2
from sqlalchemy import create_engine

def read_data():
    with open('connection.json', 'r') as file:
        db_config = json.load(file)

    # Create a connection string
    conn_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(conn_str)
    return engine





def dashboard():
    chart = CustomPieChart()


    st.title("Dashboard")


    # Filters block
    st.sidebar.divider()
    primary_btn = st.sidebar.button(label="Filter", type="primary")


    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    
    st.sidebar.divider()
    satisfaction_level = st.sidebar.selectbox("Customer satisfaction level", options=['All','(0-25)%','(25-50)%','(50-75)%','(75-100)%'], index=0)
    #st.sidebar.divider()
    performance_level = st.sidebar.selectbox("Agent performance level", options=['All','(0-25)%','(25-50)%','(50-75)%','(75-100)%'], index=0)
    
    agent = st.sidebar.selectbox("Agent", options=['All','John','Arsen','David','Karen'], index=0)
    st.sidebar.divider()
    Topic_search = st.sidebar.text_input('Search Via Topic')

    Topic_search_button_clicked = st.sidebar.button("Search", type="primary")
    filter_dict = {}
    if primary_btn:      
        filter_dict = {'start_date':start_date,'end_date':end_date,'satisfaction_level':satisfaction_level,
                       'performance_level':performance_level,'agent':agent}
        print(filter_dict)

     # Replace this with your SQL query
    try:
        query_call = """SELECT * FROM public.call
                    WHERE starttime > '{x}' and endtime < '{y}';""".format(x=filter_dict['start_date'],y=filter_dict['end_date'])
        call_info = pd.read_sql_query(query_call, read_data())
        print(call_info)
    except:
        print('not')

    
    
    

    # ### Importing Data Frame
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Calls", value=50)
    col2.metric(label="Satisfied calls", value=30, delta=10)
    col3.metric(label="Not Satisfied calls", value=20, delta=-10,delta_color="inverse")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('## ⚠️')
    with col2:
        col2.metric(label="Alert", value=2)
    with col3:
        call_alert = pd.read_csv('alerts.csv',index_col=0)
        st.write(call_alert)
        


    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Customer Satisfaction Level")
        chart.create_custom_pie_chart(progress=60, hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agent Performance Rate")
        chart.create_custom_pie_chart(progress=81, hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Customer Care")
        chart.create_custom_pie_chart(progress=75, hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

    st.divider()
    col1, col2= st.columns(2)

    with col1:
        st.caption("Average voice emotion")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_bar_chart([20,30,59,20],['Happy','Neutral','Sad','Angry'])
        with tab2:
            chart.create_bar_chart([30,40,60,10],['Happy','Neutral','Sad','Angry'])

    with col2:
        st.caption("Average text emotion")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_bar_chart([20,30,59],['Positive','Neutral','Negative'])
        with tab2:
            chart.create_bar_chart([30,40,60],['Positive','Neutral','Negative'])


    st.divider()


    col1, col2= st.columns(2)
    with col1:
        st.caption("Share of voice emotion on timeline")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_grouped_bar_chart(Happy = [30,30,70],Neutral=[10,50,20],Sad=[35,25,55],Angry=[14,43,23])
        with tab2:
            chart.create_grouped_bar_chart(Happy = [10,30,50],Neutral=[60,30,25],Sad=[34,23,66],Angry=[23,12,54])

    with col2:
        st.caption("Share of text emotion on timeline")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_grouped_bar_chart(Happy = [23,54,76],Neutral=[87,45,23],Sad=[34,25,55],Angry=[65,43,23])
        with tab2:
            chart.create_grouped_bar_chart(Happy = [35,34,40],Neutral=[10,56,20],Sad=[35,86,55],Angry=[14,43,23])

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col3:
        with open('topics.json', 'r') as file:
            loaded_data = json.load(file)

        st.caption("Top Call Topics")
        chart.plot_top_topics(loaded_data)
        
    with col2:
        st.caption("Analysis of irony across calls")
        chart.create_pie_chart_ironic_ornot(ironic_count=30,non_ironic_count=150)
    with col1:
        st.caption("Hate speech analysis across calls")
        chart.create_hate_speech_pie_chart(hateful_count = 5, targeted_count = 12, aggressive_count = 6, Normal = 45)
    
    ################################################
    st.divider()


    st.caption("Last Calls")

    # Replace this with your SQL query
    query_call = """SELECT * FROM public.call
    ORDER BY id ASC LIMIT 100"""
    ### Importing Data Frame
    call_info = pd.read_sql_query(query_call, read_data())

    #call_info = pd.read_csv('Call_information.csv',index_col=0)
    st.write(call_info)

    ################################################
    

def individual_call():

    st.sidebar.markdown('#### Agent')
    st.sidebar.image('./Images/Ashot Nikoghosyan.JPG', caption='Ashot Nikoghosyan', width=200)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Call Report")



    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### Call ID - {}".format('13b3'))
        st.markdown("##### Call Topic - {}".format('Card Issues'))
        st.markdown("##### Aspect - {}".format('Transaction problem`  Status - Solved \u2713'))
        
        
    with col3:
        st.markdown("##### Call Duration - {} min {} seconds".format('3','24'))
        st.markdown("##### Call Datetime - {}".format('12/11/2023 23:12:05'))

    st.divider()

    chart = CustomPieChart()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Customer Satisfaction Level")
        chart.create_custom_pie_chart(progress=80, hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agent Performance Rate")
        chart.create_custom_pie_chart(progress=90, hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Customer Care")
        chart.create_custom_pie_chart(progress=85, hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

    st.divider()
    st.markdown("### MoodMap")

    # sql_query = """SELECT * FROM public.call_mood_agent
    #         ORDER BY callid ASC, starttime ASC, endtime ASC LIMIT 100"""
    # df_em = pd.read_sql_query(sql_query, read_data())
    # df_em.emotion = np.where(df_em.emotion == 'angry',1,df_em.emotion)
    # df_em.emotion = np.where(df_em.emotion == 'sad',2,df_em.emotion)
    # df_em.emotion = np.where(df_em.emotion == 'neutral',3,df_em.emotion)
    # df_em.emotion = np.where(df_em.emotion == 'happy',4,df_em.emotion)

    tab1, tab2 = st.tabs(["Customer", "Agent"])
    with tab1:
        chart.generate_emotion_plot([1,2,1,2,3,4,3,4,4])
    with tab2:
        chart.generate_emotion_plot([4,4,3,4,2,1,4,3,2,4,4,4])

    st.divider()

    st.markdown("### Text Emotion")
    tab1, tab2 = st.tabs(["Customer", "Agent"])
    with tab1:
        chart.generate_text_emotion_plot([1,2,1,2,3,3,3])
    with tab2:
        chart.generate_text_emotion_plot([3,2,1,2,3,3,3,3,2,1,1,3])
    

        
def login():

    st.image('./Images/logo.png')#width=200)

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Replace this section with your actual authentication logic
        if username == 'moodmap' and password == 'moodmap':
            st.success('Logged in successfully!')
            st.session_state.is_logged_in = True
            st.experimental_rerun()
        else:
            st.error('Incorrect username or password')

def main():
    st.set_page_config( 
        page_title='MoodMap.ai', 
        layout='wide'
    )


    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False



    if not st.session_state.is_logged_in:
        login()
    else:
        page = st.sidebar.selectbox("Go to", ["Dashboard", "Individual Call"])

        if page == "Dashboard":
            dashboard()
    
        if page == "Individual Call":
            st.sidebar.divider()
            call_id = st.sidebar.text_input('Call ID')
            search_button_clicked = st.sidebar.button("Search", type="primary")

            

            if search_button_clicked and call_id == '13b3':
                individual_call()
        

if __name__ == "__main__":
    main()