import requests
from bs4 import BeautifulSoup
import re

# Portfolio analysis functionality 
# portfolio_url = input('Paste the link to the url of the portfolio you would like to analyze here: ')

def strtonum(dict):
    # Keys to be exculded from being converted to numbers
    excluded = ['ticker', 'name', 'price', 'desc']

    for key, value in dict.items():
        if key in excluded or value == 'N/A':
            print(f'The value for {key} is listed as "N/A" or is an excluded key')
            continue
        # Convert to int
        try:
            value = value.replace(',','').replace('%','')
            dict[key] = int(value)
        except ValueError:
            # Convert to float
            try:
                dict[key] = float(value)
            except ValueError:
                print(f'Unable to convert {value} to num')
    return dict

def get_data(ticker):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    URL = f'https://ca.finance.yahoo.com/quote/{ticker}'
    stats_url = f'https://ca.finance.yahoo.com/quote/{ticker}/key-statistics'
    profile_url = f'https://ca.finance.yahoo.com/quote/{ticker}/profile'
    r_norm = requests.get(URL, headers=headers)
    r = requests.get(stats_url, headers=headers)
    r_profile = requests.get(profile_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_profile = BeautifulSoup(r_profile.text, 'html.parser')

    # Error checking if there is a Stats page
    has_stats = BeautifulSoup(r_norm.text, 'html.parser').find('li', {'data-test': 'STATISTICS'}) != None
    if not has_stats:
        print(f'No stats accessible for {ticker}')
        return None

    all_stats = soup.findAll('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})

    stock = {
        'ticker': ticker,
        'name': re.sub(r' \(.*\)', '', soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text),
        'price': f"${soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text} CAD",
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

    print(f'Data collected from {stock["name"]}')

    return stock

#algo: 
# forward P/E ---> P/E Ratio <= 25
# Price/Book ----> P/B Ratio <= 3
# Diluted EPS ---> EPS <= 8%
# Total Debt/Equity (mrq) <= 70%
# forward Dividend & Yield > 
# 5 Year Average Dividend Yield -> Undervalued
# Payout ratio <= 75%
def algo_analysis(dict):
    score = 0
    dict = strtonum(dict)
    # 2 points
    if dict['P/E'] <= 25:
        score +=2
        print('P/E is valid')
    if dict['P/B'] <= 3:
        score +=1
        print('P/B is valid')
    if dict['EPS'] <= 8:
        score +=1
        print('EPS is valid')
    if dict['D/E'] <= 70:
        score +=1
        print('D/E is valid')
    # 3 points
    if dict['FADY'] > dict['5YADY']:
        score +=3
        print('This stock is undervalued (FADY > 5YADY)!')
    if dict['PR'] <= 75:
        score +=1
        print('PR is valid')

    # Total = 9 points
    print(f'The score for this stock is {score}/9 => {(score/9)*100}%')
    return score

def main():
    stock_to_search = input('Enter a ticker symbol: ')
    stock_dict = get_data(stock_to_search)
    # If the stock dictionary isn't None
    if stock_dict:
        print(f'Getting stock data for {stock_to_search}...\n{stock_dict}\n')
        return algo_analysis(stock_dict)


if __name__ == '__main__':
    main()


# EXTRA: 
# Portfolio functionality
# ?Look at Analysis/ recommendation rating????
# If no stats page then look at performance of last 5-year or risk and if no risk don't buy
#   - ?Historical data for 5 years, take first and last value and see if current is higher than 5 yrs ago