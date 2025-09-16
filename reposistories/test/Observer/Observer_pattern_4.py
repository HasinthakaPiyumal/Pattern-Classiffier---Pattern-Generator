class Button:
    def __init__(self, label):
        self._label = label
        self._click_handlers = []

    def attach(self, handler):
        self._click_handlers.append(handler)

    def detach(self, handler):
        self._click_handlers.remove(handler)

    def _notify(self):
        for handler in self._click_handlers:
            handler.update(self._label)

    def click(self):
        print(f"Button '{self._label}' was clicked.")
        self._notify()

class ClickHandler:
    def __init__(self, name):
        self._name = name

    def update(self, button_label):
        print(f"Handler '{self._name}' processed click from button '{button_label}'.")

class LoggerHandler:
    def __init__(self):
        pass

    def update(self, button_label):
        print(f"LOGGER: Button '{button_label}' click event logged.")

if __name__ == "__main__":
    submit_button = Button("Submit")
    cancel_button = Button("Cancel")

    handler_form_submit = ClickHandler("FormSubmit")
    handler_analytics = ClickHandler("AnalyticsTracker")
    logger = LoggerHandler()

    submit_button.attach(handler_form_submit)
    submit_button.attach(handler_analytics)
    submit_button.attach(logger)

    cancel_button.attach(logger)

    submit_button.click()
    print("-" * 20)
    cancel_button.click()

    submit_button.detach(handler_analytics)
    print("-" * 20)
    submit_button.click()