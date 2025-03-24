# モジュールのインポート
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import csv
import os
import re
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# ローレンツ関数の定義
def lorentzian(x, A, x0, gamma):
    return A / np.pi * (gamma / ((x - x0)**2 + gamma**2))

# 合成ローレンツ関数の定義
def multi_lorentzian(x, *params):
    y = np.zeros_like(x, dtype=np.float64)
    for i in range(0, len(params), 3):
        A = params[i]
        x0 = params[i+1]
        gamma = params[i+2]
        y += lorentzian(x, A, x0, gamma)
    return y

# 引数からファイル名を取得
args = sys.argv
wave_path = args[1]
files = os.listdir(wave_path)

# 結果出力用のディレクトリを作成
output_dir = "_" + args[1]
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# 結果を保存するcsvファイルを作成
with open(output_dir + "/result.csv", "w", newline='') as csvFile:
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
        WAVE_SMP_TIME = wave_setting_data.values[1]
        wave_record_count = wave_setting_data.values[0]

        # 波形データの読み出しとフーリエ変換後のX軸単位を計算
        wave_x = pd.read_csv(path, header=None, usecols=[3])
        wave_df = pd.read_csv(path, header=None, usecols=[4])
        smp_count = len(wave_df.index.values)
        x_unit_fft = 1/WAVE_SMP_TIME/smp_count  #[Hz]
        print("FFT interval: " + str(x_unit_fft[0]) + " [Hz]")

        ## フーリエ変換前の波形をグラフに描画
        #plt.figure(figsize=(10,8))
        #plt.plot(wave_x, wave_df.values, 'o', lw=1)
        #plt.xlim([0, None])
        #plt.ylim([None, None])
        #plt.xlabel("time [s]")
        #plt.ylabel("amplitude [V]")
        #plt.savefig(args[3] + "/" + wave_length + ".jpg")
        #plt.close()

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
        ##0付近はDC成分の影響が出ているので描画しない(csvには残す)
        FQ_SEARCH_ST = x_unit_fft #[Hz]
        FQ_SEARCH_ED = float(args[2]) #[Hz]
        st_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ST).argmin()
        ed_index = np.abs(np.asarray(fft_x) - FQ_SEARCH_ED).argmin()

        ## グラフを描画して[波長].jpgで保存
        #plt.figure(figsize=(10,8))    
        #plt.plot(fft_x[st_index:ed_index],amplitude[st_index:ed_index], 'o', lw=1)
        #plt.xlim([0, float(args[2])])
        #plt.ylim([0,None])
        #plt.xlabel("frequency [Hz]")
        #plt.ylabel("amplitude [V]")
        #plt.savefig(output_dir + "/" + wave_length + "_fft.jpg")
        #plt.close()

        #wave_lengthに一番近い波長とその時の振幅を取得
        picked_wave_length = min(fft_x[st_index:ed_index], key=lambda x:abs(float(x)-float(wave_length)))[0]
        picked_wave_length = picked_wave_length[0] if isinstance(picked_wave_length, list) else picked_wave_length
        picked_amplitude = amplitude[fft_x.index(picked_wave_length)]
        print("wave length: " + str(picked_wave_length) + " [Hz]")
        print("amplitute: " + str(picked_amplitude) + " [V]")

        # 結果をcsvに保存
        with open(output_dir + "/result.csv", "a", newline='') as csvFile:
            writer = csv.writer(csvFile)
            #writer.writerow([picked_wave_length, picked_amplitude])
            writer.writerow([wave_length, picked_amplitude])

# 結果をグラフにプロット
result_frequency = pd.read_csv(output_dir + "/result.csv", header=0, usecols=[0])
result_amplitude = pd.read_csv(output_dir + "/result.csv", header=0, usecols=[1])
xy_sorted = sorted(zip(result_frequency.values, result_amplitude.values))
sorted_result_frequency, sorted_result_amplitude = zip(*xy_sorted)
sorted_result_frequency = np.ravel(sorted_result_frequency)
sorted_result_amplitude = np.ravel(sorted_result_amplitude)

# 移動平均の追加（ウィンドウサイズは3）
df = pd.DataFrame({'amplitude': sorted_result_amplitude})
df['moving_average'] = df['amplitude'].rolling(window=5).mean()

# NaNを除去（移動平均の初めの数点はNaNになるため）
df = df.dropna()

plt.figure(figsize=(10,8))    
plt.plot(sorted_result_frequency[len(sorted_result_frequency) - len(df):], df["moving_average"], 'o', lw=1)
plt.xlim([None, None])
plt.ylim([0, None])
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig(output_dir + "/av.jpg")
plt.close()

# ピーク検出（移動平均を使用）
peaks, properties = find_peaks(df['moving_average'].values, height=0.05, distance=30)
print(peaks)
print(properties)
plt.figure(figsize=(10,8))    
plt.plot(peaks, properties["peak_heights"], 'o', lw=1)
plt.xlim([0, None])
plt.ylim([0, None])
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig(output_dir + "/peaks.jpg")
plt.close()
# ピークの高さ順にソート
sorted_indices = np.argsort(properties['peak_heights'])[::-1]  # 降順にソート
sorted_peaks = peaks[sorted_indices]

n = args[3] if len(args) > 3 else 4
top_n_peaks = sorted_peaks[:int(n)]
initial_params = []
for peak in top_n_peaks:
    A = sorted_result_amplitude[peak]
    x0 = sorted_result_frequency[peak]
    half_max = A / 2.0  # 半値
    # 半値全幅（FWHM）を計算するための近似値を見つける
    indices = np.where(sorted_result_amplitude > half_max)[0]
    gamma = sorted_result_frequency[indices[-1]] - sorted_result_frequency[indices[0]]  # 幅
    initial_params.extend([A, x0, gamma])
    print("A=" + str(A) + ", x0=" + str(x0) + ", gamma=" + str(gamma))

print(initial_params)
# ローレンツ関数でフィッティング
params, covariance = curve_fit(multi_lorentzian, sorted_result_frequency, sorted_result_amplitude, p0=initial_params, maxfev=20000)
print(params)
print(covariance)

plt.figure(figsize=(10,8))    
plt.plot(sorted_result_frequency, sorted_result_amplitude, 'o', lw=1)
plt.xlim([0, None])
plt.ylim([0, None])
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig(output_dir + "/result.jpg")
plt.close()
