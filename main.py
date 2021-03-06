# Imports
from random import choice, randint
from rich import print as rprint
from art import *
from rich.console import Console
from rich.table import Table
from pystyle import Colorate, Colors
from database import Database
import sys
from animations.load_animation import load_animation
import requests
import json
import validators

# Clears the screen
console = Console()

# Ores that are obtained are picked from this list
obtainableOres = []

# Function to get random splash text


def get_random_line(file_name):
    line = choice(open(file_name).readlines())
    return line


def get_server():
    while True:
        rprint("[blue]Enter the server you want to connect to:[/blue]")
        rprint("[green]If you are unsure, be sure to check out the official lord of the mines server at https://mine.errorcodezero.ml[/green]")
        rprint("[magenta]By the way do not add a / at the end of the url[/magenta]")

        userInput = input()
        if validators.url(userInput) == True:
            request = requests.get(userInput)
            try:
                jsonRequest = json.loads(request.text)
            except:
                rprint("[red]Error: Could not connect to server[/red]")
                continue
        else:
            rprint("[red]Invalid url![/red]")
            continue
        url = userInput

        while True:
            rprint("[green]Are you signing up(y/n)[/green]")
            userInput = input()
            if userInput == "y":
                username = input("Username: ")
                password = input("Password: ")
                request = requests.get(url + f"/signup/{username}/{password}")
                request = requests.get(url + f"/ores/{username}/{password}")
                try:
                    ores = json.loads(request.text)["ores"]
                except:
                    rprint("[red]Error: Could not connect to server[/red]")
                    rprint("[red]Press enter to exit[/red]")
                    input()
                    sys.exit()
                request = requests.get(url + f"/shop/{username}/{password}")
                try:
                    shopItems = json.loads(request.text)["shop_items"]
                except:
                    rprint("[red]Error: Could not connect to server[/red]")
                    rprint("[red]Press enter to exit[/red]")
                    input()
                    sys.exit()
                return main_menu(url, username, password, ores, shopItems)
            elif userInput == "n":
                username = input("Username: ")
                password = input("Password: ")
                request = requests.get(url + f"/items/{username}/{password}")
                try:
                    ores = json.loads(request.text)["ores"]
                except:
                    rprint("[red]Error: Could not connect to server[/red]")
                    rprint("[red]Press enter to exit[/red]")
                    input()
                    sys.exit()
                try:
                    shopItems = json.loads(request.text)["items"]
                except:
                    rprint("[red]Error: Could not connect to server[/red]")
                    rprint("[red]Press enter to exit[/red]")
                    input()
                    sys.exit()
                return main_menu(url, username, password, ores, shopItems)


def main_menu(url, username, password, ores, shopItems):
    # Splash Screen
    splash_screen = text2art("LordOfTheMines")

    # Colored Splash Screen
    rgb_splash_screen = Colorate.Diagonal(Colors.blue_to_red, splash_screen)

    print(rgb_splash_screen)

    # Random splash text
    splash_text = get_random_line("variables/splash.txt")
    rprint(f"[white]{splash_text}[/white]")

    # Asks questions to the user
    rprint("[blue]What would you like to do?[/blue]")
    rprint("[green]1. Mine[/green]")
    rprint("[green]2. Sell[/green]")
    rprint("[green]3. Shop[/green]")
    rprint("[green]4. Inventory[/green]")
    rprint("[green]5. Info[/green]")
    rprint("[green]6. Craft[/green]")
    userInput = input()
    console = Console()
    # Mine
    if userInput == "1" or userInput.lower() == "mine":
        while True:
            console.clear()
            return mine(url, username, password, ores, shopItems)
    # Sell
    elif userInput == "2" or userInput.lower() == "sell":
        while True:
            console.clear()
            return sell(url, username, password, ores, shopItems)
    # Shop
    elif userInput == "3" or userInput.lower() == "shop":
        while True:
            console.clear()
            return shop(url, username, password, ores, shopItems)
    # Inventory
    elif userInput == "4" or userInput.lower() == "inventory":
        while True:
            console.clear()
            return inventory(url, username, password, ores, shopItems)
    # Info
    elif userInput == "5" or userInput.lower == "info":
        while True:
            console.clear()
            return info(url, username, password, ores, shopItems)
    # Craft
    elif userInput == "6" or userInput.lower() == "craft":
        while True:
            console.clear()
    # Invalid input
    else:
        rprint("[red]Invalid input[/red]")
        main_menu(url, username, password, ores, shopItems)

# Mine


