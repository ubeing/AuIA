# 实现一个数组的冒泡排序函数
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
# 测试数组
arr = [64, 34, 25, 12, 22, 11, 90]
bubbleSort(arr)
print ("排序后的数组:")
for i in range(len(arr)):
    print ("%d" %arr[i]),
# 输出结果
# 排序后的数组:
# 11 12 22 25 34 64 90

# Path: firstPython.py
# 实现一个数组的选择排序函数
def selectionSort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# 测试数组
arr = [64, 25, 12, 22, 11]
selectionSort(arr)
print ("排序后的数组:")
for i in range(len(arr)):
    print ("%d" %arr[i]),
# 输出结果
# 排序后的数组:
# 11 12 22 25 64
