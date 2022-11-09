#⓪モジュールのインポート
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

args = sys.argv
wave_path = args[1]

#書き出し用のcsvデータを抽出
df = pd.read_csv(wave_path, header=None)

#csvから設定値を抽出
wave_setting_data = pd.read_csv(wave_path, header=None, usecols=[1])
WAVE_SMP_TIME = wave_setting_data.values[1]   #[sec] => 10us
wave_record_count = wave_setting_data.values[0]

#①波形データの読み出しとフーリエ変換後のX軸単位を計算
wave_df = pd.read_csv(wave_path, header=None, usecols=[4])
smp_count = len(wave_df.index.values)
x_unit_fft = 1/WAVE_SMP_TIME/smp_count  #[Hz]
print(str(x_unit_fft)+"[Hz]")

#②フーリエ変換の実行
##フーリエ変換後のX座標単位からグラフプロット用のリストを作成する
fft_x = [i*x_unit_fft for i in range(smp_count)]
##FFT処理を実施する
wave_fft = np.fft.fft(wave_df.iloc[:,0].values)
##処理後の値は複素数なので絶対値をとる
wave_fft_abs=abs(wave_fft)

##振幅の算出
amplitude = wave_fft_abs / (smp_count/2)

#④FFTによる周波数分析結果をグラフにプロット
##グラフ描画範囲を設定する
FQ_SEARCH_ST = 0 #[Hz]
FQ_SEARCH_ED = float(args[2]) #[Hz]
st_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ST).argmin()
ed_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ED).argmin()

plt.figure(figsize=(10,8))    
plt.plot(fft_x[st_index:ed_index],amplitude[st_index:ed_index],lw=1)
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig("./" + args[3] + ".jpg")
plt.show()

#csvファイル用に時間と周波数の行データを生成
time = []
freq = []
for i in range(smp_count):
    time.append(float(WAVE_SMP_TIME) * i)
    freq.append(float(x_unit_fft) * i)

#csvファイルの作成
df.insert(5, "", "")
df.insert(6, "time /s" , time)
df.insert(7, "frequency /Hz", freq)
df.insert(8, "fft_abs", wave_fft_abs)
df.insert(9, "amplitude /V", amplitude)
df.to_csv("./" + args[3] + ".csv")