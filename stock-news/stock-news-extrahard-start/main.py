import requests
from datetime import date, timedelta, datetime
import smtplib

now = datetime.now()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
parameters = {"function": "TIME_SERIES_DAILY", "symbol": STOCK, "apikey": "KWM78OQN145VV3LZ"}
yesterday = str(date.today() - timedelta(days=1))
day_before_day = str(date.today() - timedelta(days=2))
EMAIL = "testmail6587189@gmail.com"
PASSWORD = "Sairam@123"
# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()

if now.strftime("%A") == "Monday" or "Tuesday" or "Saturday" or "Sunday":
    print("Market were on leave")

else:
    close_value_today = float(data['Time Series (Daily)'][yesterday]['4. close'])
    close_value_previous_day = float(data['Time Series (Daily)'][day_before_day]['4. close'])
    percentage_difference = (abs(close_value_today - close_value_previous_day) / close_value_today) * 100
    if percentage_difference > 5:
        news_parameters = {"apiKey": "aec00a74520d44e5a49d89ea78604da2", "qInTitle": COMPANY_NAME}
        news_request = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
        news = news_request.json()["articles"]
        three_articles = news[3::]
        formatted_news = format(str({f"\nHeadline:{article['title']}.\n brief:{article['description']}," for article in
                                     three_articles}).encode('utf-8'))
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(to_addrs=EMAIL, msg=f"subject: News for the day \n\n {formatted_news}", from_addr=EMAIL)
# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
