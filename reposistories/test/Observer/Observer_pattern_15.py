class Button:
    def __init__(self, label="Button"):
        self.label = label
        self._click_listeners = []

    def add_listener(self, listener):
        self._click_listeners.append(listener)

    def remove_listener(self, listener):
        self._click_listeners.remove(listener)

    def click(self):
        print(f"\nButton '{self.label}' was clicked!")
        self._notify_listeners("click")

    def _notify_listeners(self, event_type):
        for listener in self._click_listeners:
            listener.on_event(self.label, event_type)

class ClickListener:
    def __init__(self, name):
        self.name = name

    def on_event(self, button_label, event_type):
        print(f"Listener {self.name}: Received '{event_type}' event from button '{button_label}'.")

if __name__ == '__main__':
    my_button = Button("Submit")
    reset_button = Button("Reset")

    listener1 = ClickListener("Logger")
    listener2 = ClickListener("Analytics")

    my_button.add_listener(listener1)
    my_button.add_listener(listener2)
    reset_button.add_listener(listener1)

    my_button.click()
    reset_button.click()

    my_button.remove_listener(listener2)
    my_button.click()