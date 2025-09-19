import uuid

class OrderValidationService:
    def process(self, order_data):
        print(f"Service: Validating Order ID {order_data['order_id']}...")
        if not order_data.get('items'):
            return {'status': 'failed', 'reason': 'No items in order'}
        if order_data.get('total_amount', 0) <= 0:
            return {'status': 'failed', 'reason': 'Invalid total amount'}
        for item in order_data['items']:
            if item.get('quantity', 0) <= 0:
                return {'status': 'failed', 'reason': f"Invalid quantity for item {item.get('product_id')}"}
        order_data['validation_status'] = 'success'
        print(f"Service: Order ID {order_data['order_id']} validated.")
        return order_data

class PaymentProcessingService:
    def process(self, order_data):
        if order_data.get('validation_status') != 'success':
            return {'status': 'failed', 'reason': 'Order not validated'}
        print(f"Service: Processing payment for Order ID {order_data['order_id']} (Amount: {order_data['total_amount']})...")
        payment_successful = True
        if payment_successful:
            order_data['payment_status'] = 'paid'
            order_data['transaction_id'] = str(uuid.uuid4())
            print(f"Service: Payment successful for Order ID {order_data['order_id']}. Transaction ID: {order_data['transaction_id']}")
        else:
            order_data['payment_status'] = 'failed'
            order_data['reason'] = 'Payment failed'
            print(f"Service: Payment failed for Order ID {order_data['order_id']}.")
        return order_data

class InventoryUpdateService:
    def process(self, order_data):
        if order_data.get('payment_status') != 'paid':
            return {'status': 'failed', 'reason': 'Payment not successful'}
        print(f"Service: Updating inventory for Order ID {order_data['order_id']}...")
        for item in order_data['items']:
            print(f"  - Decrementing stock for product {item['product_id']} by {item['quantity']}")
        order_data['inventory_status'] = 'updated'
        print(f"Service: Inventory updated for Order ID {order_data['order_id']}.")
        return order_data

class ShippingLabelGenerationService:
    def process(self, order_data):
        if order_data.get('inventory_status') != 'updated':
            return {'status': 'failed', 'reason': 'Inventory not updated'}
        print(f"Service: Generating shipping label for Order ID {order_data['order_id']}...")
        shipping_id = f"SHIP-{str(uuid.uuid4())[:8].upper()}"
        order_data['shipping_label_id'] = shipping_id
        order_data['shipping_status'] = 'generated'
        print(f"Service: Shipping label '{shipping_id}' generated for Order ID {order_data['order_id']}.")
        return order_data

class ConfirmationEmailService:
    def process(self, order_data):
        if order_data.get('shipping_status') != 'generated':
            return {'status': 'failed', 'reason': 'Shipping label not generated'}
        print(f"Service: Sending confirmation email for Order ID {order_data['order_id']}...")
        customer_email = order_data.get('customer_email', 'unknown@example.com')
        print(f"  - Email sent to {customer_email} with order details and shipping ID {order_data['shipping_label_id']}.")
        order_data['email_status'] = 'sent'
        print(f"Service: Confirmation email sent for Order ID {order_data['order_id']}.")
        return order_data

class OrderProcessingPipeline:
    def __init__(self, services):
        self.services = services

    def run_pipeline(self, initial_data):
        current_data = initial_data.copy()
        print(f"\n--- Starting Order Processing Pipeline for Order ID: {current_data.get('order_id')} ---")
        for service in self.services:
            print(f"Executing step: {service.__class__.__name__}")
            result = service.process(current_data)
            if result.get('status') == 'failed':
                print(f"Pipeline failed at {service.__class__.__name__}: {result.get('reason')}")
                return result
            current_data = result
        print(f"--- Order Processing Pipeline completed for Order ID: {current_data.get('order_id')} ---")
        return current_data

if __name__ == "__main__":
    validation_service = OrderValidationService()
    payment_service = PaymentProcessingService()
    inventory_service = InventoryUpdateService()
    shipping_service = ShippingLabelGenerationService()
    email_service = ConfirmationEmailService()

    ecommerce_pipeline = OrderProcessingPipeline([
        validation_service,
        payment_service,
        inventory_service,
        shipping_service,
        email_service
    ])

    order_data_1 = {
        'order_id': 'ORD-001',
        'customer_id': 'CUST-001',
        'customer_email': 'alice@example.com',
        'items': [
            {'product_id': 'PROD-A', 'quantity': 2, 'price': 10.00},
            {'product_id': 'PROD-B', 'quantity': 1, 'price': 25.00}
        ],
        'total_amount': 45.00
    }

    final_order_status_1 = ecommerce_pipeline.run_pipeline(order_data_1)
    print("\nFinal Order Status 1:")
    print(final_order_status_1)

    order_data_2 = {
        'order_id': 'ORD-002',
        'customer_id': 'CUST-002',
        'customer_email': 'bob@example.com',
        'items': [],
        'total_amount': 0.00
    }

    final_order_status_2 = ecommerce_pipeline.run_pipeline(order_data_2)
    print("\nFinal Order Status 2:")
    print(final_order_status_2)
