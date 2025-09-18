import abc
import random

class AttackStrategy(abc.ABC):
    @abc.abstractmethod
    def attack(self, attacker_name, target_name):
        pass

class MeleeAttack(AttackStrategy):
    def attack(self, attacker_name, target_name):
        damage = random.randint(10, 25)
        print(f"{attacker_name} performs a MELEE attack on {target_name}, dealing {damage} damage!")
        return damage

class RangedAttack(AttackStrategy):
    def attack(self, attacker_name, target_name):
        accuracy = random.uniform(0.6, 1.0)
        if accuracy > 0.8:
            damage = random.randint(15, 30)
            print(f"{attacker_name} launches a RANGED attack on {target_name}, hitting for {damage} damage!")
        else:
            damage = 0
            print(f"{attacker_name} launches a RANGED attack on {target_name}, but MISSES!")
        return damage

class MagicAttack(AttackStrategy):
    def attack(self, attacker_name, target_name):
        mana_cost = 15
        damage = random.randint(20, 40)
        print(f"{attacker_name} casts a MAGIC spell on {target_name}, consuming {mana_cost} mana and dealing {damage} magical damage!")
        return damage

class GameCharacter:
    def __init__(self, name, health, mana, attack_strategy: AttackStrategy):
        self._name = name
        self._health = health
        self._mana = mana
        self._attack_strategy = attack_strategy

    def set_attack_strategy(self, strategy: AttackStrategy):
        self._attack_strategy = strategy

    def take_damage(self, damage):
        self._health -= damage
        print(f"{self._name} takes {damage} damage. Health: {self._health}")
        if self._health <= 0:
            print(f"{self._name} has been defeated!")

    def perform_attack(self, target):
        print(f"\n{self._name} is attacking {target._name}...")
        damage = self._attack_strategy.attack(self._name, target._name)
        if damage > 0:
            target.take_damage(damage)

    def get_status(self):
        return f"{self._name} (Health: {self._health}, Mana: {self._mana})"

if __name__ == "__main__":
    hero = GameCharacter("Brave Knight", 100, 50, MeleeAttack())
    monster = GameCharacter("Goblin", 70, 0, MeleeAttack())
    wizard = GameCharacter("Wise Mage", 80, 100, MagicAttack())

    print(hero.get_status())
    print(monster.get_status())
    print(wizard.get_status())

    hero.perform_attack(monster)
    print(monster.get_status())

    wizard.perform_attack(monster)
    print(monster.get_status())

    print(f"\n{hero._name} equips a bow!")
    hero.set_attack_strategy(RangedAttack())
    hero.perform_attack(monster)
    print(monster.get_status())

    hero.perform_attack(monster)
    print(monster.get_status())

    hero.perform_attack(wizard)
    print(wizard.get_status())