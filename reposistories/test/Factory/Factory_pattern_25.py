class ShippingService:
    def calculate_cost(self, weight: float, distance: float) -> float:
        pass
    def get_delivery_estimate(self) -> str:
        pass

class StandardShipping(ShippingService):
    def calculate_cost(self, weight: float, distance: float) -> float:
        return 5.0 + (weight * 0.5) + (distance * 0.01)
    def get_delivery_estimate(self) -> str:
        return "5-7 business days"

class ExpressShipping(ShippingService):
    def calculate_cost(self, weight: float, distance: float) -> float:
        return 15.0 + (weight * 1.5) + (distance * 0.05)
    def get_delivery_estimate(self) -> str:
        return "1-2 business days"

class InternationalShipping(ShippingService):
    def calculate_cost(self, weight: float, distance: float) -> float:
        return 25.0 + (weight * 2.0) + (distance * 0.1)
    def get_delivery_estimate(self) -> str:
        return "7-14 business days"

class ShippingFactory:
    def create_shipping_service(self, service_type: str) -> ShippingService:
        if service_type == "standard":
            return StandardShipping()
        elif service_type == "express":
            return ExpressShipping()
        elif service_type == "international":
            return InternationalShipping()
        else:
            raise ValueError(f"Unknown shipping service type: {service_type}")

factory = ShippingFactory()

standard_svc = factory.create_shipping_service("standard")
express_svc = factory.create_shipping_service("express")
intl_svc = factory.create_shipping_service("international")

weight = 2.5
distance = 150.0

print(f"Standard Shipping Cost: ${standard_svc.calculate_cost(weight, distance):.2f}, Delivery: {standard_svc.get_delivery_estimate()}")
print(f"Express Shipping Cost: ${express_svc.calculate_cost(weight, distance):.2f}, Delivery: {express_svc.get_delivery_estimate()}")
print(f"International Shipping Cost: ${intl_svc.calculate_cost(weight, distance):.2f}, Delivery: {intl_svc.get_delivery_estimate()}")

try:
    drone_svc = factory.create_shipping_service("drone")
except ValueError as e:
    print(e)