#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:38:47 2020

@author: mickael
"""

import time
from datetime import datetime
import pickle
# Vol honteux de script pour pas faire dl de module
# from prettytable import PrettyTable
from prettytable import PrettyTable


def print_list(txt):
    for elt in txt:
        print(elt)


def load_ascii(filename):
    with open(filename, 'r') as f:
        ascii_txt = f.readlines()
    return [elt.strip("\n") for elt in ascii_txt]


def req_input(list_possible):
    """
    Request input from user within a list of possible choice.
    """
    if type(list_possible) == dict:
        list_possible = list(list_possible.keys())

    action = input()
    while action.lower() not in list_possible:
        print("wrong input, possible expected values: " +
              str(list_possible))
        action = input()
    return action.lower()


def req_amount(max_amount):
    """
    Request input from user within a list of possible choice.
    """

    action = input()
    while int(action) > max_amount:
        print("wrong input, possible expected values bellow: " +
              str(max_amount))
        action = input()
    return int(action)


def value_function(x, n=1.25, a=1, b=0):
    """
    x = level
    n = power
    b = Base stat value
    a = proficiency
    """
    return x**n + a*x + b


"""

   ╔═╗╔═╗╔═╗╔╦╗╔═╗╦═╗╦ ╦
   ╠╣ ╠═╣║   ║ ║ ║╠╦╝╚╦╝
   ╩  ╩ ╩╚═╝ ╩ ╚═╝╩╚═ ╩

