import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df , region_df)


st.sidebar.title('Olympics Analysis')
st.sidebar.image('20140204000881966198-original.jpg')

user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally' , 'Overall Analysis' , 'country-wise Analaysis' , 'Athelete-wise Analysis')
)


# st.dataframe(df)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Taly')
    years, country = helper.country_year_list(df)

    selected_years = st.sidebar.selectbox('select year' , years)
    selected_country = st.sidebar.selectbox('select country' , country)
    medal_tally = helper.fetch_medal_tally(df , selected_years , selected_country)
    
    if selected_years == 'Overall' and selected_country == 'Overall':
        st.title('Overall  Tally')
    
    if selected_years != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in ' + str(selected_years))

    if selected_years == 'Overall' and selected_country != 'Overall':
        st.title('Medal tally in ' + selected_country)

    if selected_years != 'Overall' and selected_country != 'Overall':
        st.title('Medal tally in ' + str(selected_years) + " " + -++9+++- selected_country)

    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    nations= df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)


    col1 , col2 , col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Atheletes')
        st.title(atheletes)

    with col3:
        st.header('Nations')
        st.title(atheletes)

    nation_over_time = helper.data_over_time(df , 'region')

    plt.figure(figsize = (10 , 6))
    fig = px.line(nation_over_time , x = 'Year' , y = 'region' )
    # fig.show()

    st.title('Participating nation over the year')

    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df , 'Event')

    plt.figure(figsize = (10 , 6))
    fig = px.line(events_over_time , x = 'Year' , y = 'Event' )
    # fig.show()

    st.title('Events nation over the year')

    st.plotly_chart(fig)

    atheletes_over_time = helper.data_over_time(df , 'Name')

    plt.figure(figsize = (10 , 6))
    fig = px.line(atheletes_over_time , x = 'Year' , y = 'Name' )
    # fig.show()

    st.title("Athletes over the years")

    st.plotly_chart(fig)


    st.title("NO. of Events over (Every time)")

    fig , ax = plt.subplots(figsize = (20 , 20))
    x = df.drop_duplicates(['Year' , 'Sport' , 'Event'])

    ax = sns.heatmap(x.pivot_table(index = 'Sport' , columns = 'Year' , values = 'Event' , aggfunc = 'count').fillna(0).astype('int'), annot = True)

    st.pyplot(fig)



    st.title('Most Succesful Athletes')
    sport_list = df['Sport'].unique().tolist()

    sport_list.sort()

    sport_list.insert(0 , 'Overall')

    selected_sport = st.selectbox('Select a sport' , sport_list)

    x = helper.most_succcessful(df , selected_sport)

    st.table(x)

if user_menu == 'country-wise Analaysis':

    st.sidebar.title('Country wise Analysis')


    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('select a country', country_list )
    country_df = helper.year_wise_medal_tally(df ,selected_country)
    fig = px.line(country_df , x = 'Year' , y = 'Medal')
    st.title(selected_country + 'Medal Tally over the year')
    st.plotly_chart(fig)


    pt = helper.country_event_heatmap(df , selected_country)
    st.title(selected_country + 'Medal Tally over the year')

    fig , ax = plt.subplots(figsize = (20 , 20))
    # x = df.drop_duplicates(['Year' , 'Sport' , 'Event'])

    ax = sns.heatmap(pt , annot= True)

    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    top10_df = helper.most_succcessful_countrywise(df , selected_country)
    st.table(top10_df)


if user_menu == 'Athelete-wise Analysis':

    
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()


    fig = ff.create_distplot([x1 , x2 , x3 , x4] , ['Overall Age' , 'Gold Medalist' , 'Silver Medalist' , 'Bronze Medalist'] , show_hist = False , show_rug = False)
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.title('Distribution of Age')
    
    st.plotly_chart(fig)


    x = []
    name = []

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']


    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)


    fig = ff.create_distplot(x , name , show_hist= False , show_rug=False)
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.title('Distribution of Age wrt Sport (Gold Medalist)')
    
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'],y = temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men Vs Women Parition over the year')
    final = helper.men_vs_women(df)
    fig = px.line(final , x = 'Year' , y = ['Male','Female'] )

    st.plotly_chart(fig)