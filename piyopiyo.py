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

    def schedule_free_show(self):
        print(self.free_list)


path_kyoko = 'Kyokosan.ics'
path_godai = 'Godaisan.ics'

kyokosan = Ikkokukan()
godaisan = Ikkokukan()
#soichirosan = Ikkokukan()

isMatch = False
inviteEnd = False
day = 1

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
    print("END: " + matchObj.group())
    i += 1
#print(l_DTSTART)

with open(path_godai) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
#print(l_DTSTART)

'''
kyokosan.isogashi_list = [1,2,4,7,8,11,12,14,16,17,19,20,22,24,27,30]
godaisan.isogashi_list = [2,3,5,7,9,11,13,14,15,18,19,24,26,28,30,31]

print("二人の日程を入力してください．終了する場合は0を入力してください．")

print("響子さんの空いてる日is:")
while kyokosan.isEnd == False:
    kyokosan.schedule_free_add(input())

print("五代さんの空いてる日is:")
while godaisan.isEnd == False:
    godaisan.schedule_free_add(input())


while day < 32:
    if day not in kyokosan.isogashi_list:
        kyokosan.free_list.append(day)
    if day not in godaisan.isogashi_list:
        godaisan.free_list.append(day)
    day += 1

kyokosan.free_list.sort()
godaisan.free_list.sort()

print("響子さんの空いてる日is:")
kyokosan.schedule_free_show()
print("五代さんの空いてる日is:")
godaisan.schedule_free_show()

matched_list = []
for kyoko in kyokosan.free_list:
    for godai in godaisan.free_list:
        if kyoko == godai:
            matched_list.append(kyoko)
            isMatch = True

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

else:
    print("来月は頑張ってください...")
'''