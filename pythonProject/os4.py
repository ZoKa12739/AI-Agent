import math

# 生成随机磁道号（这里简化为直接输入，可扩展为随机生成）
def generate_track_numbers(n):
    tracks = list(map(int, input("随机生成磁道号（用空格分隔）：").split()))
    while len(tracks) != n:
        print("磁道数不符，请重新输入！")
        tracks = list(map(int, input("随机生成磁道号（用空格分隔）：").split()))
    print("数据生成成功！")
    return tracks

# 显示算法选择菜单
def show_menu():
    print("****************************************")
    print("-------------- 算法选择 --------------")
    print("1. 最短寻道时间算法（SSTF）")
    print("2. 扫描算法（SCAN）")
    print("0. 退出程序")
    print("****************************************")

# 最短寻道时间优先（SSTF）算法
def sstf(tracks, current_track):
    total_movement = 0
    remaining_tracks = tracks.copy()
    accessed_tracks = []

    while remaining_tracks:
        # 找到与当前磁道距离最近的磁道
        closest_track = min(remaining_tracks, key=lambda x: abs(x - current_track))
        # 计算移动的磁道数
        total_movement += abs(closest_track - current_track)
        # 更新当前磁道
        current_track = closest_track
        # 记录访问的磁道
        accessed_tracks.append(current_track)
        # 移除已访问的磁道
        remaining_tracks.remove(current_track)

    # 计算平均寻道长度
    avg_movement = total_movement / len(accessed_tracks)
    return accessed_tracks, total_movement, avg_movement

# 扫描算法（SCAN）
def scan(tracks, current_track, direction="inward"):
    """
    direction: "inward"（向内，磁道号减小）或 "outward"（向外，磁道号增大）
    """
    total_movement = 0
    remaining_tracks = tracks.copy()
    accessed_tracks = []

    # 按磁道号排序
    remaining_tracks.sort()
    # 找到当前磁道的位置
    current_index = None
    for i, track in enumerate(remaining_tracks):
        if track >= current_track:
            current_index = i
            break
    if current_index is None:
        current_index = len(remaining_tracks) - 1

    # 根据方向扫描
    if direction == "outward":
        # 先处理当前磁道右侧的请求
        for track in remaining_tracks[current_index:]:
            total_movement += abs(track - current_track)
            current_track = track
            accessed_tracks.append(current_track)
        # 处理左侧的请求
        for track in reversed(remaining_tracks[:current_index]):
            total_movement += abs(track - current_track)
            current_track = track
            accessed_tracks.append(current_track)
    else:
        # 先处理当前磁道左侧的请求（向内）
        for track in reversed(remaining_tracks[:current_index + 1]):
            total_movement += abs(track - current_track)
            current_track = track
            accessed_tracks.append(current_track)
        # 处理右侧的请求
        for track in remaining_tracks[current_index + 1:]:
            total_movement += abs(track - current_track)
            current_track = track
            accessed_tracks.append(current_track)

    # 计算平均寻道长度
    avg_movement = total_movement / len(accessed_tracks)
    return accessed_tracks, total_movement, avg_movement

# 主程序
def main():
    n = int(input("请输入要处理的磁道数："))
    tracks = generate_track_numbers(n)

    while True:
        show_menu()
        method = input("请输入你想使用的方法：")

        if method == "0":
            print("退出程序！")
            break
        elif method == "1":
            current_track = int(input("请输入当前磁道号："))
            accessed, total, avg = sstf(tracks, current_track)
            print("排序后的磁道分布：", " ".join(map(str, sorted(tracks))))
            for track in accessed:
                print(f"当前访问的磁道：{track}")
            print(f"移动的总磁道数：{total}")
            print(f"移动的平均磁道数：{avg:.2f}")
        elif method == "2":
            current_track = int(input("请输入当前磁道号："))
            direction = input("请输入扫描方向（inward/outward）：")
            accessed, total, avg = scan(tracks, current_track, direction)
            print("排序后的磁道分布：", " ".join(map(str, sorted(tracks))))
            for track in accessed:
                print(f"当前访问的磁道：{track}")
            print(f"移动的总磁道数：{total}")
            print(f"移动的平均磁道数：{avg:.2f}")
        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()