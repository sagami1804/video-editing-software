
## コマンド一覧

### 基本設定系コマンド（文の前に記述することを推奨）

### `\setSubtitle{font=Corporate-Logo-Rounded-Bold-ver3.otf, size=35, color=white, stroke_color=#FF00BF, stroke_width=4, color2=white, stroke_color2=#00CC1B}`

| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
| font | x | 70 | フォントを指定する |
| size | x | 70 | フォントのサイズを指定する |
| color | x | white | フォントの色を指定する |
| stroke_color| x | black | 文字の縁の色を指定する|
| color2 | x | white | 2人目のフォントの色を指定する(会話モード時のみ有効) |
| stroke_color2| x | black | 2人目の文字の縁の色を指定する(会話モード時のみ有効)|

- 字幕の見た目を設定します。
- 例：  
  ```text
  \setSubtitle{size=40, color=white, stroke_color=black, stroke_width=2}
  ```
<br><br>


### `\setTitle{font=Corporate-Logo-Rounded-Bold-ver3.otf, size=100, color=white, stroke_color=black, stroke_width=3}`

| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
| size | x | 70 | フォントのサイズを指定する |
| color | x | white | フォントの色を指定する |
| stroke_color| x | black | 文字の縁の色を指定する|

- タイトルのスタイルを設定します。
<br><br>


### `\setTalk{speed=1.1, silence_duration=0.5, talker1=2, talker2=3}`

| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
|speed|x|1.2|音声スピードを指定する|
|silence_duration|x|0.5|次の字幕までの間の長さを指定する|
|talker1|x|2|メインボイスキャラクターを指定する|
|talker2|x|3|サブボイスキャラクターを指定する|

- 合成音声（VoiceVox）の設定を行います。
- キャラクターボイスの取得するサンプルとID一覧はこちらを参照してください
    https://puarts.com/?pid=1830
<br><br>


### `\setBG{(0,255,0)}`
- グリーンバックモードでの背景色を設定します。
- 0~255までの値を取るRGBで色を指定できます。

> ※ これらの `\set~` コマンドは途中で再設定することも可能です。
<br><br>


### 本文中で使うコマンド

### `\title{text= , duration=3}`

- 指定したタイトルテキストを表示します。
- 例：  
  ```text
  \title{text=はじめに, duration=3}
  ```
| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
|duration|o|なし|タイトルテキストの表示時間を指定|
<br><br>


### `\se{path= }`

- SE（効果音）を挿入します。
- 例：  
  ```text
  \se{path=enter.wav}
  ```
<br><br>


### `\delay{<duration>}`

- (duration)秒の間を挿入します
- 例:
  ```text
  \delay{1.5}
  ```

| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
|duration|o|なし|間の時間を指定|
<br><br>


### 環境コマンド（画像や特殊レイアウトに使用）

### `\begin{<環境名>}[<オプション>]` ～ `\end{<環境名>}`

- 環境を使って、特定の構造（例：画像）を指定した場所に挿入できます。

#### 画像環境
- 画像を\beginから\endまで表示します
```text
\begin{image}[path=image.png,tag=cat,z=3]
~
\end{image}[tag=cat]
```
| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
|tag|x|なし|タグの指定|
|z|x|なし|重なり順の指定(数値が大きいほど前面)|

#### 画像環境(簡易版)
- tagやzのオプションを省略して記述することもできます
- tagを省略すると、直上の\beginで指定した画像を終了します
```text
\begin{image}[path=image.png]
~
\end{image}
```
<br><br>


#### BGM環境
- BGMを\beginから\endまで再生します
- もしBGMの長さが足らなければループ再生します
```text
\begin{bgm}[path=bgm.mp3,volume=0.2]
~
\end{bgm}
```
| option | 必須 | 初期値 | 説明 |
| ---- | ---- | ---- | ---- |
|volume|o|なし|指定したbgmの音量の指定|
---
