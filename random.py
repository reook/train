import random

# 生成包含10个随机数的列表
random_numbers = [random.randint(1, 100) for _ in range(10)]

# 计算平均值
average = sum(random_numbers) / len(random_numbers)

# 输出结果
print("生成的随机数列表:", random_numbers)
print("平均值:", average)
