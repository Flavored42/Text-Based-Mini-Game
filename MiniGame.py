


import random
import os

class Game:
    
    def __init__(self):
        self.turns = 0
        self.pots_picked = 0
        self.pots_used = 0
        self.enemies = 0
        self.doors_seen = 0
        self.doors_opened = 0 
        self.keys = 0
        self.lvl = 1
    
    @property
    def damage(self):
        return self.lvl * 1.5

    # Clear Screen
    def clear(self):
        os.system('cls')

    # On Open
    def openme(self):
        self.welcome()
        self.get_name()
        self.start()

    # Welcome Message
    def welcome(self):
        self.clear()
        print('Welcome to my Mini Game!')
        User.enter()

    # Get User Name
    def get_name(self):
        self.clear()
        print('What should we name you?')
        ask = input('\n')
        User.name = ask 
        print(f'Greetings, {ask}! Try not to get lost...')
        User.enter()

    # Start
    def start(self):
        while User.HP > 0:
            self.clear()
            print(User.name)
            print(f'\nHP ~ {User.HP}')
            print(f'Potions ~ {User.pots}')
            if User.location != None:
                print(f'Location ~ {User.location}')
            print(f'Maze Level ~ {Game.lvl}\n')
            if Enemy.alive == True:
                print(f'\n{Enemy.name} HP ~ {Enemy.HP}\n')
            User.actions()
        else:
            self.clear()
            print('You have died, {User.name}...\n')
            if User.pots > 10:
                print('Would you like to spend 10 potions to revive? (y/n)')
                ask = User.yorn()
                if ask in ['y','Y']:
                    User.pots -= 9
                    self.pots_used += 9
                    User.use_pot()
                else:
                    self.ending()
            else:
                self.ending()
    
    # Ending
    def ending(self):
        print(f'Turns Taken ~ {self.turns}')
        print(f'Doors Seen ~ {self.doors_seen}')
        print(f'Doors Opened ~ {self.doors_opened}')
        print(f'Enemies Slain ~ {self.enemies}')
        print(f'Potions Picked Up ~ {self.pots_picked}')
        print(f'Potions Used ~ {self.pots_used}')
        print(f'Keys Picked Up ~ {self.keys}')
        User.enter()

Game = Game()

