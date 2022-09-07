import json, datetime, csv
from scraper import Predictz, WinDrawWin, DATE
from tabulate import tabulate

wdw_obj = WinDrawWin.get()
prz_obj = Predictz.get()
wdw_today = wdw_obj.data[DATE]
prz_toady = prz_obj.data[DATE]
# Fix the zulu bet in scraper.py and add it here.


def file_handler(file_name):
    fh = open(file_name)
    raw_data = fh.read()
    fh.close()
    return raw_data

# Not like this to load the data
zul_today = json.loads(file_handler(f'{DATE}(zul).json'))[DATE]

websites_data_list = [wdw_today,prz_toady,zul_today]

stakes_list = []
data_list = []

# CSV writer.
output_data = open(f'output{DATE}.csv', 'w', newline='\n')
output_writer = csv.writer(output_data)
output_headers = ['Date','League Name', 'Fixtures', 'Windrawwin', 'Predictz', 'Zulubet', 'Home Win', 'Draw', 'Away Win']
output_writer.writerow(output_headers)

# zulubet website got different team naming style... I used this procedure to compare the names
def check_zulu(league_name, match):
    team_name_fragments = match.split(' ')
    for team_name_fragment in team_name_fragments:
        for zul_match in list(zul_today[league_name].keys()):
            if team_name_fragment in zul_match.split(' '):
                return zul_match

# Analysis done in this function
def analayze(stakes_list):
    win, draw, lose = 0, 0, 0
    not_found = []
    for val in stakes_list:
        if val == '1':
            win += 1
        elif val == '2':
            lose += 1
        elif val == 'X':
            draw += 1
        elif val == '1X' or val == 'X1':
            win += 0.5
            draw += 0.5
        elif val == '2X' or val == 'X2':
            lose += 0.5
            draw += 0.5
        elif val == '12' or val == '21':
            lose += 0.5
            win += 0.5
        elif val == 'None':
            not_found.append(val)
    else:
        try:
            total_data = len(stakes_list) - len(not_found)
            win = (win/total_data) * 100
            lose = (lose/total_data) * 100
            draw = (draw/total_data) * 100
            # print(f"Win: {round(win,2)}%, Draw: {round(draw,2)}%, Lose:{round(lose,2)}%")
            return [round(win,2), round(draw,2), round(lose,2)]
        except:
            print('on try')
            pass

def create_csv():
    global stakes_list
    global data_list
    for league_name in wdw_today.keys():
        matches = list(wdw_today[league_name].keys())  
        for match in matches:
            for website_data in websites_data_list:
                try:
                    orginal_match = match
                    if website_data == zul_today:
                        match = check_zulu(league_name, match)
                        if match == None:
                            match = orginal_match

                    stake = website_data[league_name][match]["Stake"]
                    stakes_list.append(stake)
                    match = orginal_match
                except:
                    stake = 'None'
                    stakes_list.append(stake)
            data_list.append(DATE)
            data_list.append(league_name)
            data_list.append(match)
            for i in stakes_list:
                data_list.append(i)
            else:
                # analysis here.
                for j in analayze(stakes_list):
                    data_list.append(j)
            
            output_writer.writerow(data_list)

            data_list = []
            stakes_list = []
    else:
        output_data.close()
        print('Data successfully written.')

def main():
    ...


if __name__ == '__main__':
    create_csv()
    wdw_obj.write_data()
    prz_obj.write_data()

