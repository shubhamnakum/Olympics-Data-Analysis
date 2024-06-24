import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.header("Olympics Analysis")
st.sidebar.image("Olympic-logo.webp")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis',
     'Country-wise Analysis', 'Athlete-wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    Medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal tally of ' + selected_country +
                 ' in ' + str(selected_year) + ' in Olympics')
    st.table(Medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("nations")
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations Over the Year')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events Over the Year')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes Over the Year')
    st.plotly_chart(fig)

    st.title('No of Events over time (Every Sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year',
                     values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    Sport_list = df['Sport'].unique().tolist()
    Sport_list.sort()
    Sport_list.insert(0, 'Overall')
    selected_Sport = st.selectbox('Select a Sport', Sport_list)

    x = helper.most_successful(df, selected_Sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' rMedal tally over the Year')
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    st.title('Country wise Events Analysis of ' +
             selected_country+' over the Years')
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    successful_country_wise = helper.most_successful_countrywise(
        df, selected_country)
    st.title('Most Successful Athletes of ' + selected_country)
    st.table(successful_country_wise)

if user_menu == 'Athlete-wise Analysis':
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age Distribution', 'Gold Medalist',
                             'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    Sport_list = df['Sport'].unique().tolist()
    Sport_list.sort()
    Sport_list.insert(0, 'Overall')
    st.title('Height vs Weight')
    selected_Sport = st.selectbox('Select a Sport', Sport_list)
    temp_df = helper.weight_v_height(df, selected_Sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df,
                         hue='Medal', style=temp_df['Sex'], s=60)

    st.pyplot(fig)

    temp_df = helper.men_v_women(df)
    fig = px.line(temp_df, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)
