#Tweeter data scrapping
#Author = santhosh V
#version = 1.0
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
st.title("Tweeter Data Scrapping")
option = st.selectbox('Search By',('username', '#HASHTAG', "Keyword"))
limit = st.slider("limit of data to be scrapped", 0, 1000)
st.write(limit)
def ttscp(from_filters):
    attributes_container = []
    since1 = st.date_input("since")
    until1 = st.date_input("until")
    filters = [f'since:{since1}', f'until:{until1}']
    filters.append(' OR '.join(from_filters))
    tweet1 = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(' '.join(filters)).get_items()):
        if i > limit:
            break
        attributes_container.append(
                [tweet.date, tweet.likeCount, tweet.url, tweet.content, tweet.id, tweet.user.username,
                 tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.media])
        tweet1.append(tweet)
    # Using sntwitter.TwitterSearchScraper to scrape data and append tweets to list
    tweets_df1 = pd.DataFrame(attributes_container,
                              columns=["date", "like_count", "url", "tweet_content", "id", "user", "reply_count",
                                       "retweet_count", "language", "source"])
    return tweets_df1

if option == "username":
        hash_tag = st.text_input("username")
        from_filters = []
        from_filters.append(f'from:{hash_tag}')
        df = ttscp(from_filters)
        st.write(df.astype(str))

elif option == "#HASHTAG":
    try:
        hash_tag1 = st.text_input("HASHTAG")
        hash_tag = "#"+ hash_tag1
        st.write(hash_tag)
        from_filters = []
        from_filters.append(hash_tag)
        df = ttscp(from_filters)
        st.write(df.astype(str))
    except BaseException as e:
        pass
elif option == "Keyword":
    try:
        hash_tag = st.text_input("Keyword")
        from_filters = []
        from_filters.append(hash_tag)
        df = ttscp(from_filters)
        st.write(df.astype(str))
    except BaseException as e:
        pass
try:
    json1 = df.head(limit).to_json()
    csv = df.head(limit).to_csv()
except BaseException as e:
    pass

st.sidebar.title("Download the Scapped Data")
try:
    st.sidebar.download_button(label='📥 csv',
                                        data=csv,
                                        file_name= 'scrap.csv')
    st.sidebar.download_button(label='📥 json',
                                        data=json1,
                                        file_name= 'scrap.json')
except BaseException as e:
    pass

st.sidebar.title("Upload to MONGO")
button1 = st.sidebar.button("Upload to Mongo")

if button1:
    from pymongo import MongoClient

    # call fun1 from file2.py
    data = df.head(limit)
    client = MongoClient("mongodb://localhost:27017");
    print("Connection Successful")
    mydb = client["TWEET"]
    import json

    # records = json.loads(tweets_df1.to_json(orient='records'))
    data = json.loads(data.to_json(orient='records'))
    from datetime import datetime

    Date = datetime.now().strftime('%d-%m-%Y')
    dict1 = {"Scraped Word": hash_tag, "Scraped Date": Date, "Data": data}
    mydb.mycol.insert_many([dict1])
