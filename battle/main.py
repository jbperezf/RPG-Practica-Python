from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create magic:
# black magic:
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")
# white magic:
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]


# Create items:
# potion items:
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "500 HP", 100)
# elixir items:
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party", 9999)
mega_elixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)
# attack items:
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate people:
player = Person(460, 65, 60, 34, player_spells, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===============================")
    player.choose_action()
    choice = input("\nChoose action: ")
    index = int(choice) - 1

# Attack
    if index == 0:
        dmg = player.generate_dmg()
        enemy.take_dmg(dmg)
        print("You attacked for {} dmg points.".format(dmg))

# Magic
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("\nChoose magic: ")) - 1

        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_dmg()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nYou don't have enough MP.\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n{} heals for {} HP.".format(spell.name, magic_dmg) + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_dmg(magic_dmg)
            print(bcolors.OKBLUE + "\n{} deals {} points of damage.".format(spell.name, magic_dmg) + bcolors.ENDC)

# Items
    elif index == 2:
        player.choose_item()
        item_choice = int(input("\nChoose item: ")) - 1

        if item_choice == -1:
            continue

        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\nYou ran out of this item.\n" + bcolors.ENDC)
            continue

        player.items[item_choice]["quantity"] -= 1

        item = player.items[item_choice]["item"]
        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKBLUE + "\n{} heals for {} HP.".format(item.name, item.prop) + bcolors.ENDC)
        elif item.type == "elixir":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKBLUE + "\n{} restores HP/MP.".format(item.name) + bcolors.ENDC)
        elif item.type == "attack":
            enemy.take_dmg(item.prop)
            print(bcolors.FAIL + "\n{} deals {} damage!".format(item.name, item.prop) + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_dmg()
    player.take_dmg(enemy_dmg)
    print("Enemy attacks for {} points of dmg.".format(enemy_dmg))

    print("--------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")
    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp())+ "/" + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You have been defeated." + bcolors.ENDC)
        running = False
