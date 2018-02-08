#######################################################################################
# 2median.py
# Claire Fritzler - 001167579
# 4110 Assignment 2
#
# The 2median.py program should:
# - Take an optional parameter -n value
# - If the optional parameter is not included, then we read from the input GML file
# - Check if the network is a path
# - Check if the nodes all have weights
# - Check if the edges all have lengths
# - Return the OPT-1-Median and the ID of the node where the 1 median will be located
#######################################################################################

import networkx as nx
import random
import argparse
import os
import math

# Function to initialize the graph with n nodes and write the graph to a GML file
def initGraph(n, f):
	Graph = nx.path_graph(n)
	
	#Initialize weights
	for i in range(0, n):
		weight = random.randint(1, 20)
		Graph.node[i]['weight'] = weight
	
	#initialize lengths		
	for i in range(1, n):
		length = random.randint(1, 10)
		Graph.edges[i-1, i]['length'] = length
		
	f = f + ".gml"
	nx.write_gml(Graph, f)
	return Graph

# Function to check if the network is a path
# Property of paths: number of nodes - number of edges = 1
def isPath(Graph):
	edges = nx.number_of_edges(Graph)
	nodes = nx.number_of_nodes(Graph)
	
	if((nodes - edges) != 1):
		return False
	else:
		return True
		
# Function to check if the nodes all have weights		
def haveWeights(Graph):
	for i in Graph.nodes():
		if(not Graph.node[i]['weight']):
			return False
		if(Graph.node[i]['weight'] < 1):
			return False
	return True

# Function to check if all the edges have lengths
def haveLengths(Graph):
	for source, target, edge in Graph.edges(data = True):
		if(not edge):
			print("Your graph is missing an edge")
			return False
		elif(edge['length'] < 1):
			print("Your graph has invalid edge lengths")
			return False
	return True
	
# Parse the input user arguments 	
parser = argparse.ArgumentParser(description='1-Median Calculator for a Graph')
parser.add_argument('-n', nargs='?', type=int, help='Number of nodes')
parser.add_argument('file', type=str, help='GML File')
parser.add_argument('-p', nargs='?', type = int, help='Number of facilities')
args = parser.parse_args()
n = args.n
file = args.file
p = args.p

newFile = False
# If the user does not provide integer n then read the GML file
if(n is None):
	try:
		Graph = nx.read_gml(file)
		print("GML file has been read")
	except:
		print(file + ": File cannot be read")
# If n is provided, construct the network
else:
	print("A random graph with " + str(n) + " nodes will be generated for you")
	Graph = initGraph(n, file)
	

if(not isPath(Graph)):
	print("Your graph is not a simple path")
	exit()
	
if(not haveWeights(Graph)):
	print("Your graph has invalid weights")
	exit()

if(not haveLengths(Graph)):
	print("Your graph has invalid lengths")
	exit()	
	

nx.write_gml(Graph, file)

if(p is None):
	print("You did not specify the number of facilities to place")
	p = input("Please specify the number of facilities")
	

######################################################
# P-Median
#
#####################################################

n = len(Graph.nodes())
costF = []
costG = []
F = []
G = []


# Calculates the cost on a subpath
def FCost(path):
	cost = []
	for facility in path.nodes():
		sum = 0
		for customer in path.nodes():
			if (customer != facility):
				weight = path.node[customer]['weight']
				distance = nx.shortest_path_length(Graph, customer, facility, 'length')
				sum = sum + (weight * distance)
			cost.append([sum, facility])
	minCost = min(cost)
	return minCost

# Helper function
# Calculate the cost of a facility on a subpath
def GCost(path, facility):
	sum = 0
	for customer in path.nodes():
		if customer != facility:
			weight = path.node[customer]['weight']
			distance = nx.shortest_path_length(Graph, customer, facility, 'length')
			sum = sum + (weight * distance)
	return sum

#Calculate the base case for F	
def BaseCaseF(i):
	if (i == (n-1)):
		return (0,n-1)
	else:
		id = []
		for t in range(i, n):
			id.append(t)
		path = Graph.subgraph(id)
		minCost = FCost(Graph)
		return minCost

# Calculate the base case of G
def BaseCaseG(i):
	if i == (n-1):
		return (0,n-1)
	else:
		id = []
		for t in range(i , n):
			id.append(t)
		path = Graph.subgraph(id)
		minCost = GCost(path, i)
		return minCost

# Helper function
# gives the leftmost facility
def placeFacilities():
	facilities = []
	temp = 0
	###### HINT::: This has to go from p down to 1
	for q in range(p, 0, -1):
		if(q == p):
			temp = costF[q-1][0]
		else:
			temp = costF[q-1][temp]
		facilities.append(temp)
		if len(facilities) == p:
			break
		temp = GCost[q-1][k]
	return facilities
	

# Calculate the p-median using the DP algorithm from the papers	
def PMedian():
	initF = []
	rowF = []
	initG = []
	rowG = []
	for i in range(n - 1, -1, -1):
		min = BaseCaseF(i)
		initF.append(min[0])
		rowF.append(min[1])
		initF.append(BaseCaseG(i))
		rowG.append(i)
	
	rowF.reverse()
	rowG.reverse()
	initF.reverse()
	initG.reverse()
	
	costF.append(list(initF))
	costG.append(list(initG))
	F.append(list(rowF))
	G.append(list(rowG))
	
	for i in range(1, p):
		val = []
		for j in range(0, n):
			val.append(j)
		F.append(val)
		G.append(val)
		costF.append(val)
		costG.append(val)
		
	return costF[p-1][0] 
		
		#  Getting key errors trying to calculate the weight of the vertices					
	for q in range(2, p+1):
		for j in range(n, 0, -1):
			for k in range(j, n+1):
				sum = 0
				for t in range(j, k+1):
					weight = Graph.node[t]['weight']
					distance = nx.shortest_path_length(Graph, t-1, k-1, 'length')
					sum = sum + (weight * distance)
				if costF[q-1][j-1] > (sum + costG[q-1][k-1]):
					costF[q-1][j-1] = sum + costF[q-1][k-1]
					F[q-1][j-1] = k-1
			for k in range(j+1, n+2):
				sum = 0
				for t in range(j, k):
					weight = Graph.node[t-1]['weight']
					distance = nx.shortest_path_length(Graph, t-1, j-1, 'length')
					sum = sum + (weight * distance)
				if k == (n+1):
					costG[q-1][j-1] = min(costG[q-1][j-1], sum)
				else:
					if costG[q-1][j-1] > (sum + costF[q-1][k-1]):
						costG[q-1][j-1] = sum + costF[q-1][k-1]
						G[q-1][j-1] = k-1
	return costF[p-1][0] 
   
     		
cost = PMedian()

print("The cost of the", p,"-median is: ", cost)

############################################################################################
# 1-Median Calculation:
# Calculate the cost of each node and store it in a list 
# Go through the list and find the minimum value
############################################################################################

costs = []
for facility in Graph.nodes():
	sum = 0
	for customer in Graph.nodes():
		if(customer != facility):
			weight = Graph.node[customer]['weight']
			distance = nx.shortest_path_length(Graph, customer, facility, 'length')
			sum = sum + (weight + distance)
	costs.append((sum, facility))
	
optimalFacility = min(costs, key=lambda t: (t[0]))
print("The cost of the 1-Median is: " + str(optimalFacility[0]))
print("The ID of the 1-Median is: " + str(optimalFacility[1]))




