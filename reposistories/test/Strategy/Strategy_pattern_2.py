import abc

class SortingStrategy(abc.ABC):
    @abc.abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortingStrategy):
    def sort(self, data):
        n = len(data)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        print(f"Bubble sorted: {data}")
        return data

class QuickSort(SortingStrategy):
    def sort(self, data):
        def _quick_sort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return _quick_sort(left) + middle + _quick_sort(right)
        sorted_data = _quick_sort(list(data)) # Create a copy to avoid modifying original list in _quick_sort
        print(f"Quick sorted: {sorted_data}")
        return sorted_data

class Sorter:
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortingStrategy):
        self._strategy = strategy

    def execute_sort(self, data):
        return self._strategy.sort(data)

if __name__ == "__main__":
    data1 = [3, 1, 4, 1, 5, 9, 2, 6]
    sorter = Sorter(BubbleSort())
    sorter.execute_sort(list(data1)) # Pass a copy

    data2 = [5, 2, 8, 1, 9, 4]
    sorter.set_strategy(QuickSort())
    sorter.execute_sort(list(data2)) # Pass a copy