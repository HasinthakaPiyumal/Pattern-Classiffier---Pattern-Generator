class FormatStrategy:
    def format_text(self, text):
        raise NotImplementedError
class UppercaseFormat(FormatStrategy):
    def format_text(self, text):
        return text.upper()
class LowercaseFormat(FormatStrategy):
    def format_text(self, text):
        return text.lower()
class TitlecaseFormat(FormatStrategy):
    def format_text(self, text):
        return text.title()
class TextFormatter:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def apply_format(self, text):
        return self._strategy.format_text(text)
formatter = TextFormatter(UppercaseFormat())
print(f"Uppercase: {formatter.apply_format('hello world')}")
formatter.set_strategy(LowercaseFormat())
print(f"Lowercase: {formatter.apply_format('HELLO WORLD')}")
formatter.set_strategy(TitlecaseFormat())
print(f"Titlecase: {formatter.apply_format('hello world')}")