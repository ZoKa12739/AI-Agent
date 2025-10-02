import pandas as pd
from fitparse import FitFile
import matplotlib.pyplot as plt

def visualize_heart_rate(file_path):
    """
    解析.fit文件，计算并打印每分钟平均心率，然后绘制成折线图。

    :param file_path: .fit文件的路径
    """
    try:
        # --- 1. 数据提取和处理 (与之前相同) ---
        fitfile = FitFile(file_path)
        data_points = []
        for record in fitfile.get_messages('record'):
            timestamp, heart_rate = None, None
            for data in record:
                if data.name == 'timestamp':
                    timestamp = data.value
                elif data.name == 'heart_rate':
                    heart_rate = data.value
            if timestamp and heart_rate:
                data_points.append({'time': timestamp, 'heart_rate': heart_rate})

        if not data_points:
            print("文件中未找到有效的心率数据。")
            return

        df = pd.DataFrame(data_points)
        df.set_index('time', inplace=True)

        # 使用 'min' 替换 'T'
        minute_avg_hr = df['heart_rate'].resample('min').mean().dropna()

        print("--- 每分钟平均心率 ---")
        print(minute_avg_hr.astype(int))
        print("--- 分析完毕 ---")


        # --- 2. 新增的绘图功能 ---
        print("正在生成心率图表...")

        # 创建一个图形窗口，设置尺寸
        plt.figure(figsize=(12, 6))

        # 绘制折线图，设置标记和线条样式
        minute_avg_hr.plot(kind='line', marker='o', linestyle='-')

        # 添加中文支持 (如果显示乱码，需要设置字体)
        plt.rcParams['font.sans-serif'] = ['SimHei'] # 例如 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        # 设置图表标题和坐标轴标签
        plt.title('每分钟平均心率变化图 (Average Heart Rate Per Minute)')
        plt.xlabel('时间 (Time)')
        plt.ylabel('平均心率 (Avg Heart Rate - bpm)')

        # 添加网格线，让图表更容易阅读
        plt.grid(True)

        # 优化布局，防止标签重叠
        plt.tight_layout()

        # 显示图表
        plt.show()

    except Exception as e:
        print(f"处理文件时出错: {e}")

# --- 使用方法 ---
your_file_path = r'C:\StudyHub\竞赛资料\AI模型智能体大赛\运动数据\Zepp20250927180647.fit' # 请确保路径正确
visualize_heart_rate(your_file_path)