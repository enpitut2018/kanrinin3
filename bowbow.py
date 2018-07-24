#icsファイルインポートなし版

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

#あらかじめスケジュールを入力しておくパターン
kyokosan.isogashi_list = [1,2,4,7,8,11,12,14,16,17,19,20,22,24,27,30]
godaisan.isogashi_list = [2,3,5,7,9,11,13,14,15,18,19,24,26,28,30,31]

'''
#手入力パターン
print("二人の日程を入力してください．終了する場合は0を入力してください．")

print("響子さんの忙しい日is:")
while kyokosan.isEnd == False:
    kyokosan.schedule_isgashi_add(input())

print("五代さんの忙しい日is:")
while godaisan.isEnd == False:
    godaisan.schedule_isogashi_add(input())
'''

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
    