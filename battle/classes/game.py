import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_dmg(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print(" {}. {}".format(i, item))
            i += 1

    def choose_target(self, enemies):
        i = 1

        print(bcolors.OKBLUE + bcolors.BOLD + "\nTARGET" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print(" {}. {}".format(i, enemy.name))
                i += 1

        enemy_choice = int(input("\nChoose a target: ")) - 1
        return enemy_choice

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\nMAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print(" {}. {} (cost: {})".format(i, spell.name, spell.cost))
            i += 1
        print("\nEnter 0 to go back.")

    def choose_item(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\nITEMS" + bcolors.ENDC)
        for item in self.items:
            print(" {}. {}: {}. (x{})".format(i, item["item"].name, item["item"].description, item["quantity"]))
            i += 1
        print("\nEnter 0 to go back.")

    def get_enemy_stats(self):
        # Formatting
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 50
        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        spaces_needed_in_hp = 11 - len(hp_string)
        blank_space = " "

        while len(hp_string) < 11:
            hp_string = (blank_space * spaces_needed_in_hp) + hp_string
            spaces_needed_in_hp -= 1

        print("                     __________________________________________________ ")
        print(bcolors.BOLD + "{}:  {} ".format(self.name, hp_string) + bcolors.ENDC + "|"
              + bcolors.FAIL + hp_bar + bcolors.ENDC + "|")

    def get_players_stats(self):
        # Formatting the HP and MP bars
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 25
        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 10
        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        spaces_needed_in_hp = 9 - len(hp_string)
        mp_string = str(self.mp) + "/" + str(self.maxmp)
        spaces_needed_in_mp = 7 - len(mp_string)
        blank_space = " "

        while len(hp_string) < 9:
            hp_string = (blank_space * spaces_needed_in_hp) + hp_string
            spaces_needed_in_hp -= 1

        while len(mp_string) < 7:
            mp_string = (blank_space * spaces_needed_in_mp) + mp_string
            spaces_needed_in_mp -= 1

        print("                     _________________________               __________ ")
        print(bcolors.BOLD + "{}:    {}".format(self.name, hp_string) + bcolors.ENDC + " |"
              + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|" + bcolors.BOLD +
              "     {} ".format(mp_string) + bcolors.ENDC + "|" + bcolors.OKBLUE + mp_bar
              + bcolors.ENDC + "|")
