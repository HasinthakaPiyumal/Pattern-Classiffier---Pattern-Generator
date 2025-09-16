class ChatRoom:
    def __init__(self, name):
        self.name = name
        self._users = set()
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def join_room(self, username):
        if username not in self._users:
            self._users.add(username)
            print(f"\n{username} has joined {self.name}.")
            self.notify(username, "joined")
        else:
            print(f"{username} is already in {self.name}.")

    def leave_room(self, username):
        if username in self._users:
            self._users.remove(username)
            print(f"\n{username} has left {self.name}.")
            self.notify(username, "left")
        else:
            print(f"{username} is not in {self.name}.")

    def notify(self, username, action):
        for observer in self._observers:
            observer.on_user_event(self.name, username, action)

class ChatUser:
    def __init__(self, username):
        self.username = username

    def on_user_event(self, room_name, affected_user, action):
        if self.username != affected_user:
            print(f"[{self.username} in {room_name}]: {affected_user} has {action}.")

if __name__ == '__main__':
    general_chat = ChatRoom("General Chat")

    user_alice = ChatUser("Alice")
    user_bob = ChatUser("Bob")
    user_charlie = ChatUser("Charlie")

    general_chat.attach(user_alice)
    general_chat.attach(user_bob)
    general_chat.attach(user_charlie)

    general_chat.join_room("Alice")
    general_chat.join_room("Bob")
    general_chat.join_room("Charlie")
    general_chat.leave_room("Bob")
    general_chat.join_room("David")
    general_chat.detach(user_alice)
    general_chat.leave_room("Charlie")