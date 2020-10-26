#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:50:10 2020

@author: mickael
"""

import graphviz

adv_ressource = {"copper_plate": {"components": {"copper": 5},
                                   "product": 1,
                                   "price": 7,
                                   "rank": 0},

                  "copper_cable": {"components": {"copper_plate": 1},
                                   "product": 5,
                                   "price": 3,
                                   "rank": 1},

                  "iron_plate": {"components": {"iron": 5},
                                 "product": 1,
                                 "price": 8,
                                 "rank": 1},

                  "steel": {"components": {"iron_plate": 4},
                            "product": 1,
                            "price": 40,
                            "rank": 2},

                  "iron_gear_wheel": {"components": {"iron_plate": 1},
                                      "product": 5,
                                      "price": 1,
                                      "rank": 2},

                  "circuit": {"components": {"iron_plate": 1,
                                             "copper_cable": 1},
                              "product": 1,
                              "price": 1,
                              "rank": 2},

                  "adv_circuit": {"components": {"circuit": 1,
                                                 "copper_cable": 1,
                                                 "steel": 1},
                                  "product": 1,
                                  "price": 1,
                                  "rank": 3},

                  "solar_panel": {"components": {"copper_plate": 1,
                                                 "circuit": 1},
                                  "product": 1,
                                  "price": 1,
                                  "rank": 3},
                  "low_density_structure": {"components": {"copper_plate": 1,
                                                           "steel": 1},
                                            "product": 1,
                                            "price": 1,
                                            "rank": 3},

                  "processing_unit": {"components": {"circuit": 1,
                                                     "adv_circuit": 1},
                                      "product": 1,
                                      "price": 1,
                                      "rank": 4},
                  "speed_module": {"components": {"circuit": 1,
                                                  "iron_gear_wheel": 1},
                                   "product": 1,
                                   "price": 1,
                                   "rank": 3},
                  "rocket_control_unit": {"components": {"processing_unit": 1,
                                                         "speed_module": 1},
                                          "product": 1,
                                          "price": 1,
                                          "rank": 5},
                  "rocket_part": {"components": {"rocket_control_unit": 1,
                                                 "low_density_structure": 1},
                                  "product": 1,
                                  "price": 1,
                                  "rank": 6},
                  "space_module": {"components": {"rocket_part": 1,
                                                  "solar_panel": 1},
                                   "product": 1,
                                   "price": 1000,
                                   "rank": 7}
                  }


def link(d_link, name="default", f_name="link_default.gv"):
    g = graphviz.Digraph(name, filename=f_name,
                         node_attr={'color': 'lightblue2', 'style': 'filled'})

    with g.subgraph(name="iron") as c:
        c.node('iron', shape="box")
        c.node_attr.update(style='filled', color='lightgrey')

    with g.subgraph(name="copper") as c:
        c.node('copper', shape="box")
        c.node_attr.update(style='filled', color='antiquewhite')

    g.node_attr.update(color='lightblue2', style='filled')
    for key in d_link.keys():
        g.node(key, shape="box", label="<" + " ".join(key.split("_")) + "<BR /><FONT POINT-SIZE='11'>"+"Price: " + str(d_link[key]["price"]) + "</FONT>>")

        for comp in d_link[key]["components"].keys():
            g.edge(comp, key, label=" "+str(d_link[key]["components"][comp]))
    g.view()


if __name__ == "__main__":
    link(adv_ressource)
