import requests
from bs4 import BeautifulSoup
import re

# Portfolio analysis functionality 
# portfolio_url = input('Paste the link to the url of the portfolio you would like to analyze here: ')

def get_data(ticker):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    stats_url = f'https://ca.finance.yahoo.com/quote/{ticker}/key-statistics' # if there is no stats page it will redirect but idk if this will work w scrapper
    profile_url = f'https://ca.finance.yahoo.com/quote/{ticker}/profile'
    r = requests.get(stats_url, headers=headers)
    r_profile = requests.get(profile_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_profile = BeautifulSoup(r_profile.text, 'html.parser')

    all_stats = soup.findAll('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})

    stock = {
        'ticker': ticker,
        'name': re.sub(r' \(.*\)', '', soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text),
        'price': soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text,
        'desc': soup_profile.find('p', {'class': 'Mt(15px) Lh(1.6)'}).text,

        # Trailing P/E
        'P/E': all_stats[2].text,
        # Price/Book (mrq - most recent quarter)
        'P/B': all_stats[6].text,
        # Diluted EPS (ttm - trailing twelve months)
        'EPS': all_stats[50].text,
        # Total Debt/Equity (mrq)
        'D/E': all_stats[55].text,
        # Forward Annual Dividend Yield
        'FADY': all_stats[29].text,
        # 5 Year Average Dividend Yield
        '5YADY': all_stats[32].text,
        # Payout Ratio
        'PR': all_stats[33].text
    }

    return stock

print(get_data('GFL.TO'))

# If no stats page then look at performance of last 5-year or risk and if no risk don't buy

#algo: 
# forward P/E ---> P/E Ratio <= 25
# Price/Book ----> P/B Ratio <= 3
# Diluted EPS ---> EPS <= 8%
# Total Debt/Equity (mrq) <= 70%
# forward Dividend & Yield > 
# 5 Year Average Dividend Yield -> Undervalued
# Payout ratio <= 75%

# EXTRA: 
# ?Look at Analysis/ recommendation rating????
# ?Historical data for 5 years, take first and last value and see if current is higher than 5 yrs ago
# ?Give score on stocks