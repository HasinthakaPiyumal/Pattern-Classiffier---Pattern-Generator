class NewsPublisher:
    def __init__(self):
        self._latest_news = None
        self._subscribers = []

    def attach(self, subscriber):
        self._subscribers.append(subscriber)

    def detach(self, subscriber):
        self._subscribers.remove(subscriber)

    def _notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._latest_news)

    def publish_news(self, news_item):
        self._latest_news = news_item
        self._notify()

class NewsReader:
    def __init__(self, name):
        self._name = name

    def update(self, news_item):
        print(f"{self._name} received news: '{news_item}'")

if __name__ == "__main__":
    publisher = NewsPublisher()

    reader1 = NewsReader("Alice")
    reader2 = NewsReader("Bob")
    reader3 = NewsReader("Charlie")

    publisher.attach(reader1)
    publisher.attach(reader2)

    publisher.publish_news("Market hits new high!")

    publisher.attach(reader3)
    publisher.detach(reader1)

    publisher.publish_news("New government policy announced.")