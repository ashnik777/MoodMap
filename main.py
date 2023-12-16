import streamlit as st
from plots import CustomPieChart



def dashboard():
    st.title("Dashboard")


    # Filters block
    st.sidebar.divider()
    primary_btn = st.sidebar.button(label="Filter", type="primary")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    st.sidebar.divider()
    start_emotion = st.sidebar.selectbox("Start emotion", options=['All','Happy','Neutral','Sad','Angry'], index=0)
    end_emotion = st.sidebar.selectbox("End emotion", options=['All','Happy','Neutral','Sad','Angry'], index=0)
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

    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Costumers Satisfactions Levels")
        chart = CustomPieChart()
        chart.create_custom_pie_chart(progress=60, hole=0.7, color=['green', 'rgba(0,0,0,0)'], percentage=True)
    with col2:
        st.caption("Agents Performance Rate")
        chart = CustomPieChart()
        chart.create_custom_pie_chart(progress=70, hole=0.7, color=['blue', 'rgba(0,0,0,0)'], percentage=True)
    with col3:
        st.caption("Costumer Care")
        chart = CustomPieChart()
        chart.create_custom_pie_chart(progress=60, hole=0.7, color=['yellow', 'rgba(0,0,0,0)'], percentage=True)

    st.divider()
    

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
