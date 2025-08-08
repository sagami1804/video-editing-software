# テキストベース動画編集ソフト

このソフトウェアは、**LaTeX のようにテキストだけで動画編集を行う**ことができるツールです。  
動画の本文・字幕・合成音声などを、すべてテキストで記述できます。

---

## 特徴

- **コマンドなしのテキスト**は本文として扱われ、以下が自動生成されます：
  - 字幕（テキストごとに1行）
  - 合成音声（VoiceVox）
- **改行**によって、字幕および音声は分割されます。

---

## コマンド一覧

### 基本設定系コマンド（文の前に記述することを推奨）

#### `\setSubtitle{size=, color=, stroke_color=, stroke_width=}`

- 字幕の見た目を設定します。
- 例：  
  ```text
  \setSubtitle{size=40, color=white, stroke_color=black, stroke_width=2}
  ```

#### `\setTitle{size=, color=, stroke_color=, stroke_width=}`

- タイトルのスタイルを設定します。

#### `\setTalk{speed=, silence_duration=}`

- 合成音声（VoiceVox）の設定を行います。

> ※ これらの `\set~` コマンドは途中で再設定することも可能です。

### 本文中で使うコマンド

#### `\title{text=, duration=}`

- 指定したタイトルテキストを表示します。
- 例：  
  ```text
  \title{text=はじめに, duration=3}
  ```

#### `\se{path}`

- SE（効果音）を挿入します。
- 例：  
  ```text
  \se{enter.wav}
  ```

#### `\delay{duration}`
- (duration)秒の間を挿入します
- 例:
  ```text
  \delay{1.5}
  ```

### 環境コマンド（画像や特殊レイアウトに使用）

#### `\begin{環境名}[オプション]` ～ `\end{環境名}`

- 環境を使って、特定の構造（例：画像）を指定した場所に挿入できます。

#### 画像環境
- 画像を\beginから\endまで表示します
```text
\begin{image}[image.png]
~
\end{image}
```

#### BGM環境
- BGMを\beginから\endまで再生します
- もしBGMの長さが足らなければループ再生します
```text
\begin{bgm}[path=bgm.mp3,volume=0.2]
~
\end{bgm}
```
---

## 使用例

```text
\setSubtitle{size=36, color=yellow}
\setTalk{speed=1.2}

こんにちは、これはテキストベースの動画編集ソフトです。

\title{text=使い方, duration=2}

\se{start.wav}

次に、画像を表示してみましょう。

\begin{image}[scene.png]
この画像は説明のためのものです。
\end{image}
```

---

## 必要な環境・依存ライブラリ

- **Python 3.10 以上**（推奨）
- 必要なパッケージは `requirements.txt` で管理されています。  
  インストール例：
  ```bash
  pip install -r requirements.txt
  ```
- **VoiceVoxエンジン**（ローカルサーバー）が必要です。  
  [VoiceVox公式サイト](https://voicevox.hiroshiba.jp/)からダウンロードし、`http://localhost:50021` でアクセスできる状態にしてください。

---

## 実行方法

1. 必要な素材（フォント・画像・音声）を `fonts/`, `images/`, `sounds/` に配置してください。
2. VoiceVoxエンジンを起動してください。
3. ソフトを起動し、入力スペースに動画のコードを入力してください。
4. 実行ボタンを押してください
5. エンコード終了後、`output/`に動画ファイルが生成されます。

---

## 注意事項・既知の制限

- VoiceVoxエンジンが起動していない場合、音声合成は失敗します。
- フォントファイルが存在しない場合、字幕やタイトルが正しく表示されません。
- Windows環境での動作を想定しています。

---

## カスタマイズ

- 設定は `tests/__init__.py` の `Config` クラスで変更できます。
- フォントやデフォルト値を編集することで、見た目や動作を調整できます。

---

## ライセンス

MIT License

---
