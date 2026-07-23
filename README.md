# Japanese Ruby PDF Generator

日本語のテキストファイル（`.txt`）を読み込み、漢字にふりがな（ruby）を付けた PDF を生成する Windows 向けデスクトップアプリです。

## 主な機能

- UTF-8 の `.txt` ファイルを読み込み
- 漢字を含む語句に自動でふりがなを付与
- PDF 出力前のプレビュー表示
- 本文サイズ、ふりがなサイズ、行間、余白の調整
- Microsoft Edge の headless 印刷機能を利用した PDF 生成

## 動作環境

- Windows
- Microsoft Edge
- Python 3.12 以上（ソースコードから実行する場合）

PDF 生成には Microsoft Edge が必要です。Edge がインストールされていない環境では PDF を生成できません。

## exe 版の使い方

[**Releases**](https://github.com/hannah0807/japanese-ruby-pdf-generator/releases) をクリックし、最新の [**JapaneseRubyPdfGenerator.zip**](https://github.com/hannah0807/japanese-ruby-pdf-generator/releases/download/2.1/JapaneseRubyPdfGenerator.zip) をダウンロードします。

使用手順:

1. `JapaneseRubyPdfGenerator.zip` を解凍します。
2. 解凍後のフォルダを開きます。
3. `JapaneseRubyPdfGenerator.exe` を実行します。
4. 入力 TXT ファイルと出力 PDF ファイルを選択します。
5. 必要に応じて文字サイズ、行間、余白を調整します。
6. `生成 PDF` を押します。

注意: `JapaneseRubyPdfGenerator.exe` だけを別の場所へ移動しないでください。`_internal` フォルダ内のライブラリや辞書データも必要です。配布する場合は zip ファイル全体を渡してください。

## ソースコードから実行する方法

依存パッケージをインストールします。

```powershell
pip install -r requirements.txt
```

アプリを起動します。

```powershell
python app.py
```

## PDF の生成について

このアプリは、内部で HTML を生成し、Microsoft Edge の headless 印刷機能で PDF に変換します。

出力 PDF にはブラウザの既定ヘッダー・フッターが入らないように設定しています。

## ふりがなの生成について

ふりがなの付与には以下のライブラリを使用しています。

- fugashi
- unidic-lite

形態素解析の結果に基づいて読みを取得するため、一般的な文章では自動変換できます。ただし、固有名詞、特殊な読み方、文脈依存の読み、熟字訓などは完全には判定できない場合があります。

## 設定項目

アプリ画面から以下を調整できます。

- 正文大小: 本文の文字サイズ
- 注音大小: ふりがなの文字サイズ
- 行距: 行間
- 页面内边距: HTML 本文側の余白
- PDF 页边距: PDF 印刷時のページ余白

設定は `config.json` に保存されます。

## exe の再ビルド方法

PyInstaller が必要です。

```powershell
pip install pyinstaller
```

以下のコマンドでビルドします。

```powershell
pyinstaller --noconfirm --clean --windowed --name JapaneseRubyPdfGenerator --collect-all unidic_lite --collect-all fugashi --collect-all webview app.py
```

ビルド後の実行ファイルは次の場所に作成されます。

```text
dist/JapaneseRubyPdfGenerator/JapaneseRubyPdfGenerator.exe
```

配布する場合は、次のフォルダ全体を zip 化してください。

```text
dist/JapaneseRubyPdfGenerator
```

## トラブルシューティング

### PDF が生成されない

Microsoft Edge がインストールされているか確認してください。

このアプリは通常、以下のどちらかの場所にある Edge を探します。

```text
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
C:\Program Files\Microsoft\Edge\Application\msedge.exe
```

### ふりがなが期待どおりにならない

自動解析のため、すべての読みを完全に判定できるわけではありません。特に固有名詞や特殊な読み方では誤ったふりがなが付く場合があります。

### exe を起動できない

`JapaneseRubyPdfGenerator.exe` だけを取り出して実行していないか確認してください。`_internal` フォルダを含む配布フォルダ全体が必要です。
