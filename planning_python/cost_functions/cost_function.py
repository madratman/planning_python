#!/usr/bin/env python
import numpy as np
import dubins

from planning_python.utils import angles

class CostFunction(object):
  """ Wrapper class for generic cost functions
  """
  def __init__(self):
        return None

  def get_cost(self, edge):
    """Given an edge(list of states), returns the cost associated with that edge

    @param  edge: a list of states (tuples)
    @return cost: a scalar cost value associated with that edge
    """

    return 0


class PathLengthNoAng(CostFunction):
  """Penalizes euclidean length of path.
  To be used when edge contains only (x,y) or (x,y,z) coordinates"""
  def __init__(self):
    super(PathLengthNoAng, self).__init__()

  def get_cost(self, edge):
    n = len(edge)
    cost = 0
    cost += np.linalg.norm(np.asarray(edge[n-1]) - np.asarray(edge[0]))
    return cost

class PathLengthAng(CostFunction):
  """Penalizes euclidean length of path.
  To be used when edge contains heading entries as well, but we want to ignore them"""
  def __init__(self):
    super(PathLengthAng, self).__init__()

  def get_cost(self, edge):
    n = len(edge)
    cost = 0
    for i in range(n-1):
      xi = np.asarray(edge[i][:-1])
      xip1 = np.asarray(edge[i+1][:-1])
      cost += np.linalg.norm(xip1 - xi)
    return cost

class DubinsPathLength(CostFunction):
  def __init__(self, turning_radius=None):
      assert turning_radius is not None, "Please enter turning radius parameter"
      self.turning_radius = turning_radius

  def get_cost(self, edge):
    assert len(edge[0]) == 3, "state must be of form (x,y,heading)"
    
    s1 = (edge[0][0], edge[0][1], angles.normalize_angle_positive(edge[0][2]))
    s2 = (edge[-1][0], edge[-1][1], angles.normalize_angle_positive(edge[-1][2]))
    
    return dubins.path_length(s1, s2, self.turning_radius)