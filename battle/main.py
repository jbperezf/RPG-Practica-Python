from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create magic:
# - black magic:
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 30, 1000, "black")
# - white magic:
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 3000, "white")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cura, curaga]

# Create items:
# - potion items:
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "500 HP", 100)
# - elixir items:
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party", 9999)
mega_elixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)
# - attack items:
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]


# Instantiate people:
player1 = Person("Valos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Jose ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp  ", 3260, 130, 560, 25, enemy_spells, [])
enemy2 = Person("Magus", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 3089, 130, 560, 25, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


# Loop Break:
running = True
i = 0

# Game starts:
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===============================")
    # Get player stats
    print("\n")
    print("NAME:     HP:                                       MP:         ")
    for player in players:
        player.get_players_stats()

    for enemy in enemies:
        if enemy.get_hp() != 0:
            enemy.get_enemy_stats()
    print("\n")

# Players turn
    for player in players:
        # Actions menu:
        player.choose_action()
        choice = input("\nChoose action: ")
        index = int(choice) - 1

        # Attack
        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)

            print("\n{} attacked {} for {} dmg points.\n".format(player.name, enemies[enemy].name.replace(" ", ""),
                                                                 dmg))

            if enemies[enemy].get_hp() == 0:
                print("{} has been killed".format(enemies[enemy].name.replace(" ", "")))
                del enemies[enemy]

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
                print(bcolors.FAIL + "\n{}, you don't have enough MP.\n".format(player.name) + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n{} heals {} for {} HP.\n".format(spell.name, player.name, magic_dmg)
                      + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n{} deals {} {} points of damage.\n".format(spell.name, enemies[enemy].name,
                                                                                     magic_dmg) + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print("{} has been killed".format(enemies[enemy].name))
                    del enemies[enemy]

        # Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("\nChoose item: ")) - 1

            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n{} ran out of this item.\n".format(player.name) + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1
            item = player.items[item_choice]["item"]

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKBLUE + "\n{} heals {} for {} HP.\n".format(item.name, player.name, item.prop)
                      + bcolors.ENDC)

            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                        print(bcolors.OKBLUE + "\n{} restores {} HP/MP.\n".format(item.name, i.name) + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKBLUE + "\n{} restores {} HP/MP.\n".format(item.name, player.name) + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.OKBLUE + "\n{} deals {} {} points of damage!\n".format(item.name, enemies[enemy].name,
                                                                                     item.prop) + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print("{} has been killed".format(enemies[enemy].name))
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won:
    if defeated_enemies == len(enemies):
        print("----------------------------------------------------------\n")
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)

        for player in players:
            player.get_players_stats()

        for enemy in enemies:
            enemy.get_enemy_stats()

        running = False

    # Check if enemy won:
    elif defeated_players == len(players):
        print("----------------------------------------------------------\n")
        print(bcolors.FAIL + "\nYou have been defeated." + bcolors.ENDC)

        for player in players:
            player.get_players_stats()

        for enemy in enemies:
            enemy.get_enemy_stats()

        running = False

# Enemy's turn:
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

    # Attack:
        if enemy_choice == 0:
            target = random.randrange(0, 3)

            enemy_dmg = enemy.generate_dmg()
            players[target].take_dmg(enemy_dmg)

            print("\n{} attacks {} for {} points of dmg.\n".format(enemy.name, players[target].name, enemy_dmg))
            print("\n")

    # Magic:
        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            spell = enemy.magic[magic_choice]

            if spell.cost > enemy.mp:
                continue

            enemy.reduce_mp(spell.cost)
            magic_dmg = spell.generate_dmg()

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n{} heals {} for {} HP.\n".format(spell.name, enemy.name, magic_dmg)
                      + bcolors.ENDC)

            elif spell.type == "black":
                player = random.randrange(0, len(players))
                players[player].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n{} deals {} {} points of damage.\n".format(spell.name, players[player].name,
                                                                                     magic_dmg) + bcolors.ENDC)

                if players[player].get_hp() == 0:
                    print("{} has been killed".format(players[player].name))
                    del players[player]



print(bcolors.OKBLUE + "esto es azul" + bcolors.ENDC)