"""


class Factory():
    """
    As the director of the Factory you will be given report
    upon which you will have to make decision for the future.
    """
    def __init__(self):
        self.money = 1000
        self.employees = 10
        self.last_time = datetime.now()

        self.ressource = {"copper": {"prod_rate": 0.5,
                                     "total": 10,
                                     "price": 1,
                                     "buy_price": 10},
                          "iron": {"prod_rate": 0.5,
                                   "total": 10,
                                   "price": 1,
                                   "buy_price": 10}
                          }

        self.upgrade = {"prod_rate_copper": {"price": 1000,
                                             "prod_rate": 0.5,
                                             "nb_upgrade_done": 0},
                        "prod_rate_iron": {"price": 1000,
                                           "prod_rate": 0.5,
                                           "nb_upgrade_done": 0}
                        }

        self.ascii_factory = load_ascii("ascii_factory.txt")

        self.main_factory_choices = {"p": self.print_report,
                                     "b": self.buy_order,
                                     "s": self.shop,
                                     "se": self.selling_order,
                                     "sa": self.save_factory,
                                     "l": self.load_factory,
                                     "q": self.gw_quit}

        self.shop_choices = {"g": self.main_factory,
                             "u": self.shop_upgrade
                             }

    def main_factory(self):
        #   Update of factory values:
        self.update()
        # Autosave each time the player go back to main screen.
        self.autosave()
        txt = ["",
               "You're in your office, what do you want to do?",
               "(P)rint Report",
               "(B)uy      (Se)ll",
               "(S)hop",
               "(Sa)ve     (L)oad",
               "(Q)uit"]
        print("")
        print_list(self.ascii_factory)
        print_list(txt)

        action = req_input(self.main_factory_choices)
        if action == "sa":
            self.save_factory()
            return self.main_factory()

        elif action == "l":
            self.load_factory()
            return self.main_factory()

        elif action == "p":
            self.print_report()
            return self.main_factory()

        return self.main_factory_choices[action]()

    def auto_load(self):
        savename = "autosave"
        with open("saves/" + savename, "rb") as savefile:
            attr_dict = pickle.load(savefile)
        for key in attr_dict:
            setattr(self, key, attr_dict[key])
        print("autoload done")

    def autosave(self):
        self.save_factory(autosave=True)

    def save_factory(self, autosave=False):
        """
        save attribute in a pickle file
        """
        if autosave:
            savename = "autosave"
        else:
            savename = input("Choose a savename: ")
        data_dict = {"money": self.money,
                     "ressource": self.ressource,
                     "upgrade": self.upgrade
                     }
        with open("saves/" + savename, "wb") as savefile:
            pickle.dump(data_dict,
                        savefile)
        if not autosave:
            print("Progression Saved")

    def load_factory(self):
        """
        load attributes from specified pickle file
        """
        savename = input("Choose a save to load: ")
        try:
            with open("saves/" + savename, "rb") as savefile:
                attr_dict = pickle.load(savefile)
            for key in attr_dict:
                setattr(self, key, attr_dict[key])
            print("Save loaded.")
        except FileNotFoundError:
            print("", "No save found with corresponding name.")

    def gw_quit(self):
        print("Session ended.")
        return "Coward die in shame"

    def update(self):
        time_now = datetime.now()
        delta = (time_now - self.last_time).total_seconds()
        self.last_time = time_now
        for r in self.ressource.keys():
            self.ressource[r]["total"] += delta * self.ressource[r]["prod_rate"]

    def print_report(self):
        """
        Use of PrettyTable module.
        """
        x = PrettyTable()
        x.field_names = ["Ressource", "Production Rate",
                         "Total Amount", "Selling Price", "Buying Price"]

        for ressource in self.ressource.keys():
            x.add_row([ressource.capitalize(),
                       self.ressource[ressource]["prod_rate"],
                       round(self.ressource[ressource]["total"], 2),
                       self.ressource[ressource]["price"],
                       self.ressource[ressource]["buy_price"]
                       ])
        len_mon = len(str(self.money))
        print("",
              "+--------" + "-"*len_mon + "-+\n"
              "| Money: " + str(self.money) + " |")
        print(x)

    def selling_order(self):
        """
        choose ressource to sell and which amount:
        """
        self.update()
        self.print_report()
        print("", "Choose which ressource to sell or (G)o back")
        res_input = req_input(list(self.ressource.keys())+["g"])

        if res_input == "g":
            return self.main_factory()

        print("", "How much " + res_input + " do you want to sell?")
        res_amount = req_amount(self.ressource[res_input]["total"])

        profit = self.ressource[res_input]["price"] * res_amount
        self.money += profit
        self.ressource[res_input]["total"] -= res_amount

        print("You sold " + str(res_amount) + " " + res_input + " at " +
              str(self.ressource[res_input]["price"]) + " per unit"
              "for a total of: " + str(profit))
        return self.main_factory()

    def buy_order(self):
        """
        choose ressource to buy and which amount:
        """
        self.update()
        self.print_report()
        print("Choose which ressource to buy or (G)o back")
        res_input = req_input(list(self.ressource.keys())+["g"])

        if res_input == "g":
            return self.main_factory()

        print("How much " + res_input + " do you want to buy?")
        res_amount = req_amount(self.ressource[res_input]["total"])

        loss = self.ressource[res_input]["buy_price"] * res_amount

        if loss > self.money:
            print("You don't have enough money to make that purchase")
            return self.main_factory()

        self.money -= loss
        self.ressource[res_input]["total"] += res_amount

        print("You bought " + str(res_amount) + " of " + res_input + " at " +
              str(self.ressource[res_input]["buy_price"]) + " per unit"
              "for a total of: " + str(loss))
        return self.main_factory()

    def craft_order(self):
        pass

    def shop(self):
        """
        buy new ressource to craft
        buy new machine to upgrade prod
        """
        txt = ["", "",
               "You're in the Shop.",
               "(P)rint Report",
               "(U)pgrade a production rate (copper or iron)",
               "(B)uy a new ressource",
               "(H)ire     (F)ire",
               "(G)o back"
               ]

        print_list(self.ascii_factory)
        print_list(txt)

        action = req_input(self.shop_choices)
        return self.shop_choices[action]()

    def shop_upgrade(self):
        print("Which prod rate you would like to upgrade? (copper or iron)")
        x = PrettyTable()
        x.field_names = ["Ressource", "Production Rate",
                         "Prod rate augment", "Price"
                         ]
        for res in ["copper", "iron"]:
            x.add_row([res.capitalize(),
                       self.ressource[res]["prod_rate"],
                       self.upgrade["prod_rate_" + res]["prod_rate"],
                       round(value_function(self.upgrade["prod_rate_" + res]["nb_upgrade_done"], b=1000), 1)

                       ])
        print(x)

        action = req_input(["copper", "iron", "g"])
        if action == "g":
            return self.main_factory()

        upgrade_price = round(value_function(self.upgrade["prod_rate_" + action]
                                                         ["nb_upgrade_done"],
                                             b=1000),
                              1)

        if self.money < upgrade_price:
            print("You don't have enough money.")

        self.money -= upgrade_price
        self.ressource[action]["prod_rate"] += self.upgrade["prod_rate_" + action]["prod_rate"]
        self.upgrade["prod_rate_" + action]["nb_upgrade_done"] += 1

        print(action + " production rate upgrade bought")
        return self.main_factory()

    def shop_new_ressource(self):
        pass

    def add_ressource(self, ):
        pass
        # res_name = 2


if __name__ == "__main__":
    f = Factory()
    f.auto_load()
    f.main_factory()
