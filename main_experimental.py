import streamlit as st
from plots import CustomPieChart
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import json
import time
import threading
import psycopg2
import re
import difflib



def add_spaces(lst):
    modified_list = []
    for item in lst:
        modified_list.append(item.ljust(len(item) + 3))
    return modified_list


def read_data():
    with open('connection.json', 'r') as file:
        db_config = json.load(file)

    # Create a connection string
    conn_str = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(conn_str)
    return engine

def get_agents_data():
    query = """SELECT * FROM public.agent"""
    agents = pd.read_sql_query(query, read_data())
    return agents

def get_data_info(alert_calls,start_date,end_date,satisfaction_level,performance_level,agent,Topic_search):

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
                         WHERE customer_satisfaction_rate  > {c_s_0} and customer_satisfaction_rate < {c_s_1} 
                         and agent_performance_rate > {a_p_0} and agent_performance_rate < {a_p_1} and alert = True;""".format(c_s_0=satisfaction_level[0],c_s_1=satisfaction_level[1],a_p_0=performance_level[0],a_p_1=performance_level[1])
    else:
        # Replace this with your SQL query
        query_call_info = """SELECT * FROM public.callinfo
                         WHERE customer_satisfaction_rate  > {c_s_0} and customer_satisfaction_rate < {c_s_1} 
                         and agent_performance_rate > {a_p_0} and agent_performance_rate < {a_p_1};""".format(c_s_0=satisfaction_level[0],c_s_1=satisfaction_level[1],a_p_0=performance_level[0],a_p_1=performance_level[1])


    
    # Replace this with your SQL query
    query_call = """SELECT * FROM public.call
                            WHERE starttime > '{s_d}' and endtime < '{e_d}';""".format(s_d=start_date,e_d=end_date)

    

    
    df_call = pd.read_sql_query(query_call, read_data())
    df_call_info = pd.read_sql_query(query_call_info, read_data())
    df_call.rename(columns={'id':'callid'},inplace=True)

    df = pd.merge(df_call,df_call_info,how='inner',on='callid')

    if Topic_search != '':
        df = df[df.topic.isin(difflib.get_close_matches(Topic_search,df.topic,cutoff=0.6))]
    


    if agent != 'All':
        id = get_agents_data()[get_agents_data().username == agent].id[0]
        df = df[df.agentid == id]

        

    if len(df.callid) >= 2:
        # Replace this with your SQL query
        query_clint_voice_emotion = """
                            SELECT * FROM public.call_sentence_client
                            WHERE callid IN {}
                                """.format(tuple(df.callid))
        
        # Replace this with your SQL query
        query_agent_voice_emotion = """
                        SELECT * FROM public.call_sentence_agent
                        WHERE callid IN {}
                                """.format(tuple(df.callid))
        
    else:
        query_clint_voice_emotion = """
                            SELECT * FROM public.call_sentence_client
                            WHERE callid = {}
                                """.format(df.callid.values[0])
        
        query_agent_voice_emotion = """
                        SELECT * FROM public.call_sentence_agent
                        WHERE callid = {}
                                """.format(df.callid.values[0])
        
    
   
    clint_voice_emotion = pd.read_sql_query(query_clint_voice_emotion, read_data())

    
    
    agent_voice_emotion = pd.read_sql_query(query_agent_voice_emotion, read_data())

    

    clint_text_emotion = pd.read_sql_query(query_clint_voice_emotion, read_data())

    # Replace this with your SQL query
    

    agent_text_emotion = pd.read_sql_query(query_clint_voice_emotion, read_data())

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
    alerts = (df.alert == True).sum()
    
    customer_sat_level = int(df.customer_satisfaction_rate.mean())
    agent_perf_rate = int(df.agent_performance_rate.mean())
    costumer_care = int(df.callscore.mean())
    call_topics = df[['topic']]

    client_ironic_count = np.where(df.client_ironypercent > 30,1,0).sum()
    agent_ironic_count = np.where(df.agent_ironypercent > 30,1,0).sum()
    client_not_ironic_count = (1 - np.where(df.client_ironypercent > 30,1,0)).sum()
    agent_not_ironic_count = (1 - np.where(df.agent_ironypercent > 30,1,0)).sum()

    client_hateful_count = np.where(df.client_hatespeechpercent > 30,1,0).sum()
    agent_hateful_count = np.where(df.agent_hatespeechpercent > 30,1,0).sum()
    client_not_hateful_count = (1 - np.where(df.client_hatespeechpercent > 30,1,0)).sum()
    agent_not_hateful_count = (1 - np.where(df.agent_hatespeechpercent > 30,1,0)).sum()
    satisfied = np.where(df.customer_satisfaction_rate > 75, 1,0).sum()
    not_satisfied = np.where(df.customer_satisfaction_rate <= 75, 1,0).sum()

    customer_sat_list = list(df.customer_satisfaction_rate)
    agent_perf_list = list(df.agent_performance_rate)
    customer_care_list = list(df.callscore)
    call_topics_list = list(df.topic)

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
                        'client_ironic_count':client_ironic_count,
                        'agent_ironic_count':agent_ironic_count,
                        'client_not_ironic_count':client_not_ironic_count,
                        'agent_not_ironic_count':agent_not_ironic_count,
                        'client_hateful_count':client_hateful_count,
                        'agent_hateful_count':agent_hateful_count,
                        'client_not_hateful_count':client_not_hateful_count,
                        'agent_not_hateful_count':agent_not_hateful_count,
                        'satisfied':satisfied,
                        'not_satisfied':not_satisfied,

                        'customer_sat_list':customer_sat_list,
                        'agent_perf_list':agent_perf_list,
                        'customer_care_list':customer_care_list,
                        'call_topics_list':call_topics_list,
    }

    return metrics_dict

def get_ind_data(call_id):

    query_call_info = """SELECT * FROM public.callinfo
                         where callid = {}""".format(call_id)
    query_call = """SELECT * FROM public.call
                         where id = {}""".format(call_id)

    df_call_info = pd.read_sql_query(query_call_info, read_data())
    df_call = pd.read_sql_query(query_call, read_data())

    df_call.rename(columns={'id':'callid'},inplace=True)
    df = pd.merge(df_call,df_call_info,how='left',on='callid')

    ###Get agent Name
    query_agents = """
                        SELECT * FROM public.agent
                        WHERE id = {}
                            """.format(df_call.agentid.values[0])
    
    agent_df = pd.read_sql_query(query_agents, read_data())
    agent = agent_df.username.values[0]

    ####  Voice Emotion
    # Replace this with your SQL query
    query_client_voice_emotion = """
                        SELECT * FROM public.call_mood_client
                        WHERE callid = {}
                            """.format(call_id)
    client_voice_emotion = pd.read_sql_query(query_client_voice_emotion, read_data())
    # Replace this with your SQL query
    query_agent_voice_emotion = """
                        SELECT * FROM public.call_mood_agent
                        WHERE callid = {}
                            """.format(call_id)
    agent_voice_emotion = pd.read_sql_query(query_agent_voice_emotion, read_data())

    ### Text emotion
    query_client_text_emotion = """ SELECT * FROM public.call_sentence_client """
    client_text_emotion = pd.read_sql_query(query_client_text_emotion, read_data())

    query_agent_text_emotion = """ SELECT * FROM public.call_sentence_agent """
    agent_text_emotion = pd.read_sql_query(query_agent_text_emotion, read_data())

    
    topic = df.topic[0]
    duration = df.duration[0]
    datetime = df.starttime[0]
    customer_satisfaction_rate = df.customer_satisfaction_rate[0]
    agent_performance_rate = df.agent_performance_rate[0]
    callscore = df.callscore[0]

    agentinterrupts = df.agentinterrupts[0]
    clientinterrupts = df.clientinterrupts[0]
    togetherspeak = df.togetherspokentime[0]


    ## Voice Emotions
    client_voice_emotion.emotion = np.where(client_voice_emotion.emotion == 'Angry',1,client_voice_emotion.emotion)
    client_voice_emotion.emotion = np.where(client_voice_emotion.emotion == 'Sad',2,client_voice_emotion.emotion)
    client_voice_emotion.emotion = np.where(client_voice_emotion.emotion == 'Neutral',3,client_voice_emotion.emotion)
    client_voice_emotion.emotion = np.where(client_voice_emotion.emotion == 'Happy',4,client_voice_emotion.emotion)
    emotion_client = list(client_voice_emotion.emotion)
    
    agent_voice_emotion.emotion = np.where(agent_voice_emotion.emotion == 'Angry',1,agent_voice_emotion.emotion)
    agent_voice_emotion.emotion = np.where(agent_voice_emotion.emotion == 'Sad',2,agent_voice_emotion.emotion)
    agent_voice_emotion.emotion = np.where(agent_voice_emotion.emotion == 'Neutral',3,agent_voice_emotion.emotion)
    agent_voice_emotion.emotion = np.where(agent_voice_emotion.emotion == 'Happy',4,agent_voice_emotion.emotion)
    emotion_agent = list(agent_voice_emotion.emotion)


    ## Text Emotions
    client_text_emotion.sentiment = np.where(client_text_emotion.sentiment == 'Negative',1,client_text_emotion.sentiment)
    client_text_emotion.sentiment = np.where(client_text_emotion.sentiment == 'Neutral',2,client_text_emotion.sentiment)
    client_text_emotion.sentiment = np.where(client_text_emotion.sentiment == 'Positive',3,client_text_emotion.sentiment)
    text_emotion_client = list(client_text_emotion.sentiment)

    agent_text_emotion.sentiment = np.where(agent_text_emotion.sentiment == 'Negative',1,agent_text_emotion.sentiment)
    agent_text_emotion.sentiment = np.where(agent_text_emotion.sentiment == 'Neutral',2,agent_text_emotion.sentiment)
    agent_text_emotion.sentiment = np.where(agent_text_emotion.sentiment == 'Positive',3,agent_text_emotion.sentiment)
    text_emotion_agent = list(agent_text_emotion.sentiment)

    if customer_satisfaction_rate > 75:
        satisfaction = 1
    else:
        satisfaction = 0

    client_ironypercent = df.client_ironypercent[0]
    agent_ironypercent = df.agent_ironypercent[0]
    client_hatepercent = df.client_hatespeechpercent[0]
    agent_hatepercent = df.agent_hatespeechpercent[0]

    silence = df.silencepercent[0]

    dict_met = {'call_id':call_id,
                'topic':topic,
                'duration':duration,
                'datetime':datetime,
                'customer_satisfaction_rate':customer_satisfaction_rate,
                'agent_performance_rate':agent_performance_rate,
                'callscore':callscore,
                'emotion_client':emotion_client,
                'emotion_agent':emotion_agent,
                'satisfaction':satisfaction,
                'client_ironypercent':client_ironypercent,
                'agent_ironypercent':agent_ironypercent,
                'client_hatepercent':client_hatepercent,
                'agent_hatepercent':agent_hatepercent,
                'silence':silence,
                'text_emotion_client':text_emotion_client,
                'text_emotion_agent':text_emotion_agent,
                'agent':agent,
                'agentinterrupts':agentinterrupts,
                'clientinterrupts':clientinterrupts,
                'togetherspeak':togetherspeak}
    
    return dict_met

################################

def dashboard(metrics_dict):




    chart = CustomPieChart()

    st.title("Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Calls", value=metrics_dict['tatal_calls'])
    col2.metric(label="Satisfied calls", value=metrics_dict['satisfied'])
    col3.metric(label="Not Satisfied calls", value=metrics_dict['not_satisfied'])
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

    data_topic = {'call_topic': add_spaces(metrics_dict['call_topics_list']),
        'agent_performance_rate': metrics_dict['agent_perf_list'],
        'customer_performance_rate': metrics_dict['customer_sat_list'],
        'call_score': metrics_dict['customer_care_list']}

    
    chart.plot_top_performances(pd.DataFrame(data_topic))

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

    tab1, tab2 = st.tabs(["Customers", "Agents"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col3:
            st.caption("Top Call Topics")
            chart.plot_top_topics(metrics_dict['call_topics'])
        with col2:
            st.caption("Analysis of irony across calls")
            chart.create_pie_chart_ironic_ornot(ironic_count=metrics_dict['client_ironic_count'],non_ironic_count=metrics_dict['client_not_ironic_count'])
        with col1:
            st.caption("Hate speech analysis across calls")
            chart.create_hate_speech_pie_chart(hateful_count = metrics_dict['client_hateful_count'], not_hateful_count = metrics_dict['client_not_hateful_count'])
    ################################################
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col3:
            st.caption("Top Call Topics")
            chart.plot_top_topics(metrics_dict['call_topics'])
        with col2:
            st.caption("Analysis of irony across calls")
            chart.create_pie_chart_ironic_ornot(ironic_count=metrics_dict['agent_ironic_count'],non_ironic_count=metrics_dict['agent_not_ironic_count'])
        with col1:
            st.caption("Hate speech analysis across calls")
            chart.create_hate_speech_pie_chart(hateful_count = metrics_dict['agent_hateful_count'], not_hateful_count = metrics_dict['agent_not_hateful_count'])
    ################################################
    st.divider()


    st.caption("Last Calls")

    st.write(metrics_dict['df'])

    ################################################
    

def individual_call(ind_metrics_dict):

    # st.sidebar.markdown('#### Agent')
    # st.sidebar.image('./Images/Ashot Nikoghosyan.JPG', caption='Ashot Nikoghosyan', width=200)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("Call Report")

    
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### Call ID - {}".format(ind_metrics_dict['call_id']))
        st.markdown("##### Call Topic - {}".format(ind_metrics_dict['topic']))
        if ind_metrics_dict['satisfaction']:
            st.markdown("##### Status - {}".format('Satisfied \u2713'))
        else:
            st.markdown("##### Status - {}".format('Not Satisfied \u274c'))
        
        
    with col3:
        st.markdown("##### Call Duration -  {} seconds".format(ind_metrics_dict['duration']))
        st.markdown("##### Call Datetime - {}".format(ind_metrics_dict['datetime']))
        st.markdown("##### Agent Name - {}".format(ind_metrics_dict['agent']))

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

   

    tab1, tab2 = st.tabs(["Customer", "Agent"])
    with tab1:
        chart.generate_emotion_plot(ind_metrics_dict['emotion_client'])
    with tab2:
        chart.generate_emotion_plot(ind_metrics_dict['emotion_agent'])

    st.divider()

    st.markdown("### Text Emotion")
    tab1, tab2 = st.tabs(["Customer", "Agent"])
    with tab1:
        chart.generate_text_emotion_plot(ind_metrics_dict['text_emotion_client'])
    with tab2:
        chart.generate_text_emotion_plot(ind_metrics_dict['text_emotion_agent'])

    st.divider()

    tab1, tab2 = st.tabs(["Customer", "Agent"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Hate speech percent")
            chart.create_hate_speech_pie_chart(hateful_count = ind_metrics_dict['client_hatepercent'], not_hateful_count = (100-ind_metrics_dict['client_hatepercent']))
        with col2:
            st.caption("Irony speech percent")
            chart.create_pie_chart_ironic_ornot(ironic_count=ind_metrics_dict['client_ironypercent'],non_ironic_count=(100-ind_metrics_dict['client_ironypercent']))
        with col3:
            st.caption("Silence percent")
            chart.create_silence_pie_chart(silence=ind_metrics_dict['silence'],not_silence=(100-ind_metrics_dict['silence']))
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Hate speech percent")
            chart.create_hate_speech_pie_chart(hateful_count = ind_metrics_dict['agent_hatepercent'], not_hateful_count = (100-ind_metrics_dict['agent_hatepercent']))
        with col2:
            st.caption("Irony speech percent")
            chart.create_pie_chart_ironic_ornot(ironic_count=ind_metrics_dict['agent_ironypercent'],non_ironic_count=(100-ind_metrics_dict['agent_ironypercent']))
        with col3:
            st.caption("Silence percent")
            chart.create_silence_pie_chart(silence=ind_metrics_dict['silence'],not_silence=(100-ind_metrics_dict['silence']))
    ################################################
            
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
         st.markdown("##### Agent Interrupt Count - {}".format(ind_metrics_dict['agentinterrupts']))
         st.markdown("##### Client Interrupt Count - {}".format(ind_metrics_dict['clientinterrupts']))
    
    with col3:
         st.markdown("##### Together Speak Time - {} seconds".format(ind_metrics_dict['togetherspeak']))

    
def dialogue(callid):

    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("Call Dialogue ")
    



    query_agent = """ SELECT * FROM public.call_sentence_agent"""
    df_agent = pd.read_sql_query(query_agent, read_data())
    query_client = """ SELECT * FROM public.call_sentence_client"""
    df_client = pd.read_sql_query(query_client, read_data())

    query_agent_aspect = """ SELECT * FROM public.call_sentence_aspect_agent"""
    df_agent_aspect = pd.read_sql_query(query_agent_aspect, read_data())
    query_client_aspect = """ SELECT * FROM public.call_sentence_aspect_client"""
    df_client_aspect = pd.read_sql_query(query_client_aspect, read_data())

    a = df_agent[df_client.callid == callid]
    a['speaker'] = 'Agent'
    b = df_client[df_client.callid == callid]
    b['speaker'] = 'Customer'
    ab = pd.concat([a,b])
    dialogue_df = ab.sort_values(by='endtime')
    

    conversation = dialogue_df.to_dict('records')
    
    print(conversation)
    print(df_client_aspect)
    for index, line in enumerate(conversation):
        if line['speaker'] == 'Customer':
            st.text_input("Customer:", value=line['speechtext'], key=f"customer_{index}", disabled=True)
            #st.markdown(df_client_aspect[df_client_aspect.callsentenceid == line['id']][['aspect','opinion']].to_dict('records'))
            st.write(df_client_aspect[df_client_aspect.callsentenceid == line['id']][['aspect','opinion']])
        elif line['speaker'] == 'Agent':
            st.text_input("Agent:", value=line['speechtext'], key=f"agent{index}", disabled=True)
            #st.markdown(df_agent_aspect[df_agent_aspect.callsentenceid == line['id']][['aspect','opinion']].to_dict('records'))
            st.write(df_agent_aspect[df_agent_aspect.callsentenceid == line['id']][['aspect','opinion']])



        
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


            agent = st.sidebar.selectbox("Agent", options= ['All']+list(get_agents_data().username), index=0)

            st.sidebar.divider()
            Topic_search = st.sidebar.text_input('Search Via Topic')
            
            # filter_dict = {}
            if primary_btn:      
                filter_dict = {'alert_calls':alert_calls,'start_date':start_date,'end_date':end_date,'satisfaction_level':satisfaction_level,
                               'performance_level':performance_level,'agent':agent,'Topic_search':Topic_search}

                
                # metrics_dict = get_data_info(filter_dict['alert_calls'],filter_dict['start_date'],filter_dict['end_date'],filter_dict['satisfaction_level'],filter_dict['performance_level'],
                #                              filter_dict['agent'])
                # dashboard(metrics_dict)
                try:
                    metrics_dict = get_data_info(filter_dict['alert_calls'],filter_dict['start_date'],filter_dict['end_date'],filter_dict['satisfaction_level'],filter_dict['performance_level'],
                                                 filter_dict['agent'],filter_dict['Topic_search'])
                    dashboard(metrics_dict)
                except:
                    st.markdown("### There is no available data !!!")
            






        if page == "Individual Call":
            st.sidebar.divider()


            call_id = st.sidebar.text_input('Call ID')
            search_button_clicked = st.sidebar.button("Search", type="primary")

            page_2 = st.sidebar.selectbox("Select Page", ["Report", "Dialogue"])

            

            

            if search_button_clicked and page_2 == "Report":
                # ind_metrics_dict = get_ind_data(call_id)
                # individual_call(ind_metrics_dict)
                try:
                    ind_metrics_dict = get_ind_data(call_id)
                    individual_call(ind_metrics_dict)
                except:
                    st.markdown("### There is no available data !!!")
            elif search_button_clicked and page_2 == "Dialogue":
                dialogue(int(call_id))
        

        

if __name__ == "__main__":
    main()