class NotificationStrategy:
    def send(self, recipient, message):
        raise NotImplementedError
class EmailNotification(NotificationStrategy):
    def send(self, recipient, message):
        print(f"Sending email to {recipient}: '{message}'")
class SMSNotification(NotificationStrategy):
    def send(self, recipient, message):
        print(f"Sending SMS to {recipient}: '{message}'")
class PushNotification(NotificationStrategy):
    def send(self, recipient, message):
        print(f"Sending push notification to {recipient}: '{message}'")
class Notifier:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def notify(self, recipient, message):
        self._strategy.send(recipient, message)
notifier = Notifier(EmailNotification())
notifier.notify("user@example.com", "Your order has shipped.")
notifier.set_strategy(SMSNotification())
notifier.notify("+1234567890", "Your password has been reset.")
notifier.set_strategy(PushNotification())
notifier.notify("device_id_123", "New message received!")