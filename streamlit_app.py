import pandas as pd
import streamlit as st
import plotly.express as px
from pinotdb import connect
from datetime import datetime

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Connect to Pinot
conn = connect(host='54.255.221.12', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()

# Streamlit App Layout
st.title("Pageview SUBTYPE Analytics🎈")

# Show the last update time
now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.write(f"Last update: {dt_string}")

# Sidebar Filters
st.sidebar.markdown("### Filters")
# Gender Filter
query_gender = """
SELECT DISTINCT GENDER
FROM 5Pageviews_SUBTYPE 
"""
curs.execute(query_gender)
gender_options = [row[0] for row in curs]
selected_genders = st.sidebar.multiselect(
    "Select Genders to Display",
    options=gender_options,
    default=gender_options
)

# Region Filter
query_region = """
SELECT DISTINCT REGIONID
FROM 5Pageviews_SUBTYPE 
"""
curs.execute(query_region)
region_options = [row[0] for row in curs]
selected_regions = st.sidebar.multiselect(
    "Select Regions to Display",
    options=region_options,
    default=region_options
)

# Query 1: Distribution of Activities
query1 = """
SELECT SUBTYPE, COUNT(*) as Count
FROM 5Pageviews_SUBTYPE
GROUP BY SUBTYPE
ORDER BY Count DESC
"""
curs.execute(query1)
df_activities = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

# Create the first row layout with wider columns
col1, col2 = st.columns([3, 3])  # Adjust proportions to allocate more space

with col1:
    # Horizontal bar chart sorted by count (Graph 1)
    st.markdown("<h3 style='font-size: 20px;'>1. Distribution of Activities</h3>", unsafe_allow_html=True)
    fig1 = px.bar(
        df_activities,
        y='SUBTYPE',
        x='Count',
        color='SUBTYPE',
        labels={'SUBTYPE': 'SUBTYPE', 'Count': 'Count'},
        title='',  # Remove the title
        orientation='h',  # Horizontal bar chart
        width=900,  # Set width for the graph
        height=400  # Adjust height to minimize white space
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

