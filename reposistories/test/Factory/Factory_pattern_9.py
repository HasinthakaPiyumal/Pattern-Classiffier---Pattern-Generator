class Weapon:
    def attack(self):
        raise NotImplementedError

class Sword(Weapon):
    def attack(self):
        return "Swinging a sharp Sword!"

class Bow(Weapon):
    def attack(self):
        return "Firing an arrow from a Bow!"

class Axe(Weapon):
    def attack(self):
        return "Chopping with a heavy Axe!"

class WeaponFactory:
    @staticmethod
    def get_weapon(weapon_type):
        if weapon_type == "sword":
            return Sword()
        elif weapon_type == "bow":
            return Bow()
        elif weapon_type == "axe":
            return Axe()
        else:
            raise ValueError("Invalid weapon type")

if __name__ == "__main__":
    sword = WeaponFactory.get_weapon("sword")
    print(sword.attack())
    bow = WeaponFactory.get_weapon("bow")
    print(bow.attack())
    axe = WeaponFactory.get_weapon("axe")
    print(axe.attack())
    try:
        staff = WeaponFactory.get_weapon("staff")
        print(staff.attack())
    except ValueError as e:
        print(e)