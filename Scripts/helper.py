import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def fetch_medal_tally(df, year, country):
    flag = 0
    medal_df = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def country_year_list(df):
    Years = df['Year'].dropna().unique().tolist()
    Years.sort()
    Years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return Years, country

def data_over_time(df, col):
    data = (
        df.drop_duplicates(['Year', col])
        .groupby('Year')
        .size()
        .reset_index(name=col)   # ✅ keeps the same col name instead of generic 'count'
    )
    data.rename(columns={'Year': 'Edition'}, inplace=True)
    return data.sort_values('Edition')

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Athlete', 'Medals']

    # Merge to get Sport + Region
    merged = top_athletes.merge(df, left_on='Athlete', right_on='Name', how='left')

    # Keep only required columns
    final = merged[['Athlete', 'Medals', 'Sport', 'region']].drop_duplicates('Athlete')

    return final.head(15)

    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    final_df = temp_df.drop_duplicates(['Year', 'Sport', 'Event', 'Medal'])
    final_df = final_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Athlete', 'Medals']

    merged = top_athletes.merge(df, left_on='Athlete', right_on='Name', how='left')

    final = merged[['Athlete', 'Medals', 'Sport']].drop_duplicates('Athlete')

    return final.head(10)

    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    return temp_df

def men_vs_women(df):
    athletes = df.drop_duplicates(subset=['Name', 'region'])[['Year', 'Sex']]
    men = athletes[athletes['Sex'] == 'M'].groupby('Year').count()['Sex'].reset_index()
    women = athletes[athletes['Sex'] == 'F'].groupby('Year').count()['Sex'].reset_index()
    final = men.merge(women, on='Year', how='left').fillna(0)
    final.rename(columns={'Sex_x': 'Male', 'Sex_y': 'Female'}, inplace=True)
    return final
