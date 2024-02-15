import streamlit as st
from plots import CustomPieChart
import pandas as pd
import numpy as np
import json
import time
import threading
import psycopg2
from sqlalchemy import create_engine
import re

def read_data():
    with open('connection.json', 'r') as file:
        db_config = json.load(file)

    # Create a connection string
    conn_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(conn_str)
    return engine

def get_data_info(alert_calls,start_date,end_date,satisfaction_level,performance_level):

    if satisfaction_level == 'All':
        satisfaction_level = [0,100]
    else:
        satisfaction_level = [int(num) for num in re.findall(r'\d+', satisfaction_level)]

    if performance_level == 'All':
        performance_level = [0,100]
    else:
        performance_level = [int(num) for num in re.findall(r'\d+', performance_level)]

    if alert_calls == 'Alerting Calls':
        # Replace this with your SQL query
        query_call_info = """SELECT * FROM public.callinfo
                         WHERE customer_satisfaction_rate  > {c_s_0} and customer_satisfaction_rate < {c_s_1} and alert =1;""".format(c_s_0=satisfaction_level[0],c_s_1=satisfaction_level[1])
    else:
        # Replace this with your SQL query
        query_call_info = """SELECT * FROM public.callinfo
                         WHERE customer_satisfaction_rate  > {c_s_0} and customer_satisfaction_rate < {c_s_1};""".format(c_s_0=satisfaction_level[0],c_s_1=satisfaction_level[1])


    
    # Replace this with your SQL query
    query_call = """SELECT * FROM public.call
                            WHERE starttime > '{s_d}' and endtime < '{e_d}';""".format(s_d=start_date,e_d=end_date)

    # # Replace this with your SQL query
    # query_call_info = """SELECT * FROM public.callinfo
    #                      WHERE customer_satisfaction_rate  > {c_s_0} and customer_satisfaction_rate < {c_s_1};""".format(c_s_0=satisfaction_level[0],c_s_1=satisfaction_level[1])

    df_call = pd.read_sql_query(query_call, read_data())
    df_call_info = pd.read_sql_query(query_call_info, read_data())

    df = pd.merge(df_call,df_call_info,how='inner',on='callid')

    # Replace this with your SQL query
    query_clint_voice_emotion = """
                        SELECT * FROM public.call_sentence_client
                        WHERE callid IN {}
                            """.format(tuple(df.callid))
    

    clint_voice_emotion = pd.read_sql_query(query_clint_voice_emotion, read_data())

    # Replace this with your SQL query
    query_agent_voice_emotion = """
                        SELECT * FROM public.call_sentence_agent
                        WHERE callid IN {}
                            """.format(tuple(df.callid))
    
    print(query_agent_voice_emotion)
    agent_voice_emotion = pd.read_sql_query(query_agent_voice_emotion, read_data())

    # Replace this with your SQL query
    query_clint_text_emotion = """
                        SELECT * FROM public.call_sentence_client
                        WHERE callid IN {}
                            """.format(tuple(df.callid))

    clint_text_emotion = pd.read_sql_query(query_clint_text_emotion, read_data())

    # Replace this with your SQL query
    query_agent_text_emotion = """
                        SELECT * FROM public.call_sentence_agent
                        WHERE callid IN {}
                            """.format(tuple(df.callid))

    agent_text_emotion = pd.read_sql_query(query_agent_text_emotion, read_data())

       # Extract emotions and counts
    voice_emotions_clinet = pd.DataFrame(clint_voice_emotion.meanemotion.value_counts()).reset_index()['meanemotion'].tolist()
    voice_counts_client = pd.DataFrame(clint_voice_emotion.meanemotion.value_counts()).reset_index()['count'].tolist()


    # Extract emotions and counts
    voice_emotions_agent = pd.DataFrame(agent_voice_emotion.meanemotion.value_counts()).reset_index()['meanemotion'].tolist()
    voice_counts_agent = pd.DataFrame(agent_voice_emotion.meanemotion.value_counts()).reset_index()['count'].tolist()

    # Extract emotions and counts
    text_emotions_clinet = pd.DataFrame(clint_text_emotion.sentiment.value_counts()).reset_index()['sentiment'].tolist()
    text_counts_client = pd.DataFrame(clint_text_emotion.sentiment.value_counts()).reset_index()['count'].tolist()

    # Extract emotions and counts
    text_emotions_agent = pd.DataFrame(agent_text_emotion.sentiment.value_counts()).reset_index()['sentiment'].tolist()
    text_counts_agent = pd.DataFrame(agent_text_emotion.sentiment.value_counts()).reset_index()['count'].tolist()

    tatal_calls = len(df)
    alerts = df.alert.value_counts()[1]
    customer_sat_level = int(df.customer_satisfaction_rate.mean())
    agent_perf_rate = int(df.agent_performance_rate.mean())
    costumer_care = int(df.callscore.mean())
    call_topics = df[['topic']]
    ironic_count = np.where(df.ironypercent > 30,1,0).sum()
    not_ironic_count = (1 - np.where(df.ironypercent > 30,1,0)).sum()
    hateful_count = np.where(df.hatespeechpercent > 30,1,0).sum()
    not_hateful_count = (1 - np.where(df.hatespeechpercent > 30,1,0)).sum()
    satisfied = df.satisfied.value_counts()[0]
    not_satisfied = df.satisfied.value_counts()[1]

    metrics_dict = {
                        'df':df,
                        'voice_emotions_clinet':voice_emotions_clinet,
                        'voice_counts_client':voice_counts_client,
                        'voice_emotions_agent':voice_emotions_agent,
                        'voice_counts_agent':voice_counts_agent,
                        'text_emotions_clinet':text_emotions_clinet,
                        'text_counts_client':text_counts_client,
                        'text_emotions_agent':text_emotions_agent,
                        'text_counts_agent':text_counts_agent,
                        'tatal_calls':tatal_calls,
                        'alerts':alerts,
                        'customer_sat_level':customer_sat_level,
                        'agent_perf_rate':agent_perf_rate,
                        'costumer_care':costumer_care,
                        'call_topics':call_topics,
                        'ironic_count':ironic_count,
                        'not_ironic_count':not_ironic_count,
                        'hateful_count':hateful_count,
                        'not_hateful_count':not_hateful_count,
                        'satisfied':satisfied,
                        'not_satisfied':not_satisfied
    }

    return metrics_dict

