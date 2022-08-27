"""
Scrap major football leagues predictions from
https://www.predictz.com
Developed by @Henoxx
"""
from bs4 import BeautifulSoup
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

EPL_URL = "https://www.predictz.com/predictions/england/premier-league/"
LALIGA_URL = "https://www.predictz.com/predictions/spain/la-liga/"
BUN_URL = "https://www.predictz.com/predictions/germany/bundesliga/"
MAJOR_LEAGUES = [EPL_URL, LALIGA_URL, BUN_URL]

class Predictz():
    def __init__(self):
        self.fixtures = []
        self.stakes = []
        self.predictions = []
        self.data_dict = {}

    def raw_data(self, url):
        self.res = requests.get(url, headers=HEADERS).text
        self.soup = BeautifulSoup(self.res, 'html.parser')

        self.table_rows = self.soup.find(class_="pztable")

        return self.table_rows

    def get(self, url=EPL_URL):
        for row in self.raw_data(url):
            try:
                fixt = row.find_all(class_="fixt")[0].string
                self.fixtures.append(fixt)
                pred = row.contents[0].string
                stake = pred.split(' ')[0]
                if stake.lower() != "draw":
                    stake += " Win"
                self.stakes.append(stake)
                self.predictions.append(pred.split(' ')[1])
                self.data_dict[fixt] = {'Stake': stake, 'Prediction': pred.split(' ')[1]}
            except:
                pass

        table_form = {"Fixtures": self.fixtures, "Stake": self.stakes, "Predictions":self.predictions}
        return table_form