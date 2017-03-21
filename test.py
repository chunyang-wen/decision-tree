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


attributes = generate_attributes()
training_set = generate_training_set()

print attributes
print training_set

dec = dectree.DecisionTree(training_set, attributes)

print [ x.get_attribute('Color') for x in training_set ]
print [ x.get_attribute('Size') for x in training_set ]
print [ x.get_label() for x in training_set ]

tree = dec.construct()



