class Notifier:
    def send(self, message):
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, message):
        return f"Sending email: {message}"

class SMSNotifier(Notifier):
    def send(self, message):
        return f"Sending SMS: {message}"

class PushNotifier(Notifier):
    def send(self, message):
        return f"Sending push notification: {message}"

class NotificationFactory:
    @staticmethod
    def get_notifier(notifier_type):
        if notifier_type == "email":
            return EmailNotifier()
        elif notifier_type == "sms":
            return SMSNotifier()
        elif notifier_type == "push":
            return PushNotifier()
        else:
            raise ValueError("Invalid notifier type")

if __name__ == "__main__":
    email_notifier = NotificationFactory.get_notifier("email")
    print(email_notifier.send("Hello via email!"))
    sms_notifier = NotificationFactory.get_notifier("sms")
    print(sms_notifier.send("Hello via SMS!"))
    push_notifier = NotificationFactory.get_notifier("push")
    print(push_notifier.send("Hello via push!"))
    try:
        slack_notifier = NotificationFactory.get_notifier("slack")
        print(slack_notifier.send("Hello via Slack!"))
    except ValueError as e:
        print(e)