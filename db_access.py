from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text
import api_data as ad

load_dotenv()

# create engine
connection_string = os.getenv("MYSQL_CONNECTION")
engine = create_engine(connection_string)

#Save defined spotify charts in table
def save_all_charts():
    tmp_countries = ['Global', 'USA', 'UK', 'Italy', 'Germany', 'France', 'Spain',
                        'Netherlands', 'Iceland', 'Switzerland']
    
    for country in tmp_countries:
        print(country)
        df = ad.get_top_songs_for_country(country)
        df.to_sql(name='top_songs', con=engine, if_exists='append', index=False)

def get_top_songs():
    sql = 'SELECT * FROM top_songs;'
    with engine.connect() as conn:
        query = conn.execute(text(sql))
    df = pd.DataFrame(query.fetchall())
    return df


def get_rank_dance(country):
    sql = 'SELECT top_songs.Rank, Danceability, Country FROM top_songs WHERE country = ' + "'" + country + "'" 
    with engine.connect() as conn:
        query = conn.execute(text(sql))
    df = pd.DataFrame(query.fetchall())
    return df
