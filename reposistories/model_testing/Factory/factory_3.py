from abc import ABC, abstractmethod

class UIComponent(ABC):
    @abstractmethod
    def render(self):
        pass

class Button(UIComponent):
    def render(self):
        return "Rendering a Button"

class TextField(UIComponent):
    def render(self):
        return "Rendering a Text Field"

class Checkbox(UIComponent):
    def render(self):
        return "Rendering a Checkbox"

class UIComponentFactory:
    def get_component(self, component_type: str) -> UIComponent:
        if component_type.lower() == "button":
            return Button()
        elif component_type.lower() == "textfield":
            return TextField()
        elif component_type.lower() == "checkbox":
            return Checkbox()
        else:
            raise ValueError(f"Unknown component type: {component_type}")

if __name__ == "__main__":
    factory = UIComponentFactory()
    components = ["button", "textfield", "checkbox"]
    for c in components:
        comp = factory.get_component(c)
        print(comp.render())
