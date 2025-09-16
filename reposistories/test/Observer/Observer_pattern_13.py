class NewsPublisher:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def publish_news(self, headline, content):
        print(f"\nNews Publisher: Publishing '{headline}'")
        for subscriber in self._subscribers:
            subscriber.receive_news(headline, content)

class EmailSubscriber:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def receive_news(self, headline, content):
        print(f"Email to {self.name} ({self.email}): Subject: {headline}\nBody: {content[:50]}...")

class SMSSubscriber:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def receive_news(self, headline, content):
        print(f"SMS to {self.name} ({self.phone_number}): {headline[:100]}...")

if __name__ == '__main__':
    publisher = NewsPublisher()
    email_sub = EmailSubscriber("Alice", "alice@example.com")
    sms_sub = SMSSubscriber("Bob", "123-456-7890")
    email_sub2 = EmailSubscriber("Charlie", "charlie@example.com")

    publisher.subscribe(email_sub)
    publisher.subscribe(sms_sub)
    publisher.subscribe(email_sub2)

    publisher.publish_news("Market soars!", "Stocks hit record highs today as investors react positively to new economic data...")
    publisher.unsubscribe(sms_sub)
    publisher.publish_news("Tech innovations!", "A new breakthrough in AI promises to revolutionize computing...")