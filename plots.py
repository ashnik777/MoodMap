import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

class CustomPieChart:
    def __init__(self):
        self.progress = None
        self.hole = 0.6
        self.color = ['green', 'rgba(0,0,0,0)']
        self.percentage = True
        self.fig = None
        self.categories = None

    def create_custom_pie_chart(self, progress, hole=0.6, color=['green', 'rgba(0,0,0,0)'], percentage=True):
        self.progress = progress
        self.hole = hole
        self.color = color
        self.percentage = percentage

        remaining_progress = 100 - self.progress

        self.fig = px.pie(values=[self.progress, remaining_progress], names=['Progress', 'Remaining'],
                          hole=self.hole, color_discrete_sequence=self.color)

        self.fig.update_traces(textinfo='none')

        self.fig.update_layout(
            width=300, 
            height=300,
            showlegend=False,
            plot_bgcolor='black',
            paper_bgcolor='rgb(16,18,22)'
        )
        
        if self.percentage:
            self.fig.add_annotation(
                x=0.5, y=0.5,
                text=f"{self.progress}%",
                showarrow=False,
                font=dict(color='white', size=40)
            )


        st.plotly_chart(self.fig)

    def create_bar_chart(self,values,categories):
    # Creating the bar chart
        self.categories = categories
        self.fig = go.Figure(data=[go.Bar(x=self.categories, y=values)])

        # Updating layout
        self.fig.update_layout(
            width=500, 
            height=400,
            xaxis=dict(title='Categories', showgrid=False),
            yaxis=dict(title='Percent', showgrid=False),
            plot_bgcolor='rgb(16,18,22)',
            paper_bgcolor='rgb(16,18,22)'
        )

        # Display the chart
        st.plotly_chart(self.fig)

