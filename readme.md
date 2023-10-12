# csvファイルを読み取っていい感じにフーリエ変換してくれるプログラム

## 事前準備
プログラムをsolに持っていきます。

```
$scp -r python-fft UECアカウント名@sol.edu.cc.uec.ac.jp:./
```

pythonを使うために、solにログインして以下のコードを実行してください(初回のみ)

```
$module load python/3.10.2  
$python3 -m pip install matplotlib numpy pandas scipy
```

## 使い方
実験結果は`[波長].csv`の形で一つのディレクトリ内にまとめて配置してください。
まず、ローカルのディレクトリをsolに持っていきます。

`
$scp [dir_name] UECアカウント名@sol.edu.cc.uec.ac.jp:[fft.py_path]
`

次に、フーリエ変換をしたいファイルを`fft.py`と同じディレクトリに置いて、以下のコマンドを実行してください。
`
$python3 fft.py [dir] [frequency] [output_dir]
`

`[dir]`: データの入ったディレクトリ名
`[frequency]`: グラフに表示する最大周波数
`[output_dir]`: 結果を出力するディレクトリ名

上のコマンドを実行すると、`[output_dir]`に各波長のフーリエ変換後のグラフと、最終的な結果である`result.jpg`,`result.csv`が出力されます。

最後に、出力されたファイルをローカルに持っていきます。

`
scp UECアカウント名@sol.edu.cc.uec.ac.jp:[output_dir] [local_path] 
`

例：`hoge`内のデータを3000Hzまでグラフ化して`fuga`というディレクトリ名で結果を出力したい

```
// ローカルからsolにファイル転送
$scp hoge UECアカウント名@sol.edu.cc.uec.ac.jp:python-fft/

// solにログインして実行
$python3 fft.py hoge 3000 fuga 

// solをログアウトしてローカルで実行
$scp UECアカウント名@sol.edu.cc.uec.ac.jp:python-fft/fuga ./
```