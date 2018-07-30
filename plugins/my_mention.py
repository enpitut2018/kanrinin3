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
import os #ファイル削除に使用
import datetime #日付型を使用するのに必要
#python2.79以降必要
#ファイルをダウンロードする許可
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

ScheFlag = 0
help_count = 0
empty_flag = True

file_path = "/tmp/schedule.ics"
database_path = "DataBase.txt"

boshu_start_str = '2018072908'
boshu_end_str = '2018080322'
#現状start時間>end時間の場合挙動がおかしいので終電で帰ってください
boshu_start = datetime.datetime.strptime(boshu_start_str, "%Y%m%d%H")
boshu_end = datetime.datetime.strptime(boshu_end_str, "%Y%m%d%H")

everyone_busy_set = set()
everyone_free_set = set()

#各set初期化
def everyone_free_init():
    global everyone_free_set

    #空のfree_setに範囲内の時間全て入れる(全体集合的なもの)
    everyone_free_set = set()
    calc_date = boshu_start
    while calc_date <= boshu_end:
        #22時になったら翌8時にスキップみたいなことしてる
        if calc_date.hour == boshu_end.hour:
            calc_date = calc_date.replace(hour=boshu_start.hour)
            if boshu_start.hour < boshu_end.hour:
                calc_date = calc_date + datetime.timedelta(days=1)
        everyone_free_set.add(calc_date)
        calc_date = calc_date + datetime.timedelta(hours=1)

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

@respond_to(r'^start$')
def schedulestart_func(message):
    global ScheFlag

    if ScheFlag == 0:
        #ScheFlag = 1
        #text = message.body['text']
        #splited = re.split('\s', text.replace('.', ''))
        #message.reply(splited[1]) # メンション
        everyone_busy_set = set()
        everyone_free_init()
        message.send("日程調整を開始します．参加者を登録してください．")
        ScheFlag = 1
        
    else:
        message.reply("already started.")

@respond_to(r'^end$')
def scheduleend_func(message):
    global ScheFlag
    global everyone_busy_set
    global everyone_free_set
    global boshu_start
    global boshu_end
    global empty_flag

    if ScheFlag == 1:
        if empty_flag == False:
            message.send("皆さんが参加できる日はこちらになります.")
            hatsugen = "期間："+str(boshu_start.date())+" ~ "+str(boshu_end.date())+" "+str(boshu_start.hour)+":00 - "+str(boshu_end.hour)+":00"
            message.send(hatsugen)
            everyone_free_set = everyone_free_set - everyone_busy_set
            #暇な日セットをソートしてからリスト型に保存
            free_list = sorted(everyone_free_set)
            empty_flag = True
            ScheFlag = 0

            i=0
            while i+1 < len(free_list):
                
                if free_list[i].weekday() == 0:
                    youbi = '(月)'
                elif free_list[i].weekday() == 1:
                    youbi = '(火)'
                elif free_list[i].weekday() == 2:
                    youbi = '(水)'
                elif free_list[i].weekday() == 3:
                    youbi = '(木)'
                elif free_list[i].weekday() == 4:
                    youbi = '(金)'
                elif free_list[i].weekday() == 5:
                    youbi = '(土)'
                elif free_list[i].weekday() == 6:
                    youbi = '(日)'

                hatsugen = str(free_list[i].month) + '/' + str(free_list[i].day) + youbi + " " + str(free_list[i].hour) + ":00 - "

                osusume = 1
                free_list[i] = free_list[i] + datetime.timedelta(hours=1)
                while i+1 < len(free_list) and free_list[i].hour == free_list[i+1].hour:
                    i += 1
                    osusume += 1
                    free_list[i] = free_list[i] + datetime.timedelta(hours=1)
                hatsugen = hatsugen + str(free_list[i].hour) + ":00  ("+str(osusume)+"時間)"
                message.send(hatsugen)

                i += 1
            message.send("頑張ってくださいね！")
            
        #startしたけど誰も追加せずにend
        else:
            message.reply('startって言ったくせに…若くてかわいいガールフレンドがいるんじゃないの…私をからかったんだわ。ひどい…女心を弄んで……')
            ScheFlag = 0
    #startしてないのにend
    else:
        message.send("already ended")

@respond_to(r'^flag$')
def flag_func(message):
    global ScheFlag
    message.reply(str(ScheFlag))

#デバッグ用,非公開のurlを公開するので
@respond_to(r'^showdb$')
def showdb_funk(message):
    global database_path
    with open(database_path, 'r') as f:
        for line in f.readlines():
            matchObj = re.search(r'\$.+\s', line)
                message.send(str(matchObj.group()))

@respond_to(r'^help$')
def help_func(message):
    global help_count

    if help_count < 2:
        message.send('〜使い方〜\nstart\nでスケジュール調整を開始します\n$アカウント名 または GoogleカレンダーのURLを入力することで参加者に追加できます (例)$kyoko\nset 2018070108-2018073122\nのように入力することで，スケジュール範囲を 2018/7/1 ~ 2018/7/31 の 8:00 - 22:00 に設定します(デフォルトの範囲設定)\nreg $(ユーザー名) [Googleカレンダーの非公開URL] ： 一刻館の電話帳にお名前とURLを加えます\nend : スケジュール調整を終了し，全員が参加できる日を表示します')
        help_count += 1
    else:
        message.reply('大変！！今すぐ救急車を呼びます！！')
        help_count = 0

