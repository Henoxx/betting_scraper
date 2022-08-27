"""
Scrap major football leagues predictions from
https://www.predictz.com
Developed by @Henoxx
"""
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

EPL_URL = "https://www.predictz.com/predictions/england/premier-league/"
LALIGA_URL = "https://www.predictz.com/predictions/spain/la-liga/"
BUN_URL = "https://www.predictz.com/predictions/germany/bundesliga/"
MAJOR_LEAGUES = [EPL_URL, LALIGA_URL, BUN_URL]

class Predictz():
    def __init__(self,fixtures=None, stakes=None, predictions=None, data_dict=None, table_form=None):
        self.fixtures = fixtures
        self.stakes = stakes
        self.predictions = predictions
        self.data_dict = data_dict
        self.table_form = table_form

    def __str__(self):
        try:
            return str(tabulate(self.table_form, headers="keys"))
        except:
            return "Some Error occured!"

    @classmethod
    def get(cls, url=BUN_URL):
        if url == 'epl':
            url = EPL_URL
        
        fixtures = []
        stakes = []
        predictions = []
        data_dict = {}
        res = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(res, 'html.parser')

        table_rows = soup.find(class_="pztable")


        for row in table_rows:
            try:
                fixt = ''.join(list(row.find_all(class_="fixt")[0].a.strings))
                fixtures.append(fixt)
                pred = row.contents[0].string
                stake = pred.split(' ')[0]
                if stake.lower() != "draw":
                    stake += " Win"
                stakes.append(stake)
                predictions.append(pred.split(' ')[1])
                data_dict[fixt] = {'Stake': stake, 'Prediction': pred.split(' ')[1]}
            except:
                pass

        table_form = {"Fixtures": fixtures, "Stake": stakes, "Predictions":predictions}
        return cls(fixtures, stakes, predictions, data_dict, table_form)