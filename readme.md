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

---

## 本文中で使うコマンド

### `\title{text=, duration=}`

- 指定したタイトルテキストを表示します。
- 例：  
  ```text
  \title{text=はじめに, duration=3}
  ```

### `\se{path}`

- SE（効果音）を挿入します。
- 例：  
  ```text
  \se{sounds/enter.wav}
  ```

### 環境コマンド（画像や特殊レイアウトに使用）

#### `\begin{環境名}[オプション]` ～ `\end{環境名}`

- 環境を使って、特定の構造（例：画像）を挿入できます。

#### 画像環境の例

```text
\begin{image}[image.png]
（ここに本文やキャプションを書くこともできます）
\end{image}
```

---

## 使用例

```text
\setSubtitle{size=36, color=yellow}
\setTalk{speed=1.2}

こんにちは、これはテキストベースの動画編集ソフトです。

\title{text=使い方, duration=2}

\se{sounds/start.wav}

次に、画像を表示してみましょう。

\begin{image}[scene.png]
この画像は説明のためのものです。
\end{image}
```

---

## ライセンス

MIT License

---
