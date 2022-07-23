import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Data Analysis')
st.sidebar.image('https://nationwideradiojm.com/wp-content/uploads/2020/05/olympic-rings-1024x640.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Analysis', 'Overall No. Stats', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Analysis':
    st.sidebar.header('Medal Analysis')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal analysis")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal analysis for olympics held in " +str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Medals analysis of " +selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("Medals analysis of " +selected_country +" during " +str(selected_year) + " olympics.")

    st.table(medal_tally)

if user_menu == 'Overall No. Stats':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Total number of")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.header(editions)
    with col2:
        st.header("Host Cities")
        st.header(cities)
    with col3:
        st.header("Sports")
        st.header(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.header(events)
    with col2:
        st.header("Nations")
        st.header(nations)
    with col3:
        st.header("Athletes")
        st.header(athletes)

    nations_over_time = helper.data_overtime(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    fig.update_layout(autosize=False,width=1000,height=600, yaxis_title='No. of Nations',xaxis_title='Year',)
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_overtime(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    fig.update_layout(autosize=False,width=1000,height=600, yaxis_title='No. of Events',xaxis_title='Year',)
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_overtime(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    fig.update_layout(autosize=False,width=1000,height=600, yaxis_title='No. of Players',xaxis_title='Year',)
    st.title('Players over the years')
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    fig.update_layout(autosize=False,width=1000,height=600, yaxis_title='No. of Medals',xaxis_title='Year',)
    st.header(selected_country +' Medal Tally over the years')
    st.plotly_chart(fig)


    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


    st.header(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600, yaxis_title='Probability of winning',xaxis_title='Age',)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    st.title('Gender Ratio')
    final = helper.gender_ratio(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'], labels={'Year': 'year', 'value': 'No. of Females or Males'})
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
