class GameCharacter:
    def attack(self) -> str:
        pass
    def defend(self) -> str:
        pass

class Warrior(GameCharacter):
    def attack(self) -> str:
        return "Warrior swings a mighty sword!"
    def defend(self, ) -> str:
        return "Warrior raises a sturdy shield!"

class Mage(GameCharacter):
    def attack(self) -> str:
        return "Mage casts a powerful fire spell!"
    def defend(self, ) -> str:
        return "Mage conjures a magical barrier!"

class Archer(GameCharacter):
    def attack(self) -> str:
        return "Archer fires a precision arrow!"
    def defend(self, ) -> str:
        return "Archer dodges swiftly!"

class CharacterFactory:
    def create_character(self, character_type: str) -> GameCharacter:
        if character_type == "warrior":
            return Warrior()
        elif character_type == "mage":
            return Mage()
        elif character_type == "archer":
            return Archer()
        else:
            raise ValueError(f"Unknown character type: {character_type}")

factory = CharacterFactory()

warrior = factory.create_character("warrior")
mage = factory.create_character("mage")
archer = factory.create_character("archer")

print(warrior.attack())
print(warrior.defend())
print(mage.attack())
print(mage.defend())
print(archer.attack())
print(archer.defend())

try:
    rogue = factory.create_character("rogue")
except ValueError as e:
    print(e)