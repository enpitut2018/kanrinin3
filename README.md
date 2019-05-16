## 管理人さんチーム 「管理人さん」
## プロダクト概要(エレベーターピッチ)
　お友達と遊びたい！チームのミーティングがしたい！でも一から都合の良い日を見つけるのがめんどくさい人のための，スケジュール提案ボットです．予定を合わせたいユーザを選択するだけで，ユーザ間での都合のいい日時を表示します．操作もslack上で行うことができ，専用のwebアプリに飛ぶ必要もありません．あなたのスケジュール管理，ちょっと簡単にしませんか？ 
## どこで使えるか
* slackbotとして[enPiT2018](https://enpit2018.slack.com/messages/DBXTX88F4/)上で動作しています
* [Googleカレンダー](https://calendar.google.com/)のエクスポートファイル(ics形式)をサポートします  
## メンバー
* tanaka
* suto
* kanazawa
* hayashi
* [yusa](https://github.com/yungoyungo)
## 何が管理人さんなのか

![ささっ](http://www.ne.jp/asahi/rumic/k-asuka/c_images/Maison3.jpg "管理人さんは管理人さんです")

# how to run

`git clone https://github.com/enpitut2018/kanrinin3.git`  
`pip3 install slackbot`  

## トークンの発行
[Slack API](https://api.slack.com/)で新規アプリ作成
作成したアプリ内の`OAuth & Permissions`にある`Bot User OAuth Access Token`をコピー  
`slackbot_settings.py`にあるAPI_TOKENに先程のトークンを入れます    


## run
`python3 run.py`  

## stop
現状`Ctrl + c`

## 管理人さんの動作を変更したい

アクションは全て`plugin/my_mention.py`内に記述されてます（これが正解かは分からない、多分不正解）  
ので、編集して自分だけのオリジナル管理人さんを作ろう！

# 参考リンク
- https://qiita.com/sukesuke/items/1ac92251def87357fdf6  
