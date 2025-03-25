import pandas as pd
import os
import psycopg2
from get_data import get_article_data

df = get_article_data()
print(df)

df.columns=df.columns.str.lower()
df.columns= df.columns.str.replace(' ', '_')
df.columns

df['reading_time']= df['reading_time'].str.replace(' min read', '')
df['reading_time']= df['reading_time'].astype(int)
df['article_content']= df['article_content'].str.replace('\n', '')
df['time_uploaded']= pd.to_datetime(df['time_uploaded'])

df= df.astype({
    'link': 'string', 
    'title' : 'string',
    'author' : 'string',
    'tags' : 'string',
    'reading_time' : 'int64',
    'article_content' : 'string',
    'word_count' : 'int64',
    'sentiment' : 'string',
    'compound_score' : 'float64'
})



#print(df)
db_params= {
    'dbname' : "postgres",
    'user': "testtech",
    'password': os.getenv('DB_PASSWORD'),
    'host' : "testtech.postgres.database.azure.com",
    'port' : "5432"
}

try:
    conn = psycopg2.connect(**db_params)
    cursor=conn.cursor()

    query= """
    INSERT INTO ammy (link, title, time_uploaded, author, tags, reading_time, article_content, word_count, sentiment, compound_score)
    VALUES (%s, %s,%s,%s,%s, %s, %s, %s, %s, %s)
    ON CONFLICT (link) DO NOTHING;  --aviods duplicate primary key errors
    """

 #insert dataframe record one by one
    for _, row in df.iterrows():
        cursor.execute(query, (
            row['link'], row['title'],row['time_uploaded'], row['author'], row['tags'], 
            row['reading_time'], row['article_content'], row['word_count'], row['sentiment'], row['compound_score']
        ))

    conn.commit()
    print('data inserted successfully')

except Exception as e:
        print('Error:', e)

finally:
    if conn:
        cursor.close()
        conn.close()


