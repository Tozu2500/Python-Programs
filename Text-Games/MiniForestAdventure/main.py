import random

class Player:
    def __init__(self):
        self.health = 100
        self.inventory = []
        self.current_room = "forest"
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

player_name = input("Enter your player name: ")

def display_status(player):
    print(f"\n--- {player_name} Status ---\n")
    print(f"Health: {player.health}/100")
    print(f"Inventory: {', '.join(player.inventory) if player.inventory else 'Empty'}")
    print(f"Location: {player.current_room.title()}")

def forest_room(player):
    print("\n 🌲 You're in a dark forest and you see a glowing mushroom and a sword, a rusty sword.")
    print("What do you want to do?")
    print("1. Take the mushroom")
    print("2. Take the sword")
    print("3. Go to the cave down further")
    print("4. Go to a village near by")

    choice = input("Enter your choice (1-4): ")

    if choice == "1" and "mushroom" not in player.inventory:
        player.inventory.append("mushroom")
        print("You picked up the glowing mushroom. It might be a useful healing tool!")
    elif choice == "2" and "sword" not in player.inventory:
        player.inventory.append("sword")
        print("You picked up the rusty rusty sword! Now you can defend yourself.")
    elif choice == "3":
        player.current_room = "cave"
    elif choice == "4":
        player.current_room = "village"
    else:
        print("Invalid choice or item already taken!")

def cave_room(player):
    print("\n 🦇 You enter a scary looking cave and a wild bat comes and attacks you!")

    if "sword" in player.inventory:
        print("You fight the bat with your sword and defeated it!")
        print("You found a treasure chest with a health potion inside of it!")
        if "health_potion" not in player.inventory:
            player.inventory.append("health_potion")
    else:
        print("Without a weapon, the bat scratches you!")
        player.take_damage(20)
        print(f"You lost 20 health! Current health is: {player.health}")

    print("\n 1. Go back to the forest")
    print("2. Go even deeper into the cave")

    choice = input("Enter your choice (1-2): ")

    if choice == "1":
        player.current_room = "forest"
    else:
        print("You go deeper and find an exit from the cave to the village you saw earlier!")
        player.current_room = "village"

def village_room(player):
    print("\n 🏘️ You arrive at a peaceful looking village. There's a smart and wise and looking healer present.")
    print("What do you want to do?")
    print("1. Talk to the healer")
    print("2. Use a glowing mushroom (if you have one)")
    print("3. Use a health potion (if you have one)")
    print("4. Go back to the forest")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        print("Healer: 'Welcome long traveler! I can see you got some damage done to you man.'")
        if player.health < 100:
            print("The healer notices your wounds and heals you!")
            player.heal(100)
    elif choice == "2":
        print("You eat the glowing mushroom and you start to feel a lot better!")
        player.heal(30)
        player.inventory.remove("mushroom")
    elif choice == "3" and "health_potion" in player.inventory:
        print("You drink the health potion and recover fully!")
        player.heal(50)
        player.inventory.remove("health_potion")
    elif choice == "4":
        player.current_room = "forest"
    else:
        print("Invalid choice or you don't have that item!")

def main():
    print("🌲 Welcome to the forest adventure game 🌲")
    print("Explore different areas and places, collect items and survive!")
    print("Type 'quit' at any time to exit.")

    player = Player()

    while True:
        display_status(player)

        if player.health <= 0:
            print("\n 💀 Game Over! You died!")
            print("Thanks for playing!")
            break

        if player.current_room == "forest":
            forest_room(player)
        elif player.current_room == "cave":
            cave_room(player)
        elif player.current_room == "village":
            village_room(player)

        quit_check = input("\nPress Enter to continue or type 'quit' to exit: ")
        if quit_check.lower() == 'quit':
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()
