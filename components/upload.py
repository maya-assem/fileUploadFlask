import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor

def handle_file_upload():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Detect file type based on columns
            if 'Call From' in df.columns:
                st.write("Processing Call Data...")
                processed_df = DataProcessor.process_call_data(df)
                file_type = 'call'
            elif 'Channel' in df.columns:
                st.write("Processing Chat Data...")
                processed_df = DataProcessor.process_chat_data(df)
                file_type = 'chat'
            else:
                st.error("Unknown file format")
                return None, None
                
            st.success("File processed successfully!")
            return processed_df, file_type
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None, None
            
    return None, None
