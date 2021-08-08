import networkx as nx
import numpy as np


def get_name():
    return "Roy Paz"


def get_id():
    return "208421271"


def epidmeic_analysis(network, model_type='SIS', infection_time=2, p=0.05, epochs=20, seed=208421271):
    np.random.seed(seed)
    infections_total = 0
    infection_current = 0
    mortality_total = 0
    r_0 = 0  # count infections
    k_last = 0
    recover_dict = {}
    temp_net = network.copy()
    # pos = nx.spring_layout(temp_net, k=0.15)  # Seed for reproducible layout
    nodes = list(temp_net.nodes)
    for n in nodes:  # check recover status and append new infected nodes
        if temp_net.nodes[n]['status'] == 'i':  # infected node
            infections_total += 1  # count infections
            recover_dict[n] = infection_time  # new node get X infection_time
    for epoc in range(epochs):
        # color_map = []   #for draw
        # for node in temp_net:
        #     if temp_net.nodes[node]['status'] == 's':
        #         color_map.append('#1B40B6')
        #     else:
        #         color_map.append('#BC092F')
        #     edges = temp_net.edges()
        #     weights = [temp_net[u][v]['contacts'] for u, v in edges]
        # node_position = []
        # node_position_dict = {}
        # nx.draw(temp_net, pos=pos, node_size=50, node_color=color_map, width=np.array(weights) / 11, alpha= 0.9)
        # plt.show()
        for n in nodes:
            if temp_net.nodes[n]['status'] == 'i':  # infected node
                for node_contact in list(temp_net[n]):  # search for his contact nodes
                    if temp_net.nodes[node_contact]['status'] == 's':  # check only healthy friends
                        meetings = temp_net[n][node_contact]['contacts']  # meetings with evey neighber
                        result = np.random.choice(['s', 'i'], meetings, p=[1 - p, p])  # if the meetings was infectet
                        if 'i' in result:  # if the neighber infected
                            temp_net.nodes[node_contact]['status'] = 'i'  # change status to infected
        for n in nodes:  # check the mortality in the network
            if n in recover_dict:
                node_p = temp_net.nodes[n]['mortalitylikelihood']  # the node mortality likelihood
                mortality_result = np.random.choice([0, 1], p=[1 - node_p, node_p])  # 1 for death
                if mortality_result == 1:
                    mortality_total += 1  # count number of death
                    temp_net.remove_node(n)  # if the node is dead, remove from the network
                    del recover_dict[n]
                    nodes.remove(n)  # also remove from the node list
        for n in nodes:  # check recover status and append new infected nodes
            if temp_net.nodes[n]['status'] == 'i':  # infected node
                if n not in recover_dict.keys():
                    infections_total += 1  # count infections
                    recover_dict[n] = infection_time  # new node get X infection_time
                else:
                    recover_dict[n] -= 1  # old node get -1 to the infection_time left
                    if recover_dict[n] == 0:  # the node recovered
                        if model_type == 'SIS':
                            del recover_dict[n]  # the node be able enter again the recover_dict
                            temp_net.nodes[n]['status'] = 's'  # recovering : able to ill again in the next iteration
                        if model_type == 'SIR':  #### SIR MODEL
                            del recover_dict[n]
                            temp_net.remove_node(n)  # if the node is healthy, remove from the network
                            nodes.remove(n)  # also remove from the node list
    infection_current = len(recover_dict)
    r_0 = infection_current / (infections_total * p)
    analysis_dict = {'infections_total': infections_total, 'infection_current': infection_current,
                     'mortality_total': mortality_total, 'r_0': r_0}
    return analysis_dict


def vaccination_analysis(network, model_type='SIR', infection_time=2, p=0.05, epochs=10, seed=208421271, vaccines=1,
                         policy='rand'):
    np.random.seed(seed)
    temp_network2 = network.copy()
    for _ in range(vaccines):
        if policy == 'rand':
            result = np.random.choice(list(temp_network2))  # random nodes to immunize
        if policy == 'betweenness':
            betweenness_dict = nx.betweenness_centrality(temp_network2)  # find max betweenness
            result = max(betweenness_dict, key=betweenness_dict.get)
        if policy == 'degree':
            degree_dict = nx.degree_centrality(temp_network2)  # find max betweenness
            result = max(degree_dict, key=degree_dict.get)
        if policy == 'mortality':
            mortality_dict = dict(temp_network2.nodes('mortalitylikelihood'))
            result = max(mortality_dict, key=mortality_dict.get)
        temp_network2.remove_node(result)  # if the node is vaccinate, remove from the network
    analysis_dict = epidmeic_analysis(temp_network2, model_type=model_type, infection_time=infection_time, p=p,
                                      epochs=epochs, seed=seed)
    return analysis_dict


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from collections import Counter
    B = {'infections_total': 0, 'infection_current': 0, 'mortality_total': 0, 'r_0': 0}
    B = Counter(B)
    A = 0
    a = 0
    iteration = 40
    G1 = nx.read_gml('epidemic1.gml', label='label')
    G2 = nx.read_gml('epidemic2.gml', label='label')
    settings = ['A', 'B', 'C', 'D']
    settings0 = 0
    settings1 = ['A','B']
    settings_2 = ['C','D']
    policies = ['rand', 'betweenness', 'degree', 'mortality']
    models = ['SIS','SIR']
    time = [2,5]
    pro = [0.05,0.1]

    print('\033[1m' + '---Q1---' + '\033[0m')
    for net, ne in zip([G1,G2],['G1','G2']):
        print(f'{ne} Settings:')
        for model in models:
            if model == 'SIR':
                settings0 = settings_2
            if model == 'SIS':
                settings0 = settings1
            for t,setting,p0 in zip(time,settings0,pro):
                for se in range(1, iteration + 1):
                    a = epidmeic_analysis(net, model_type=model, infection_time=t, p=p0, epochs=20, seed=se)
                    A = Counter(a)
                    B.update(A)
                B = dict(B)
                for key in B.keys():
                    B[key] /= iteration
                print(f'{setting}: ', B)
                B = Counter({'infections_total': 0, 'infection_current': 0, 'mortality_total': 0, 'r_0': 0})
        print(' ')

    print('\033[1m' + '---Q2---' + '\033[0m')
    for net, ne in zip([G1,G2],['G1','G2']):
        print(f'{ne} Settings:')
        for pol,setting in zip(policies,settings):
            for se in range(1, iteration + 1):
                a = vaccination_analysis(net, model_type='SIS', infection_time=3, p=0.1, epochs=30, seed=se,
                                           vaccines=20, policy=pol)
                A = Counter(a)
                B.update(A)
            B = dict(B)
            for key in B.keys():
                B[key] /= iteration
            print(f'{setting}: ',B)
            B = Counter({'infections_total': 0, 'infection_current': 0, 'mortality_total': 0, 'r_0': 0})
        print(' ')

