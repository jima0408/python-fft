# csvファイルを読み取っていい感じにフーリエ変換してくれるプログラム

## 事前準備
solを使う場合はまず以下のコードを実行してください。

```
$module load python/3.10.2  
$python3 -m pip install matplotlib numpy pandas
```

## 使い方
フーリエ変換をしたいファイルを`fft.py`と同じディレクトリに置いて、以下のコマンドを実行してください。
`
$python3 fft.py [file_name] [frequency] [output_name]
`

`[file_name]`: フーリエ変換したいcsvファイルの名前
`[frequency]`: グラフに表示する最大周波数
`[output_name]`: 出力するファイルの名前


例：`hoge.csv`というファイルを3000Hzまでグラフ化して`fuga.csv`という名前で出力したい
`
$python3 fft.py hoge.csv 3000 fuga 
`

上のコマンドを実行すると、フーリエ変換されたデータ類が格納された`fuga.csv`と、横軸周波数(3000Hzまで)で縦軸が振幅のグラフ画像の`fuga.jpg`が出力されます。