def get_ind_data(call_id):
    query_call_info = """SELECT * FROM public.callinfo
                         where callid = {}""".format(call_id)
    query_call = """SELECT * FROM public.call
                         where callid = {}""".format(call_id)

    df_call_info = pd.read_sql_query(query_call_info, read_data())
    df_call = pd.read_sql_query(query_call, read_data())

    df = pd.merge(df_call,df_call_info,how='left',on='callid')

    # Replace this with your SQL query
    query_clint_text_emotion = """
                        SELECT * FROM public.call_mood_agent
                        WHERE callid = {}
                            """.format(call_id)
    clint_text_emotion = pd.read_sql_query(query_clint_text_emotion, read_data())
    # Replace this with your SQL query
    query_agent_text_emotion = """
                        SELECT * FROM public.call_mood_agent
                        WHERE callid = {}
                            """.format(call_id)
    agent_text_emotion = pd.read_sql_query(query_agent_text_emotion, read_data())

    call_id
    topic = df.topic[0]
    duration = df.duration[0]
    datetime = df.starttime[0]
    customer_satisfaction_rate = df.customer_satisfaction_rate[0]
    agent_performance_rate = df.agent_performance_rate[0]
    callscore = df.callscore[0]
    emotion_client = list(clint_text_emotion.emotion_in_numbers)[::-1]
    emotion_agent = list(agent_text_emotion.emotion_in_numbers)

    dict_met = {'call_id':call_id,'topic':topic,'duration':duration,'datetime':datetime,
                'customer_satisfaction_rate':customer_satisfaction_rate,'agent_performance_rate':agent_performance_rate,
                'callscore':callscore,'emotion_client':emotion_client,'emotion_agent':emotion_agent}
    return dict_met

################################

