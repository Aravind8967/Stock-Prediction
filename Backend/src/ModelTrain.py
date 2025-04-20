from .FindValues import FindValues
from neuralprophet import NeuralProphet, set_log_level, save
import pandas as pd
import json


class ModelTrain:
    def __init__(self, c_list, model_name, traing_set):
        self.c_list = c_list
        self.model_name = model_name
        self.traing_set = traing_set
        self.companies_df = self.companiesToDF()

    def companiesToDF(self):
        companies_df = {}
        count = 1
        for c_name in self.c_list:
            try: 
                details = FindValues(c_name)
                data = details.getCompanyDetails()
                df = pd.DataFrame({
                    'ds' : pd.to_datetime(data['years'], format='%Y'),
                    'y' : data[self.traing_set],
                    'ID' : c_name
                })
                companies_df[c_name] = df
                print(f'{count} : {c_name} : added to the dict')
                count += 1
            except Exception as e:
                print(f'{c_name} : error company :{e}')
        return companies_df

    def trainModel(self):
        print("model traing started")
        df_all = pd.concat(self.companies_df.values(), ignore_index=True)
        set_log_level("ERROR")
        
        model = NeuralProphet(
            trend_global_local="global",
            season_global_local="local",
        )

        matrics = model.fit(df_all, freq='Y')
        print('model training done')
        
        save(model, f'Models/{self.model_name}.np')
        print('model saved successfully')


if __name__ == '__main__':
    c_list = []
    with open('companies_list.json', 'r') as file:
        companies = json.load(file)
    
    count = 1
    
    for company in companies: 
        c_list.append(company['c_symbol'])
        print(f'{count} : {company} : added to list')
        count += 1

    model = ModelTrain(c_list, model_name='globle_revenue_model', traing_set='revenue')
