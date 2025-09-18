def add_shipping_insurance(func):
    def wrapper(base_price):
        price_with_insurance = func(base_price) + 5.00
        print(f"Added shipping insurance: +$5.00")
        return price_with_insurance
    return wrapper

def apply_loyalty_discount(func):
    def wrapper(base_price):
        price_after_discount = func(base_price) * 0.90
        print(f"Applied loyalty discount: -10%")
        return price_after_discount
    return wrapper

def apply_seasonal_discount(func):
    def wrapper(base_price):
        price_after_seasonal_discount = func(base_price) * 0.95
        print(f"Applied seasonal discount: -5%")
        return price_after_seasonal_discount
    return wrapper

@add_shipping_insurance
@apply_loyalty_discount
@apply_seasonal_discount
def calculate_final_price(base_price):
    print(f"Base order price: ${base_price:.2f}")
    return base_price

if __name__ == "__main__":
    initial_price = 100.00
    final_price = calculate_final_price(initial_price)
    print(f"Final price after all adjustments: ${final_price:.2f}")

    print("\n--- Another order without loyalty discount ---")
    @add_shipping_insurance
    @apply_seasonal_discount
    def calculate_final_price_no_loyalty(base_price):
        print(f"Base order price: ${base_price:.2f}")
        return base_price

    final_price_no_loyalty = calculate_final_price_no_loyalty(50.00)
    print(f"Final price after all adjustments: ${final_price_no_loyalty:.2f}")