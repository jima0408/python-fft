#⓪モジュールのインポート
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import csv
import os
import re

# 引数からファイル名を取得
args = sys.argv
wave_path = args[1]
files = os.listdir(wave_path)

# 結果を保存するcsvファイルを作成
with open(args[3] + "/result.csv", "w", newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["frequency /Hz", "amplitude /V"])

for file in files:
    isCsv = re.search('.csv', file)
    if isCsv:
        #ファイル名から波長を取得
        wave_length = re.search('(\d+)', file).group(1)
        path = args[1] + "/" + file
        print(file)

        #csvから設定値を抽出
        wave_setting_data = pd.read_csv(path, header=None, usecols=[1])
        WAVE_SMP_TIME = wave_setting_data.values[1]   #[sec] => 10us
        wave_record_count = wave_setting_data.values[0]

        # 波形データの読み出しとフーリエ変換後のX軸単位を計算
        wave_df = pd.read_csv(path, header=None, usecols=[4])
        smp_count = len(wave_df.index.values)
        x_unit_fft = 1/WAVE_SMP_TIME/smp_count  #[Hz]
        print("FFT interval: " + str(x_unit_fft[0]) + " [Hz]")

        # フーリエ変換の実行
        ##フーリエ変換後のX座標単位からグラフプロット用のリストを作成する
        fft_x = [i*x_unit_fft for i in range(smp_count)]
        ##FFT処理を実施する
        wave_fft = np.fft.fft(wave_df.iloc[:,0].values)
        ##処理後の値は複素数なので絶対値をとる
        wave_fft_abs=abs(wave_fft)

        ##振幅の算出
        amplitude = wave_fft_abs / (smp_count/2)

        # FFTによる周波数分析結果をグラフにプロット
        ##グラフ描画範囲を設定する
        FQ_SEARCH_ST = 0 #[Hz]
        FQ_SEARCH_ED = float(args[2]) #[Hz]
        st_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ST).argmin()
        ed_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ED).argmin()

        # グラフを描画して[波長].jpgで保存
        plt.figure(figsize=(10,8))    
        plt.plot(fft_x[st_index:ed_index],amplitude[st_index:ed_index],lw=1)
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude [V]")
        plt.savefig(args[3] + "/" + wave_length + ".jpg")
        plt.close()

        #wave_lengthに一番近い波長とその時の振幅を取得
        picked_wave_length = min(fft_x[st_index:ed_index], key=lambda x:abs(float(x)-float(wave_length)))[0]
        picked_amplitude = amplitude[fft_x.index(picked_wave_length)]
        print("wave length: " + str(picked_wave_length) + " [Hz]")
        print("amplitute: " + str(picked_amplitude) + " [V]")

        # 結果をcsvに保存
        with open(args[3] + "/result.csv", "a", newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([picked_wave_length, picked_amplitude])
        
    
# 結果をグラフにプロット
result_frequency = pd.read_csv(args[3] + "/result.csv", header=1, usecols=[0])
result_amplitude = pd.read_csv(args[3] + "/result.csv", header=1, usecols=[1])
xy_sorted = sorted(zip(result_frequency.values, result_amplitude.values))
sorted_result_frequency, sorted_result_amplitude = zip(*xy_sorted)

plt.figure(figsize=(10,8))    
plt.plot(sorted_result_frequency, sorted_result_amplitude, 'o', lw=1)
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig(args[3] + "/result.jpg")
plt.close()