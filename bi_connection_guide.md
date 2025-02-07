# BI Tool Connection Guide - Looker Studio Setup

## Database Connection Details
- Host: Use the value from PGHOST environment variable
- Port: Use the value from PGPORT environment variable  
- Database: Use the value from PGDATABASE environment variable
- Username: bi_reader
- Password: bi_secure_password

## Detailed Looker Studio Setup Steps

1. Go to https://lookerstudio.google.com/
2. Click "Create" > "Report"
3. Click "Create new data source"
4. Search for and select "PostgreSQL" from the connector list
5. Enter the connection details:
   - Host: [PGHOST value]
   - Port: [PGPORT value] 
   - Database: [PGDATABASE value]
   - Username: bi_reader
   - Password: bi_secure_password
6. Click "AUTHENTICATE"
7. In the table selection dropdown, choose `analytics_dashboard`
8. Click "ADD TO REPORT"

## Recommended Visualizations

1. Call Center Performance:
   - Chart type: Time series
   - Dimension: call_date
   - Metrics: count of calls, average call_duration
   - Filter: call_status

2. Lead Conversion:
   - Chart type: Funnel
   - Metrics: total leads, fresh leads, converted leads
   - Dimension: lead_source

3. Agent Performance:
   - Chart type: Scorecard
   - Metrics: average response_time, messages per chat
   - Dimension: employee

4. Channel Distribution:
   - Chart type: Pie chart
   - Dimension: channel
   - Metric: count of chats

## Real-time Updates
- Data is automatically updated when new files are processed
- The analytics_dashboard view combines both calls and chat data
- Refresh interval can be set in Looker Studio (recommended: 15 minutes)

## Available Fields in analytics_dashboard

### Call Metrics
- call_id: Unique call identifier
- call_timestamp: When the call occurred
- call_duration: Duration in seconds
- call_status: Call outcome
- call_is_fresh_lead: If this was a fresh lead
- lead_source: Source of the lead

### Chat Metrics
- chat_id: Unique chat identifier
- channel: Communication channel
- messages: Number of messages
- response_time: Agent response time
- chat_created_on: Chat start time
- chat_closed_on: Chat end time
- chat_is_fresh_lead: If this was a fresh lead

## Troubleshooting
- If connection fails, verify the host and port values
- Ensure you're using SSL/TLS connection
- For "Connection refused" errors, check if your IP is allowlisted

## For Power BI:
1. Open Power BI Desktop
2. Click "Get Data" > "Database" > "PostgreSQL"
3. Enter the connection details above
4. Choose between:
   - Import Mode: Data is cached and refreshed periodically
   - DirectQuery Mode: Real-time querying (recommended for live dashboards)
5. Select the `analytics_dashboard` view or individual tables

## Important Notes:
- The database connection uses SSL by default
- Data is automatically updated when new records are added
- The `analytics_dashboard` view provides a unified view of all data
- Connection is read-only for security

## Available Tables/Views:
1. analytics_dashboard (recommended):
   - Combined view of calls and chats
   - Pre-joined data for easier reporting
   - Includes all relevant metrics

2. call_records:
   - Raw call data
   - Call durations, status, and outcomes

3. chat_records:
   - Raw chat interactions
   - Response times and chat metrics