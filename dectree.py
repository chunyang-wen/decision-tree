#!/bin/env python
# coding: utf-8

# Instance
# id, atrr1, attr2, ..., label

class Attribute(object):
    """Used to descirbe attributes"""

    def __init__(self, name, kinds):
        self._name = name
        self._kinds = kinds
        self._kind_num = len(kinds)

    def get_name(self):
        return self._name

    def get_num(self):
        return self._kind_num

    def get_kinds(self):
        return self._kinds


class Instance(object):

    def __init__(self, attributes):
        self._attributes = attributes
        assert len(attributes) > 0, 'must have at least one attribute'

    def set_attribute_value(attribute_values):
        assert len(attribute_values) == len(self._attributes),\
                'value and name must have equal length'
        self._attribute_values = {}
        map(lambda x, y: self._attribute_values[x.get_name()] = y,
                self._attributes,
                self._attribute_values)

    def get_attribute(name):
        """get specified attribute value"""
        self._attribute_values.get(name, None)


class Node(object):
    """used to describe node of a decision tree"""

    def __init__(self, is_root, is_leaf, descendants):
        self._is_leaf = is_leaf
        self._is_root = is_root
        self._descenddants = descendants

    def descendants(self):
        return self._descenddants

    def is_leaf(self):
        return self._is_leaf

    def is_root(self):
        return self._is_root


class DecisionTree(object):

    def __init__(self, training_set):
        self._training_set = training_set

    def construct(self):
        """contruct decision tree"""
        pass

    def predict(self, instance):
        """predict label based on attribute of instance, using constructed tree
        """
        pass
