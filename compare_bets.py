import json, datetime, csv
from operator import delitem

DATE = datetime.datetime.now().strftime('%Y-%m-%d')

game_data = {}
league_data = {}
def file_handler(file_name):
    fh = open(file_name)
    raw_data = fh.read()
    fh.close()
    return raw_data

wdw_today = json.loads(file_handler(f'{DATE}(wdw).json'))[DATE]
prdz_today = json.loads(file_handler(f'{DATE}(prdz).json'))[DATE]
test2_today = json.loads(file_handler(f'{DATE}(prdz).json'))[DATE]
zul_today = json.loads(file_handler(f'{DATE}(zul).json'))[DATE]
test_today = json.loads(file_handler(f'{DATE}(wdw).json'))[DATE]

websites = [wdw_today, prdz_today,zul_today,test_today, test2_today]

data_list = []
output_data = open('output.csv', 'w', newline='\n')
output_writer = csv.writer(output_data, delimiter='\t')
stakes_list = []
for league_name in wdw_today.keys():
    print(league_name)
    matches = list(wdw_today[league_name].keys())
    # data_list.append(league_name)
    for match in matches:
        print(match)
        # data_list.append(match)
        for website in websites:
            try:
                org_match = match
                if website == zul_today:
                    match_sep = match.split(' ')
                    for fragment in match_sep:
                        for zul_matches in list(zul_today[league_name].keys()):
                            if fragment in zul_matches.split(' '):
                                match = zul_matches
                stake = website[league_name][match]["Stake"]
                print(stake)
                stakes_list.append(stake)
                match = org_match
            except:
                stake = None
                stakes_list.append(stake)
                print(None)
        data_list.append(match)
        data_list.append(stakes_list)

        stakes_list = []
    print('-'*20)
    output_writer.writerow(data_list)
    data_list = []
else:
    output_data.close()
    print('Date written to csv file.')
# for league_name in wdw_today[DATE].keys():
#     if league_name in prdz_today[DATE].keys():
#         wdw_pred = wdw_today[DATE][league_name]
#         prdz_pred = prdz_today[DATE][league_name]
#         print(wdw_pred.keys())
#         for games in wdw_pred.keys():
#             if games in prdz_pred.keys():
#                 print(games)
#                 print('-> wdw :', wdw_pred[games]['Stake'])
#                 print('-> prdz:', prdz_pred[games]['Stake'])
#                 game_data[games] = [wdw_pred[games]['Stake'],prdz_pred[games]['Stake']]
#             else:
#                 game_data[games] = [wdw_pred[games]['Stake'], None]

#     league_data[league_name] = game_data
#     game_data = {}


# print()
# for leagues in league_data:
#     print(leagues)
#     print(league_data[leagues])
#     print()