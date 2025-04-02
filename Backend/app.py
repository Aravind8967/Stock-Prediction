from flask import Flask, jsonify
from flask_cors import CORS
import json
from src import SharePricePrediction, PredictValues

app = Flask(__name__)
CORS(app)


@app.route('/<c_name>/getSharePrice/<int:future_years>')
def getSharePrice(c_name, future_years):
    share_price_prediction = SharePricePrediction(company_name=c_name)
    share_price = share_price_prediction.SharePrice(future_years=future_years)
    previous_share_price = share_price['previous_share_price']
    future_share_price = share_price['future_share_price']
    
    # Parse JSON strings to Python dictionaries
    data = {
        'previous_share_price': json.loads(previous_share_price.to_json(orient='records', date_format='iso')),
        'future_share_price': json.loads(future_share_price.to_json(orient='records', date_format='iso'))
    }
    return jsonify(data)

@app.route('/<c_name>/getFundamentals/<int:future_years>')
def getFundamentals(c_name, future_years):
    predicted_values = PredictValues(c_name=c_name)
    fundamental_values = predicted_values.getFutureValues(future_year=future_years)
    print(fundamental_values)
    return jsonify(fundamental_values)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    # print(getFundamentals('ITC', 5))