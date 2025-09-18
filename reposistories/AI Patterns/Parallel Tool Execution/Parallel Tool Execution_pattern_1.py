import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_inventory(item_id, quantity):
    print(f"  [Inventory Tool] Checking inventory for {quantity} of {item_id}...")
    time.sleep(random.uniform(0.5, 1.5))
    if item_id == "SKU001" and quantity <= 5:
        print(f"  [Inventory Tool] {quantity} of {item_id} available.")
        return {"tool": "inventory", "status": "success", "available": True}
    else:
        print(f"  [Inventory Tool] {quantity} of {item_id} NOT available or insufficient.")
        return {"tool": "inventory", "status": "failure", "available": False}

def process_payment(order_id, amount, payment_details):
    print(f"  [Payment Tool] Processing payment for order {order_id}, amount ${amount:.2f}...")
    time.sleep(random.uniform(1.0, 2.0))
    if random.random() > 0.1:
        print(f"  [Payment Tool] Payment for order {order_id} successful.")
        return {"tool": "payment", "status": "success", "transaction_id": f"TXN{random.randint(1000, 9999)}"}
    else:
        print(f"  [Payment Tool] Payment for order {order_id} failed.")
        return {"tool": "payment", "status": "failure", "error": "Insufficient funds or declined"}

def calculate_loyalty_points(customer_id, order_value):
    print(f"  [Loyalty Tool] Calculating loyalty points for customer {customer_id} (order value ${order_value:.2f})...")
    time.sleep(random.uniform(0.3, 0.8))
    points = int(order_value * 0.1)
    print(f"  [Loyalty Tool] Customer {customer_id} earned {points} loyalty points.")
    return {"tool": "loyalty", "status": "success", "points_earned": points}

def estimate_shipping(address, items_weight):
    print(f"  [Shipping Tool] Estimating shipping for {items_weight}kg to {address}...")
    time.sleep(random.uniform(0.7, 1.2))
    shipping_cost = items_weight * 5.0 + 10.0
    delivery_days = random.randint(3, 7)
    print(f"  [Shipping Tool] Shipping estimated: ${shipping_cost:.2f}, delivery in {delivery_days} days.")
    return {"tool": "shipping", "status": "success", "cost": shipping_cost, "delivery_days": delivery_days}

def update_inventory(item_id, quantity):
    print(f"  [Sequential] Updating inventory: Reducing {quantity} of {item_id}...")
    time.sleep(0.5)
    print(f"  [Sequential] Inventory updated for {item_id}.")
    return {"tool": "update_inventory", "status": "success"}

def generate_invoice(order_details, payment_info, shipping_info, loyalty_info):
    print(f"  [Sequential] Generating invoice for order {order_details['order_id']}...")
    time.sleep(0.7)
    invoice_id = f"INV{random.randint(10000, 99999)}"
    print(f"  [Sequential] Invoice {invoice_id} generated. Total: ${order_details['total_amount'] + shipping_info['cost']:.2f}")
    return {"tool": "generate_invoice", "status": "success", "invoice_id": invoice_id}


def process_order_parallel(order_details):
    """
    Implements the Parallel Tool Execution Design Pattern for e-commerce order processing.

    Real-world usage: An e-commerce system processing customer orders, where tasks like
    inventory check, payment processing, loyalty points calculation, and shipping estimation
    can run concurrently.

    Simulation pattern: Utilizes `time.sleep()` to simulate network latency, database
    access, and external API calls, making the tasks I/O-bound and suitable for
    `ThreadPoolExecutor`. Randomness is introduced for payment success/failure.
    """
    order_id = order_details["order_id"]
    customer_id = order_details["customer_id"]
    item_id = order_details["item_id"]
    quantity = order_details["quantity"]
    total_amount = order_details["total_amount"]
    payment_details = order_details["payment_details"]
    shipping_address = order_details["shipping_address"]
    items_weight = order_details["items_weight"]

    print(f"\n--- Starting Parallel Order Processing for Order {order_id} ---")

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_inventory = executor.submit(check_inventory, item_id, quantity)
        future_payment = executor.submit(process_payment, order_id, total_amount, payment_details)
        future_loyalty = executor.submit(calculate_loyalty_points, customer_id, total_amount)
        future_shipping = executor.submit(estimate_shipping, shipping_address, items_weight)

        print("\n  [Orchestrator] Waiting for parallel tasks to complete...")
        for future in as_completed([future_inventory, future_payment, future_loyalty, future_shipping]):
            result = future.result()
            results[result["tool"]] = result

    print("\n  [Orchestrator] All parallel tasks completed. Checking dependencies...")

    inventory_ok = results.get("inventory", {}).get("available", False)
    payment_ok = results.get("payment", {}).get("status") == "success"

    if inventory_ok and payment_ok:
        print(f"\n--- Core Order Fulfillment for Order {order_id} - Prerequisites Met! ---")
        update_inventory_result = update_inventory(item_id, quantity)
        generate_invoice_result = generate_invoice(
            order_details,
            results.get("payment"),
            results.get("shipping"),
            results.get("loyalty")
        )
        print(f"\n--- Order {order_id} Processed Successfully! ---")
        return {
            "order_status": "completed",
            "final_results": {
                **results,
                "update_inventory": update_inventory_result,
                "generate_invoice": generate_invoice_result
            }
        }
    else:
        print(f"\n--- Order {order_id} Processing Failed - Prerequisites Not Met! ---")
        if not inventory_ok:
            print("  Reason: Insufficient inventory.")
        if not payment_ok:
            print("  Reason: Payment failed.")
        return {
            "order_status": "failed",
            "final_results": results
        }

if __name__ == "__main__":
    order_1 = {
        "order_id": "ORD789",
        "customer_id": "CUST123",
        "item_id": "SKU001",
        "quantity": 2,
        "total_amount": 150.75,
        "payment_details": {"card_type": "Visa", "last_four": "1234"},
        "shipping_address": "123 Main St, Anytown, USA",
        "items_weight": 0.8
    }

    order_2 = {
        "order_id": "ORD790",
        "customer_id": "CUST124",
        "item_id": "SKU002",
        "quantity": 10,
        "total_amount": 250.00,
        "payment_details": {"card_type": "Mastercard", "last_four": "5678"},
        "shipping_address": "456 Oak Ave, Otherville, USA",
        "items_weight": 2.5
    }

    order_3 = {
        "order_id": "ORD791",
        "customer_id": "CUST125",
        "item_id": "SKU001",
        "quantity": 1,
        "total_amount": 50.00,
        "payment_details": {"card_type": "Amex", "last_four": "9012"},
        "shipping_address": "789 Pine Ln, Somewhere, USA",
        "items_weight": 0.3
    }
    
    print("-----------------------------------------------------")
    print("       Processing Order 1 (Expected: Success)        ")
    print("-----------------------------------------------------")
    result_1 = process_order_parallel(order_1)
    import json
    print("\nFinal Result 1:")
    print(json.dumps(result_1, indent=2))

    print("\n\n-----------------------------------------------------\n")
    print("       Processing Order 2 (Expected: Inventory Fail) ")
    print("-----------------------------------------------------\n")
    result_2 = process_order_parallel(order_2)
    print("\nFinal Result 2:")
    print(json.dumps(result_2, indent=2))

    print("\n\n-----------------------------------------------------\n")
    print("       Processing Order 3 (Expected: Random Payment Fail) ")
    print("-----------------------------------------------------\n")
    result_3 = process_order_parallel(order_3)
    print("\nFinal Result 3:")
    print(json.dumps(result_3, indent=2))