_notification_service_instance = None

def get_notification_service(service_type="email"):
    global _notification_service_instance
    if _notification_service_instance is None:
        _notification_service_instance = _NotificationService(service_type)
    return _notification_service_instance

class _NotificationService:
    def __init__(self, service_type):
        self.service_type = service_type
        self.sent_notifications = []

    def send_notification(self, recipient, message, channel="email"):
        notification = {"recipient": recipient, "message": message, "channel": channel}
        self.sent_notifications.append(notification)
        return {"status": "sent", "notification_id": hash(f"{recipient}{message}{channel}")}

    def get_sent_count(self):
        return len(self.sent_notifications)

if __name__ == "__main__":
    ns1 = get_notification_service("SMS")
    ns2 = get_notification_service("Push")

    print(f"Are ns1 and ns2 the same instance? {ns1 is ns2}")
    print(f"NS1 service type: {ns1.service_type}")
    print(f"NS2 service type: {ns2.service_type}")

    ns1.send_notification("user@example.com", "Welcome!", "email")
    ns2.send_notification("+1234567890", "Your order has shipped!", "SMS")

    print(f"Total notifications sent: {ns1.get_sent_count()}")
    print(f"First notification: {ns2.sent_notifications[0]}")