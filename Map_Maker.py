#Riley Underwood

import os, random

global game_map, map_size_x, map_size_y

game_map_stats = {"block": "[ ]"}
map_draw_x = "[ ]" #Each row of the map.
game_map = 0

#Standard menu giving options to the player on what to do.
def Menu():
    global game_map, map_size_x, map_size_y
    print('''| 1: Create Map
| 2: Draw Map
| 3: Load Map
| 4: Save Map''')
    menu_choice = input(":")
    if menu_choice == ("1"):
        print('''| 1: Automatic
| 2: Manual Map''')
        menu_sub1_choice = input(":")
        if menu_sub1_choice == ("1"):
            Aut_Map_Maker()
        elif menu_sub1_choice == ("2"):
            Man_Map_Maker()
        else:
            print("Option currently unavailable.")
            Menu()
##    elif menu_choice == ("2"):
##        if game_map == 0: #Checks if a map has been created:
##            print("")
##            os.system('cls')
##            print("You gotta make a map first!")
##            Menu()
##        else:
##            Place_Obstacle()
##    elif menu_choice == ("3"):
##        if game_map == 0:
##            print("")
##            os.system('cls')
##            print("You gotta make a map first!")
##            Menu()
##        else:
##            print("")
##            os.system('cls')
##            print("Option currently unavailable.")
##            Menu()
##    elif menu_choice == ("4"):
##        if game_map == 0:
##            print("")
##            os.system('cls')
##            print("You gotta make a map first!")
##            Menu()
##        else:
##            print("")
##            os.system('cls')
##            print("Option currently unavailable.")
##            Menu()
    elif menu_choice == ("2"):
        if game_map == 0:
            print("")
            os.system('cls')
            print("You gotta make a map first!")
            Menu()
        else:
            print("")
            os.system('cls')
            Map_Draw()
    elif menu_choice == ("3"):
        Load_Map()
    elif menu_choice == ("4"):
        if game_map == 0:
            print("")
            os.system('cls')
            print("You gotta make a map first!")
            Menu()
        else:
            Save_Map()
    else:
        print("")
        os.system('cls')
        print("Please enter a valid number.")
        Menu()

def Aut_Map_Maker(): #Will draw a map with random sizes from 5-15.
    global game_map, map_size_x, map_size_y
    print("")
    os.system('cls')
    map_size_x = 10 #random.randrange(10,101)
    map_size_y = 10 #random.randrange(10,101)
    game_map = [['[ ]' for __ in range(map_size_x)] for _ in range(map_size_y)]
    Map_Draw()

def Man_Map_Maker():
    global game_map, map_size_x, map_size_y
    print("")
    os.system('cls')
    worked = False
    try: #Inputting the measurments of the map, also making sure that it fits the proper dimensions.
        map_size_x = int(input("How wide do you want the map to be? (X) (10-100) |"))
        map_size_y = int(input("How long do you want the map to be? (Y) (10-100) |"))
        if map_size_x >= 10 and map_size_x <= 100 and map_size_y >= 10 and map_size_y <= 100:
            game_map = [['[ ]' for __ in range(map_size_x)] for _ in range(map_size_y)]
            worked = True
        else:
            print("Please enter a from 10 to 100.")
            Man_Map_Maker()
    
    except(ValueError):
        print("Please enter a from 10 to 100.")
        Man_Map_Maker()
    if worked:
        Map_Draw()

    
def Place_Obstacle(): #Places an obstacle at the given coordinates.
    global game_map, map_size_x, map_size_y
    print("")
    os.system('cls')
    item = input("What do you want to place? |") #What ever is typed here will be the obstacle as a string.
    item_x = input("Where will you place the item? (x position) |")
    item_y = input("Where will you place the item? (y position) |")
    try:
        game_map[int(item_y)][int(item_x)] =(f"[" +(item)+ "]")
    except(IndexError):
        print("Please type a valid point on the map.")
        Place_Obstacle()
    Map_Draw()

#Draws the map with the given dimensions.
def Map_Draw():
    global game_map, map_size_x, map_size_y
    for y in range(map_size_y): #Makes an empty column.
        column = str()
        for x in range(map_size_x): #Adds each item to the column.
            column += f"{game_map[y][x]}" #The full column.
        print(column) #This will print as many times as there are columns because it is inside the first "for" loop.
    ##Menu()

def Load_Map(load_name):
    global game_map, map_size_x, map_size_y
    game_map = []
##    load_name = input("What is the level's name? |")
    map_load = open((f'{load_name}.LPM'), "r")
    line = map_load.readline() #Reads the first line once to get it started.
    linesplit = line.split(",")
    map_size_x = int(linesplit[0])
    map_size_y = int(linesplit[1])
    line = map_load.readline()
    while line:  # Assures the program runs through the whole file.
        linesplit = line.split("'")
        column = []
        for f in linesplit:
            f = f.strip(" \n")
            column.append(f)
        game_map.append(column)
        line = map_load.readline()  # Assures that the program checks more than one line.
    map_load.close()
    print("")
    os.system('cls')
    print("Finished!")
    ##Menu()

##def Save_Map():
##    global game_map, map_size_x, map_size_y
##    save_name = input("What will you call the level? |")
##    map_save = open((f'{save_name}.LPM'), "w")
##    map_save.write(f'{map_size_x} {map_size_y}\n')
##    map_save.write(f'{game_map}')
##    map_save.close()
##    print("")
##    os.system('cls')
##    print("Finished!")
##    ##Menu()

def Save_Map():
    global game_map, map_size_x, map_size_y
    save_name = input("What will you call the level? |")
    map_save = open((f'{save_name}.LPM'), "w")
    map_save.write(f'{map_size_x},{map_size_y} \n')
    for y in range(map_size_y):
        column_write = (str())
        for x in range(map_size_x):
            if (x+1) < map_size_x:
                column_write += f"{game_map[y][x]}'"
            else:
                column_write += f"{game_map[y][x]}"
        map_save.write(f'{column_write} \n')
    map_save.close()
    print("")
    os.system('cls')
    print("Finished!")
    ##Menu()
