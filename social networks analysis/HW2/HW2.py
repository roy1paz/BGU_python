import networkx as nx
from networkx.algorithms import community
from networkx import edge_betweenness_centrality
import community as community_louvain
import itertools
from networkx.algorithms.community import k_clique_communities
from random import random
import pandas as pd
import networkx.algorithms.community as nx_comm
import json
import datetime as dt
import os


def get_name():
    return "Roy Paz"


def get_id():
    return "208421271"


'''           1          '''
# 1.1
def community_detector(algorithm_name, network, most_valualble_edge=None):
    if algorithm_name == 'girvin_newman':
        temp = []
        modul = []
        communities_generator = community.girvan_newman(network, most_valualble_edge)
        k = nx.number_of_nodes(network) / 2
        limited = itertools.takewhile(lambda c: len(c) <= k, communities_generator)
        for i in limited:
            temp.append(list(sorted(c) for c in i))
        for i in temp:
            modul.append(community.modularity(network, i))
        communities = temp[modul.index(max(modul))]
        dic = {'num_partitions': len(communities), 'modularity': community.modularity(network, communities),
               'partition': list(communities)}

    if algorithm_name == 'louvain':
        partition = community_louvain.best_partition(network)
        communities = []
        temp = []
        for j in range(max(partition.values()) + 1):
            for key, value in partition.items():
                if value == j:
                    temp.append(key)
            communities.append(temp.copy())
            temp.clear()
        dic = {'num_partitions': len(communities), 'modularity': community.modularity(network, communities),
               'partition': list(communities)}

    if algorithm_name == 'clique_percolation':
        cliques = list(community.k_clique_communities(network, 3))
        k = [list(x) for x in cliques]
        net_nodes = list(network.nodes)
        for lis in range(len(k) - 1):
            for element in k[lis]:
                for nextlis in range(1, len(k)):
                    if element in k[nextlis]:
                        k[nextlis].remove(element)
        for lis in k:
            for node in net_nodes:
                if node in lis:
                    net_nodes.remove(node)
        for node in net_nodes:
            k.append([node])
        communities = [set(x) for x in k]
        label = nx_comm.label_propagation_communities(network)
        dic = {'num_partitions': len(communities), 'modularity': nx_comm.modularity(network, label),
               'partition': list(communities)}
    return dic


# 1.2 most_valualble_edge
def edge_selector_optimizer(network):
    centrality = edge_betweenness_centrality(network)
    max_cent = max(centrality.values())
    centrality = {e: c / max_cent for e, c in centrality.items()}
    centrality = {e: c + random() for e, c in centrality.items()}
    return max(centrality, key=centrality.get)

'''            2          '''
# 2.1
# noinspection PyUnreachableCode
def construct_heb_edges(files_path, start_date='2019-03-15', end_date='2019-04-15', non_parliamentarians_nodes=0):
    edges_dic = {}
    data = []
    temp = []
    retweets = []  # only retweets
    non_central = {}
    non_nodes_id = []
    central_players = []  # retweets that include only central players
    count = 0
    json_format = 'Hebrew_tweets.json.%Y-%m-%d.txt'
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    csv_file = files_path + '/central_political_players.csv'
    central_political_players = pd.read_csv(csv_file)  # open csv
    for filename in os.listdir(files_path):
        if filename != 'central_political_players.csv' and start_date <= dt.datetime.strptime(filename,
                                                                                              json_format) <= end_date:
            with open(files_path + '/' + filename) as f:
                data.extend(list([json.loads(line) for line in f]))
                # temp= (pd.DataFrame.from_dict(data,orient='columns')) #to dataframe
    players_id = list(central_political_players['id'])
    for tweet in data:
        if tweet["text"][:2] == 'RT':  # only retweets
            retweets.append(tweet)
    for tweet in retweets:
        if tweet['user']['id'] in players_id and tweet['retweeted_status']['user'][
            'id'] in players_id:  # only retweets of central players
            central_players.append(tweet)
    for tweet in central_players:  # {('USER_X_ID','USER_Y_ID'): number of times USER_X_ID retweeted USER_Y_ID)}
        if (tweet['user']['id'], tweet['retweeted_status']['user']['id']) not in edges_dic:
            edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] = 1
        else:
            edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] += 1
    if non_parliamentarians_nodes != 0:  # make non_parliamentarians_nodes
        for tweet in retweets:  # make dict of non central players which are connect to central players
            if tweet['user']['id'] in players_id and tweet['retweeted_status']['user']['id'] not in players_id:
                if (tweet['user']['id'], tweet['retweeted_status']['user']['id']) not in non_central:
                    non_central[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] = 1
                else:
                    non_central[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] += 1
        while count < non_parliamentarians_nodes:  # add to the main dict the max value non parliamentarians nodes
            maximum = max(non_central, key=non_central.get)  # max non user
            if maximum[1] not in non_nodes_id:
                non_nodes_id.append(maximum[1])  # collect the id of the max non nodes
                count += 1
            non_central.pop(maximum)
        l = []
        for tweet in retweets:  # match all the edges for the new nodes
            if (tweet['user']['id'] in players_id and tweet['retweeted_status']['user'][
                'id'] in non_nodes_id):  # append to edge dict
                if (tweet['user']['id'], tweet['retweeted_status']['user']['id']) not in edges_dic:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] = 1
                else:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] += 1
            if tweet['user']['id'] in non_nodes_id and tweet['retweeted_status']['user'][
                'id'] in players_id:
                if (tweet['user']['id'], tweet['retweeted_status']['user']['id']) not in edges_dic:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] = 1
                else:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] += 1
            if tweet['user']['id'] in non_nodes_id and tweet['retweeted_status']['user'][
                'id'] in non_nodes_id:
                if (tweet['user']['id'], tweet['retweeted_status']['user']['id']) not in edges_dic:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] = 1
                else:
                    edges_dic[(tweet['user']['id'], tweet['retweeted_status']['user']['id'])] += 1
    return edges_dic

