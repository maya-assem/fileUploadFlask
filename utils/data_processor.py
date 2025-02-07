import pandas as pd
import numpy as np
from datetime import datetime
from .phone_utils import standardize_phone_number

class DataProcessor:
    @staticmethod
    def process_call_data(df, existing_leads_df=None):
        df = df.copy()

        # Clean phone numbers and remove angle brackets
        df['Call From'] = df['Call From'].apply(lambda x: standardize_phone_number(str(x)))
        df['Call To'] = df['Call To'].apply(lambda x: standardize_phone_number(str(x)))

        # Convert durations to numeric, handling any non-numeric values
        for col in ['Call Duration', 'Ring Duration', 'Talk Duration']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Initialize new columns
        try:
            df['lead_date'] = pd.to_datetime(df['Time']).dt.date
            df['call_date'] = df['lead_date']  # Use the same date for both
        except Exception as e:
            print(f"Error processing dates: {str(e)}")
            df['lead_date'] = None
            df['call_date'] = None

        df['is_fresh_lead'] = False
        df['source'] = None

        # Determine if fresh lead
        if existing_leads_df is not None and not existing_leads_df.empty:
            try:
                existing_leads_df['lead_date'] = pd.to_datetime(existing_leads_df['Created on']).dt.date
                existing_leads_df['phone_number'] = existing_leads_df['Client'].apply(
                    lambda x: standardize_phone_number(str(x)))

                for idx, row in df.iterrows():
                    call_number = row['Call To']
                    call_date = row['lead_date']

                    # Check if number exists in leads and if call was made on the same day
                    matching_lead = existing_leads_df[
                        (existing_leads_df['phone_number'] == call_number) & 
                        (existing_leads_df['lead_date'] == call_date)
                    ]

                    if not matching_lead.empty:
                        df.at[idx, 'is_fresh_lead'] = True
                        df.at[idx, 'source'] = matching_lead.iloc[0]['Channel']
            except Exception as e:
                print(f"Error processing lead matching: {str(e)}")

        # Clean any tabs or whitespace from ID field
        df['ID'] = df['ID'].astype(str).str.strip()

        return df

    @staticmethod
    def process_chat_data(df):
        df = df.copy()

        # Convert datetime columns with error handling
        datetime_columns = ['Created on', 'Agent replied on', 'Last message posted on', 'Agent closed on']
        for col in datetime_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except Exception as e:
                print(f"Error converting datetime column {col}: {str(e)}")
                df[col] = None

        # Add lead date with error handling
        try:
            df['lead_date'] = df['Created on'].dt.date
        except Exception as e:
            print(f"Error setting lead_date: {str(e)}")
            df['lead_date'] = None

        df['is_fresh_lead'] = False  # Initialize the column

        # Clean and standardize phone numbers from client field
        df['phone_number'] = df['Client'].apply(lambda x: standardize_phone_number(str(x)))

        # Convert numeric columns
        numeric_columns = ['Messages', 'Waiting for agent to respond', 'Conversation duration',
                         'Chat bot time', 'Initial response time', 'Total response time',
                         'Average response time', 'Maximum response time']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Clean chat ID
        df['#'] = df['#'].astype(str).str.strip()

        return df