#!/bin/env python
# coding:utf-8

import math
import operator

class Entropy(object):

    def __init__(self, probs):
        """init"""
        self._probs = probs
        assert len(self._probs) > 0, 'must contain at least 1 probility'

    def entropy(self):
        """
        ent = -p*log(p)
        """
        ent = 0.0
        p1 = map(lambda x : 1 if x == 0 else x, self._probs)
        p1 = map(lambda x: -x * math.log(x, 2), p1)
        return reduce(operator.add, p1)


class RatioEntropy(Entropy):
    """Use to calculate an entropy with a ratio"""

    def __init__(self, probs, instance_num, total_num):
        """init"""
        super(RatioEntropy, self).__init__(probs)
        self._ratio = instance_num * 1.0 / total_num

    # overide
    def entropy(self):
        return self._ratio * super(RatioEntropy, self).entropy()


