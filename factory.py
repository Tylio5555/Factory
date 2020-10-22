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
from prettyt import PrettyTable


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


class Factory():
    """
    As the director of the Factory you will be given report
    upon which you will have to make decision for the future.
    """
    def __init__(self):
        self.money = 1000
        self.prod_per_s = 0.1
        self.employees = 10
        self.last_time = datetime.now()
        

        self.ressource = {"copper": {"prod_rate": 0.1,
                                     "total": 10,
                                     "price": 1},
                          "iron": {"prod_rate": 0.1,
                                   "total": 10,
                                   "price": 1}
                          }

        self.main_factory_choices = {"p": self.print_report,
                                     "s": self.shop,
                                     "sa": self.save_factory,
                                     "l": self.load_factory,
                                     "q": self.gw_quit}
    def main_factory(self):
        #   Update of factory values:
        self.update()

        txt = ["", "",
               "You're in your office, what do you want to do?",
               "(P)rint Report",
               "(S)hop"
               "(Sa)ve     (L)oad",
               "(Q)uit"]

        print_list(self.ascii_factory)
        print_list(txt)

        action = req_input(self.town_choices)
        if action == "sa":
            self.save_world()
            return self.main_town()

        elif action == "l":
            self.load_world()
            return self.main_town()

        # Autosave each time the player go back to town and do something else.
        self.autosave()
        return self.main_factory_choices[action]()

    def save_factory(self, autosave=False):
        """
        save attribute in a pickle file
        """
        if autosave:
            savename = "autosave"
        else:
            savename = input("Choose a savename: ")
        data_dict = {"ressource": self.ressource}
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
        with open("saves/" + savename, "rb") as savefile:
            attr_dict = pickle.load(savefile)
        for key in attr_dict:
            setattr(self, key, attr_dict[key])
        print("Save loaded.")

    def gw_quit(self):
        print("Session ended.")
        return "Coward die in shame"

    def update(self):
        time_now = datetime.now()
        print(time_now - self.last_time)
        self.last_time = time_now

    def print_report(self):
        """
        Use of PrettyTable module to show a list of dragon object.
        """
        x = PrettyTable()
        x.field_names = ["Ressource", "Production Rate", "Total Amount"]

        for ressource in self.ressource.keys():

        i = 1
        for d in list_d:
            x.add_column(str(i),
                         [d.name,
                          d.elem_type.capitalize(),
                          d.level,
                          round(d.hp),
                          round(d.mp),
                          round(d.attack),
                          round(d.attack_spe),
                          round(d.defense),
                          round(d.defense_spe),
                          d.proficiency])
            i += 1
        print(x)
        return self.main_factory()
    
    def selling_order(self):
        """
        choose ressource to sell and which amount
        """
        pass
    

    def shop(self):
        """
        buy new ressource to craft
        buy new machine to upgrade prod
        """
        txt = ["", "",
               "You're in the Shop.",
               "(P)rint Report",
               "(H)ire     (F)ire"
               ]

        print_list(self.ascii_factory)
        print_list(txt)
if __name__ == "__main__":
    Factory()