from matplotlib import pyplot as plt
from urlextract import URLExtract
from collections import Counter
import pandas as pd
import seaborn as sns


def fetch_stats(optionSelected, df):
    # array to store the total words
    words = []

    # filtering the dataframe
    if optionSelected != "Overall":
        df = df[df["user"] == optionSelected]

    # number of total messages
    numMessages = df.shape[0]

    # number of total words
    for message in df["messages"]:
        words.extend(message.split())
    numWords = len(words)

    # total media
    numMedia = df[df["messages"] == "<Media omitted>\n"].shape[0]

    # total links
    urls = []
    extractor = URLExtract()
    for message in df["messages"]:
        urls.extend(extractor.find_urls(message))
    numLinks = len(urls)

    return numMessages, numWords, numMedia, numLinks


def most_busy_users(df, st):
    busiestUsers = df["user"].value_counts().head(10)
    fig, ax = plt.subplots()
    name = busiestUsers.index
    count = busiestUsers
    ax.bar(name, count)
    plt.xticks(rotation=90)
    st.pyplot(fig)


def most_busy_usersdf(df, st):
    busiestUsers = round((df["user"].value_counts() / df.shape[0]) * 100, 3).reset_index()
    busiestUsers.rename(columns={"index": "user"}, inplace=True)
    st.dataframe(busiestUsers)


def words_df(optionSelected, df, st):
    # filtering the dataframe
    if optionSelected != "Overall":
        df = df[df["user"] == optionSelected]

    words = []
    for message in df["messages"]:
        words.extend(message.split())

    mostCommonWords = Counter(words).most_common(20)
    df2 = pd.DataFrame(mostCommonWords)
    # removing group messages
    temp = df[df["user"] != "group_notification"]
    # removing media omitted
    temp = temp[temp["messages"] != "<Media omitted>\n"]
    # removing stop words
    f = open("stop_hinglish.txt", "r")
    stopHinglish = f.read()
    words = []
    for message in temp["messages"]:
        for word in message.lower().split():
            if word not in stopHinglish:
                words.append(word)

    mostCommonWords = Counter(words).most_common(20)
    mostCommonWords = pd.DataFrame(mostCommonWords, columns=["word", "count"])
    fig, ax = plt.subplots()
    ax.barh(mostCommonWords["word"], mostCommonWords["count"])
    st.pyplot(fig)


def timeline(optionSelected, df, st):
    # filtering the dataframe
    if optionSelected != "Overall":
        df = df[df["user"] == optionSelected]

    # activity stats
    activedays = df["day_name"].value_counts()
    activemonths = df["month"].value_counts()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most Active Days")
        fig, ax = plt.subplots()
        ax.bar(activedays.index, activedays.values)
        st.pyplot(fig)

    with col2:
        st.subheader("Most Active Months")
        fig, ax = plt.subplots()
        ax.bar(activemonths.index, activemonths.values)
        plt.xticks(rotation=90)
        st.pyplot(fig)


    st.title("Timeline")
    timeline = df.groupby(["year", "month_num", "month"]).count()["messages"].sort_values(ascending=False).reset_index()
    # merging year and month
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))
    timeline["time"] = time

    fig, ax = plt.subplots()
    ax.plot(timeline["time"], timeline["messages"])
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # timeline day
    timelinegrid = df.groupby("onlydate").count()["messages"].reset_index()
    fig, ax = plt.subplots()
    ax.plot(timelinegrid["onlydate"], timelinegrid["messages"])
    plt.xticks(rotation=90)
    plt.figure(figsize=(18,10))
    st.pyplot(fig)


def heatmap(optionSelected, df, st):
    st.title("Activity HeatMap")
    # filtering the dataframe
    if optionSelected != "Overall":
        df = df[df["user"] == optionSelected]

    activityHeatmap = df.pivot_table(index="day_name", columns="period", values="messages", aggfunc="count").fillna(0)
    fig, ax = plt.subplots()
    ax = sns.heatmap(activityHeatmap)
    st.pyplot(fig)

