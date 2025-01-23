def generate_heart():
    x_scale = 0.05  # 水平缩放系数，补偿终端字符宽高比
    y_scale = 0.1   # 垂直缩放系数
    
    for y in range(15, -15, -1):
        line = []
        for x in range(-30, 30):
            # 将像素坐标转换为数学坐标
            x_norm = x * x_scale
            y_norm = y * y_scale
            
            # 心形隐式方程计算
            heart_eq = (x_norm**2 + y_norm**2 - 1)**3 - x_norm**2 * y_norm**3
            if heart_eq <= 0:
                # 使用ANSI转义码显示红色星号
                line.append('\033[31m*\033[0m')
            else:
                line.append(' ')
        print(''.join(line))

generate_heart()
