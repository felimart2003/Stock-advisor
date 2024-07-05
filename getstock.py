import requests
from bs4 import BeautifulSoup

portfolio_url = input('Paste the link to the url of the portfolio you would like to analyze here: ')

def get_data(ticker):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    stockinfo_url = f'https://ca.finance.yahoo.com/quote/{ticker}/'
    r = requests.get(stockinfo_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    stock = {
        'ticker': ticker,
        'price': ,
        'desc': ,
    }

# If no stats page then look at performance of last 5-year or risk and if no risk don't buy

#algo: 
# forward Dividend & Yield > 5 Year Average Dividend Yield -> Undervalued
# P/E Ratio <= 25
# P/B Ratio <= 3
# Payout ratio <= 75%
# EPS <= 8%
# Total Debt/Equity (mrq) <= 70%
# ?Look at Analysis/ recommendation rating????
# ?Historical data for 5 years, take first and last value and see if current is higher than 5 yrs ago