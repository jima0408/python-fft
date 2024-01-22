import numpy as np
import sys
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import csv
import pandas as pd
import matplotlib.pyplot as plt

# ローレンツ関数の定義
def lorentzian(x, A, x0, gamma):
    return A / np.pi * (gamma / ((x - x0)**2 + gamma**2))

def get_args():
    data = str(input("csvファイルのパスを入力してください："))
    fq_st = int(input("フィッティングの開始周波数を入力してください："))
    fq_ed = int(input("フィッティングの終了周波数を入力してください："))
    output_dir = str(input("結果を出力するディレクトリを入力してください："))
    return data, fq_st, fq_ed, output_dir

# 引数の取得
data, fq_st, fq_ed, output_dir = get_args()

# 結果をグラフにプロット
result_frequency = pd.read_csv(data, header=0, usecols=[0])
result_amplitude = pd.read_csv(data, header=0, usecols=[1])
xy_sorted = sorted(zip(result_frequency.values, result_amplitude.values))
sorted_result_frequency, sorted_result_amplitude = zip(*xy_sorted)
sorted_result_frequency = np.ravel(sorted_result_frequency)
sorted_result_amplitude = np.ravel(sorted_result_amplitude)

# 移動平均の追加（ウィンドウサイズは3）
df = pd.DataFrame({'amplitude': sorted_result_amplitude})
df['moving_average'] = df['amplitude'].rolling(window=5).mean()

# NaNを除去（移動平均の初めの数点はNaNになるため）
df = df.dropna()

# 特定の周波数領域のデータを指定
indices = (sorted_result_frequency >= fq_st) & (sorted_result_frequency <= fq_ed)
selected_frequency = sorted_result_frequency[indices]
selected_amplitude = sorted_result_amplitude[indices]

# ピーク検出（移動平均を使用）
peaks, properties = find_peaks(selected_amplitude, height=0.02, distance=30)
# ピークの高さ順にソート
sorted_indices = np.argsort(properties['peak_heights'])[::-1]  # 降順にソート
sorted_peaks = peaks[sorted_indices]

n = 1
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

# ローレンツ関数でフィッティング
params, covariance = curve_fit(lorentzian, selected_frequency, selected_amplitude, p0=initial_params, maxfev=20000)
print(params)

plt.figure(figsize=(10,8))    
plt.plot(sorted_result_frequency, sorted_result_amplitude, 'o', lw=1)
plt.plot(selected_frequency, lorentzian(selected_frequency, *params), label='Fitted', color='red')
#plt.xlim([0, None])
plt.xlim([None, None])
plt.ylim([0, None])
plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude [V]")
plt.savefig(output_dir + "/lorenz.jpg")
plt.close()

# Q値と半値幅をcsvに保存
FWHM = 2 * params[1]
Q_value = params[2] / FWHM
f = initial_params[1]

# 結果をDataFrameに格納
results = pd.DataFrame({
    "Parameter": ["FWHM", "Q_value", "f"],
    "Value": [FWHM, Q_value, f]
})

csv_file_path = output_dir + "/fitting_results.csv"
results.to_csv(csv_file_path, index=False)
