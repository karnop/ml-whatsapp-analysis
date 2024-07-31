import re
import pandas as pd


def preprocessor(data):
    # separating messages
    datepattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202f[AP]M\s-\s'
    messages = re.split(datepattern, data)[1:]
    # seperating date
    date = re.findall(datepattern, data)
    # making the dataframe
    df = pd.DataFrame({"user_message": messages, "message_date": date})
    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M\u202f%p - ")
    df.rename(columns={"message_date": "date"}, inplace=True)
    # seperating users and messages from the user_message col
    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split('([\w\W]+?):\s', message)
        # user name
        if (entry[1:]):
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["messages"] = messages
    df.drop(columns=["user_message"], inplace=True)
    # seperating month, year
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["minute"] = df["date"].dt.minute
    df["hour"] = df["date"].dt.hour
    df["month_num"] = df["date"].dt.month
    df["onlydate"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()

    # for heatmap
    period = []
    for hour in df[["day_name","hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period
    return df