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

def main():
    fixtures, predictions, scores, data = [],[],[],{}
    url = LINK
    res = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(res, 'html.parser')
    fixt_data = {}
    league_data = {}
    league_ids = {'England%20Premier%20League':'epl','Italy%20Serie%20A':'serie-A','Spain%20La%20Liga':'laliga', 'Germany%20Bundesliga':'bun'}
    
    content = soup.find(id='content')
    contentfull = content.find_all(class_='contentfull')[1]
    
    for league in league_ids.keys():
        try:
            league_title = league_ids[league]
            league = contentfull.find(id=league)
            fixt_table = league.find_next_sibling(class_='wdwtablest')
            fixt_table_rows = fixt_table.find_all(class_='wttr')
            for row in fixt_table_rows:
                fixture = row.find(class_='wtl5fcont')
                try:
                    fixture = ''.join(list(fixture.find(class_='wtfixt').a.strings))
                    fixtures.append(fixture)
                    pred = row.find(class_='wtprd').string
                    predictions.append(pred)
                    score = row.find(class_='wtsc').string
                    scores.append(score)
                    fixt_data[fixture] = {"Stake": STAKES[pred], "score":score}
                    league_data[league_title] = fixt_data
                    data[DATE] = league_data
                    write_data(data)
                except:
                    pass
            fixt_data = {}
            table_form = {"Fixtures": fixtures, "Predictions":predictions, "Scores": scores}
            print('-'*10, league_title + f'{[DATE]}' +'-'*10)
            print(tabulate(table_form, headers="keys", tablefmt='grid'))
            print()
            fixtures, predictions, scores = [],[],[]
        except:
            pass

def write_data(data, file_name=f'{DATE}.json'):
    file_name = file_name
    data = data
    fh = open(file_name, 'w')
    fh.write(json.dumps(data, indent=4))
    fh.close()
    
    


if __name__ == "__main__":
    main()