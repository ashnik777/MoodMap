import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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

        self.color = ['red' if progress <= 60 else 'orange' if progress <= 80 else 'green', 'rgba(0,0,0,0)']

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

    def create_grouped_bar_chart(self,Happy, Neutral, Sad, Angry):

        categories = ['start part of call', 'mean part of call', 'finish part of call']
        # Create traces for each group with specified colors
        trace1 = go.Bar(
            x=categories,
            y=Happy,
            name='Happy',
            marker=dict(color='green')  # Change color here
        )
        trace2 = go.Bar(
            x=categories,
            y=Neutral,
            name='Neutral',
            marker=dict(color='yellow')  # Change color here
        )
        trace3 = go.Bar(
            x=categories,
            y=Sad,
            name='Sad',
            marker=dict(color='orange')  # Change color here
        )
        trace4 = go.Bar(
            x=categories,
            y=Angry,
            name='Angry',
            marker=dict(color='red')  # Change color here
        )

        # Assign traces to data variable
        data = [trace1, trace2, trace3, trace4]

        # Layout settings with background color
        layout = go.Layout(
            width=500, 
            height=400,
            yaxis=dict(title='percents', showgrid=False),
            barmode='group',  # To create a grouped bar chart
            plot_bgcolor='rgb(16,18,22)',
            paper_bgcolor='rgb(16,18,22)'  # Change background color here
        )

        # Create figure
        self.fig = go.Figure(data=data, layout=layout)

        st.plotly_chart(self.fig)


    def create_pie_chart_ironic_ornot(self,ironic_count, non_ironic_count):
        # Create data for Pie chart
        labels = ['Ironic', 'Not Ironic']
        values = [ironic_count, non_ironic_count]

        # Create Pie chart
        self.fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='none')])
        self.fig.update_layout(
            width=300,
            height=400,
            plot_bgcolor='rgb(16,18,22)',
            paper_bgcolor='rgb(16,18,22)'
        )

        st.plotly_chart(self.fig)

    def create_hate_speech_pie_chart(self,hateful_count, targeted_count, aggressive_count, Normal):
        # Create data for Pie chart
        labels = ['Hateful', 'Targeted', 'Aggressive', 'Normal']
        values = [hateful_count, targeted_count, aggressive_count, Normal]

        # Create Pie chart
        self.fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='none')])
        self.fig.update_layout(
            width=300,
            height=400,
            plot_bgcolor='rgb(16,18,22)',
            paper_bgcolor='rgb(16,18,22)'
        )

        st.plotly_chart(self.fig)

    def generate_emotion_plot(self,input_histogram):
        df = pd.DataFrame({'Emotion': input_histogram})

        emotion_mapping = {1: 'Angry', 2: 'Sad', 3: 'Neutral', 4: 'Happy'}

        df['Emotion'] = df['Emotion'].map(emotion_mapping)

        emoji_mapping = {'Angry': '😡', 'Sad': '😢', 'Neutral': '😐', 'Happy': '😊'}

        fixed_order_with_emojis = ['Angry', 'Sad', 'Neutral', 'Happy']
        fixed_order_emojis_with_text = [f'{emoji_mapping[emotion]} {emotion}' for emotion in fixed_order_with_emojis]

        self.fig = px.line(df, x=df.index * 3, y='Emotion', markers=True, line_shape='spline')

        layout = {
            'height': 400,
            'width': 1000,
            'yaxis': {
                'title': 'Emotions',
                'tickmode': 'array',
                'ticktext': fixed_order_emojis_with_text,
                'tickvals': fixed_order_with_emojis,
                'categoryorder': 'array',
                'categoryarray': fixed_order_with_emojis,
                'tickfont': {'size': 16, 'color': 'white'},
                'showgrid': True,
                'gridwidth': 0.1,
                'gridcolor': 'grey'
            },
            'xaxis':{
                 'title': 'Duration',
                 'showgrid': False
            },
            'plot_bgcolor': 'rgb(16,18,22)',#'snow',
            'paper_bgcolor': 'rgb(16,18,22)',
            'font': {'family': 'Arial', 'size': 12, 'color': 'white'},
            'showlegend': False

        }


        self.fig.update_layout(**layout)
        self.fig.update_traces(
            marker=dict(size=8, line=dict(width=2, color='deeppink'), color='deeppink'),
            line=dict(color='snow', width=3),
            hovertemplate=f'Second: %{{x}}<br>{self.fig.data[0].name} Emotion: %{{text}}',
            text=self.fig.data[0]['y']
        )
        
        st.plotly_chart(self.fig)

    def plot_top_topics(self,data):
        # Create DataFrame
        df = pd.DataFrame(data)
    
        # Count the occurrences of each topic and sort by frequency in ascending order
        top_topics = df['topics'].value_counts().head(10).sort_values(ascending=True)
    
        # Create a DataFrame from the value counts
        top_topics_df = top_topics.reset_index()
        top_topics_df.columns = ['Topics', 'Frequency']
    
        # Plotting using Plotly
        self.fig = px.bar(top_topics_df, x='Frequency', y='Topics', orientation='h')
        self.fig.update_layout(
            plot_bgcolor='rgb(16,18,22)',
            paper_bgcolor='rgb(16,18,22)',  # Change background color to light gray
            width=300,  # Adjust width of the plot
            height=400,  # Adjust height of the plot
            xaxis=dict(showgrid=False, title='', tickvals=[]),  # Remove vertical gridlines
            yaxis=dict(showgrid=False, title=''),  # Remove horizontal gridlines
            font=dict(color='white')
        )
        st.plotly_chart(self.fig)
