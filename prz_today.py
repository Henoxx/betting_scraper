"""
Scrap major football leagues predictions from
https://www.predictz.com
Developed by @Henoxx
"""

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import datetime, json

DATE = datetime.datetime.now().strftime('%Y-%m-%d')
LINK = "https://www.predictz.com/predictions/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
STAKES = {"Draw": "X", "Away": "2", "Home": "1"}

class Predictz():
    def __init__(self, data=None, table_form=None):
        self.data = data
        self.table_form = table_form

    def __str__(self):
        self.message = f"{DATE}(TODAY) https://predictz.com Football predictions.\nCheck prz_{DATE}.json file after writing data."
        return self.message
    
    def write_data(self, file_name=f'prz_{DATE}.json'):
        self.file_name = file_name
        self.file_handler = open(self.file_name, 'w')
        self.file_handler.write(json.dumps(self.data, indent=4))
        self.file_handler.close()

        return print(f"{self.file_name} saved.")
    
    @classmethod
    def get(cls):
        # Variable Declarations
        fixtures, predictions, scores, data = [],[],[],{}
        fixt_data, league_data = {},{}

        # Fetching soup data
        url = LINK
        res = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(class_='pttable')

        league_title = ''
        league_title_flag = 'flag'
        for child in content(class_='pttr'):
            try:
                league_title = child.find(class_='ptgame').a.attrs['href'].split('/')[5]
                league_title_rep = child.find(class_='ptgame').a.attrs['href'].split('/')[4]

                if league_title != league_title_flag and fixtures != []:
                    table_form = {"Fixtures": fixtures, "Predictions":predictions , "Scores": scores}
                    print('-'*10, league_title_flag + f'{[DATE]}' +'-'*10)
                    print(tabulate(table_form, headers="keys", tablefmt='grid'))
                    print()
                    fixt_data = {}
                    fixtures, predictions, scores = [],[],[]

                fixture = child.find(class_='ptgame').a.string
                fixtures.append(fixture)

                pred_all = child.find(class_='ptprd').div.string.split(' ')
                pred = pred_all[0]
                predictions.append(pred)

                score = pred_all[1]
                scores.append(score)

                

                fixt_data[fixture] = {"Stake": STAKES[pred], "score":score}
                if league_title not in league_data.keys():
                    league_data[league_title] = fixt_data
                else:
                    league_title_rep = league_title_rep + '-' + league_title
                    print(league_title_rep)
                    league_data[league_title_rep] =fixt_data

                data[DATE] = league_data
                league_title_flag = child.find(class_='ptgame').a.attrs['href'].split('/')[5]
            except:
                pass
        else:
            # When process finishes without break the last league is displaied here.
            table_form = {"Fixtures": fixtures, "Predictions":predictions , "Scores": scores}
            print('-'*10, league_title_flag + f'{[DATE]}' +'-'*10)
            print(tabulate(table_form, headers="keys", tablefmt='grid'))
            print()
            fixt_data = {}
            fixtures, predictions, scores = [],[],[]

        return cls(data, table_form)


def main():
    todays_data = Predictz.get()
    todays_data.write_data()
    print(todays_data)

if __name__ == "__main__":
    main()