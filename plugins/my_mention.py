# coding: utf-8

'''
#文字コードを指定
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import urllib.request #ファイルを落とすのに必要
import re #文章を分割するためのライブラリ

import datetime
#python2.79以降必要
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

ScheFlag = 0
URL = ''

file_path = "data/schedule.ics"

boshu_start_str = '20180701'
boshu_end_str = '20180731'
boshu_start = datetime.datetime.strptime(boshu_start_str, "%Y%m%d")
boshu_end = datetime.datetime.strptime(boshu_end_str, "%Y%m%d")

#各set初期化
def schedule_init():
    everyone_busy_set = set()
    everyone_free_set = set()

    calc_date = boshu_start
    while calc_date <= boshu_end:
        everyone_free_set.add(calc_date)
        calc_date = calc_date + datetime.timedelta(days=1)

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@respond_to('start')
def schedulestart_func(message):
    global ScheFlag

    if ScheFlag == 0:
        #ScheFlag = 1
        #text = message.body['text']
        #splited = re.split('\s', text.replace('.', ''))
        #message.reply(splited[1]) # メンション
        schedule_init()
        message.reply("Let's scheduling！Move input faze.")
        ScheFlag = 1
        
    else:
        message.reply("You forgot [scheduleend]...？")

@respond_to('end')
def scheduleend_func(message):
    global ScheFlag
    global everyone_busy_set
    global everyone_free_set

    if ScheFlag == 1:
        ScheFlag = 0
        message.reply("I will informed you of the convenient days for everyone!!!!")
        everyone_free_set = everyone_free_set - everyone_busy_set
        #暇な日セットをソートしてからリスト型に保存
        free_list = sorted(everyone_free_set)

        i=0
        while i < len(free_list):
            
            if free_list.weeks == 0:
                youbi = '(月)'
            elif free_list.weeks == 1:
                youbi = '(火)'
            elif free_list.weeks == 2:
                youbi = '(水)'
            elif free_list.weeks == 3:
                youbi = '(木)'
            elif free_list.weeks == 4:
                youbi = '(金)'
            elif free_list.weeks == 5:
                youbi = '(土)'
            elif free_list.weeks == 6:
                youbi = '(日)'

            hatsugen = str(free_list[i].month) + '/' + str(free_list[i].day) + youbi
            message.reply(hatsugen)
            i += 1
        
    else:
        message.reply("Oh, I didn't expect that.")
    
@respond_to('flag')
def flag_func(message):
    global ScheFlag
    message.reply(str(ScheFlag))

@listen_to("だるい")
def listen_func(message):
    message.send('誰かがだるいと投稿したようだ')      # ただの投稿
    message.reply('お前かーーー！！！！')                           # メンション

@respond_to('cool') #ハッシュがついていたら、
def cool_func(message):
    message.reply('Thank you. スタンプ押しとくね')     # メンション
    message.react('+1')     # リアクション

@default_reply()
def default_func(message):
    global ScheFlag
    global URL
    global everyone_busy_set
    flag = 0
    if ScheFlag == 1:
        text = message.body['text']     # メッセージを取り出す
       
        #ファイルをオープン
        file = open("DataBase.txt")
        lines = file.readlines()
        file.close()

        #データベースを１行ずつ検索して、見つかったらその日のURLを渡してあげる
        for line in lines:
           if line.find(text) >= 0:
                d = re.search("(.*) (.*)", line)
                URL = d.group(2)
                #message.reply(d.group(2))
                message.reply("Success!! Any other?")
                flag = 1
                
                #インスタンス生成
                kyokosan = Ikkokukan()

                kyokosan.set_url(URL)
                kyokosan.run()
        
                #みんなの忙しいリストに自分の忙しいリストを追加
                #全員の忙しい日セット == 個人の忙しい日セットの和集合
                everyone_busy_set = everyone_busy_set | kyokosan.busy_set

                
        #検索ができなかった場合
        if flag == 0:
            message.reply("Sorry, I don't know...")

    else:
        message.reply("うっせ！ばか！")


class Ikkokukan():
    global file_path
    
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
            matchObj_start = re.search('[0-9]{8}', l_DTSTART[i])
            ##matchObj_start = re.search('[0-9]{8}T[0-9]{6}', l_DTSTART[i])
            #print(matchObj_start)

            #日付型に変換
            date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%d")
            #date_formatted_start = datetime.datetime.strptime(matchObj_start.group(), "%Y%m%dT%H%M%S")

            #date_formatted_start = date_formatted_start + datetime.timedelta(hours=9)
            #print("start: ", end="")
            #print(date_formatted_start.date())

            #予定終了日
            matchObj_end = re.search('[0-9]{8}', l_DTEND[i])
            #matchObj_end = re.search('[0-9]{8}T[0-9]{6}', l_DTEND[i])

            #日付型に変換
            date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%d")
            #date_formatted_end = datetime.datetime.strptime(matchObj_end.group(), "%Y%m%dT%H%M%S")

            #date_formatted_end = date_formatted_end + datetime.timedelta(hours=9)
            #print('end  : ', end="")
            #print(date_formatted_end.date())

            #予定のある日を計算
            calc_date = date_formatted_start
            while calc_date < date_formatted_end:
                self.schedule_busy_add(calc_date)
                calc_date = calc_date + datetime.timedelta(days=1)
            
            i += 1