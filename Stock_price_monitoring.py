import tushare as ts
import time
from datetime import datetime
import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import winsound  # Windows系统使用
# 或者使用
# from playsound import playsound  # 跨平台使用

class StockMonitor:
    def __init__(self, config_path='config.json'):
        # 加载配置
        self.load_config(config_path)

        # 初始化日志
        self.setup_logging()

        # 设置 Tushare Token 并初始化
        ts.set_token(self.config['tushare_token'])
        self.api = ts
        self.positions = {}
        self.alert_threshold = self.config.get('alert_threshold', 0.05)
        self.positions_file = self.config.get('positions_file', 'positions.json')
        self.max_retries = self.config.get('max_retries', 3)
        self.timeout = self.config.get('timeout', 5)
        self.alert_sound_freq = 1000
        self.alert_sound_duration = 1000
        self.load_positions()

    def load_config(self, config_path):
        """加载配置文件"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件 {config_path} 不存在。")
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def setup_logging(self):
        """配置日志记录"""
        log_file = self.config.get('log_file', 'stock_monitor.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.info("日志系统初始化完成。")

    def load_positions(self):
        """从文件加载已保存的持仓信息"""
        if os.path.exists(self.positions_file):
            try:
                with open(self.positions_file, 'r') as f:
                    self.positions = json.load(f)
                logging.info("持仓信息加载成功。")
            except json.JSONDecodeError as e:
                logging.error(f"加载持仓信息失败: {e}")
                self.positions = {}
        else:
            logging.info("持仓文件不存在，初始化为空。")
            self.positions = {}

    def save_positions(self):
        """保存持仓信息到文件"""
        try:
            with open(self.positions_file, 'w') as f:
                json.dump(self.positions, f, ensure_ascii=False, indent=4)
            logging.info("持仓信息保存成功。")
        except Exception as e:
            logging.error(f"保存持仓信息失败: {e}")

    def add_position(self, stock_code, buy_price, shares):
        """添加股票持仓"""
        if not stock_code.startswith(('6', '0', '3')):
            print("请输入正确的股票代码!")
            logging.warning(f"无效的股票代码: {stock_code}")
            return
        
        self.positions[stock_code] = {
            'buy_price': float(buy_price),
            'shares': int(shares)
        }
        self.save_positions()
        print(f"已添加股票{stock_code}的持仓信息")
        logging.info(f"添加持仓: {stock_code}, 买入价: {buy_price}, 数量: {shares}")

    def get_real_time_price(self, stock_code):
        """使用 ts.realtime_quote 获取实时股价，带有重试机制"""
        for attempt in range(1, self.max_retries + 1):
            try:
                # 获取实时行情，支持多个股票代码以逗号分隔
                df = self.api.realtime_quote(ts_code=stock_code)
                if df.empty:
                    logging.warning(f"未获取到 {stock_code} 的实时数据。")
                    return None
                current_price = float(df.iloc[0]['PRICE'])
                logging.info(f"获取到 {stock_code} 的当前价格: {current_price}")
                return current_price
            except Exception as e:
                logging.warning(f"尝试第 {attempt} 次获取 {stock_code} 实时价格失败: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(1)  # 等待1秒后重试
                continue
                
        logging.error(f"获取 {stock_code} 实时价格失败，已重试 {self.max_retries} 次。")
        return None

    def play_alert_sound(self):
        """播放警告声音"""
        try:
            # Windows系统使用 winsound
            winsound.Beep(self.alert_sound_freq, self.alert_sound_duration)
            
            # 或者使用 playsound（跨平台）
            # playsound('alert.wav')  # 需要准备一个音频文件
        except Exception as e:
            logging.error(f"播放警告声音失败: {e}")

    def monitor_stocks(self):
        """监控股票价格"""
        monitor_interval = self.config.get('monitor_interval', 10)
        max_workers = self.config.get('max_workers', 5)
        logging.info("开始监控股票价格。")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                print("\n" + "="*50)
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"当前时间: {current_time}")
                logging.info("监控循环开始。")

                # 提交所有股票的价格获取任务
                future_to_stock = {executor.submit(self.get_real_time_price, code): code for code in self.positions}

                for future in as_completed(future_to_stock):
                    stock_code = future_to_stock[future]
                    current_price = future.result()
                    if current_price is None:
                        print(f"获取{stock_code}价格失败，请检查网络或股票代码")
                        logging.error(f"获取 {stock_code} 价格失败。")
                        continue

                    info = self.positions[stock_code]
                    buy_price = info['buy_price']
                    shares = info['shares']

                    # 计算收益率
                    change_rate = (current_price - buy_price) / buy_price
                    profit = (current_price - buy_price) * shares

                    # 打印信息
                    print(f"\n股票代码: {stock_code}")
                    print(f"买入价: {buy_price:.2f}")
                    print(f"当前价: {current_price:.2f}")
                    print(f"持仓数量: {shares}")
                    print(f"收益率: {change_rate*100:.2f}%")
                    print(f"盈亏: {profit:.2f}")
                    logging.info(f"{stock_code}: 买入价={buy_price}, 当前价={current_price}, 持仓={shares}, 收益率={change_rate*100:.2f}%, 盈亏={profit}")

                    # 预警判断
                    if abs(change_rate) >= self.alert_threshold:
                        warning_msg = f"警告: {stock_code} 股价波动超过 {self.alert_threshold*100:.2f}%!"
                        print(warning_msg)
                        logging.warning(warning_msg)
                        self.play_alert_sound()

                logging.info(f"监控循环结束，等待 {monitor_interval} 秒后继续。")
                time.sleep(monitor_interval)  # 等待指定时间后再次监控

def main():
    monitor = StockMonitor()
    
    while True:
        print("\n1. 添加股票持仓")
        print("2. 开始监控")
        print("3. 退出")
        
        choice = input("请选择操作: ").strip()
        
        if choice == '1':
            stock_code = input("请输入股票代码: ").strip()
            try:
                buy_price = float(input("请输入买入价格: ").strip())
                shares = int(input("请输入持仓数量: ").strip())
                monitor.add_position(stock_code, buy_price, shares)
            except ValueError:
                print("输入无效，请确保买入价格是数字，持仓数量是整数。")
                logging.error("用户输入无效的数据。")
        elif choice == '2':
            print("开始监控股票价格...")
            monitor.monitor_stocks()
        elif choice == '3':
            print("退出程序。")
            logging.info("用户选择退出程序。")
            break
        else:
            print("无效的选择，请重试")
            logging.warning(f"用户输入无效的选择: {choice}")

if __name__ == "__main__":
    main()
