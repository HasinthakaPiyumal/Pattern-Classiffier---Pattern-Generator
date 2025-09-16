import abc

class PathfindingStrategy(abc.ABC):
    @abc.abstractmethod
    def find_path(self, start, end):
        pass

class DirectPathfinding(PathfindingStrategy):
    def find_path(self, start, end):
        print(f"Finding direct path from {start} to {end}: [{start} -> {end}]")
        return [start, end]

class RoadNetworkPathfinding(PathfindingStrategy):
    def find_path(self, start, end):
        # In a real scenario, this would involve complex graph traversal
        intermediate_point = "City Center"
        print(f"Finding path via road network from {start} to {end}: [{start} -> {intermediate_point} -> {end}]")
        return [start, intermediate_point, end]

class Navigator:
    def __init__(self, strategy: PathfindingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PathfindingStrategy):
        self._strategy = strategy

    def navigate(self, start_location, end_location):
        return self._strategy.find_path(start_location, end_location)

if __name__ == "__main__":
    navigator = Navigator(DirectPathfinding())
    navigator.navigate("Home", "Work")

    navigator.set_strategy(RoadNetworkPathfinding())
    navigator.navigate("Airport", "Hotel")