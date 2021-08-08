import networkx as nx


def get_name():
    return "Roy Paz"


def get_id():
    return "208421271"


def centrality_measures(network, node, iterations= 100):  # calculate the centrality measures for a specific node
    dict = {}
    dict['dc'] = nx.degree_centrality(network)[node]
    dict['cs'] = nx.closeness_centrality(network, u= node)
    dict['nbc'] = nx.betweenness_centrality(network)[node]
    dict['pr'] = nx.pagerank(network, max_iter= iterations)[node]  # use the default 0.85 dumping factor.
    h, auth = nx.hits(network, max_iter= iterations)
    dict['auth'] = auth[node]
    return dict  # {'dc': , 'cs': , 'nbc': , 'pr': , 'auth': }


def single_step_voucher(network):  # selects the best candidate for the voucher (one step)
    centrality = nx.degree_centrality(network)
    node = max(centrality, key=centrality.get)
    return node


def multiple_step_voucher(network):  # selects the best candidate for the voucher (unlimited steps, as fast as we can)
    centrality = nx.closeness_centrality(network)
    node = max(centrality, key=centrality.get)
    return node


# selects the best candidate for the voucher (unlimited steps, as fast as we can), voucher diminished by 2.5% every step and limited to 4 steps
def multiple_steps_diminished_voucher(network):
    node = generic_multiple_steps_diminished_voucher(network)
    return node


def find_most_valuable(network):
    betweenness = nx.betweenness_centrality(network)  # find max betweenness
    node = max(betweenness, key=betweenness.get)
    return node

def generic_multiple_steps_diminished_voucher(network, max_steps= 4, r= 2.5):
    nodes = list(network.nodes)  #nodes list
    nodes_profit = {}
    for n in nodes:
        profit = 0      # count the profit for each step
        node_path = nx.shortest_path(network, n)  # all the pathes of each node
        for step in range(1,max_steps+1):
            for path in node_path.values():
                if len(path) == step+1:     # if path in the same step
                    rate = ((100 - r)/100) ** step
                    profit += rate   # calculate the voucher profit for each path (10-r)/100) ** step
        nodes_profit[n] = profit                 # add the profit to a node: profit dict
    node = max(nodes_profit, key=nodes_profit.get)
    return node


if __name__ == "__main__":
    G1 = nx.read_gml('friendships.gml.txt', label='label')
    print('node 1:', centrality_measures(G1, 1))
    print('node 50:', centrality_measures(G1, 50))
    print('node 100:', centrality_measures(G1, 100))
    print('The node who gets the single step voucher:', single_step_voucher(G1)) #105
    print('The node who gets the multiple step voucher:', multiple_step_voucher(G1)) #23
    print('The node who gets the multiple steps diminished voucher:', multiple_steps_diminished_voucher(G1)) #23
    print('The most valuable node:', find_most_valuable(G1)) #333
    print('',generic_multiple_steps_diminished_voucher(G1,10,7))