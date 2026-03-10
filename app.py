from flask import Flask, render_template, request, jsonify
from getstock import get_data, strtonum

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ticker = data.get('ticker', '').strip().upper()

    if not ticker or not ticker.isalnum() and '.' not in ticker:
        return jsonify({'error': 'Invalid ticker symbol.'}), 400

    stock = get_data(ticker)
    if stock is None:
        return jsonify({'error': f'No statistics accessible for {ticker}. Please check the ticker symbol.'}), 404

    # Run analysis
    result = run_analysis(stock)
    return jsonify(result)


def run_analysis(stock):
    """Analyze a stock dict and return structured results."""
    raw = dict(stock)  # keep original for display
    display = {
        'ticker': raw['ticker'],
        'name': raw['name'],
        'price': raw['price'],
        'desc': raw['desc'],
    }

    converted = strtonum(dict(stock))
    score = 0
    checks = []

    # Undervalued check (3 pts)
    if isinstance(converted.get('5YADY'), float) and isinstance(converted.get('FADY'), (int, float)) and converted['FADY'] > converted['5YADY']:
        score += 3
        checks.append({'metric': 'Undervalued (FADY > 5YADY)', 'value': f"{raw['FADY']} > {raw['5YADY']}", 'passed': True, 'points': 3})
    else:
        checks.append({'metric': 'Undervalued (FADY > 5YADY)', 'value': f"{raw.get('FADY', 'N/A')} vs {raw.get('5YADY', 'N/A')}", 'passed': False, 'points': 0})

    # P/E check (2 pts)
    if converted.get('P/E') != 'N/A' and isinstance(converted.get('P/E'), (int, float)) and converted['P/E'] <= 25:
        score += 2
        checks.append({'metric': 'P/E Ratio (≤ 25)', 'value': raw['P/E'], 'passed': True, 'points': 2})
    else:
        checks.append({'metric': 'P/E Ratio (≤ 25)', 'value': raw.get('P/E', 'N/A'), 'passed': False, 'points': 0})

    # P/B check (1 pt)
    if isinstance(converted.get('P/B'), (int, float)) and converted['P/B'] <= 3:
        score += 1
        checks.append({'metric': 'P/B Ratio (≤ 3)', 'value': raw['P/B'], 'passed': True, 'points': 1})
    else:
        checks.append({'metric': 'P/B Ratio (≤ 3)', 'value': raw.get('P/B', 'N/A'), 'passed': False, 'points': 0})

    # EPS check (1 pt)
    if isinstance(converted.get('EPS'), (int, float)) and converted['EPS'] <= 8:
        score += 1
        checks.append({'metric': 'EPS (≤ 8)', 'value': raw['EPS'], 'passed': True, 'points': 1})
    else:
        checks.append({'metric': 'EPS (≤ 8)', 'value': raw.get('EPS', 'N/A'), 'passed': False, 'points': 0})

    # D/E check (1 pt)
    if isinstance(converted.get('D/E'), (int, float)) and converted['D/E'] <= 70:
        score += 1
        checks.append({'metric': 'D/E Ratio (≤ 70%)', 'value': raw['D/E'], 'passed': True, 'points': 1})
    else:
        checks.append({'metric': 'D/E Ratio (≤ 70%)', 'value': raw.get('D/E', 'N/A'), 'passed': False, 'points': 0})

    # PR check (1 pt)
    if isinstance(converted.get('PR'), (int, float)) and converted['PR'] <= 75:
        score += 1
        checks.append({'metric': 'Payout Ratio (≤ 75%)', 'value': raw['PR'], 'passed': True, 'points': 1})
    else:
        checks.append({'metric': 'Payout Ratio (≤ 75%)', 'value': raw.get('PR', 'N/A'), 'passed': False, 'points': 0})

    # CR check (1 pt)
    if isinstance(converted.get('CR'), (int, float)) and converted['CR'] >= 1:
        score += 1
        checks.append({'metric': 'Current Ratio (≥ 1)', 'value': raw['CR'], 'passed': True, 'points': 1})
    else:
        checks.append({'metric': 'Current Ratio (≥ 1)', 'value': raw.get('CR', 'N/A'), 'passed': False, 'points': 0})

    percentage = (score / 10) * 100
    if percentage >= 70:
        verdict = 'Strong Buy'
    elif percentage >= 50:
        verdict = 'Consider'
    elif percentage >= 30:
        verdict = 'Weak'
    else:
        verdict = 'Avoid'

    return {
        'display': display,
        'checks': checks,
        'score': score,
        'total': 10,
        'percentage': percentage,
        'verdict': verdict,
    }


if __name__ == '__main__':
    app.run(debug=True)