class User:

    def __init__(self):
        self.name = None
        self.HP = 10
        self.pots = 3
        self.rubbish = 0
        self.keys = 0
        self.loot = []
        self.location = None
        self.lvl = 1

    # Enter Prompt
    def enter(self):
        input('Press Enter To Continue...')

    # Y or N
    def yorn(self):
        ask = input('\n> ')
        while ask not in ['y','n','Y','N']:
            print('Please choose Y or N!')
            ask = input('\n> ')
        return ask

    # Actions
    def actions(self):
        print('[1] ~ Move')
        print('[2] ~ Attack')
        print('[3] ~ Open Loot')
        print('[4] ~ Use Potion')
        print('[5] ~ My Stats')
        ask = input('\n> ')
        while ask not in ['1','2','3','4','5']:
            print('Please choose 1 through 5!')
            ask = input('\n> ')
        if ask in ['1','2','3','4']:
            # Move
            if ask == '1':
                if Enemy.alive == True:
                    print('You cannot move when there is an enemy!')
                    Enemy.attack()
                else:
                    self.move()
            # Attack
            elif ask == '2':
                if Enemy.alive == True:
                    self.attack()
                else:
                    print('You swing away, yet hit nothing!')
                    self.enter()
            # Open Loot
            elif ask == '3':
                self.open_loot()
            # Use Potion
            elif ask == '4':
                self.use_pot()
            Game.turns += 1
        else:
            self.my_stats()

    # Move
    def move(self):
        mover = False
        if self.location == 'Enemy Den':
            roll = random.randint(1,101)
            if roll - self.lvl in range(1,80):
                Enemy.encounter()
            else:
                mover = True
        else:
            mover = True
        if mover == True:
            Game.clear()
            roll = random.randint(1,10)
            print(roll)
            if roll in range(1,5):
                self.location = 'Enemy Den'
                print('You have stumbled into an Enemy Den!')
            elif roll in range(5,7):
                self.location = 'Loot Room'
                print('You have found a Loot Room!')
                self.enter()
                self.find_loot()
            elif roll in range(7,9):
                self.location = 'Merchant'
                print('You have found a Merchant!')
            elif roll in range(9,10):
                self.location = 'Door'
                Game.doors_seen += 1
                print('You are in front of a door!')
            self.enter()
            mover = False

    # Attack
    def attack(self):
        amount = random.randint(1,self.lvl) + 1 
        Enemy.HP -= amount
        print(f'You attacked {Enemy.name} for {amount} damage!')
        if Enemy.HP <= 0:
            print(f'You have slain {Enemy.name}!')
            Enemy.alive = False 
            self.lvl += 1
            Game.enemies += 1
            self.enter()
        else:
            Enemy.attack()

    # Open Loot
    def open_loot(self):
        print(f'Potions ~ {self.pots}')
        if self.keys > 0:
            print(f'Keys ~ {self.keys}')
        if self.rubbish > 0:
            print(f'Rubbish ~ {self.rubbish}')
        if self.keys > 0 and self.location == 'Door':
            print('Would you like to unlock the door? (y/n)')
            ask = self.yorn()
            if ask in ['y','Y']:
                self.keys -= 1
                Game.doors_opened += 1
                Game.lvl += 1 
        if self.rubbish > 0 and self.location == 'Merchant':
            print('Would you like to sell your Rubbish? (y/n)')
            ask = self.yorn()
            if ask in ['y','Y']:
                print(f'How much Rubbish would you like to sell? ({self.rubbish} available)')
                ask = int(input)
                while ask > self.rubbish or ask <= 0:
                    print('Hmm...')
                    ask = int(input)
                else:
                    self.rubbish -= ask 
                    self.pots += ask 
                    Game.pots_picked += ask
                    print(f'You have gained {ask} potions by selling your rubbish!')
                    self.enter()
        else:
            self.enter()

    # Use Potion
    def use_pot(self):
        self.pots -= 1
        Game.pots_used += 1
        self.HP = 10 + self.lvl
        print(f'You have used a potion! Potions remaining: {self.pots}')
        self.enter()

    # Found Loot
    def find_loot(self):
        item = None
        roll = random.randint(1,101)
        if roll in range(1,51):
            print('You find nothing!')
        elif roll in range(51,61):
            item = 'Key'
        elif roll in range(61,86):
            item = 'Rubbish'
        elif roll in range(86,101):
            item = 'Potion'
        if item != None:
            print(f'You have found {item}!')
            print(f'Would you like to pick up {item}? (y/n)')
            ask = self.yorn()
            if ask in ['y','Y']:
                if item == 'Potion':
                    self.pots += 1
                    Game.pots_picked += 1
                elif item == 'Rubbish':
                    self.rubbish += 1
                elif item == 'Key':
                    self.keys += 1
                    Game.keys += 1
                print(f'You have picked up {item}!')
            else:
                print(f'You have left {item} behind...')
        item = None

    # My Stats
    def my_stats(self):
        print(f'Level ~ {self.lvl}')
        print(f'Potions Picked Up ~ {Game.pots_picked}')
        print(f'Potions Used ~ {Game.pots_used}')
        if Game.keys > 0:
            print(f'Keys Picked Up ~ {Game.keys}')
        if Game.doors_seen > 0:
            print(f'Doors Seen ~ {Game.doors_seen}')
        if Game.doors_opened > 0:
            print(f'Doors Opened ~ {Game.doors_opened}')
        self.enter()

User = User()

class Enemy:

    def __init__(self):
        self.alive = False
        self.names = ['Orc','Lizard','Goblin','Skeleton']
        self.lvl = 1

    @property
    def damage(self):
        floats = [1,1.2,1.4,1.6,1.8,2]
        return self.lvl * random.choice(floats)

    def encounter(self):
        self.alive = True
        self.name = random.choice(self.names)
        self.HP = random.randint(self.lvl,round(User.HP) + 1)
        print(f'You have encountered a {self.name}!')
        User.enter()

    def attack(self):
        print(f'{self.name} attacked for {self.damage}!')
        User.HP -= self.damage 
        if User.HP <= 0:
            User.dead()
        else:
            User.enter()
    
Enemy = Enemy()

Game.openme()
