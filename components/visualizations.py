import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Visualizations:
    @staticmethod
    def create_call_status_pie(df):
        status_counts = df['Status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title='Call Status Distribution'
        )
        return fig

    @staticmethod
    def create_hourly_call_volume(df):
        df['hour'] = pd.to_datetime(df['Time']).dt.hour
        hourly_counts = df['hour'].value_counts().sort_index()
        fig = px.line(
            x=hourly_counts.index,
            y=hourly_counts.values,
            title='Hourly Call Volume',
            labels={'x': 'Hour of Day', 'y': 'Number of Calls'}
        )
        return fig

    @staticmethod
    def create_agent_performance(df):
        agent_stats = df.groupby('Employee').agg({
            'Messages': 'mean',
            'Total response time': 'mean',
            'Conversation duration': 'mean'
        }).round(2)

        fig = px.bar(
            agent_stats,
            barmode='group',
            title='Agent Performance Metrics'
        )
        return fig

    @staticmethod
    def create_channel_distribution(df):
        channel_counts = df['Channel'].value_counts()
        fig = px.bar(
            x=channel_counts.index,
            y=channel_counts.values,
            title='Distribution by Channel',
            labels={'x': 'Channel', 'y': 'Number of Conversations'}
        )
        return fig

    @staticmethod
    def create_fresh_leads_by_date(df):
        fresh_leads = df[df['is_fresh_lead']].groupby(['lead_date', 'source']).size().reset_index(name='count')
        fig = px.bar(
            fresh_leads,
            x='lead_date',
            y='count',
            color='source',
            title='Fresh Leads by Date and Source',
            labels={'count': 'Number of Fresh Leads', 'lead_date': 'Date'}
        )
        return fig

    @staticmethod
    def create_lead_funnel(df_calls, df_chats):
        total_leads = len(df_chats['phone_number'].unique())
        contacted_leads = len(df_calls['Call To'].unique())
        answered_calls = len(df_calls[df_calls['Status'] == 'ANSWERED']['Call To'].unique())

        fig = go.Figure(go.Funnel(
            y=['Total Leads', 'Contacted Leads', 'Answered Calls'],
            x=[total_leads, contacted_leads, answered_calls]
        ))
        fig.update_layout(title='Lead Funnel Analysis')
        return fig

    @staticmethod
    def create_response_time_distribution(df):
        fig = px.histogram(
            df,
            x='Total response time',
            title='Response Time Distribution',
            labels={'Total response time': 'Response Time (seconds)'}
        )
        return fig

    @staticmethod
    def create_conversion_by_source(df_chats, df_calls):
        # Calculate conversion rates by source
        sources = df_chats['Channel'].unique()
        conversion_data = []

        for source in sources:
            source_leads = df_chats[df_chats['Channel'] == source]['phone_number'].unique()
            converted = df_calls[
                (df_calls['Call To'].isin(source_leads)) & 
                (df_calls['Status'] == 'ANSWERED')
            ]['Call To'].nunique()

            total = len(source_leads)
            conversion_rate = (converted / total * 100) if total > 0 else 0

            conversion_data.append({
                'source': source,
                'conversion_rate': conversion_rate
            })

        df_conversion = pd.DataFrame(conversion_data)
        fig = px.bar(
            df_conversion,
            x='source',
            y='conversion_rate',
            title='Conversion Rate by Source',
            labels={'source': 'Source', 'conversion_rate': 'Conversion Rate (%)'}
        )
        return fig