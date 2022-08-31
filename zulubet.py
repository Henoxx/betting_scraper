"""
Scrap major football leagues predictions from
https://www.zulubet.com/
Developed by @Henoxx
"""
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate



HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

url_all = "https://www.zulubet.com/"
major_league_names = ['England Premier League', 'Italy Serie A']




class Zulubet:
    def __init__(self):
        self.fixtures = []
        self.predictions = []
        self.stakes = []
        self.data_dict = {}

    def convert_to_text(self, pred):
        pred = str(pred).lower()
        try:
            if pred == '1':
                pred = 'Home Win'
            elif pred == '1x':
                pred = 'Home or Draw'
            elif pred == '2':
                pred = 'Away Win'
            elif pred == '2x':
                pred = 'Away or Draw'
            elif pred == 'x':
                pred = 'Draw'
        except:
            pred = 'Unknown'
        
        return pred


    def get(self, url=url_all):
        res = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(res, 'html.parser')

        table_rows = soup.find(class_="content_table")
         
        c = 0
        for row in table_rows:
            try:
                league_name = row.img.attrs['title']
                if league_name in major_league_names:
                    fixt = row.span.a.string
                    self.fixtures.append(fixt)
                    tds = row.find_all('td')
                    stake = self.convert_to_text(tds[9].string)
                    self.stakes.append(stake)
                    self.data_dict[fixt] = {'Stake': stake, 'Prediction': None}
            except:
                pass
        table_form = {"Fixtures": self.fixtures, "Stake": self.stakes, "Prediction": self.predictions}
        return(table_form)

def main():
    data = Zulubet()
    data = data.get()
    print(tabulate(data, headers="keys"))
 
if __name__ == "__main__":
    main()