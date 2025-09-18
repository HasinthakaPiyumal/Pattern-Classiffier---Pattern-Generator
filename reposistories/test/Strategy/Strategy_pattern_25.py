import abc
import math
import random

class RouteOptimizationStrategy(abc.ABC):
    @abc.abstractmethod
    def optimize_route(self, stops):
        pass

class ShortestDistanceRoute(RouteOptimizationStrategy):
    def _distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def optimize_route(self, stops):
        if not stops:
            return [], 0.0

        unvisited = set(range(len(stops)))
        current_stop_idx = 0
        path = [current_stop_idx]
        total_distance = 0.0

        unvisited.remove(current_stop_idx)

        while unvisited:
            next_stop_idx = -1
            min_dist = float('inf')

            for i in unvisited:
                dist = self._distance(stops[current_stop_idx], stops[i])
                if dist < min_dist:
                    min_dist = dist
                    next_stop_idx = i

            if next_stop_idx != -1:
                path.append(next_stop_idx)
                total_distance += min_dist
                current_stop_idx = next_stop_idx
                unvisited.remove(next_stop_idx)
            else:
                break

        print(f"Optimized route by shortest distance: Path {path}, Total Distance {total_distance:.2f}")
        return path, total_distance

class FastestTimeRoute(RouteOptimizationStrategy):
    def _travel_time(self, p1, p2, traffic_factor=1.0):
        base_distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        base_time = base_distance / 10.0
        return base_time * traffic_factor

    def optimize_route(self, stops):
        if not stops:
            return [], 0.0

        unvisited = set(range(len(stops)))
        current_stop_idx = 0
        path = [current_stop_idx]
        total_time = 0.0

        unvisited.remove(current_stop_idx)

        while unvisited:
            next_stop_idx = -1
            min_time = float('inf')
            traffic_factor = random.uniform(0.8, 1.5)

            for i in unvisited:
                time_taken = self._travel_time(stops[current_stop_idx], stops[i], traffic_factor)
                if time_taken < min_time:
                    min_time = time_taken
                    next_stop_idx = i

            if next_stop_idx != -1:
                path.append(next_stop_idx)
                total_time += min_time
                current_stop_idx = next_stop_idx
                unvisited.remove(next_stop_idx)
            else:
                break

        print(f"Optimized route by fastest time (simulated traffic): Path {path}, Total Time {total_time:.2f} hours")
        return path, total_time

class DeliveryService:
    def __init__(self, name, optimization_strategy: RouteOptimizationStrategy):
        self._name = name
        self._stops = []
        self._strategy = optimization_strategy

    def add_stop(self, x, y):
        self._stops.append((x, y))

    def set_optimization_strategy(self, strategy: RouteOptimizationStrategy):
        self._strategy = strategy

    def plan_delivery(self):
        print(f"\n--- {self._name} Delivery Planning ---")
        if not self._stops:
            print("No stops added for delivery.")
            return
        print(f"Stops to deliver: {self._stops}")
        self._strategy.optimize_route(self._stops)

if __name__ == "__main__":
    delivery_stops = [(0, 0), (10, 5), (3, 12), (15, 8), (7, 2)]

    service1 = DeliveryService("Express Logistics", ShortestDistanceRoute())
    for stop in delivery_stops:
        service1.add_stop(stop[0], stop[1])
    service1.plan_delivery()

    service2 = DeliveryService("QuickShip Courier", FastestTimeRoute())
    for stop in delivery_stops:
        service2.add_stop(stop[0], stop[1])
    service2.plan_delivery()

    service1.set_optimization_strategy(FastestTimeRoute())
    service1.plan_delivery()