# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Parameters
    l = [25, 35, 30, 40]
    hc = [
        [0, 3.5, 5, 5],
        [3.5, 0, 5, 3],
        [5, 5, 0, 5],
        [5, 3, 5, 0]
        ]
    f = [
        [0, 25, 35, 50],
        [25, 0, 10, 15],
        [35, 10, 0, 50],
        [50, 15, 50, 0]
        ]
    c = 1.00
    
    #Indices
    n = len(f)
    M = 999
    
    #Create model
    m = Model("Example 12.2")
    
    #Decision variables
    x = m.addVars(range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "Center")
    xp = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "XP")
    xn = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "XN")
    y = m.addVars(range(n), range(n), vtype = GRB.BINARY, name = "Y")
    
    #Set objective fuction
    m.setObjective(quicksum(c * f[i][j] * (xp[i,j] + xn[i,j]) for i in range(n-1) for j in range(i+1, n)), GRB.MINIMIZE)
    
    #Write constraints    
    for i in range(n-1):
        for j in range(i+1, n):
            m.addConstr(x[i] - x[j] == xp[i,j] - xn[i,j], name = "Absolute_Value_Constraint")
            m.addConstr(x[i] - x[j] + M * y[i,j] >= 0.5 * (l[i] + l[j]) + hc[i][j])
            m.addConstr(x[j] - x[i] + M *(1 - y[i,j]) >= 0.5 * (l[i] + l[j]) + hc[i][j]) 

    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')