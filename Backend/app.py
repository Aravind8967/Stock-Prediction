from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from src import SharePricePrediction, PredictValues, CompaniesDB

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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

@app.route('/<c_name>/getCompany')
def getCompany(c_name):
    try:
        c_db = CompaniesDB()
        c_details = c_db.searchName(c_name)
        if c_details['status'] == 200:
            return jsonify(c_details)
        else:
            return jsonify({'status': 404, 'data': 'Company not found'}), 404
    except Exception as e:
        print(f"Error fetching company details: {e}")
        return jsonify({'status': 500, 'data': 'Internal server error'}), 500

@app.route('/suggestions')
def getSuggestions():
    query = request.args.get('query')
    if query:
        c_db = CompaniesDB()
        suggestions = c_db.getNameSuggestions(query)
        return jsonify({'status' : 200, 'data': suggestions})

    return jsonify({'status' : 404, 'data': 'Missing query parameter'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    # print(getFundamentals('ITC', 5))