#!/bin/env python
# coding: utf-8
# author: chunyang.wen@gmail.com

import copy
import dectree
import util

def generate_attributes():

    attributes = []
    attributes.append(dectree.Attribute('Color', ['Red', 'Blue']))
    attributes.append(dectree.Attribute('Size', ['Big', 'Small']))

    result = {}
    map(lambda x:result.setdefault(x.get_name(), x), attributes)
    return result

def generate_training_set():

    instances = []
    attributes = {'Size': 'Big', 'Color' : 'Red'}
    instances.append(dectree.Instance(copy.deepcopy(attributes), 'Good'))
    attributes['Color'] = 'Blue'
    instances.append(dectree.Instance(copy.deepcopy(attributes), 'Bad'))
    instances.append(dectree.Instance(copy.deepcopy(attributes), 'Bad'))
    return instances

def generate_node():
    COLOR_BLUE = 'Blue'
    COLOR_RED = 'Red'
    SIZE_BIG = 'Big'
    SIZE_SMALL = 'Small'
    root = dectree.Node(True, False)
    root.set_attribute('ROOT')
    root.set_kind('KIND')
    node1 = dectree.Node(False, True)
    node1.set_attribute('Color')
    node1.set_kind(COLOR_BLUE)
    node2 = dectree.Node(False, False)
    node2.set_attribute('Size')
    node2.set_kind(SIZE_SMALL)
    node3 = dectree.Node(False, True)
    node3.set_attribute('Color')
    node3.set_kind(COLOR_RED)
    root.add_descendants(COLOR_BLUE, node1)
    root.add_descendants(SIZE_SMALL, node2)
    node2.add_descendants(COLOR_RED, node3)
    return root


attributes = generate_attributes()
training_set = generate_training_set()
nodes = generate_node()

print attributes
print training_set

dec = dectree.DecisionTree(training_set, attributes)

print [ x.get_attribute('Color') for x in training_set ]
print [ x.get_attribute('Size') for x in training_set ]
print [ x.get_label() for x in training_set ]
print nodes

tree = dec.construct()
print tree.predict(training_set[0])


