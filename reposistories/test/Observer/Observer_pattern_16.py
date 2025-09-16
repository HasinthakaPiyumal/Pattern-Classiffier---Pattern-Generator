class GameCharacter:
    def __init__(self, name, initial_health):
        self.name = name
        self._health = initial_health
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def take_damage(self, amount):
        self._health = max(0, self._health - amount)
        print(f"\n{self.name} took {amount} damage. Health: {self._health}")
        self.notify()

    def heal(self, amount):
        self._health = min(100, self._health + amount)
        print(f"\n{self.name} healed {amount}. Health: {self._health}")
        self.notify()

    def get_health(self):
        return self._health

    def notify(self):
        for observer in self._observers:
            observer.update(self.name, self._health)

class HealthBarDisplay:
    def __init__(self, display_id):
        self.display_id = display_id

    def update(self, character_name, current_health):
        bar = "█" * (current_health // 10) + "-" * ((100 - current_health) // 10)
        print(f"Health Bar {self.display_id} for {character_name}: [{bar}] {current_health}%")

if __name__ == '__main__':
    hero = GameCharacter("Hero", 100)
    enemy = GameCharacter("Goblin", 50)

    hero_bar = HealthBarDisplay("Hero HUD")
    enemy_bar = HealthBarDisplay("Enemy Target")

    hero.attach(hero_bar)
    enemy.attach(enemy_bar)

    hero.take_damage(20)
    enemy.take_damage(10)
    hero.heal(15)
    hero.take_damage(90)
    enemy.detach(enemy_bar)
    enemy.take_damage(20)