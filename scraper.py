"""
Scrap major football leagues predictions from
https://www.windrawwin.com
https://www.predictz.com
https://www.zulubet.com
Developed by @Henoxx https://www.henoxx.com
"""

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import datetime, json

DATE = datetime.datetime.now().strftime('%Y-%m-%d')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

LINK_PRZ = "https://www.predictz.com/predictions/"
LINK_WDW = "https://www.windrawwin.com/predictions/today/"
STAKES = {"Draw": "X", "Away": "2", "Home": "1"}
STAKES_WDW = {"Draw": "X", "Away Win": "2", "Home Win": "1"}

class Predictz():
    def __init__(self, data=None, table_form=None):
        self.data = data
        self.table_form = table_form

    def __str__(self):
        self.message = f"{DATE}(TODAY) https://predictz.com Football predictions.\nCheck prz_{DATE}.json file after writing data."
        return self.message
    
    def print_data(self):
        self.league_titles = self.table_form.keys()
        for league_title in self.league_titles:
            print('-'*10, league_title + f'{[DATE]}' +'-'*10)
            print(tabulate(self.table_form[league_title], headers="keys", tablefmt='grid'))
            print()
    
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
        fixt_data, league_data, table_form = {},{},{}

        # Fetching soup data
        url = LINK_PRZ
        print('Conecting...')
        res = requests.get(url, headers=HEADERS ,timeout=10).text
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(class_='pttable')
        print('Data found. Analyzing...')

        league_title = ''
        league_title_flag = 'flag'
        for child in content(class_='pttr'):
            try:
                league_title = child.find(class_='ptgame').a.attrs['href'].split('/')[5]
                league_title_rep = child.find(class_='ptgame').a.attrs['href'].split('/')[4]

                if league_title != league_title_flag and fixtures != []:
                    table_form = {league_title: {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}}
                    # print('-'*10, league_title_flag + f'{[DATE]}' +'-'*10)
                    # print(tabulate(table_form, headers="keys", tablefmt='grid'))
                    # print()
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
                    league_data[league_title_rep] =fixt_data

                data[DATE] = league_data
                league_title_flag = child.find(class_='ptgame').a.attrs['href'].split('/')[5]

            except:
                pass
        else:
            # When process finishes without break the last league is displaied here.
            # table_form = {"Fixtures": fixtures, "Predictions":predictions , "Scores": scores}
            # table_form ={league_title: {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}}
            # print('-'*10, league_title_flag + f'{[DATE]}' +'-'*10)
            # print(tabulate(table_form, headers="keys", tablefmt='grid'))
            # print()
            table_form ={league_title: {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}}
            fixt_data = {}
            fixtures, predictions, scores = [],[],[]

        return cls(data, table_form)

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

    def print_data(self):
        self.league_titles = self.table_form.keys()
        for league_title in self.league_titles:
            print('-'*10, league_title + f'{[DATE]}' +'-'*10)
            print(tabulate(self.table_form[league_title], headers="keys", tablefmt='grid'))
            print()
        
    @classmethod
    def get(cls):
        # Variable Declarations
        fixtures, predictions, scores, data = [],[],[],{}
        fixt_data, league_data, table_form = {},{},{}
        league_titles = []
        league_ids = {'England%20Premier%20League':'premier-league',
                      'Italy%20Serie%20A':'serie-A',
                      'Spain%20La%20Liga':'la-liga',
                      'Germany%20Bundesliga':'bundesliga',
                      'Champions%20League':'champions-league',
                      'South%20Korea%20K%20League%201':'k-league-1'}

        # Fetching soup data
        url = LINK_WDW
        print('Conecting...')
        res = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(id='content')
        contentfull = content.find_all(class_='contentfull')[1]
        print('Data found. Analyzing...')

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

                        fixt_data[fixture] = {"Stake": STAKES_WDW[prediction], "Score": score}
                        league_data[league_title] = fixt_data
                        data[DATE] = league_data
                    
                    except:
                        pass

                table_form ={league_title: {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}}

                # clear data holders for the purpouse of adding new data.
                fixt_data = {}
                fixtures, predictions, scores = [],[],[]
            except:
                pass
        
        return cls(data, table_form)


