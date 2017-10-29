#!/usr/bin/env python
"""This file takes as input an environment database folder and num_envs, runs a-star on the database with different heuristic 
weights and returns the results. 

Author: Mohak Bhardwaj
Date: October 6, 2017
"""
import argparse
from collections import defaultdict
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.insert(0, "..")
import time
from planning_python.environment_interface.env_2d import Env2D
from planning_python.state_lattices.common_lattice.xy_analytic_lattice import XYAnalyticLattice
from planning_python.cost_functions.cost_function import PathLengthNoAng
from planning_python.heuristic_functions.heuristic_function import EuclideanHeuristicNoAng, ManhattanHeuristicNoAng
from planning_python.data_structures.planning_problem import PlanningProblem
from planning_python.planners.astar import Astar

x_lims = [0, 200]
y_lims = [0, 200]

env_params = {'x_lims': x_lims, 'y_lims': y_lims}
lattice_params = {'x_lims': x_lims, \
                    'y_lims': y_lims, \
                    'resolution': [1, 1], \
                    'origin': (0, 0), \
                    'rotation': 0, \
                    'connectivity': 'eight_connected', \
                    'path_resolution': 1}

cost_fn = PathLengthNoAng()
heuristic_fn = EuclideanHeuristicNoAng()
lattice = XYAnalyticLattice(lattice_params)
lattice.precalc_costs(cost_fn)
planner = Astar()
start_n = lattice.state_to_node((0,0))
goal_n = lattice.state_to_node((199, 199))

def run_benchmark(folder):
    global env_params, lattice_params, cost_fn, heuristic_fn, lattice, planner, start_n, goal_n
     
    # h_weight_list = range(1, 100, 10)
    # h_weight_list = [0] + h_weight_list
    h_weight_list = [0]
    e = Env2D()
    print('Running benchmark')
    subdirs = sorted(os.listdir(os.path.abspath(folder)))

    for subdir in subdirs:
        curr_env_file = os.path.join(folder, subdir,'map.png')
        # print curr_env_file
        e.initialize(curr_env_file, env_params)

        for h_weight in h_weight_list:
            prob_params = {'heuristic_weight': h_weight}
            prob = PlanningProblem(prob_params)
            prob.initialize(e, lattice, cost_fn, heuristic_fn, start_n, goal_n, visualize=False)
            planner.initialize(prob) 
            path, path_cost, num_expansions, plan_time, came_from, cost_so_far, c_obs = planner.plan()
            if len(path)==0:
                print "no solution for ", os.path.join(folder, subdir,'map.png')
                continue
            # path has duplicates due to transitions 
            path_to_save = [each_transition[0] for each_transition in path]
            path_to_save.append(path[-1][1])
            path_to_save_npy = np.asarray(path_to_save)
            # print path
            # print path_to_save_npy    
            path_to_save_npy.dump(os.path.join(folder, subdir, 'path.npy'))

            # results[h_weight].append((num_expansions,plan_time))
            planner.clear_planner() #clear the planner in the end
            e.initialize_plot(start_n, goal_n)
            e.plot_path(path)

            plt.gca().set_axis_off()
            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            			  hspace = 0, wspace = 0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.savefig(os.path.join(folder, subdir, 'solution.png'), bbox_inches = 'tight', pad_inches = 0)
            plt.close()
            # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--database_folders', required=True)
    args = parser.parse_args()
    #Run the benchmark and save results
    run_benchmark(args.database_folders)
    # print(results)

