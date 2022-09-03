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
LINK = "https://www.predictz.com/predictions/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
STAKES = {"Draw": "X", "Away": "2", "Home": "1"}

def main():
    fixtures, predictions, scores, data = [],[],[],{}
    url = LINK
    res = requests.get(url, headers=HEADERS).text
    print('Connected to server. Getting data...')
    soup = BeautifulSoup(res, 'html.parser')
    print('Exploring data...')
    fixt_data = {}
    league_data = {}
    data = {}
    content = soup.find(class_='pttable')
    
    league_title = ''
    league_title_flag = 'x'
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

            
            write_data(data)

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
        print('Finished.')
        print('Json file created.')


def write_data(data, file_name=f'{DATE}(prdz).json'):
    file_name = file_name
    data = data
    fh = open(file_name, 'w')
    fh.write(json.dumps(data, indent=4))
    fh.close()
    
    


if __name__ == "__main__":
    main()