def dashboard(metrics_dict):


    chart = CustomPieChart()

    st.title("Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Calls", value=metrics_dict['tatal_calls'])
    col2.metric(label="Satisfied calls", value=metrics_dict['satisfied'], delta=10)
    col3.metric(label="Not Satisfied calls", value=metrics_dict['not_satisfied'], delta=-10,delta_color="inverse")
    st.divider()
    
    col1, col2 = st.columns(2) #, col3 = st.columns(3)
    with col1:
        st.markdown('## ⚠️')
    with col2:
        col2.metric(label="Alert", value=metrics_dict['alerts'])
    # with col3:
    #     call_alert = pd.read_csv('alerts.csv',index_col=0)
    #     st.write(call_alert)
        


    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Customer Satisfaction Level")
        chart.create_custom_pie_chart(progress=metrics_dict['customer_sat_level'], hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agent Performance Rate")
        chart.create_custom_pie_chart(progress=metrics_dict['agent_perf_rate'], hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Customer Care")
        chart.create_custom_pie_chart(progress=metrics_dict['costumer_care'], hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

    st.divider()
    col1, col2= st.columns(2)

    with col1:
        st.caption("Average voice emotion")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_bar_chart(metrics_dict['voice_counts_client'],metrics_dict['voice_emotions_clinet'])
        with tab2:
            chart.create_bar_chart(metrics_dict['voice_counts_agent'],metrics_dict['voice_emotions_agent'])

    with col2:
        st.caption("Average text emotion")
        tab1, tab2 = st.tabs(["Customers", "Agents"])
        with tab1:
            chart.create_bar_chart(metrics_dict['text_counts_client'],metrics_dict['text_emotions_clinet'])
        with tab2:
            chart.create_bar_chart(metrics_dict['text_counts_agent'],metrics_dict['text_emotions_agent'])


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
        # with open('topics.json', 'r') as file:
        #     loaded_data = json.load(file)

        st.caption("Top Call Topics")
        chart.plot_top_topics(metrics_dict['call_topics'])
        
    with col2:
        st.caption("Analysis of irony across calls")
        chart.create_pie_chart_ironic_ornot(ironic_count=metrics_dict['ironic_count'],non_ironic_count=metrics_dict['not_ironic_count'])
    with col1:
        st.caption("Hate speech analysis across calls")
        chart.create_hate_speech_pie_chart(hateful_count = metrics_dict['hateful_count'], not_hateful_count = metrics_dict['not_hateful_count'])
    ################################################
    st.divider()


    st.caption("Last Calls")

    st.write(metrics_dict['df'])

    ################################################
    

def individual_call(ind_metrics_dict):

    # st.sidebar.markdown('#### Agent')
    # st.sidebar.image('./Images/Ashot Nikoghosyan.JPG', caption='Ashot Nikoghosyan', width=200)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Call Report")



    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### Call ID - {}".format(ind_metrics_dict['call_id']))
        st.markdown("##### Call Topic - {}".format(ind_metrics_dict['topic']))
        st.markdown("##### Aspect - {}".format('Transaction problem`  Status - Solved \u2713'))
        
        
    with col3:
        st.markdown("##### Call Duration -  {} seconds".format(ind_metrics_dict['duration']))
        st.markdown("##### Call Datetime - {}".format(ind_metrics_dict['datetime']))

    st.divider()

    chart = CustomPieChart()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Customer Satisfaction Level")
        chart.create_custom_pie_chart(progress=ind_metrics_dict['customer_satisfaction_rate'], hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agent Performance Rate")
        chart.create_custom_pie_chart(progress=ind_metrics_dict['agent_performance_rate'], hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Customer Care")
        chart.create_custom_pie_chart(progress=ind_metrics_dict['callscore'], hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

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
        chart.generate_emotion_plot(ind_metrics_dict['emotion_client'])
    with tab2:
        chart.generate_emotion_plot(ind_metrics_dict['emotion_agent'])

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

            st.sidebar.divider()
            alert_calls = st.sidebar.selectbox("## Select Allerting Calls ⚠️", options=['All','Alerting Calls'], index=0)
            
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
            # filter_dict = {}
            if primary_btn:      
                filter_dict = {'alert_calls':alert_calls,'start_date':start_date,'end_date':end_date,'satisfaction_level':satisfaction_level,
                               'performance_level':performance_level,'agent':agent}

                # metrics_dict = get_data_info(filter_dict['alert_calls'],filter_dict['start_date'],filter_dict['end_date'],filter_dict['satisfaction_level'],filter_dict['performance_level'])
                # dashboard(metrics_dict)
                try:
                    metrics_dict = get_data_info(filter_dict['alert_calls'],filter_dict['start_date'],filter_dict['end_date'],filter_dict['satisfaction_level'],filter_dict['performance_level'])
                    dashboard(metrics_dict)
                except:
                    print('not')
            
        



        if page == "Individual Call":
            st.sidebar.divider()
            call_id = st.sidebar.text_input('Call ID')
            search_button_clicked = st.sidebar.button("Search", type="primary")

            

            if search_button_clicked:
                # ind_metrics_dict = get_ind_data(call_id)
                # individual_call(ind_metrics_dict)
                try:
                    ind_metrics_dict = get_ind_data(call_id)
                    individual_call(ind_metrics_dict)
                except:
                    print('no')
        

if __name__ == "__main__":
    main()