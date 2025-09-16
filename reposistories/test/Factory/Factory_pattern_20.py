import abc

class Character(abc.ABC):
    @abc.abstractmethod
    def attack(self):
        pass
    @abc.abstractmethod
    def defend(self):
        pass

class Warrior(Character):
    def attack(self):
        return "Warrior swings a mighty sword!"
    def defend(self):
        return "Warrior raises a shield!"

class Mage(Character):
    def attack(self):
        return "Mage casts a powerful fire spell!"
    def defend(self):
        return "Mage conjures a magical barrier!"

class CharacterFactory:
    @staticmethod
    def create_character(char_type: str) -> Character:
        if char_type == "warrior":
            return Warrior()
        elif char_type == "mage":
            return Mage()
        else:
            raise ValueError("Invalid character type")

if __name__ == "__main__":
    warrior = CharacterFactory.create_character("warrior")
    print(warrior.attack())
    print(warrior.defend())
    mage = CharacterFactory.create_character("mage")
    print(mage.attack())
    print(mage.defend())