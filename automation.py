import pyvisa as visa
visa.log_to_screen()
import time

def get_args():
    start_freq = int(input("周波数の開始値を入力してください："))
    termination = int(input("周波数の終端値を入力してください："))
    step_width = int(input("周波数増加のステップ幅を入力してください："))
    save_dir = str(input("保存先のディレクトリ名を指定してください（例: data/20211211)："))
    return start_freq,termination,step_width,save_dir

# 初期値の取得
start_freq, termination, step_width, save_dir = get_args()

# pyvisaの初期化
rm = visa.ResourceManager()

# 接続されているすべてのVISAリソースの一覧を取得
resources = rm.list_resources()

print("接続されているVISAリソースの一覧:")
for resource in resources:
    print(resource)

func_gen = rm.open_resource('GPIB0::11::INSTR')
scope = rm.open_resource('GPIB0::1::INSTR')


# ファンクションジェネレーターの出力を最大に設定
func_gen.write('VOLTAGE:AMPLITUDE 10.00')
# オシロスコープの出力をsin波に指定
func_gen.write('FUNCTION SIN')
print("ファンクションジェネレーターの設定完了")
# オシロスコープの波形保存形式をcsvに指定
scope.write('SAVe:WAVEform:FILEFormat SPREADSHEETCsv')
print("オシロスコープの設定完了")
print("セッティング完了")

freq = start_freq # 開始周波数
while freq <= termination:
    print(str(freq) + "Hz")
    func_gen.write('FREQUENCY '+ str(freq)) # ファンクションジェネレータの周波数設定
    func_gen.write('OUTPut1:STATe ON') # 設定した周波数で出力
    time.sleep(1)

    # 保存先(USB固定)
    csvName = '"E:/' + save_dir + '/' + str(freq) + '.csv"'

    print(csvName)

    scope.write('SAVe:WAVEform CH1, ' + csvName) # CHは使っているチャンネルに応じて適宜変更
    time.sleep(3)

    freq += step_width

# 出力を止めて接続解除
func_gen.write('OUTPut1:STATe OFF')
func_gen.close()
scope.close()
rm.close()
