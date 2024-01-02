list = [4, 2, 8, 9, 7, 1, 3]


def selectionSort(list):
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            min_idx = i
            if list[min_idx] > list[j]:
                min_idx = j
            list[i], list[min_idx] = list[min_idx], list[i]
    return list


print(selectionSort(list))
