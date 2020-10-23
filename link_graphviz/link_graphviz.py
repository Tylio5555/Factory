#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:50:10 2020

@author: mickael
"""

import graphviz

adv_ressource = {"copper_plate": {"components": {"copper": 1}},
                 "copper_cable": {"components": {"copper_plate": 1}},
                 "iron_plate": {"components": {"iron": 1}},
                 "iron_gear_wheel": {"components": {"iron_plate": 1},
                                     "product": 5},
                 "circuit": {"components": {"iron_plate": 1,
                                            "copper_cable": 1},
                             "product": 1}
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
        for comp in d_link[key]["components"].keys():
            g.edge(comp, key, label=" "+str(d_link[key]["components"][comp]))
    g.view()


if __name__ == "__main__":
    link(adv_ressource)
