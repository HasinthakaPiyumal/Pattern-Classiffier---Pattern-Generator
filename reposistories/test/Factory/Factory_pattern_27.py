class Notification:
    def send(self, recipient: str, message: str) -> str:
        pass

class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        return f"Sending Email to {recipient}: '{message[:50]}...'"

class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        return f"Sending SMS to {recipient}: '{message[:50]}...'"

class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        return f"Sending Push Notification to {recipient}: '{message[:50]}...'"

class NotificationFactory:
    def create_notification(self, channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "push":
            return PushNotification()
        else:
            raise ValueError(f"Unsupported notification channel: {channel}")

factory = NotificationFactory()

email_notif = factory.create_notification("email")
sms_notif = factory.create_notification("sms")
push_notif = factory.create_notification("push")

msg = "Your order #12345 has been shipped and will arrive within 2 business days."

print(email_notif.send("user@example.com", msg))
print(sms_notif.send("+15551234567", msg))
print(push_notif.send("device_id_abc", msg))

try:
    webhook_notif = factory.create_notification("webhook")
except ValueError as e:
    print(e)