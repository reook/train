def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    # 插入排序处理小数组
    def insertion_sort(array):
        arr_copy = list(array)
        for i in range(1, len(arr_copy)):
            key = arr_copy[i]
            j = i - 1
            while j >= 0 and key < arr_copy[j]:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            arr_copy[j + 1] = key
        return arr_copy
    
    if len(arr) <= 10:
        return insertion_sort(arr)
    
    # 三数取中法选择pivot
    first = arr[0]
    middle_val = arr[len(arr) // 2]
    last = arr[-1]
    pivot = sorted([first, middle_val, last])[1]
    
    # 单次遍历分割数组
    left, middle, right = [], [], []
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)
    
    return quicksort(left) + middle + quicksort(right)

# 示例
arr = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(arr))  # 输出: [1, 1, 2, 3, 6, 8, 10]
