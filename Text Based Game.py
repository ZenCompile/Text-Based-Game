import random

DUNGEONS = ["Layer1", "Layer2", "Layer3", "Layer4", "Layer5","Layer6","Layer7","Layer8",
            "Layer9", "Layer10", "Layer11", "Layer12", "Layer13", "Layer14","Layer15", "END"]
dungeonCounter = -1

ITEM_DROPS = ["Health_Potion", "Sword", "Mace"]

class Player:

    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.health = 10
        self.attack = 1  # base attack value

    def show_health(self):
        print(self.health)

    def increase_health(self, health):
        self.health += health

    def take_damage(self, amount):
        self.health -= amount
        return amount

    def add_item(self, item):
        if len(self.inventory) <= 3:
            self.inventory.append(item)
            print(f"{item} Has been added to your inventory.")
        else:
            print("You have too many items!")

    def check_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")


class Monster:

    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, amount):
        self.health -= amount
        return amount


def DungeonChanger():
    global dungeonCounter
    dungeonCounter += 1
    if dungeonCounter >= len(DUNGEONS):
        print("No more dungeons!")
        return None
    current_dungeon = DUNGEONS[dungeonCounter]
    if current_dungeon == "END":
        print("You Won!")
    return current_dungeon


def explore(player):
    event = random.choices(["enemy", "treasure", "nothing"],
                           weights=[5, 3, 1],
                           k=1
                           )[0]
    if event == "enemy":
        monsters = [
            {"name": "Goblin", "health": 5, "attack": 1},
            {"name": "Orc", "health": 10, "attack": 2},
            {"name": "Slime", "health": 3, "attack": 1}
        ]
        monster_info = random.choice(monsters)
        monster = Monster(monster_info["name"], monster_info["health"], monster_info["attack"])
        actionPicker(player, monster)
    elif event == "treasure":
        item = random.choice(ITEM_DROPS)
        player.add_item(item)
    else:
        print("You wander but find nothing...")


def actionPicker(player, monster):
    print(f"You have encountered a {monster.name}!\n")
    print("1. Fight\n2. Run\n3. Inventory")

    while True:
        try:
            action = int(input("Pick an option: "))
        except ValueError:
            print("Enter a valid number.")
            continue

        if action == 1:  # Fight
            # Player attack
            player_attack_roll = random.choices(["hit", "dodge"], weights=[2, 1])[0]
            # Monster attack
            monster_attack_roll = random.choices(["hit", "dodge"], weights=[monster.attack, 3])[0]

            if player_attack_roll == "hit":
                monster.take_damage(player.attack)
                print(f"You hit {monster.name} for {player.attack} damage! ({monster.health} HP left)")
            else:
                print(f"You missed! {monster.name} dodged your attack.")

            if monster.health <= 0:
                print(f"{monster.name} has been killed!")
                break

            # Monster's turn
            if monster_attack_roll == "hit":
                player.take_damage(monster.attack)
                print(f"{monster.name} hits you for {monster.attack} damage! ({player.health} HP left)")
            else:
                print(f"{monster.name} missed! You dodged the attack.")

            if player.health <= 0:
                print("You have died!")
                break

        elif action == 2:  # Run
            escape_roll = random.choices(["escape", "fail"], weights=[1, 4])[0]
            if escape_roll == "escape":
                print("You escaped successfully!")
                break
            else:
                print("Failed to escape! The monster attacks!")
                if random.choices(["hit", "dodge"], weights=[monster.attack, 3])[0] == "hit":
                    player.take_damage(monster.attack)
                    print(f"{monster.name} hits you for {monster.attack} damage! ({player.health} HP left)")
                else:
                    print(f"{monster.name} missed! You dodged the attack.")

        elif action == 3:  # Inventory
            player.check_inventory()
            if not player.inventory:
                continue

            print("Which item would you like to use?")
            for idx, item in enumerate(player.inventory, start=1):
                print(f"{idx}. {item}")

            while True:
                try:
                    choice = int(input("Pick item number: "))
                    if 1 <= choice <= len(player.inventory):
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Enter a valid number.")

            item_choice = player.inventory[choice - 1]
            ITEM_EFFECTS = {
                "Health_Potion": lambda player: player.increase_health(5),
                "Sword": lambda player: setattr(player, "attack", player.attack + 2),
                "Mace": lambda player: setattr(player, "attack", player.attack + 3)
            }

            effect = ITEM_EFFECTS.get(item_choice)
            if effect:
                effect(player)
                print(f"You used {item_choice}!")
                if item_choice == "Health_Potion":
                    player.inventory.pop(choice - 1)

        else:
            print("Invalid option. Choose 1, 2, or 3.")


StartGame = True
while StartGame:
    player_choice = input("Would you like to play? (y/n): ").lower()
    if player_choice in ("yes", "y"):
        # Player Created
        name_your_character = input("What is your name: ")
        main_character = Player(name_your_character)

        while True:
            current_dungeon = DungeonChanger()
            if current_dungeon is None:
                break
            print(f"\nYou enter {current_dungeon}...\n")
            explore(main_character)

            if main_character.health <= 0:
                print("Game over!")
                break
        
        print("Thanks for playing!")
        break

    elif player_choice in ("no", "n"):
        print("Maybe next time!")
        break
    else:
        print("Enter yes/y or no/n")
