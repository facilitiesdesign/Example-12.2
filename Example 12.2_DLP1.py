# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Parameters
    l = [25, 35, 30, 40]
    width = [20, 20, 20, 20]
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
    y = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
        ]
    c = 1.00
    
    #Indices
    n = len(f)
    M = 999
    
    #Create model
    m = Model("Example 12.2")
    
    #Decision variables
    u = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "u")
    v = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "v")
    w = m.addVars(range(n), range(n), lb = -GRB.INFINITY, vtype = GRB.CONTINUOUS, name = "w")    
    
    #Set objective fuction
    m.setObjective(quicksum(u[i,j]*(0.5*(l[i] + l[j]) + hc[i][j] - M*y[i][j]) + v[i,j]*(0.5*(l[i] + l[j]) +hc[i][j] - M*(1 - y[i][j])) for i in range(n-1) for j in range(i+1, n)), GRB.MAXIMIZE)
    
    #Write constraints    
    for i in range(n-1):
        for j in range(i+1,n):
            m.addConstr(w[i,j] <= c*f[i][j])
            m.addConstr(-w[i,j] <= c*f[i][j])
    for i in range(n):
        m.addConstr(quicksum(u[i,j] - v[i,j] + w[i,j] for j in range(i+1,n)) + quicksum(-u[j,i] + v[j,i] - w[j,i] for j in range(i)) <= 0)

    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')