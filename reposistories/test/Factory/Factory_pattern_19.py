import abc

class MessageSender(abc.ABC):
    @abc.abstractmethod
    def send(self, recipient: str, message: str):
        pass

class EmailSender(MessageSender):
    def send(self, recipient: str, message: str):
        return f"Sending email to {recipient}: '{message}'"

class SMSSender(MessageSender):
    def send(self, recipient: str, message: str):
        return f"Sending SMS to {recipient}: '{message}'"

class MessageSenderFactory:
    @staticmethod
    def create_sender(sender_type: str) -> MessageSender:
        if sender_type == "email":
            return EmailSender()
        elif sender_type == "sms":
            return SMSSender()
        else:
            raise ValueError("Invalid sender type")

if __name__ == "__main__":
    email_sender = MessageSenderFactory.create_sender("email")
    print(email_sender.send("user@example.com", "Hello via email!"))
    sms_sender = MessageSenderFactory.create_sender("sms")
    print(sms_sender.send("+1234567890", "Hello via SMS!"))