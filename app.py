import streamlit as st
import pandas as pd
from database.models import init_db
from database.operations import DatabaseOperations
from components.upload import handle_file_upload
from components.visualizations import Visualizations
from utils.data_processor import DataProcessor

def main():
    st.set_page_config(
        page_title="Lead Pipeline Dashboard",
        page_icon="📞",
        layout="wide"
    )

    st.title("📊 Lead Pipeline Dashboard")

    # Initialize database
    try:
        engine = init_db()
        db_ops = DatabaseOperations(engine)
        st.success("Connected to database successfully!")
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return

    # File upload section
    st.header("📁 Upload Data")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Call Data")
        call_file = st.file_uploader("Upload Call CSV", type="csv", key="call_file")

    with col2:
        st.subheader("Chat Data")
        chat_file = st.file_uploader("Upload Chat CSV", type="csv", key="chat_file")

    if call_file is not None and chat_file is not None:
        try:
            # Load and process data
            df_calls = pd.read_csv(call_file)
            df_chats = pd.read_csv(chat_file)

            # Process chat data first
            processed_chats = DataProcessor.process_chat_data(df_chats)

            # Process call data with reference to chat data for fresh lead detection
            processed_calls = DataProcessor.process_call_data(df_calls, df_chats)

            # Store in database
            db_ops.store_call_records(processed_calls)
            db_ops.store_chat_records(processed_chats)

            st.success("Data processed and stored successfully!")

            # Create visualizations
            st.header("📈 Lead Pipeline Analytics")

            # Layout the visualizations in a grid
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(Visualizations.create_fresh_leads_by_date(processed_calls))
                st.plotly_chart(Visualizations.create_channel_distribution(processed_chats))
                st.plotly_chart(Visualizations.create_conversion_by_source(processed_chats, processed_calls))

            with col2:
                st.plotly_chart(Visualizations.create_lead_funnel(processed_calls, processed_chats))
                st.plotly_chart(Visualizations.create_response_time_distribution(processed_chats))
                st.plotly_chart(Visualizations.create_agent_performance(processed_chats))

            # Show summary metrics
            st.header("📊 Key Metrics")

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                total_leads = len(processed_chats['phone_number'].unique())
                st.metric("Total Leads", total_leads)

            with metric_col2:
                fresh_leads = len(processed_calls[processed_calls['is_fresh_lead']]['Call To'].unique())
                st.metric("Fresh Leads", fresh_leads)

            with metric_col3:
                avg_response_time = processed_chats['Total response time'].mean()
                st.metric("Avg Response Time (s)", f"{avg_response_time:.2f}")

            with metric_col4:
                conversion_rate = (fresh_leads / total_leads * 100) if total_leads > 0 else 0
                st.metric("Conversion Rate", f"{conversion_rate:.1f}%")

            # Show raw data
            st.header("🔍 Raw Data Preview")
            tab1, tab2 = st.tabs(["Call Data", "Chat Data"])

            with tab1:
                st.dataframe(processed_calls)

            with tab2:
                st.dataframe(processed_chats)

        except Exception as e:
            st.error(f"Error processing files: {str(e)}")

if __name__ == "__main__":
    main()