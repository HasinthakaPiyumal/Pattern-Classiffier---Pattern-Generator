import abc
import datetime
import time

class PublishingStrategy(abc.ABC):
    @abc.abstractmethod
    def publish(self, article_title, content, author):
        pass

class InstantPublishStrategy(PublishingStrategy):
    def publish(self, article_title, content, author):
        publish_time = datetime.datetime.now()
        print(f"--- INSTANT PUBLISH ---")
        print(f"Article '{article_title}' by {author} published immediately at {publish_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Content preview: {content[:50]}...")
        return True

class ScheduledPublishStrategy(PublishingStrategy):
    def __init__(self, publish_datetime: datetime.datetime):
        self._publish_datetime = publish_datetime

    def publish(self, article_title, content, author):
        now = datetime.datetime.now()
        if now < self._publish_datetime:
            print(f"--- SCHEDULED PUBLISH ---")
            print(f"Article '{article_title}' by {author} scheduled for {self._publish_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}. Waiting...")
            return False
        else:
            print(f"--- SCHEDULED PUBLISH ---")
            print(f"Article '{article_title}' by {author} published as scheduled at {self._publish_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Content preview: {content[:50]}...")
            return True

class DraftPublishStrategy(PublishingStrategy):
    def publish(self, article_title, content, author):
        print(f"--- DRAFT PUBLISH ---")
        print(f"Article '{article_title}' by {author} saved as DRAFT.")
        print(f"Content preview: {content[:50]}...")
        return False

class ArticlePublisher:
    def __init__(self, default_strategy: PublishingStrategy):
        self._publishing_strategy = default_strategy
        self._articles = []

    def set_publishing_strategy(self, strategy: PublishingStrategy):
        self._publishing_strategy = strategy

    def create_and_publish_article(self, title, content, author):
        print(f"\nAttempting to publish article: '{title}'")
        if self._publishing_strategy.publish(title, content, author):
            self._articles.append({"title": title, "author": author, "status": "Published"})
            print(f"Article '{title}' successfully processed and recorded as published.")
        else:
            self._articles.append({"title": title, "author": author, "status": "Draft/Scheduled"})
            print(f"Article '{title}' processed as draft or scheduled.")

    def list_articles(self):
        print("\n--- Current Articles ---")
        if not self._articles:
            print("No articles.")
            return
        for article in self._articles:
            print(f"Title: {article['title']}, Author: {article['author']}, Status: {article['status']}")

if __name__ == "__main__":
    publisher = ArticlePublisher(DraftPublishStrategy())

    publisher.create_and_publish_article("My First Draft", "This is the content of my first draft article...", "John Doe")
    publisher.list_articles()

    publisher.set_publishing_strategy(InstantPublishStrategy())
    publisher.create_and_publish_article("Breaking News", "Important event just happened...", "Jane Smith")
    publisher.list_articles()

    future_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    publisher.set_publishing_strategy(ScheduledPublishStrategy(future_time))
    publisher.create_and_publish_article("Upcoming Event", "Details about an event next month...", "Alice Brown")
    publisher.list_articles()

    print("\nSimulating passage of time...")
    time.sleep(6)
    print("\nRe-checking scheduled article status:")
    publisher.set_publishing_strategy(ScheduledPublishStrategy(future_time))
    publisher.create_and_publish_article("Upcoming Event (recheck)", "Details about an event next month...", "Alice Brown")
    publisher.list_articles()