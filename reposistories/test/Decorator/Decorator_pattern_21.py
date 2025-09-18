class Order:
    def __init__(self, description, cost):
        self._description = description
        self._cost = cost

    def get_cost(self):
        return self._cost

    def get_description(self):
        return self._description

class OrderDecorator:
    def __init__(self, decorated_order):
        self._decorated_order = decorated_order

    def get_cost(self):
        return self._decorated_order.get_cost()

    def get_description(self):
        return self._decorated_order.get_description()

class DiscountDecorator(OrderDecorator):
    def __init__(self, decorated_order, discount_percentage):
        super().__init__(decorated_order)
        self._discount_percentage = discount_percentage

    def get_cost(self):
        base_cost = super().get_cost()
        return base_cost * (1 - self._discount_percentage / 100)

    def get_description(self):
        return super().get_description() + f", with {self._discount_percentage}% discount"

class ShippingCostDecorator(OrderDecorator):
    def __init__(self, decorated_order, shipping_fee):
        super().__init__(decorated_order)
        self._shipping_fee = shipping_fee

    def get_cost(self):
        return super().get_cost() + self._shipping_fee

    def get_description(self):
        return super().get_description() + f", plus ${self._shipping_fee:.2f} shipping"

class GiftWrapDecorator(OrderDecorator):
    def __init__(self, decorated_order, wrap_cost):
        super().__init__(decorated_order)
        self._wrap_cost = wrap_cost

    def get_cost(self):
        return super().get_cost() + self._wrap_cost

    def get_description(self):
        return super().get_description() + f", with gift wrap (${self._wrap_cost:.2f})"

if __name__ == "__main__":
    base_order = Order("Laptop and accessories", 1200.00)
    print(f"Base Order: {base_order.get_description()} Cost: ${base_order.get_cost():.2f}")

    order_with_discount = DiscountDecorator(base_order, 10)
    print(f"Discounted Order: {order_with_discount.get_description()} Cost: ${order_with_discount.get_cost():.2f}")

    order_with_shipping = ShippingCostDecorator(order_with_discount, 25.00)
    print(f"Discounted + Shipping: {order_with_shipping.get_description()} Cost: ${order_with_shipping.get_cost():.2f}")

    final_order = GiftWrapDecorator(order_with_shipping, 5.00)
    print(f"Final Order: {final_order.get_description()} Cost: ${final_order.get_cost():.2f}")

    another_order = Order("Book", 20.00)
    another_order = ShippingCostDecorator(another_order, 3.50)
    another_order = DiscountDecorator(another_order, 5)
    print(f"Another Order: {another_order.get_description()} Cost: ${another_order.get_cost():.2f}")