import networkx as nx
import pickle
import numpy as np
import powerlaw  # Power laws are probability distributions with the form:p(x)∝x−α
from scipy.stats import binom_test
import statsmodels.api as sm
import pylab as py


def get_name():
    return "Roy Paz"


def get_id():
    return "208421271"


# 1.1
def random_networks_generator(n, p, directed, num_networks, seed=208421271):
    networks_l = []
    seed = np.random.RandomState(seed)
    for i in range(num_networks):
        G = nx.fast_gnp_random_graph(n, p, seed, directed)
        networks_l.append(G)
    return networks_l


# network_l = random_networks_generator(100, 0.6, False, 10)


# 1.2
def network_stats(G):
    stats = {}
    stats['degrees_avg'] = len(nx.edges(G)) / (2 * len(nx.nodes(G)))
    stats['degrees_std'] = np.std(G)
    degree_l = []
    for i in G.degree():
        degree_l.append(i[1])
    stats['degrees_max'] = float(max(degree_l))
    stats['degrees_min'] = float(min(degree_l))
    if not nx.is_connected(G):
        cc = G.subgraph(max(nx.connected_components(G), key=len))
        stats['spl'] = nx.average_shortest_path_length(cc)
        stats['diameter'] = float(nx.diameter(cc))
    else:
        stats['spl'] = nx.average_shortest_path_length(G)
        stats['diameter'] = float(nx.diameter(G))
    return stats


# 1.3
def networks_avg_stats(networks_l):
    degrees_avg = []
    degrees_std = []
    degrees_max = []
    degrees_min = []
    diameter = []
    spl = []
    nets_stats = []
    for i in range(len(networks_l)):
        nets_stats.append(network_stats(networks_l[i]))
    for i in nets_stats:
        degrees_avg.append(i["degrees_avg"])
        degrees_std.append(i["degrees_std"])
        degrees_max.append(i["degrees_max"])
        degrees_min.append(i["degrees_min"])
        diameter.append(i["spl"])
        spl.append(i["diameter"])
    av_nets_stats = {'degrees_avg': np.mean(degrees_avg), 'degrees_std': np.mean(degrees_std),
                     'degrees_max': np.mean(degrees_max), 'degrees_min': np.mean(degrees_min),
                     'spl': np.mean(spl), 'diameter': np.mean(diameter)}
    return av_nets_stats


# print(networks_avg_stats(network_l))


# 1.5
# a = random_networks_generator(100, 0.1, False, 20)
# b = random_networks_generator(100, 0.6, False, 20)
# c = random_networks_generator(1000, 0.1, False, 10)
# d = random_networks_generator(1000, 0.6, False, 10)
# gnp_nets = [a,b,c,d]
#
# for i in gnp_nets:
#     print(networks_avg_stats(i))


# 2
infile = open('rand_nets.p', 'rb')
rand_net = pickle.load(infile)
infile.close()


def rand_net_hypothesis_testing(network, theoretical_p, alpha=0.05):
    links = network.number_of_nodes() * theoretical_p
    nodes = network.number_of_nodes()
    probability = 2 * nx.number_of_edges(network) / (nodes * (nodes - 1))
    p_value = binom_test(x=links, n=nodes, p=probability, alternative='two-sided')
    if p_value <= alpha:
        return (p_value, 'reject')
    else:
        return (p_value, 'accept')


# print(rand_net_hypothesis_testing(rand_net[0], 0.6))

# 2.3

def most_probable_p(network):
    p_options = [0.01, 0.1, 0.3, 0.6]
    for i in p_options:
        result = rand_net_hypothesis_testing(network, i)[1]
        if result == 'accept':
            return i
    return -1


test = np.random.normal(network_stats(rand_net[0])['degrees_avg'],network_stats(rand_net[0])['degrees_std'], 30)
sm.qqplot(test, line= '45')
py.show()

# p = most_probable_p(rand_net[0])
# print(rand_net_hypothesis_testing(rand_net[0], p))

# 3
infile = open('scalefree_nets.p', 'rb')
scalefree_nets = pickle.load(infile)
infile.close()


def find_opt_gamma(network, treat_as_social_network=True):
    degrees = []
    for i in network.degree():
        degrees.append(i[1])
    fit = powerlaw.Fit(degrees, discrete=treat_as_social_network)
    return fit.power_law.alpha


# network_gammas = []
# for i in range(len(scalefree_nets)):
#     network_gammas.append(find_opt_gamma(scalefree_nets[i]))
# print(network_gammas)

# print(network_stats(scalefree_nets[0]))

# 4
infile = open('multigraph_scalefree_nets.p', 'rb')
multigraph_scalefree_nets = pickle.load(infile)
infile.close()


def network_classifier(network):
    epsilon = 0.8
    n = network.number_of_nodes()
    edges = network.number_of_edges()
    deg = []
    for i in network.degree():
        deg.append(i[1])
    # p = most_probable_p(network) #2 * nx.number_of_edges(network) / (n * (n - 1))
    full_rand_g = nx.gnm_random_graph(n, edges)
    d_preserving = nx.expected_degree_graph(deg)
    av_dis = network_stats(network)["spl"]
    av_dis_full_rand = network_stats(full_rand_g)["spl"]
    av_dis_d_pres = network_stats(d_preserving)["spl"]
    if av_dis < av_dis_full_rand and abs(av_dis_d_pres - av_dis) <= epsilon:
        return 2
    else:
        return 1

# for i in range(len(multigraph_scalefree_nets)):
#     print(network_classifier(multigraph_scalefree_nets[i]))
#

#
# for i in range(len(rand_net)):
#     print(network_classifier(rand_net[i]))
# for i in range(len(scalefree_nets)):
#     print(network_classifier(scalefree_nets[i]))
