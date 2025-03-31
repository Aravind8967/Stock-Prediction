from .APICall import CompanyDetails
from .FindValues import FindValues
from .PredictValues import PredictValues
from .sharePricePrediction import SharePricePrediction


class Analyse:
    def __init__(self, c_name):
        self.c_name = c_name
        self.company_details = SharePricePrediction(self.c_name)
        self.predict_values = PredictValues(self.c_name)

    def values(self):
        return self.predict_values.getFutureValues(10)

if __name__ == '__main__':
    c_name = 'ITC'
    analyse = Analyse(c_name)
    current_values = analyse.getAPIValues()
    future_values = analyse.predictionValues()
    for c_value in current_values:
        print(f'Previous {c_value} : {current_values[c_value]}')

    print('=============================================================================')

    for f_value in future_values:
        print(f'Future {f_value} : {future_values[f_value]}')