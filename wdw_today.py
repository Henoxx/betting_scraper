"""
Scrap major football leagues predictions from
https://www.windrawwin.com
Developed by @Henoxx
"""

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import datetime, json

DATE = datetime.datetime.now().strftime('%Y-%m-%d')
LINK = "https://www.windrawwin.com/predictions/today/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
STAKES = {"Draw": "X", "Away Win": "2", "Home Win": "1"}

class WinDrawWin():
    def __init__(self, data=None, table_form=None):
        self.data = data
        self.table_form = table_form

    def __str__(self):
        self.message = f"{DATE} Football predictions.\nCheck wdw_{DATE}.json file after writing data."
        return self.message
    
    def write_data(self, file_name=f'wdw_{DATE}.json'):
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
        league_ids = {'England%20Premier%20League':'premier-league',
                      'Italy%20Serie%20A':'serie-A',
                      'Spain%20La%20Liga':'la-liga',
                      'Germany%20Bundesliga':'bundesliga'}

        # Fetching soup data
        url = LINK
        res = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(id='content')
        contentfull = content.find_all(class_='contentfull')[1]

        # Fetching datas
        for league in league_ids.keys():
            try:
                # Fetching rows
                league_title = league_ids[league]
                league = contentfull.find(id=league)
                fixt_table = league.find_next_sibling(class_='wdwtablest')
                fixt_table_rows = fixt_table.find_all(class_='wttr')

                # Fetching each info
                for row in fixt_table_rows:
                    fixture = row.find(class_='wtl5fcont')
                    try:
                        fixture = ''.join(list(fixture.find(class_='wtfixt').a.strings))
                        fixtures.append(fixture)
                        
                        prediction = row.find(class_='wtprd').string
                        predictions.append(prediction)

                        score = row.find(class_='wtsc').string
                        scores.append(score)

                        fixt_data[fixture] = {"Stake": STAKES[prediction], "Score": score}
                        league_data[league_title] = fixt_data
                        data[DATE] = league_data
                    
                    except:
                        pass

                table_form = {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}
                print('-'*10, league_title + f'{[DATE]}' +'-'*10)
                print(tabulate(table_form, headers="keys", tablefmt='grid'))
                print()

                # clear data holders for the purpouse of adding new data.
                fixt_data = {}
                fixtures, predictions, scores = [],[],[]
            except:
                pass
        
        return cls(data, table_form)



def main():
    todays_data = WinDrawWin.get()
    todays_data.write_data()
    print(todays_data)

if __name__ == "__main__":
    main()