@respond_to(r'^set')
def set_func(message):
    global boshu_start
    global boshu_end
    text = message.body['text']
    matchObj_error = re.search(r'^set\s[0-9]{10}-[0-9]{10}$', text)
    if matchObj_error == None:
        message.send('募集期間を変えるには\nset 2018070108-2018073122\n(年-月-日-時)のような形でお願いします')
    else:
        matchObj = re.findall('[0-9]{10}', text)
        boshu_start = datetime.datetime.strptime(matchObj[0], "%Y%m%d%H")
        boshu_end = datetime.datetime.strptime(matchObj[1], "%Y%m%d%H")
        everyone_free_init()
        message.send("募集期間を変えました！")
        hatsugen = "期間："+str(boshu_start.date())+" ~ "+str(boshu_end.date())+" "+str(boshu_start.hour)+":00 - "+str(boshu_end.hour)+":00"
        message.send(hatsugen)

@respond_to(r'^reg')
def reg_func(message):
    text = message.body['text']
    matchObj_id = re.search(r'\$.+\s', text)
    matchObj_url = re.search(r'https://calendar\.google\.com/calendar/ical/.+/private-.+/basic\.ics', text)
    #idとurlが揃っていれば
    if matchObj_id != None and matchObj_url != None:
        with open(database_path,'a') as f:
            try:
                f.write(matchObj_id.group())
                f.write(matchObj_url.group()+'\n')
                hatsugen = matchObj_id.group() + "をデータベースに登録しました"
                message.send(hatsugen)
            except:
                message.send('DBの登録に失敗しました...')
    else:
        message.send('データベースに登録するには\nreg $(ユーザー名) [Googleカレンダーの非公開URL]\nと入力してください')

#todo データベースから削除

@listen_to("だるい")
def listen_func(message):
    message.reply('大丈夫ですか？ご飯作りましょうか？')

@listen_to("管理人")
def listen_func(message):
    message.send('一刻館の管理人をしています，音無響子と申します')

@respond_to('cool') #ハッシュがついていたら、
def cool_func(message):
    message.reply('Thank you. スタンプ押しとくね')     # メンション
    message.react('+1')     # リアクション

@listen_to('hot') #ハッシュがついていたら、
def hot_func(message):
    message.reply('ファッキンホット(クソ暑い)')     # メンション
    message.react('hotsprings')     # リアクション

@listen_to('五代')
def godai_func(message):
    message.reply('五代さん，はい')
    message.react('godai')

@listen_to('酒' or '酔' or '祭')
def sake_func(message):
    message.react('godai')
    message.react('yotsuya')
    message.react('kyoko')

@respond_to('殺す' or '死ね')
def damedayo_funk(message):
    message.send('三鷹「人に頭が下げられない奴ってのは、一生 半人前だよ」')

@default_reply()
def default_func(message):
    global ScheFlag
    global URL
    global everyone_busy_set
    global empty_flag
    if ScheFlag == 1:
        text = message.body['text']     # メッセージを取り出す
       
        #message.send(text)
        matchObj_url = re.search(r'^.*https://calendar\.google\.com/calendar/ical/.+basic\.ics.*', text)
        matchObj_id = re.match(r'^\$.+', text)
        #渡されたのがurlだった場合
        if matchObj_url != None:
            kyokosan = Ikkokukan()
            kyokosan.set_url(matchObj_url.group())
            try:
                kyokosan.url_to_ics()
                kyokosan.ics_to_busy()
                everyone_busy_set = everyone_busy_set | kyokosan.busy_set
                message.send('Googleカレンダーから予定をインポートしました．')
                empty_flag = False
                matchObj_url = ''
            except:
                message.send('urlを開けませんでした...')
        #渡されたのがIDだった場合
        elif matchObj_id != None:
            #ファイルをオープン
            with open(database_path) as file:
                lines = file.readlines()

            mitsukarimashita = False
            #データベースを１行ずつ検索して、見つかったらその日のURLを渡してあげる
            for line in lines:
                if line.find(text) >= 0:
                    d = re.search("(.*) (.*)", line)
                    URL = d.group(2)
                    #message.reply(d.group(2))
                    mitsukarimashita = True
                    
                    #インスタンス生成
                    kyokosan = Ikkokukan()
                    try:
                        kyokosan.set_url(URL)
                        kyokosan.url_to_ics()
                        kyokosan.ics_to_busy()
                        #みんなの忙しいリストに自分の忙しいリストを追加
                        #全員の忙しい日セット == 個人の忙しい日セットの和集合
                        everyone_busy_set = everyone_busy_set | kyokosan.busy_set
                        message.send("登録されたIDから予定をインポートしました")
                        empty_flag = False
                    except:
                        message.send('IDを開けませんでした...')
                    break
            if mitsukarimashita == False:
                message.send('電話帳にお名前が見つかりません...')

            mitsukarimashita = False

        #IDでもurlでもなかった場合
        else:
            message.send("IDまたはGoogleカレンダーのURLを指定してください...\nendで予定を出力します")
        text = ''

    else:
        message.send('四谷「そういう大事なことは口に出して言わない方がいいですよ」')
        #message.send('お困りの際はいつでも私宛てに「help」と仰ってくださいね！')
        #message.send("こっこっ，この，む...無職の甲斐性なしの貧乏人っっっ！")


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

    #忙しいリストを作成
    #事前にset_urlが必要
    def run(self):
        self.url_to_ics()
        self.ics_to_busy()

    #カレンダーのurlをセット
    def set_url(self,url):
        self.url_schedule = url

    #セットされたカレンダーのurlを表示
    #事前にset_urlが必要
    def show_url(self):
        message.send("url:"+self.url_schedule)

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

            #予定のある時間をbusy_setに追加
            calc_date = date_formatted_start
            while calc_date < date_formatted_end:
                self.schedule_busy_add(calc_date)
                calc_date = calc_date + datetime.timedelta(hours=1)
            
            i += 1
        #使用したicsファイルを削除
        os.remove(file_path)