def construct_heb_network(edges_dict):
    G = nx.DiGraph()
    for key, value in edges_dict.items():
        G.add_edges_from([key], weight=value)
    return G


# if __name__ == "__main__":
#     import matplotlib as mpl
#     import matplotlib.pyplot as plt
#     import time

    #
    #     net = nx.les_miserables_graph()
    #     print("girvin newman", community_detector('girvin_newman', net))
    #     print("girvin newman optimize", community_detector('girvin_newman',net,most_valualble_edge= edge_selector_optimizer))
    #     print("louvain", community_detector('louvain',net))
    #     print("clique percolation", community_detector('clique_percolation',net))
    # central_nodes = construct_heb_edges('hebrew_twitter_data',start_date= '2019-03-15',end_date= '2019-04-15')
    # extra_nodes = construct_heb_edges('hebrew_twitter_data', start_date='2019-03-15', end_date='2019-04-15',non_parliamentarians_nodes= 30)
    # net1 = construct_heb_network(central_nodes)
    # net2 = construct_heb_network(extra_nodes)
    # print("girvin newman", community_detector('girvin_newman', net1))
    # print("girvin newman", community_detector('girvin_newman', net2))
    #
    # pos = nx.layout.spring_layout(net2)
    #
    # node_sizes = [3 + 10 * i for i in range(len(net2))]
    # M = net2.number_of_edges()
    # edge_colors = range(2, M + 2)
    # edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    #
    # nodes = nx.draw_networkx_nodes(net2, pos, node_size=node_sizes, node_color="blue")
    # edges = nx.draw_networkx_edges(
    #     net2,
    #     pos,
    #     node_size=node_sizes,
    #     arrowstyle="->",
    #     arrowsize=10,
    #     edge_color=edge_colors,
    #     edge_cmap=plt.cm.Blues,
    #     width=2,
    #     with_labels= True,
    # )
    # # set alpha value for each edge
    # for i in range(M):
    #     edges[i].set_alpha(edge_alphas[i])
    #
    # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    # pc.set_array(edge_colors)
    # plt.colorbar(pc)
    #
    # ax = plt.gca()
    # ax.set_axis_off()
    # plt.show()

    # start = time.perf_counter()
    # central_political_players = list(pd.read_csv(
    #     'C:/Users/roy1p/Desktop/PycharmProjects/BGU python/social networks analysis/HW2/hebrew_twitter_data/central_political_players.csv')[
    #                                      'id'])
    # girv = "girvin_newman"
    #
    # for x in [0, 20, 40]:
    #     edges_dict = construct_heb_edges(
    #         files_path='C:/Users/roy1p/Desktop/PycharmProjects/BGU python/social networks analysis/HW2/hebrew_twitter_data',
    #         start_date='2019-03-15',
    #         # end_date='2019-01-15',
    #         end_date='2019-04-15',
    #         non_parliamentarians_nodes=x)
    #     graph = construct_heb_network(edges_dict)
    #     graph_central = community_detector(network=graph, algorithm_name=girv)
    #
    #     nodes_list = graph.nodes
    #     count_non_central = 0
    #     for node in nodes_list:
    #         if node not in central_political_players:
    #             count_non_central += 1
    #
    #     output = ""
    #     if x == count_non_central:
    #         output = "GOOD JOB!"
    #     else:
    #         output = 'YOURE NOOB!'
    #
    #     print(
    #         f'girvan_newman non = {x} : {dict([(k, v) for k, v in graph_central.items()][:2])} FOUND {count_non_central} POLITICIANS {output}')
    #
    # # print(f'OMER --- max: len: {len(edges_dict)}, first: {list(edges_dict.items())[0]}')
    # finish = time.perf_counter()
    # print(f'finished in {round(finish - start, 2)} seconds')
