# csvファイルを読み取っていい感じにフーリエ変換してくれるプログラム

## 事前準備
solにログインして以下のコードを実行してください。

```
$module load python/3.10.2  
$python3 -m pip install matplotlib numpy pandas
```

## 使い方
まず、ローカルのファイルをsolに持っていきます。

`
scp [file_name] UECアカウント名@sol.edu.cc.uec.ac.jp:[fft.py_path]
`

次に、フーリエ変換をしたいファイルを`fft.py`と同じディレクトリに置いて、以下のコマンドを実行してください。
`
$python3 fft.py [file_name] [frequency] [output_name]
`

`[file_name]`: フーリエ変換したいcsvファイルの名前
`[frequency]`: グラフに表示する最大周波数
`[output_name]`: 出力するファイルの名前

上のコマンドを実行すると、フーリエ変換されたデータ類が格納された`fuga.csv`と、横軸周波数(3000Hzまで)で縦軸が振幅のグラフ画像の`fuga.jpg`が出力されます。

最後に、出力されたファイルをローカルに持っていきます。

`
scp UECアカウント名@sol.edu.cc.uec.ac.jp:[output_file] [local_path] 
`

例：`hoge.csv`というファイルを3000Hzまでグラフ化して`fuga.csv`という名前で出力したい

```
// ローカルからsolにファイル転送
$scp hoge.csv UECアカウント名@sol.edu.cc.uec.ac.jp:python-fft/

// solにログインして実行
$python3 fft.py hoge.csv 3000 fuga 

// solをログアウトしてローカルで実行
$scp UECアカウント名@sol.edu.cc.uec.ac.jp:python-fft/fuga.csv ./
```