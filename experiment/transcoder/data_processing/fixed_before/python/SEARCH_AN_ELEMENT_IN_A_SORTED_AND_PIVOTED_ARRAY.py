def f_gold(arr, l, h, key):
    if l > h:
        return - 1
    mid = (l + h) // 2
    if arr[mid] == key:
        return mid
    if arr[l] <= arr[mid]:
        if key >= arr[l] and key <= arr[mid]:
            return f_gold(arr, l, mid - 1, key)
        return f_gold(arr, mid + 1, h, key)
    if key >= arr[mid] and key <= arr[h]:
        return f_gold(arr, mid + 1, h, key)
    return f_gold(arr, l, mid - 1, key)
f_gold(*([5, 6, 7, 8, 9, 10, 1, 2, 3], 0, 8, 3))