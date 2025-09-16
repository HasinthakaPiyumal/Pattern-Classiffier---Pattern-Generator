class SortStrategy:
    def sort(self, data):
        raise NotImplementedError
class AscendingSortStrategy(SortStrategy):
    def sort(self, data):
        return sorted(data)
class DescendingSortStrategy(SortStrategy):
    def sort(self, data):
        return sorted(data, reverse=True)
class Sorter:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def perform_sort(self, data):
        return self._strategy.sort(data)
data = [3, 1, 4, 1, 5, 9, 2, 6]
sorter = Sorter(AscendingSortStrategy())
print(f"Ascending: {sorter.perform_sort(data)}")
sorter.set_strategy(DescendingSortStrategy())
print(f"Descending: {sorter.perform_sort(data)}")