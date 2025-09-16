import datetime

class ChatRoom:
    def __init__(self, topic):
        self._topic = topic
        self._messages = []
        self._participants = []

    def attach(self, participant):
        self._participants.append(participant)
        print(f"{participant._name} joined chat room '{self._topic}'.")

    def detach(self, participant):
        self._participants.remove(participant)
        print(f"{participant._name} left chat room '{self._topic}'.")

    def _notify(self, sender_name, message_content):
        for participant in self._participants:
            if participant._name != sender_name:
                participant.update(self._topic, sender_name, message_content)

    def send_message(self, sender, message_content):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {sender._name}: {message_content}"
        self._messages.append(full_message)
        print(f"ChatRoom '{self._topic}' received: {full_message}")
        self._notify(sender._name, message_content)

class User:
    def __init__(self, name):
        self._name = name

    def update(self, room_topic, sender_name, message_content):
        print(f"{self._name} in '{room_topic}' received from {sender_name}: '{message_content}'")

if __name__ == "__main__":
    tech_chat = ChatRoom("Python Devs")

    user_alice = User("Alice")
    user_bob = User("Bob")
    user_charlie = User("Charlie")

    tech_chat.attach(user_alice)
    tech_chat.attach(user_bob)

    tech_chat.send_message(user_alice, "Hello everyone!")
    tech_chat.send_message(user_bob, "Hi Alice, how's it going?")

    tech_chat.attach(user_charlie)
    tech_chat.send_message(user_alice, "Welcome Charlie!")

    tech_chat.detach(user_bob)
    tech_chat.send_message(user_charlie, "Bob left, I guess?")