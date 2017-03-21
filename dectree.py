#!/bin/env python
# coding: utf-8

# Instance
# id, atrr1, attr2, ..., label

import operator
import util

class Attribute(object):
    """Used to descirbe attributes"""

    def __init__(self, name, kinds):
        super(Attribute, self).__init__()
        self._name = name
        self._kinds = kinds
        self._kind_num = len(kinds)

    def get_name(self):
        return self._name

    def get_num(self):
        return self._kind_num

    def get_kinds(self):
        return self._kinds

    def __repr__(self):
        result = "Attribute: %s %s" % (self._name, self._kinds)
        return result

    __str__ = __repr__


class Instance(object):

    def __init__(self, attributes, label):
        super(Instance, self).__init__()
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

    def set_label(self, label):
        self._label = label
        return self

    def __repr__(self):
        result = "Instance: %s %s" % (self._attributes, self._label)
        return result

    __str__ = __repr__


class Node(object):
    """used to describe node of a decision tree"""

    def __init__(self, is_root, is_leaf):
        super(Node, self).__init__()
        self._is_leaf = is_leaf
        self._is_root = is_root
        self._descenddants = []
        self._attribute_name = 'None'
        self._label = 'None'
        self._kind = 'None'

    def add_descendants(self, descendant):
        self._descenddants.append(descendant)
        return self

    def is_leaf(self):
        return self._is_leaf

    def is_root(self):
        return self._is_root

    def descendants(self):
        return self._descenddants

    def set_attribute(self, name):
        self._attribute_name = name
        return self

    def set_label(self, label):
        self._label = label
        return self

    def set_kind(self, kind):
        self._kind = kind
        return self

    @staticmethod
    def dfs_traverse(node, path, paths):
        """
        Args:
            node, next node to traverse
            path, current path
            paths, total paths
        """
        # TODO make results more direct
        # a:b
        # a means current category
        # b means kind of its parent category

        path.append(':'.join([node._attribute_name, node._kind]))
        if 0 == len(node.descendants()):
            paths.append("-->".join(path))
        else:
            for descendant in node.descendants():
                Node.dfs_traverse(descendant, path, paths)
        path.pop()

    def __repr__(self):
        """use dfs"""
        path = []
        paths = []
        Node.dfs_traverse(self, path, paths)
        if 0 == len(paths):
            return "\t".join(path)
        else:
            return "\n".join(paths)

    __str__ = __repr__


class DecisionTree(object):

    def __init__(self, training_set, attribute_set):
        super(DecisionTree, self).__init__()
        self._training_set = training_set
        self._attribute_set = attribute_set
        self._root = Node(True, False)

    def construct(self):
        """construct"""
        self.construct_helper(self._training_set,
                self._attribute_set,
                self._root,
                'None')
        return self

    def construct_helper(self,
            training_set,
            attribute_set,
            parent_node,
            kind):
        """contruct decision tree"""

        # handle special case
        # 1. empty attribute_set
        # 2. all instances have same value on the same attributes

        # empty attribute set
        if 0 == len(attribute_set):
            self.construct_with_most_labels(training_set, parent_node, kind)
            return

        # select best attribute
        selected_attribute = self.select_attribute(training_set, attribute_set)
        print "Selected attribute: " , selected_attribute.get_name()
        attribute_set.pop(selected_attribute.get_name())

        # construct node
        new_node = Node(False, True)
        new_node.set_attribute(selected_attribute.get_name())
        new_node.set_kind(kind)
        parent_node.add_descendants(new_node)

        # all has same value on this property
        uniq_set = set()
        name = selected_attribute.get_name()
        map(lambda x: uniq_set.add(x.get_attribute(name)) or uniq_set, training_set)

        if 1 == len(uniq_set):
            return

        # construct each descendants
        descendants = self.divide_descendants(training_set, selected_attribute)

        # loop into each descendants
        for kind, descendant in descendants:
            self.construct_helper(descendant, attribute_set, new_node, kind)

    def select_attribute(self, training_set, attribute_set):
        """select attribute"""
        total_size = len(training_set)
        labels = {}
        map(util.agg_label(labels), training_set)
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
                map(util.agg_label(labels), my_kind)
                probs = [ v * 1.0 / len(my_kind) for v in labels.itervalues() ]
                entropy = util.RatioEntropy(probs, len(my_kind), total_size).entropy()
                print "Kind: ", kind, " Kind probs: ", probs
                print "Kind: ", kind, " Kind entropy: ", entropy
                attribute_entropy.append(entropy)
            attributes_entropy[name] = whole_entropy - sum(attribute_entropy)

        print "Entropy details: ", attributes_entropy
        name = max(attributes_entropy.iteritems(), key=operator.itemgetter(1))[0]
        return attribute_set[name]

    def divide_descendants(self, training_set, attribute):
        """divide training set"""
        name = attribute.get_name()
        for kind in attribute.get_kinds():
            instances = filter(lambda x:x.get_attribute(name) == kind, training_set)
            if len(instances):
                yield kind, instances

    def construct_with_most_labels(self, training_set, parent_node, kind):
        """return label"""
        new_node = Node(False, True)
        labels = {}
        map(util.agg_label(labels), training_set)
        max_label = max(labels.iteritems(), key=operator.itemgetter(1))[0]
        new_node.set_kind(kind)
        new_node.set_label(max_label)
        parent_node.add_descendants(new_node)

    def predict(self, instance):
        """predict label based on attribute of instance, using constructed tree
        """
        print self._root
        #return self.predict_helper(instance)

    def predict_helper(self, instance):
        pass