def mine(url, username, password, ores, shopItems):
    while True:
        """
            Picks an ore
        """
        # Asks user to type random number(To prove they are not afk)
        inputToType = randint(1, 100)
        rprint(f"Type the number {inputToType}(or type exit to exit)")
        userInput = input()
        # Checks if what they typed is the random number
        if userInput == str(inputToType):
            try:
                response = requests.request(
                    "GET", url + f"/mine/{username}/{password}")
                jsonResponse = json.loads(response.text)
                if jsonResponse["amount"] == 0:
                    rprint("[red]You mined nothing[/red]")
                else:
                    rprint(
                        f"""[green]You mined {jsonResponse["amount"]} {jsonResponse["item"]}[/green]""")
            except:
                rprint("[red]Error: Could not connect to server[/red]")
        # Exit
        elif userInput == "exit":
            console.clear()
            return main_menu(url, username, password, ores, shopItems)
        # If user doesn't type specified number
        else:
            rprint(f"You were supposed to type {inputToType}")

# Sell


def sell(url, username, password, ores, shopItems):
    """
        Sell a certain amount of ores
    """
    while True:
        # Inventory table
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Amount", justify="right", style="magenta")

        request = requests.get(url + f"/sync/{username}/{password}")
        try:
            jsonRequest = json.loads(request.text)
            userInventory = jsonRequest["user_inventory"]
        except:
            userInventory = {}
            rprint("[red]Error: Could not connect to server[/red]")
            rprint("[red]Press enter to exit[/red]")
            input()
            return main_menu(url, username, password, ores, shopItems)

        # Adds all the elements to inventory table
        for ore in userInventory:
            if ore == "coins":
                continue
            elif userInventory[ore] <= 0:
                userInventory[ore] = 0
                continue
            else:
                try:
                    table.add_row(
                        f"""{ore}""", f"""{userInventory[ore]}""")
                except:
                    table.add_row(
                        f"""{ore}""", f"""{userInventory[ore]}""")

        console.log(table)
        rprint("[magenta]What ore would you like to sell?[/magenta](type exit to exit and type sellall to sell everything)")

        # Gets user input
        userInput = input()

        # If user wants to exit
        if userInput == "exit":
            console.clear()
            return main_menu(url, username, password, ores, shopItems)

        # If user wants to sell everything
        elif userInput == "sellall":
            console.clear()
            for ore in userInventory:
                if ore == "coins":
                    continue
                elif ore in shopItems:
                    continue
                else:
                    request = requests.get(
                        url, f"/sellall/{username}/{password}")
            rprint("[green]You sold all your ore[/green]")
            try:
                request = requests.get(
                    url + "/sync/" + f"{username}/{password}")
                userInventory = json.loads(request.text)["user_inventory"]
                rprint(f"""Coins: {userInventory["coins"]}""")
            except:
                rprint(f"""Coins: 0""")
            rprint("Press enter to continue")

            input()
            return main_menu(url, username, password, ores, shopItems)

        # If ore is invalid
        elif userInput.lower() not in userInventory.keys():
            rprint(f"[red]{userInput} is not a valid ore[/red]")
            return sell(url, username, password, ores, shopItems)

        # If they try to sell coins
        elif userInput.lower() == "coins":
            return rprint(f"[red]You can't sell coins[/red]")

        try:
            if shopItems[userInput]["sellable"] == False:
                rprint("[red]You can't sell that[/red]")
                return sell(url, username, password, ores, shopItems)
        except:
            pass

        try:
            if userInventory[userInput.lower()] == 0:
                return rprint(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")
        except:
            return rprint(f"[red]You don't enough {userInput.lower()} to sell[/red]")

        ore_to_sell = userInput

        # How much does user want to sell
        rprint(
            f"[magenta]How many {ore_to_sell} would you like to sell(type exit to exit)?[/magenta]")
        userInput = input()

        # Again they can type exit
        if(userInput == "exit"):
            return main_menu(url, username, password, ores, shopItems)

        try:
            userInput = int(userInput)
        except:
            return rprint(f"[red]{userInput} is not a valid number[/red]")

        # If they don't have enough of an ore to sell
        if userInput > userInventory[ore_to_sell]:
            return rprint(f"[red]You don't have enough {ore_to_sell} to sell[/red]")

        # To prevent them from selling negative amounts
        elif userInput < 0:
            return rprint(f"[red]You can't sell negative amounts of ore[/red]")

        # Actually selling the ore
        request = requests.get(
            url + f"/sell/{username}/{password}/{ore_to_sell}/{userInput}")

# Inventory


def inventory(url, username, password, ores, shopItems):
    while True:
        # Inventory table
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Quantity", justify="right", style="magenta")

        request = requests.get(url + f"/sync/{username}/{password}")
        try:
            jsonRequest = json.loads(request.text)
        except:
            print("[red]Error: Could not connect to server[/red]")
            rprint("[red]Press enter to exit[/red]")
            jsonRequest = {}
            input()
            return main_menu(url, username, password, ores, shopItems)

        userInventory = jsonRequest["user_inventory"]

        # Adds all the elements to inventory table
        for ore in userInventory:
            try:
                if ore == "coins":
                    continue
                elif userInventory[ore] == 0:
                    continue
                else:
                    try:
                        table.add_row(
                            f"""{ore}""", f"""{userInventory[ore]}""")
                    except:
                        table.add_row(
                            f"""{ore}""", f"""{userInventory[ore]}""")
            except:
                continue

        # Prints the table
        console.print(table)

        # Coins
        try:
            rprint(f"""Coins: {userInventory["coins"]}""")
        except:
            rprint(f"""Coins: 0""")
        rprint("Press enter to continue")
        input()
        return main_menu(url, username, password, ores, shopItems)


def shop(url, username, password, ores, shopItems):
    """
        Shop
        # TODO
    """
    # Shop table
    table = Table(title="Shop")

    table.add_column("Item", justify="right", style="green", no_wrap=True)
    table.add_column("Price", justify="right", style="blue")

    # Adds all the elements to shop table
    for item in shopItems:
        try:
            table.add_row(
                f"""{item.title()}""", f"""{shopItems[item]["price"]}""")
        except:
            table.add_row(f"""{item}""", f"""Priceless""")

    console.log(table)

    request = requests.get(url + f"/sync/{username}/{password}")
    try:
        jsonRequest = json.loads(request.text)
    except:
        print("[red]Error: Could not connect to server[/red]")
        rprint("[red]Press enter to exit[/red]")
        jsonRequest = {}
        input()
        return main_menu(url, username, password, ores, shopItems)
        
    userInventory = jsonRequest["user_inventory"]

    # Coins
    try:
        rprint(f"Coins: {userInventory['coins']}")
    except:
        userInventory["coins"] = 0
        rprint(f"Coins: 0")

    # Asks what to buy
    print("What would you like to buy(type exit to exit)")
    userInput = input()
    try:
        for item in shopItems:
            if userInput.lower() == item.lower():
                if userInventory["coins"] >= shopItems[item]["price"]:
                    request = requests.get(
                        url + f"/buy/{username}/{password}/{item}/1")
                    rprint(f"[green]You bought {item}![/green]")
                    return shop(url, username, password, ores, shopItems)
                else:
                    rprint(
                        f"[red]You don't have enough coins to buy {item}[/red]")
                    rprint(f"[red]Press enter to continue[/red]")
                    input()
                    return shop(url, username, password, ores, shopItems)
            else:
                rprint("[red]Invalid item[/red]")

    except:
        rprint(
            f"[red]You don't have enough coins to buy {userInput.lower()}[/red]")
    # Exit
    if userInput.lower() == "exit":
        return main_menu(url, username, password, ores, shopItems)

# Info


def info(url, username, password, ores, shopItems):
    while True:
        # Asks user what they would like to see info about
        rprint(
            "[green]What item would you like to see more about(type exit to exit)?([/green]")

        userInput = input()
        if userInput.lower() == "exit":
            return main_menu(url, username, password, ores, shopItems)
        try:
            for item in shopItems:
                if userInput.lower() == item.lower():
                    rprint(f"""Name: [green bold]{item}[/green bold]""")
                    rprint(
                        f"""Description: [green]{shopItems[item]["description"]}[/green]""")
                    rprint("[blue]Press enter to continue")
                    input()
                    return info(url, username, password, ores, shopItems)

            for ore in ores:
                if userInput.lower() == ore.lower():
                    rprint(f"""Name: [green bold]{ore}[/green bold]""")
                    rprint(f"""Price: [green]{ores[ore]["price"]}[/green]""")
                    rprint("[blue]Press enter to continue")
                    input()
                    return info(url, username, password, ores, shopItems)
            rprint("[red]Invalid item[red]")
            return info(url, username, password, ores, shopItems)

        except:
            rprint(f"[red]{userInput} is not a valid item[/red]")
            return info(url, username, password, ores, shopItems)


# Error handling
if __name__ == "__main__":
    try:
        while True:
            get_server()

    except:
        load_animation("Exitting", 10)
        sys.exit()


# while True:
#     get_server()
