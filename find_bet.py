import json, csv
from scraper import Predictz, WinDrawWin, DATE


file_names = [f'wdw_{DATE}.json', f'prz_{DATE}.json']
web_data_list = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def file_handler(file_name):
    fh = open(file_name)
    raw_data = fh.read()
    fh.close()
    return raw_data

# Fix the zulu bet in scraper.py and add it here.
# Not like this to load the data
zul_today = json.loads(file_handler(f'{DATE}(zul).json'))[DATE]

wdw_today, prz_toady = None, None

# iterate through files and get data for analysis
for file_name in file_names:
    try:
        # temporary data for each files.
        temp_data = json.loads(file_handler(file_name))[DATE]
        web_data_list.append(temp_data)

    except:
        print(f'----- {DATE} -----')
        print('Checking data in local storage.....')
        print(bcolors.FAIL + '[DATA NOT FOUND]' + bcolors.ENDC)
        wdw_obj = WinDrawWin.get()
        prz_obj = Predictz.get()
        wdw_today = wdw_obj.data[DATE]
        prz_toady = prz_obj.data[DATE]
        break
else:
    # if data is not from the local storage.
    if wdw_today == None and prz_toady == None:
        wdw_today = web_data_list[0]
        prz_toady = web_data_list[1]

web_data_list = [wdw_today, prz_toady, zul_today]
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

# Analysis done in this function (Percentage Calculations)
def analayze(stakes_list):
    win, draw, lose = 0, 0, 0
    not_found = []  # To calculate average based on the data aquired from number of websites
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
            # later length of the list is used to know from how many websites the data is found.
            not_found.append(val)
    else:
        try:
            total_data = len(stakes_list) - len(not_found)
            # calculate percentages
            win = (win/total_data) * 100
            lose = (lose/total_data) * 100
            draw = (draw/total_data) * 100
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
            for website_data in web_data_list:
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
            for stake in stakes_list:
                data_list.append(stake)
            else:
                # analysis results written to data_list here.
                for analysis in analayze(stakes_list):
                    data_list.append(analysis)
            
            output_writer.writerow(data_list)

            data_list = []
            stakes_list = []
    else:
        output_data.close()
        print('CSV Data successfully written.')

def main():
    ...


if __name__ == '__main__':
    try:
        wdw_obj.write_data()
        prz_obj.write_data()
    except:
        print(f'----- {DATE} -----')
        print('Checking data in local storage.....')
        print(bcolors.OKBLUE + '[DATA FOUND!]' + bcolors.ENDC )
    finally:
        create_csv()

