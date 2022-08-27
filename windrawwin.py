"""
Scrap major football leagues predictions from
https://www.windrawwin.com
Developed by @Henoxx
"""
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

EPL_URL = "https://www.windrawwin.com/tips/england-premier-league/"
LALIGA_URL = "https://www.windrawwin.com/tips/spain-la-liga/"
MAJOR_LEAGUES = [EPL_URL, LALIGA_URL]
#  Add more links here

STAKE_RANKS = ["Small", "Medium", "Large"]
STAKES = ["Draw", "Away Win", "Home Win"]


class WinDrawWin():
    def __init__(self):
        self.fixtures = []
        self.stake_rank = []
        self.predictions = []
        self.stakes = []
        self.data_dict = {}
    def raw_data(self, url):
        self.res = requests.get(url, headers=headers).text
        self.soup = BeautifulSoup(self.res, 'html.parser')

        self.table_rows = self.soup.find(class_="widetable").find_all('tr')
        
        return self.table_rows
    
    def get(self, url=EPL_URL):
        for row in self.raw_data(url):
            try:
                fixt = ''.join(list(row.find_all(class_ = "fixt")[0].a.strings))
                self.fixtures.append(fixt)
                
                for td in row.find_all('td'):
                    if td.string in STAKE_RANKS:
                        stake_r = td.string
                        self.stake_rank.append(td.string)
                    elif td.string in STAKES:
                        stks = td.string
                        self.stakes.append(td.string)
                pred = row.find_all(class_="sp")[0].string
                self.predictions.append(pred)
                self.data_dict[fixt] = {'stake_rank':stake_r, 'stakes':stks, 'prediction':pred}
            except:
                pass
        # Tabulate type of return but not good
        # return {"Fixtures": self.fixtures, "Stake Ranks": self.stake_rank, "Stake": self.stakes, "Prediction": self.predictions}
        table_form = {"Fixtures": self.fixtures, "Stake Ranks": self.stake_rank, "Stake": self.stakes, "Prediction": self.predictions}
        return {'dict': self.data_dict, 'table': table_form}
    # TODO: return values for tabulate
    # TODO: let the user choose the league when calling get method