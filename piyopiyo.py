#icsファイルによるカレンダーのインポートあり版

import re

class Ikkokukan():
    def __init__(self):
        self.free_list = []
        self.isogashi_list = []
        self.isEnd = False
        
    def schedule_free_add(self,date):
        if(date.isdecimal()):
            num = int(date)
            if(num<1 or num>31):
                self.isEnd = True
            else:
                self.free_list.append(num)     

    def schedule_isogashi_add(self,date):
        if(date.isdecimal()):
            num = int(date)
            if(num<1 or num>31):
                self.isEnd = True
            else:
                self.isogashi_list.append(num)

    def schedule_free_show(self):
        print(self.free_list)

    def schedule_isogashi_show(self):
        print(self.isogashi_list)

#インスタンス作成
kyokosan = Ikkokukan()
godaisan = Ikkokukan()
#soichirosan = Ikkokukan()

#フラグ
isMatch = False
inviteEnd = False
marry = False

#ループ変数
day = 1

#icsファイルを開く
path_kyoko = 'Kyokosan.ics'
path_godai = 'Godaisan.ics'

with open(path_kyoko) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
l_DTEND = [line for line in lines_strip if 'DTSTART' in line]
i=0
while i < len(l_DTSTART):
    matchObj = re.search(r'[0-9]{8}', l_DTSTART[i])
    print("START: " + matchObj.group())
    matchObj = re.search(r'[0-9]{8}', l_DTEND[i])
    print("END:   " + matchObj.group())
    i += 1
#print(l_DTSTART)

with open(path_godai) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
#print(l_DTSTART)

#忙しい日リストから暇な日リストを作る
while day < 32:
    if day not in kyokosan.isogashi_list:
        kyokosan.free_list.append(day)
    if day not in godaisan.isogashi_list:
        godaisan.free_list.append(day)
    day += 1

#暇な日リストをソート
kyokosan.free_list.sort()
godaisan.free_list.sort()

print("響子さんの空いてる日is:")
kyokosan.schedule_free_show()
print("五代さんの空いてる日is:")
godaisan.schedule_free_show()

#暇な日マッチング
matched_list = []
for kyoko in kyokosan.free_list:
    for godai in godaisan.free_list:
        if kyoko == godai:
            matched_list.append(kyoko)
            isMatch = True

#マッチする日があった場合
if isMatch:
    sorted_list = list(set(matched_list))
    sorted_list.sort()
    print(" 二人の空いてる日is:")
    print(sorted_list)
    while inviteEnd == False:
        print("招待する日を選択してください:")
        inviteDay = input()
        if int(inviteDay) in sorted_list:
            print(inviteDay + "日に招待を送りました!!!!!!!!")
            inviteEnd = True
        else:
            print(inviteDay + "日は予定があるみたいです...")

#マッチする日がなかった場合
else:
    print("来月は頑張ってください...")
    