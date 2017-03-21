#!/bin/env python
# coding: utf-8

# Instance
# id, atrr1, attr2, ..., label

import util

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

    def __init__(self, attributes, label):
        self._attributes = attributes
        self._label = label
        print "Initial with: ", self._attributes
        print "Initial with: ", self._label
        assert len(attributes) > 0, 'must have at least one attribute'

    """
    def set_attribute_value(attribute_values):
        assert len(attribute_values) == len(self._attributes),\
                'value and name must have equal length'
        self._attribute_values = {}
        map(lambda x, y: self._attribute_values[x.get_name()] = y,
                self._attributes,
                self._attribute_values)

    """

    def get_attribute(self, name):
        """get specified attribute value"""
        print "Get attribute: ", self._attributes, ", for: ", name
        return self._attributes.get(name, None)

    def get_label(self):
        return self._label

    def __repr__(self):
        result = "Instance: %s %s" % (self._attributes, self._label)
        return result

    __str__ = __repr__


class Node(object):
    """used to describe node of a decision tree"""

    def __init__(self, is_root, is_leaf, descendants):
        self._is_leaf = is_leaf
        self._is_root = is_root
        self._descenddants = descendants

    def add_descendants(self, descendant):
        self._descenddants.append(descendant)

    def is_leaf(self):
        return self._is_leaf

    def is_root(self):
        return self._is_root

    def descendants(self):
        return self._descenddants


class DecisionTree(object):

    def __init__(self, training_set, attribute_set):
        self._training_set = training_set
        self._attribute_set = attribute_set
        self._root = Node(True, False, [])

    def construct(self):
        """construct"""
        self.construct_helper(self._training_set,
                self._attribute_set,
                self._root)

    def construct_helper(self,
            training_set,
            attribute_set,
            parent_node):
        """contruct decision tree"""

        # handle special case
        # all with the same labels

        # single sets

        # select best attribute
        selected_attribute = self.select_attribute(training_set, attribute_set)
        print "Selected attribute: " , selected_attribute.get_name()
        attribute_set.pop(selected_attribute.get_name())

        # construct node
        new_node = Node(False, True, [])
        parent_node.add_descendants(new_node)

        # construct each descendants
        descendants = self.divide_descendants(training_set, selected_attribute)

        # loop into each descendants
        for descendant in descendants:
            construct_helper(descendant, attribute_set, attribute_seq, new_node)

    def select_attribute(self, training_set, attribute_set):
        """select attribute"""
        total_size = len(training_set)
        labels = {}
        def agg_label(labels):
            def inner(x):
                label = x.get_label()
                labels.setdefault(label, 0)
                labels[label] = labels[label] + 1
            return inner
        map(agg_label(labels), training_set)
        probs = [ v * 1.0 / total_size for v in labels.itervalues() ]
        whole_entropy = util.Entropy(probs).entropy()
        attributes_entropy = {}
        print "Total size: ", total_size, " Total entropy: ", whole_entropy
        print "Traning set size: ", len(training_set)

        for attribute in attribute_set.itervalues():
            name = attribute.get_name()
            attribute_entropy = []
            print "Current analyse attribute: ", name
            # handle kinds of this attribute
            for kind in attribute.get_kinds():
                # each kind
                my_kind = filter(lambda x:x.get_attribute(name) == kind, training_set)
                print "Kind: ", kind, " Kind size: ", len(my_kind)
                if (0 == len(my_kind)):
                    continue
                labels ={}
                map(agg_label(labels), my_kind)
                probs = [ v * 1.0 / len(my_kind) for v in labels.itervalues() ]
                entropy = util.RatioEntropy(probs, len(my_kind), total_size).entropy()
                print "Kind: ", kind, " Kind probs: ", probs
                print "Kind: ", kind, " Kind entropy: ", entropy
                attribute_entropy.append(entropy)
            attributes_entropy[name] = whole_entropy - sum(attribute_entropy)

        name = None
        current_max = None
        print "Entropy details: ", attributes_entropy
        for key, value in attributes_entropy.iteritems():
            if name is None:
                name = key
                current_max = value
            if value > current_max:
                name = key
                current_max = value
        return attribute_set[name]

    def divide_descendants(self, training_set, attribute):
        """divide training set"""
        name = attribute.get_name()
        for kind in attribute.get_kinds():
            instances = filter(lambda x:x.get_attribute(name) == kind, training_set)
            if len(instances):
                yield instances

    def predict(self, instance):
        """predict label based on attribute of instance, using constructed tree
        """
        return self.predict_helper(instance)

    def predict_helper(self, instance):
        pass
