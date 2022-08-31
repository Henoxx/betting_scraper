"""
Scrap major football leagues predictions from
https://www.windrawwin.com
Developed by @Henoxx
"""
import re, json
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
from pprint import pformat
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

EPL_URL = "https://www.windrawwin.com/tips/england-premier-league/"
LALIGA_URL = "https://www.windrawwin.com/tips/germany-bundesliga/"
MAJOR_LEAGUES = [EPL_URL, LALIGA_URL]
#  Add more links here

STAKES = {"Draw": "X", "Away Win": "2", "Home Win": "1"}

class WinDrawWin:
    def __init__(self, data=None, table_form=None):
        self.data = data
        self.table_form = table_form
    
    def __str__(self) -> str:
        try:
            return str(tabulate(self.table_form, headers="keys"))
        except:
            return "Some Error occured!"
    
    def __repr__(self) -> str:
        return "Data from windrawwin.com"

    def write_data(self, file_name='data.json'):
        file_name = file_name
        self.fh = open(file_name, 'w')
        # before_write = {'23-21-22':{'epl':None}}
        # before_write['23-21-22']['epl'] = self.data
        self.fh.write(json.dumps(self.data))
        self.fh.close()
        
        return print("File saved.")
    

    @classmethod
    def get(cls, url=MAJOR_LEAGUES[1]):
        fixtures, stakes, scores, data = [],[],[],{}

        res = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(res, 'html.parser')
        date_list = []
        fixt_data = {}

        table_rows = soup.find(class_="widetable").find_all('tr')
        for row in table_rows:
            try:

                if 'fw700' in row.td.attrs['class']:
                    date = str(row.td.string)
                    date_list.append(date)
                    print(date)
                    fixt_data = {}
                else:
                    print('inside_else')
                    fixt = ''.join(list(row.find_all('td', class_ = "fixt")[0].a.string))
                    print(fixt)
                    fixtures.append(fixt)
                
                    for td in row.find_all('td'):
                        if str(td.string) in list(STAKES.keys()):
                            stake = str(td.string)
                            stakes.append(STAKES[stake])
                            print(stake)

                    score = str(row.find_all('td', class_='sp')[0].string)
                    print(score)
                    scores.append(score)
                    fixt_data[fixt] = {"Stake": STAKES[stake], "score":score}
                    data[date] = fixt_data
                    # data[fixt] = {"Stake": STAKES[stake], "score":score}


                
                # data_['12-9-21'] ={'EPL': {
                #                     fixt: {"Stake": STAKES[stake], 
                #                            "score":score} }
                #                  }
            except:
                pass
            
        table_form = {"Fixtures": fixtures, "Stake": stakes, "Scores": scores}
        return cls(data, table_form)


def main():
    data = WinDrawWin.get()
    data.write_data('bundesliga.json')
    print(data)


if __name__ == "__main__":
    main()
