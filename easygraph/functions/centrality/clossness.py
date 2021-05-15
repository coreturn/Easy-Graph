from easygraph.functions.path import *

__all__ = [
    'closeness_centrality',
]

def closeness_centrality_parallel(nodes, G, path_length):
    ret = []
    length = len(G)
    for node in nodes:
        x = path_length(G, node)
        dist = sum(x.values())
        cnt = len(x)
        if dist == 0:
            ret.append([node, 0])
        else:
            ret.append([node, (cnt-1)*(cnt-1)/(dist*(length-1))])
    return ret

def closeness_centrality(G, weight=None):
    '''Compute closeness centrality for nodes.

    .. math::

        C_{WF}(u) = \frac{n-1}{N-1} \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)},
    
    Notice that the closeness distance function computes the 
    outcoming distance to `u` for directed graphs. To use 
    incoming distance, act on `G.reverse()`.

    Parameters
    ----------
    G : graph
      A easygraph graph

    weight : None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    nodes : dictionary
      Dictionary of nodes with closeness centrality as the value.

    '''
    closeness = dict()
    nodes = G.nodes
    length = len(nodes)
    import functools
    if weight is not None:
        path_length = functools.partial(single_source_dijkstra, weight=weight)
    else:
        path_length = functools.partial(single_source_bfs)
    
    if len(G) >= 1000:
        # use parallel version for large graph
        from multiprocessing import Pool
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
        from functools import partial
        import random
        nodes = list(nodes)
        random.shuffle(nodes)

        def split(nodes, n):
            ret = []
            length = len(nodes)  # 总长
            step = int(length / n) + 1  # 每份的长度
            for i in range(0, length, step):
                ret.append(nodes[i:i + step])
            return ret
        
        nodes = split(nodes, 4)
        local_function = partial(closeness_centrality_parallel, G=G, path_length=path_length)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        res = [x for i in ret for x in i]
        closeness = dict(res)
    else:
        # use np-parallel version for samll graph
        for node in nodes:
            x = path_length(G, node)
        dist = sum(x.values())
        cnt = len(x)
        if dist  == 0:
            closeness[node] = 0
        else:
            closeness[node] = (cnt-1)*(cnt-1)/(dist*(length-1))
    return closeness
