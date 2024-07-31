import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

# putting a file uploader in the sidebar
uploadFile = st.sidebar.file_uploader("Choose a File")
if uploadFile is not None:
    bytesData = uploadFile.getvalue()
    # converting this bytedata to string
    data = bytesData.decode("utf-8")
    # getting the dataframe from preprocess.py
    df = preprocessor.preprocessor(data)


    # fetch unique users
    userList = df["user"].unique().tolist()
    userList.remove("group_notification")
    userList.sort()
    userList.insert(0, "Overall")
    optionSelected = st.sidebar.selectbox("Show Analysis for ", userList)

    # stats
    numMessages, numWords, numMedia, numLinks = helper.fetch_stats(optionSelected, df)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Total Messages")
        st.title(numMessages)

    with col2:
        st.subheader("Total Words")
        st.title(numWords)

    with col3:
        st.subheader("Total Media")
        st.title(numMedia)

    with col4:
        st.subheader("Total Links")
        st.title(numLinks)

    # finding the busiest users
    if optionSelected == "Overall":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Active Persons")
            helper.most_busy_users(df, st)

        with col2:
            st.subheader("Most Active Persons")
            helper.most_busy_usersdf(df, st)

    # timeline
    helper.timeline(optionSelected, df, st)

    # heatmap
    helper.heatmap(optionSelected, df, st)

    # # Word Cloud
    # st.title("Word Cloud")
    # helper.create_wordcloud(optionSelected, df, st)

    #  most common words
    st.title("Most Common Words")
    helper.words_df(optionSelected, df, st)


