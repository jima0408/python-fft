import pyvisa as visa
visa.log_to_screen()
import time

def get_args():
    termination = int(input("周波数の終端値を入力してください："))
    step_width = int(input("周波数増加のステップ幅を入力してください："))
    save_dir = str(input("保存先のディレクトリ名を指定してください（例: data/20211211)："))
    return termination, step_width, save_dir

# 初期値の取得
termination, step_width, save_dir = get_args()

# pyvisaの初期化
rm = visa.ResourceManager()

# 接続されているすべてのVISAリソースの一覧を取得
resources = rm.list_resources()

print("接続されているVISAリソースの一覧:")
for resource in resources:
    print(resource)

# FGとオシロのアドレス指定
func_gen = rm.open_resource('GPIB0::11::INSTR')
scope = rm.open_resource('GPIB0::1::INSTR')

# ファンクションジェネレーターの出力と波形の設定
func_gen.write('VOLTAGE:AMPLITUDE 10.00') # 最大値(10Vpp)
func_gen.write('FUNCTION SIN')
# オシロの波形保存形式をcsvに指定
scope.write('SAVe:WAVEform:FILEFormat SPREADSHEETCsv')
print("セッティング完了")

freq = 10 # 波長の最低値
while freq <= termination:
    print(str(freq) + "Hz")
    func_gen.write('FREQUENCY '+ str(freq))
    func_gen.write('OUTPut1:STATe ON')
    time.sleep(1)

    # 保存先(USB固定)
    csvName = '"E:/' + save_dir + '/' + str(freq) + '.csv"'
    print(csvName)

    # 波形の保存(CHは適宜設定)
    scope.write('SAVe:WAVEform CH2, ' + csvName)
    time.sleep(3)

    freq += step_width

func_gen.write('OUTPut1:STATe OFF')
func_gen.close()
scope.close()
rm.close()
