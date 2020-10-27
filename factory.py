#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:38:47 2020

@author: mickael
"""

import time
from datetime import datetime
import pickle
import copy
# Vol honteux de script pour pas faire dl de module
# from prettytable import PrettyTable
import pprint
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
        self.money = 100000
        self.employees = 10
        self.last_time = datetime.now()

        self.ressource = {"copper": {"prod_rate": 1,
                                     "total": 10,
                                     "price": 1,
                                     "buy_price": 10},
                          "iron": {"prod_rate": 1,
                                   "total": 10,
                                   "price": 1,
                                   "buy_price": 10}
                          }

        # prod rate st by user

        self.adv_ressource_prod_rate = {}
        # dict of fact
        # load of json / yml file instead?
        self.adv_ressource = {"copper_plate": {"components": {"copper": 2},
                                               "product": 1,
                                               "price": 4,
                                               "rank": 0,
                                               "unlock_price": 2000},

                              "copper_cable": {"components": {"copper_plate": 1},
                                               "product": 5,
                                               "price": 1,
                                               "rank": 1,
                                               "unlock_price": 2000},

                              "iron_plate": {"components": {"iron": 2},
                                             "product": 1,
                                             "price": 3,
                                             "rank": 1,
                                             "unlock_price": 2000},

                              "steel": {"components": {"iron_plate": 5},
                                        "product": 1,
                                        "price": 1,
                                        "rank": 2,
                                        "unlock_price": 2000},

                              "iron_gear_wheel": {"components": {"iron_plate": 1},
                                                  "product": 5,
                                                  "price": 1.5,
                                                  "rank": 2,
                                                  "unlock_price": 2000},

                              "circuit": {"components": {"iron_plate": 5,
                                                         "copper_cable": 10},
                                          "product": 1,
                                          "price": 50,
                                          "rank": 2,
                                          "unlock_price": 2000},

                              "adv_circuit": {"components": {"circuit": 1,
                                                             "copper_cable": 5,
                                                             "steel": 5},
                                              "product": 1,
                                              "price": 100,
                                              "rank": 3,
                                              "unlock_price": 2000},

                              "solar_panel": {"components": {"copper_plate": 10,
                                                             "circuit": 5},
                                              "product": 1,
                                              "price": 100,
                                              "rank": 3,
                                              "unlock_price": 2000},

                              "low_density_structure": {"components": {"copper_plate": 1,
                                                                       "steel": 1},
                                                        "product": 1,
                                                        "price": 5,
                                                        "rank": 3,
                                                        "unlock_price": 2000},

                              "processing_unit": {"components": {"circuit": 5,
                                                                 "adv_circuit": 3},
                                                  "product": 1,
                                                  "price": 250,
                                                  "rank": 4,
                                                  "unlock_price": 2000},

                              "speed_module": {"components": {"circuit": 10,
                                                              "iron_gear_wheel": 15},
                                               "product": 1,
                                               "price": 750,
                                               "rank": 3,
                                               "unlock_price": 2000},

                              "rocket_control_unit": {"components": {"processing_unit": 10,
                                                                     "speed_module": 10},
                                                      "product": 1,
                                                      "price": 5500,
                                                      "rank": 5,
                                                      "unlock_price": 2000},

                              "rocket_part": {"components": {"rocket_control_unit": 1,
                                                             "low_density_structure": 100},
                                              "product": 1,
                                              "price": 8500,
                                              "rank": 6,
                                              "unlock_price": 2000},

                              "space_module": {"components": {"rocket_part": 1,
                                                              "solar_panel": 50},
                                               "product": 1,
                                               "price": 10000,
                                               "rank": 7,
                                               "unlock_price": 2000}
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
                                     "c": self.set_prod_rate,
                                     "se": self.selling_order,
                                     "sa": self.save_factory,
                                     "l": self.load_factory,
                                     "q": self.gw_quit}

        self.shop_choices = {"g": self.main_factory,
                             "u": self.shop_upgrade,
                             "r": self.shop_new_ressource,
                             "p": self.print_report
                             }

    def load_adv_ressource_json(self):
        import json
        with open('adv_ressource.json') as fp:  # raise JSONDecodeError
            adv = json.load(fp)
            print(adv)

    def main_factory(self):
        #   Update of factory values:
        self.update()
        # Autosave each time the player go back to main screen.
        self.autosave()
        txt = ["",
               "You're in your office, what do you want to do?",
               "(P)rint Report",
               "(B)uy      (Se)ll",
               "(C)hange production rate",
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
                     "last_time": self.last_time,
                     "ressource": self.ressource,
                     "upgrade": self.upgrade,
                     "adv_ressource_prod_rate": self.adv_ressource_prod_rate
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

    def check_prod_rate(self):
        # check no issue in self.adv_ressource_prod_rate:
        d_res = {res: 0 for res in ["copper", "iron"] + list(self.adv_ressource_prod_rate.keys())}
        for key in self.adv_ressource_prod_rate.keys():
            for res in self.adv_ressource_prod_rate[key].keys():
                d_res[res] += self.adv_ressource_prod_rate[key][res]
        error_rate = []
        for res in d_res.keys():
            if d_res[res] > 1:
                error_rate.append(res)
        print("Error in Production rate of:", ", ".join(error_rate))
        # return True si aucun res n'a d'erreur
        return not error_rate

    def set_prod_rate(self):
        txt = ["Choose which ressource you like to change its prod rate:"]
        pprint.pprint(self.adv_ressource_prod_rate)
        l_res = [" - " + elt for elt in self.adv_ressource_prod_rate.keys()]
        print_list(txt + l_res + ["(G)o back"])

        action = req_input(l_res + ["g"])
        if action == "g":
            return self.main_factory()
        else:
            for prod in self.adv_ressource_prod_rate[action].keys():
                pr_f = float(input("Enter the prod ratio (Ex: 0.2) for " + prod + ": "))
                self.adv_ressource_prod_rate[action][prod] = pr_f
        return self.set_prod_rate()

    def update(self):
        self.update_ressource()
        self.update_adv_ressource()

    def update_ressource(self):
        time_now = datetime.now()
        delta = (time_now - self.last_time).total_seconds()
        self.last_time = time_now

        # Update of Iron and Copper:
        for r in ["copper", "iron"]:  # self.ressource.keys():
            self.ressource[r]["total"] += delta*self.ressource[r]["prod_rate"]

    def update_adv_ressource(self):
        # 1 copy of ressource values
        to_update_ressource = copy.deepcopy(self.ressource)

        # 2 dict of ressource per rank that the player own
        d_res = {}
        for res in self.adv_ressource.keys():
            if res in self.ressource.keys():
                rank = int(self.adv_ressource[res]["rank"])
                try:
                    d_res[rank].append(res)
                except KeyError:
                    d_res[rank] = [res]
        try:
            max_rank = max(d_res.keys())
        except ValueError:
            print("value error")
            return None

        # 3 pour chaque ressource de rank croissant
        i = 0
        while i <= max_rank:
            try:
                for res in d_res[i]:
                    # pour chaque ressource d'un rank
                    # get which ressource it will use and how much:
                    all_res_pos = []
                    comps = self.adv_ressource[res]["components"].keys()

                    for comp in comps:
                        prod_rate = self.adv_ressource_prod_rate[comp][res]
                        qt_comp = self.ressource[comp]["total"]

                        # quantity of a comp allocated to the craft of res
                        qt_available = prod_rate*qt_comp
                        # how many comp is required to produce 1 res
                        comp_req = self.adv_ressource[res]["components"][comp]
                        # res_pos = nb of res possible to craft according to this comp
                        res_pos = int(qt_available / comp_req)
                        all_res_pos.append(res_pos)
                    # minimum of all res_pos is how much we can craft
                    min_craft = min(all_res_pos)
                    # how much of each craft output
                    product = self.adv_ressource[res]["product"]
                    self.ressource[res]["total"] += min_craft * product
                    to_update_ressource[res]["total"] += min_craft * product
                    for comp in comps:
                        to_update_ressource[comp]["total"] -= min_craft * self.adv_ressource[res]["components"][comp]

            except KeyError:
                print("keyerror")
            i += 1
        # end
        self.ressource = to_update_ressource

    def print_report(self):
        """
        Use of PrettyTable module.
        """
        x = PrettyTable()
        x.field_names = ["Ressource", "Prod Rate",
                         "Total Amount", "Selling Price", "Buying Price"]

        for ressource in ['iron', 'copper']:
            x.add_row([ressource.capitalize(),
                       self.ressource[ressource]["prod_rate"],
                       round(self.ressource[ressource]["total"], 2),
                       self.ressource[ressource]["price"],
                       self.ressource[ressource]["buy_price"]
                       ])
        # only adv
        for ressource in self.ressource.keys():
            if ressource in ['copper', "iron"]:
                continue
            x.add_row([" ".join(ressource.split("_")).capitalize(),
                       "---",  # self.ressource[ressource]["prod_rate"],
                       round(self.ressource[ressource]["total"], 2),
                       self.ressource[ressource]["price"],
                       self.ressource[ressource]["buy_price"]
                       ])

        len_mon = len(str(self.money))
        print("", "")
        print("+--------" + "-"*len_mon + "-+\n"
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
              str(self.ressource[res_input]["price"]) + " per unit "
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

    def shop(self):
        """
        buy new ressource to craft
        buy new machine to upgrade prod rate
        """
        txt = ["", "",
               "You're in the Shop.",
               "(U)pgrade a production rate (copper or iron)",
               "Buy a new (R)essource",
               "(H)ire     (F)ire",
               "(G)o back"
               ]

        print_list(self.ascii_factory)
        print_list(txt)

        action = req_input(self.shop_choices)
        if action == "p":
            self.print_report()
            return self.shop()
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
        len_mon = len(str(self.money))
        print("+--------" + "-"*len_mon + "-+\n"
              "| Money: " + str(self.money) + " |")
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
        # 1 get all ressource which components are all in self.ressource:
        products = self.ressource.keys()
        new_pos_res = []
        for res in self.adv_ressource.keys():
            if res in products:
                continue
            # if all components of res in are producted in self.ressource
            if all([comp in products for comp in self.adv_ressource[res]["components"].keys()]):
                new_pos_res.append(res)

        if new_pos_res:
            x = PrettyTable()
            x.field_names = ["Name", "ressource used", "Rank", "Price"]
            for res in new_pos_res:
                x.add_row([res,
                           ", ".join(self.adv_ressource[res]["components"].keys()),
                           self.adv_ressource[res]["rank"],
                           self.adv_ressource[res]["unlock_price"]
                           ])
            print("Possible ressource to buy:")
            len_mon = len(str(self.money))
            print("+--------" + "-"*len_mon + "-+\n"
                  "| Money: " + str(self.money) + " |")
            print(x)
            print("(G)o back to shop")

            action = req_input(new_pos_res + ["g"])
            if action == "g":
                return self.shop()
            else:
                if self.money > self.adv_ressource[action]["unlock_price"]:
                    self.money -= self.adv_ressource[action]["unlock_price"]
                    self.add_ressource(action)
                else:
                    print("You don't have money to unlock the production of " + action)
                return self.shop()
        else:
            print("No other ressource are available to add to production.", "")
            return self.shop()

    def add_ressource(self, res_name):
        # res_name = 2
        if res_name in self.ressource.keys():
            print("ressource already owned.")
            return None
        self.ressource[res_name] = {"prod_rate": 0,
                                    "total": 0,
                                    "price": self.adv_ressource[res_name]["price"],
                                    "buy_price": self.adv_ressource[res_name]["price"]*10}
        # pour chaque composant de res
        print("in")
        components = self.adv_ressource[res_name]["components"].keys()
        for comp in components:
            print("  "+comp)
            if comp not in self.adv_ressource_prod_rate.keys():
                self.adv_ressource_prod_rate[comp] = {}
            print("adv_ressource_prod_rate:",self.adv_ressource_prod_rate)
            if res_name in self.adv_ressource_prod_rate[comp]:
                continue
            else:
                self.adv_ressource_prod_rate[comp][res_name] = round(1/len(components),1)
        # need check adv_ressource_prod_rate

if __name__ == "__main__":
    f = Factory()
    # f.auto_load()
    f.main_factory()
