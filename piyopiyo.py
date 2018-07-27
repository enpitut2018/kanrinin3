#icsファイルによるカレンダーのインポートあり版

import re
import datetime
import urllib.request
import sys

#python2.79以降必要
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

args = sys.argv

boshu_start_str = '20180701'
boshu_end_str = '20180707'
#現状start時間<end時間の場合しか対応してないです,終電で帰ってください
boshu_starthour = 8
boshu_endhour = 22

file_path = "data/schedule.ics"

everyone_busy_set = set()
everyone_free_set = set()

boshu_start = datetime.datetime.strptime(boshu_start_str, "%Y%m%d")
boshu_start = boshu_start.replace(hour=boshu_starthour)
boshu_end = datetime.datetime.strptime(boshu_end_str, "%Y%m%d")
boshu_end = boshu_end.replace(hour=boshu_endhour)

#URL1 = args[1]
#URL2 = args[2]

URL1 = "https://calendar.google.com/calendar/ical/eru9j8labfq0245qeqk39ukr2s%40group.calendar.google.com/private-fef71c3d0112f19c2480d97e2756c376/basic.ics"
URL2 = "https://calendar.google.com/calendar/ical/aliko62mpof47ljh98jn32crb0%40group.calendar.google.com/private-3f1a02b50c5e5bf0dc9d9a88815e0735/basic.ics"

file_name1 = 'data/Kyokosan.ics'
#file_name2 = 'Godaisan.ics'

#icsファイルを開く
path_kyoko = file_name1
#path_godai = file_name2

class Ikkokukan():
    def __init__(self):
        self.free_set = set() #暇な日を格納するset
        self.busy_set = set() #忙しい日を格納するset
        self.url_schedule = "" #カレンダーのurlを格納する文字列
        
    def schedule_free_add(self,date):
        self.free_set.add(date)

    def schedule_busy_add(self,date):
        self.busy_set.add(date)

    def schedule_free_show(self):
        print(self.free_set)

    def schedule_busy_show(self):
        print(self.busy_set)

    #標準入力のurlから忙しいリストを作成
    def run(self):
        self.url_to_ics()
        self.ics_to_busy()

    #標準入力からurl受け取り
    def listen_url(self):
        print('URL?:')
        input_url = input()
        if input_url == 'end':
            return True
        else:
            self.set_url(input_url)
            return False

    #カレンダーのurlをセット
    def set_url(self,url):
        self.url_schedule = url

    #セットされたカレンダーのurlを表示
    #事前にset_urlが必要
    def show_url(self):
        print("url:"+self.url_schedule)

    #urlからicsファイル取得
    #事前にset_urlが必要
    def url_to_ics(self):
        urllib.request.urlretrieve(self.url_schedule, file_path)

    #urlの指定するカレンダーから忙しいリストを作成
    #事前にset_urlが必要
    def ics_to_busy(self):
        #カレンダー読み込み
        with open(file_path) as f:
            lines = f.readlines()

        lines_strip = [line.strip() for line in lines]

        #'DTSTART', 'DTEND'を含む行を抽出しリストに保存
        l_DTSTART = [line for line in lines_strip if 'DTSTART' in line]
        l_DTEND = [line for line in lines_strip if 'DTEND' in line]

        #抽出した各行を日付形式に変換してリストに保存
        i=0
        while i < len(l_DTSTART):

            #予定開始日
            #時間設定を含む予定の場合
            matchObj_start = re.search('[0-9]{8}T[0-9]{2}', l_DTSTART[i])
            #日付型に変換
            if matchObj_start != None:
                date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%dT%H")
                date_formatted_start = date_formatted_start + datetime.timedelta(hours=9)
                #print(date_formatted_start)
            
            #終日設定の予定の場合
            else:
                matchObj_start = re.search('[0-9]{8}', l_DTSTART[i])
                #日付型に変換
                date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%d")
                #print(date_formatted_start)

            #予定終了日
            #時間設定を含む予定の場合
            matchObj_end = re.search('[0-9]{8}T[0-9]{2}', l_DTEND[i])
            if matchObj_end != None:
                date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%dT%H")
                date_formatted_end = date_formatted_end + datetime.timedelta(hours=9)
                #print(date_formatted_end)
            
            #終日設定の予定の場合
            else:
                matchObj_end = re.search('[0-9]{8}', l_DTEND[i])
                #日付型に変換
                date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%d")
                #print(date_formatted_end)

            #予定のある日をbusy_setに追加
            #2日以上続く予定に対応するためこんな感じになってます
            calc_date = date_formatted_start
            while calc_date < date_formatted_end:
                self.schedule_busy_add(calc_date)
                calc_date = calc_date + datetime.timedelta(hours=1)
            
            i += 1

#フラグ
byebye_flag = False


#everyone_free_setを初期化（期限内の全ての日時を追加）
calc_date = boshu_start
while calc_date <= boshu_end:
    if calc_date.hour > boshu_endhour:
        calc_date = calc_date.replace(hour=boshu_starthour)
        calc_date = calc_date + datetime.timedelta(days=1)
    everyone_free_set.add(calc_date)
    calc_date = calc_date + datetime.timedelta(hours=1)


while byebye_flag == False:

    #インスタンス作成
    kyokosan = Ikkokukan()
    print('URL?:')
    input_str = input()
    if input_str == 'end':
        byebye_flag = True
    else:
        kyokosan.set_url(input_str)
        kyokosan.run()
        
        #print("響子さんの忙しい日リスト:")
        #kyokosan.schedule_busy_show()
        
        #みんなの忙しいリストに自分の忙しいリストを追加
        #全員の忙しい日セット == 個人の忙しい日セットの和集合
        everyone_busy_set = everyone_busy_set | kyokosan.busy_set


#全員の忙しい日セットから暇な日セットを作る
#全員の忙しい日セットの補集合 == 全員が暇な日セット
everyone_free_set = everyone_free_set - everyone_busy_set
#暇な日セットをソートしてからリスト型に保存
free_list = sorted(everyone_free_set)

#候補日を表示
print("I will inform you of the convenient days for everyone：")
print("term："+boshu_start_str+"-"+boshu_end_str)
i=0
l_print = []
while i+1 < len(free_list):
    print(str(free_list[i].month) + "/", end="")
    print(str(free_list[i].day)," ",free_list[i].hour,":00 - ", end="")
    free_list[i] = free_list[i] + datetime.timedelta(hours=1)
    while i+1 < len(free_list) and free_list[i].hour == free_list[i+1].hour:
        i += 1
        free_list[i] = free_list[i] + datetime.timedelta(hours=1)
    print(str(free_list[i].hour), ":00")
    i += 1
print("Have a nice day!")
