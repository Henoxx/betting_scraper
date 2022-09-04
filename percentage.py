import csv
ex = open('final.csv')
ex_re = csv.reader(ex)
# for row in ex:
#     print(str(row))
ex_data = list(ex_re)
stakes = []
j = 0
for i in ex_data:
    try:
        stakes.append(ex_data[j])
        j += 2
    except:
        j += 1

win = 0
lose = 0
draw = 0
zeros = []
for stake in stakes:
    print(stake)
    for val in stake:
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

        elif val == '0':
            zeros.append(val)
    try:
        data = len(stake) - len(zeros)
        win = (win/data) * 100
        lose = (lose/data) * 100
        draw = (draw/data) * 100
        print(f"Win: {round(win,2)}%, Draw: {round(draw,2)}%, Lose:{round(lose,2)}%")
        win, lose, draw = 0,0,0
        zeros = []
    except:
        pass
    