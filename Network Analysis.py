#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 12:26:23 2018

@author: patrickchen
"""

import pandas as pd
import networkx as nx
from community import community_louvain as cm

states = [
        'Alaska','Alabama','Arkansas','Arizona','California','Colorado','Connecticut',
        'Delaware','District of Columbia','Florida','Georgia','Hawaii','Iowa','Idaho','Illinois','Indiana',
        'Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri',
        'Mississippi','Montana','North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
        'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island',
        'South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Vermont',
        'Washington','Wisconsin','West Virginia','Wyoming',
        ]

#get and clean data
data = pd.read_excel('State_to_State_Migrations_Table_2015.xls',header=0,index_col=0,skiprows=6,skip_footer=8,na_values='N/A3')
data['District of Columbia'] = 0
data = data[states].ix[states].fillna(0)
data = data > data.median().median()
data = data.unstack()
data = data[data == True]
significant_flows = data.index.tolist()


#create network
flows = nx.Graph()
flows.add_edges_from(significant_flows)
flows.remove_edges_from(flows.selfloop_edges())

#find 5 largest betweenness centralities
largest_betweeness = pd.Series(nx.betweenness_centrality(flows)).nlargest(5)
#find 5 largest closeness centralities
largest_closeness = pd.Series(nx.closeness_centrality(flows)).nlargest(5)

#find number of connected componants
num_of_connected_componants = len([nx.connected_components(flows)])

#find communities in the network and the modularity
partition = cm.best_partition(flows)

communities = pd.Series(partition)
communities = pd.DataFrame({'States':communities.index, 'Community':communities.values})

num_of_communities = len(communities['Community'].unique())

communtiy0states = communities[communities['Community']==0]['States']
communtiy1states = communities[communities['Community']==1]['States']
communtiy2states = communities[communities['Community']==2]['States']

modularity = cm.modularity (partition, flows)


#save graph
nx.write_graphml(flows, open('SignificantStatetateMigrationFlows.graphml', 'wb'))