# import tushare as ts

# #设置你的token，登录tushare在个人用户中心里拷贝
# ts.set_token('cc9a2a9b32df44e3d63b87af8efd4da41b111a746ab7d59a944fc480')

# #sina数据
# df = ts.realtime_quote(ts_code='000058.SZ,000001.SH')


# #东财数据
# # df = ts.realtime_quote(ts_code='600000.SH', src='dc')


# print(df)
# print(df.columns)

import winsound
import time

def test_sound_alerts():
    print("开始声音警告测试程序...")
    
    # 测试1：基础的Beep声
    print("\n测试1：基础Beep声")
    print("播放1000Hz，持续1秒...")
    winsound.Beep(1000, 1000)
    time.sleep(1)
    
    # 测试2：警报声（频率更高）
    print("\n测试2：高频警报声")
    print("播放2000Hz，持续1秒...")
    winsound.Beep(2000, 1000)
    time.sleep(1)
    
    # 测试3：连续警报声
    print("\n测试3：连续警报声")
    print("播放3次短促的警报声...")
    for _ in range(3):
        winsound.Beep(1500, 200)
        time.sleep(0.2)
    
    # 测试4：渐进式警报声
    print("\n测试4：渐进式警报声")
    print("频率逐渐升高...")
    for freq in range(500, 2000, 500):
        print(f"频率: {freq}Hz")
        winsound.Beep(freq, 500)
        time.sleep(0.2)

def main():
    while True:
        print("\n声音警告测试菜单：")
        print("1. 测试所有声音警告")
        print("2. 测试自定义声音")
        print("3. 退出")
        
        choice = input("\n请选择测试项目 (1-3): ").strip()
        
        if choice == '1':
            test_sound_alerts()
        elif choice == '2':
            try:
                frequency = int(input("请输入声音频率(Hz, 范围37-32767): "))
                duration = int(input("请输入持续时间(毫秒): "))
                print(f"\n播放 {frequency}Hz，持续 {duration}毫秒...")
                winsound.Beep(frequency, duration)
            except ValueError:
                print("请输入有效的数字！")
            except Exception as e:
                print(f"发生错误: {e}")
        elif choice == '3':
            print("退出测试程序...")
            break
        else:
            print("无效的选择，请重试！")

if __name__ == "__main__":
    main()