import sys
sys.path.append('../../../')
import easygraph as eg
import math

__all__ = [
    'effective_size',
    'efficiency',
    'constraint',
    'hierarchy'
]

def mutual_weight(G, u, v, weight=None):
    try:
        a_uv = G[u][v].get(weight, 1)
    except KeyError:
        a_uv = 0
    try:
        a_vu = G[v][u].get(weight, 1)
    except KeyError:
        a_vu = 0
    return a_uv + a_vu

sum_nmw_rec = {}
max_nmw_rec = {}

def normalized_mutual_weight(G, u, v, norm=sum, weight=None):
    if norm == sum:
        try:
            # res = sum_nmw_rec[(u, v)]
            # print('yes')
            return sum_nmw_rec[(u, v)]
        except KeyError:
            scale = norm(mutual_weight(G, u, w, weight)
                    for w in G.all_neighbors(u))
            nmw = 0 if scale == 0 else mutual_weight(G, u, v, weight) / scale
            sum_nmw_rec[(u,v)] = nmw
            return nmw
    elif norm == max:
        try:
            return max_nmw_rec[(u, v)]
        except KeyError:
            scale = norm(mutual_weight(G, u, w, weight)
                    for w in G.all_neighbors(u))
            nmw = 0 if scale == 0 else mutual_weight(G, u, v, weight) / scale
            max_nmw_rec[(u,v)] = nmw
            return nmw

<<<<<<< HEAD
<<<<<<< HEAD
=======
def effective_size_parallel(nodes, G, weight):
=======
def effective_size_parallel(nodes, G, weight):
    import time, os
    #print('Run task %s (%s)...' % (len(nodes), os.getpid()))
    start = time.time()
>>>>>>> 17dcc1e... parallel_partial
    ret = []
    for node in nodes:
        neighbors_of_node = set(G.all_neighbors(node))
        if len(neighbors_of_node) == 0:
            ret.append([node, float('nan')])
            continue
        ret.append([node, sum(redundancy(G, node, u, weight)
                                for u in neighbors_of_node)])
<<<<<<< HEAD
=======
    end = time.time()
    #print('Task %s finish %0.2f seconds.' % (len(nodes), (end - start)))
>>>>>>> 17dcc1e... parallel_partial
    return ret

def split(nodes, n):
    ret = []
    length = len(nodes)  # 总长
    step = int(length / n) + 1  # 每份的长度
    for i in range(0, length, step):
        ret.append(nodes[i:i + step])
    return ret

def redundancy(G, u, v, weight=None):
    nmw = normalized_mutual_weight
    r = sum(nmw(G, u, w, weight=weight) * nmw(G, v, w, norm=max, weight=weight)
            for w in set(G.all_neighbors(u)))
    return 1 - r
<<<<<<< HEAD
>>>>>>> 880991f... parallel_almost

def effective_size(G, nodes=None, weight=None, n_workers=None):
=======

def effective_size(G, nodes=None, weight=None):
>>>>>>> 17dcc1e... parallel_partial
    """Burt's metric - Effective Size.

    Parameters
    ----------
    G : easygraph.Graph

    nodes : list of nodes or None, optional (default : None)
        The nodes you want to calculate. If *None*, all nodes in `G` will be calculated.

    weight : string or None, optional (default : None)
        The key for edge weight. If *None*, `G` will be regarded as unweighted graph.

    Returns
    -------
    effective_size : dict
        The Effective Size of node in `nodes`.

    Examples
    --------

    >>> effective_size(G,
    ...                nodes=[1,2,3], # Compute the Effective Size of some nodes. The default is None for all nodes in G.
    ...                weight='weight' # The weight key of the graph. The default is None for unweighted graph.
    ...                )

    References
    ----------
    .. [1] Burt R S. Structural holes: The social structure of competition[M]. 
       Harvard university press, 2009.

    """
    sum_nmw_rec.clear()
    max_nmw_rec.clear()
    effective_size = {}
    if nodes is None:
        nodes = G
    # Use Borgatti's simplified formula for unweighted and undirected graphs
    if not G.is_directed() and weight is None:
        for v in nodes:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            E = G.ego_subgraph(v)
            if len(E)>1:
                effective_size[v] = len(E) - 1 - (2 * E.size()) / (len(E) - 1)
            else:
                effective_size[v]=0    
    else:
<<<<<<< HEAD
<<<<<<< HEAD
        for v in nodes:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            effective_size[v] = sum(redundancy(G, v, u, weight)
                                    for u in set(G.all_neighbors(v)))
=======
        
        if n_workers is not None:
            from multiprocessing import Pool
            from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
            from functools import partial
            import random
            nodes = list(nodes)
            random.shuffle(nodes)
            nodes = split(nodes, 4)
            local_function = partial(effective_size_parallel, G=G, weight=weight)
            with Pool(4) as p:
                ret = p.map(local_function, nodes)
            res = [x for i in ret for x in i]
            effective_size = dict(res)
        else:
            for v in nodes:
                # Effective size is not defined for isolated nodes
                if len(G[v]) == 0:
                    effective_size[v] = float('nan')
                    continue
                effective_size[v] = sum(redundancy(G, v, u, weight)
                                        for u in set(G.all_neighbors(v)))
>>>>>>> 880991f... parallel_almost
=======
        import time
        start = time.time()

        print("-------pool-----------")
        from multiprocessing import Pool
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
        from functools import partial
        import random
        nodes = list(nodes)
        random.shuffle(nodes)
        nodes = split(nodes, 4)
        local_function = partial(effective_size_parallel, G=G, weight=weight)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        res = [x for i in ret for x in i]
        effective_size = dict(res)

        # print("--------parallel-------")
        # from joblib import Parallel, delayed
        # from functools import partial
        # local_function = partial(effective_size_parallel, G=G, weight=weight)
        # res = Parallel(n_jobs=4)(delayed(local_function)([v]) for v in nodes)
        # effective_size = dict(res)

        # print("--------non parallel-------")
        # for v in nodes:
        #     # Effective size is not defined for isolated nodes
        #     if len(G[v]) == 0:
        #         effective_size[v] = float('nan')
        #         continue
        #     effective_size[v] = sum(redundancy(G, v, u, weight)
        #                             for u in set(G.all_neighbors(v)))
        
        end = time.time()
        print("use: ", end-start)
>>>>>>> 17dcc1e... parallel_partial
    return effective_size

def efficiency(G, nodes=None, weight=None):
    """Burt's metric - Efficiency.

    Parameters
    ----------
    G : easygraph.Graph

    nodes : list of nodes or None, optional (default : None)
        The nodes you want to calculate. If *None*, all nodes in `G` will be calculated.

    weight : string or None, optional (default : None)
        The key for edge weight. If *None*, `G` will be regarded as unweighted graph.

    Returns
    -------
    efficiency : dict
        The Efficiency of node in `nodes`.

    Examples
    --------

    >>> efficiency(G,
    ...            nodes=[1,2,3], # Compute the Efficiency of some nodes. The default is None for all nodes in G.
    ...            weight='weight' # The weight key of the graph. The default is None for unweighted graph.
    ...            )

    References
    ----------
    .. [1] Burt R S. Structural holes: The social structure of competition[M]. 
       Harvard university press, 2009.

    """
    e_size = effective_size(G=G, nodes=nodes, weight=weight)
    degree = G.degree(weight=weight)
    efficiency = {n: v / degree[n] for n, v in e_size.items()}
    return efficiency

<<<<<<< HEAD
<<<<<<< HEAD
=======
def compute_constraint_of_nodes(nodes, G, weight):
=======
def compute_constraint_of_nodes(nodes, G, weight):
    import time, os
    print('Run task %s (%s)...' % (len(nodes), os.getpid()))
    start = time.time()
>>>>>>> 17dcc1e... parallel_partial
    ret = []
    for node in nodes:
        neighbors_of_node = set(G.all_neighbors(node))
        if len(neighbors_of_node) == 0:
            ret.append([node, float('nan')])
            continue
        ret.append([node, sum(local_constraint(G, node, u, weight)
                                for u in neighbors_of_node)])
<<<<<<< HEAD
    return ret
>>>>>>> 880991f... parallel_almost
=======
    end = time.time()
    print('Task %s finish %0.2f seconds.' % (len(nodes), (end - start)))
    return ret
>>>>>>> 17dcc1e... parallel_partial

def constraint(G, nodes=None, weight=None, n_workers=None):
    """Burt's metric - Constraint.

    Parameters
    ----------
    G : easygraph.Graph

    nodes : list of nodes or None, optional (default : None)
        The nodes you want to calculate. If *None*, all nodes in `G` will be calculated.

    weight : string or None, optional (default : None)
        The key for edge weight. If *None*, `G` will be regarded as unweighted graph.

    workers : int or None, optional (default : None)
        The number of workers calculating (default: None). 
        None if not using only one worker.

    Returns
    -------
    constraint : dict
        The Constraint of node in `nodes`.

    Examples
    --------

    >>> constraint(G,
    ...            nodes=[1,2,3], # Compute the Constraint of some nodes. The default is None for all nodes in G.
    ...            weight='weight', # The weight key of the graph. The default is None for unweighted graph.
    ...            n_workers=4 # Parallel computing on four workers. The default is None for serial computing.
    ...            )

    References
    ----------
    .. [1] Burt R S. Structural holes: The social structure of competition[M]. 
       Harvard university press, 2009.

    """
    sum_nmw_rec.clear()
    max_nmw_rec.clear()
    local_constraint_rec.clear()
    if nodes is None:
        nodes = G.nodes
    constraint = {}

    def compute_constraint_of_v(v):
        neighbors_of_v = set(G.all_neighbors(v))
        if len(neighbors_of_v) == 0:
            constraint_of_v = float('nan')
        else:
            constraint_of_v = sum(local_constraint(G, v, n, weight)
                                for n in neighbors_of_v)
        return v, constraint_of_v

<<<<<<< HEAD
<<<<<<< HEAD
=======
    import time
    start = time.time()

>>>>>>> 17dcc1e... parallel_partial
    if n_workers is None:
        print("------noparallel------")
        constraint_results = []
        for v in nodes:
            constraint_results.append(compute_constraint_of_v(v))
    else:
<<<<<<< HEAD
        from joblib import Parallel, delayed
        constraint_results = Parallel(n_jobs=n_workers)(delayed(compute_constraint_of_v)(v) for v in nodes)
    for v, constraint_of_v in constraint_results:
        constraint[v] = constraint_of_v
=======
    if n_workers is not None:
=======
        print("-------pool-----------")
>>>>>>> 17dcc1e... parallel_partial
        from multiprocessing import Pool
        from functools import partial
        import random
        local_function = partial(compute_constraint_of_nodes, G=G, weight=weight)
        nodes = list(nodes)
        random.shuffle(nodes)
        nodes = split(nodes, 4)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        constraint_results = [x for i in ret for x in i]
<<<<<<< HEAD
    else:
        constraint_results = []
        for v in nodes:
            constraint_results.append(compute_constraint_of_v(v))

    constraint = dict(constraint_results)
>>>>>>> 880991f... parallel_almost
=======

        # print("-------parallel-----------")
        # from joblib import Parallel, delayed
        # constraint_results = Parallel(n_jobs=n_workers)(delayed(compute_constraint_of_v)(v) for v in nodes)
    
    end = time.time()
    print("use: ", end - start)
    constraint = dict(constraint_results)
>>>>>>> 17dcc1e... parallel_partial
    return constraint

local_constraint_rec = {}
def local_constraint(G, u, v, weight=None):
    try:
        return local_constraint_rec[(u, v)]
    except KeyError:
        nmw = normalized_mutual_weight
        direct = nmw(G, u, v, weight=weight)
        indirect = sum(nmw(G, u, w, weight=weight) * nmw(G, w, v, weight=weight)
                    for w in set(G.all_neighbors(u)))
        result = (direct + indirect) ** 2
        local_constraint_rec[(u, v)] = result
        return result

<<<<<<< HEAD
<<<<<<< HEAD
=======
def hierarchy_parallel(G, nodes):
    import time, os
    print('Run task %s (%s)...' % (len(nodes), os.getpid()))
    start = time.time()
    ret = []
    for v in nodes:
        E = G.ego_subgraph(v)
        n=len(E)-1
        C=0
        c={}
        neighbors_of_v = set(G.all_neighbors(v))
        for w in neighbors_of_v:
            C+=local_constraint(G,v,w)
            c[w]=local_constraint(G,v,w)
        if n > 1:
            ret.append([v, sum(c[w]/C*n*math.log(c[w]/C*n)/(n*math.log(n)) for w in neighbors_of_v)])
    end = time.time()
    print('Task %s finish %0.2f seconds.' % (len(nodes), (end - start)))
    return ret

>>>>>>> 17dcc1e... parallel_partial
def hierarchy(G,nodes=None,weight=None):
=======
def hierarchy_parallel(nodes, G):

    ret = []
    for v in nodes:
        E = G.ego_subgraph(v)
        n=len(E)-1
        C=0
        c={}
        neighbors_of_v = set(G.all_neighbors(v))
        for w in neighbors_of_v:
            C+=local_constraint(G,v,w)
            c[w]=local_constraint(G,v,w)
        if n > 1:
            ret.append([v, sum(c[w] / C * n * math.log(c[w] / C * n) / (n * math.log(n)) for w in neighbors_of_v)])

    return ret

def hierarchy(G,nodes=None,weight=None,n_workers=None):
>>>>>>> 880991f... parallel_almost
    """Returns the hierarchy of nodes in the graph

    Parameters
    ---------- 
    G : graph
    nodes :  dict, optional (default: None)
    weight : dict, optional (default: None)

    Returns
    -------
    hierarchy : dict
        the hierarchy of nodes in the graph

    Examples
    --------
    Returns the hierarchy of nodes in the graph G

    >>> hierarchy(G)

    Reference
    ---------
    https://m.book118.com/html/2019/0318/5320024122002021.shtm

    """
    if nodes is None:
        nodes = G.nodes
    hierarchy = {}
<<<<<<< HEAD
<<<<<<< HEAD
    con=constraint(G)
    for v in G.nodes:
        E = G.ego_subgraph(v)
        n=len(E)-1
        C=0
        c={}
        neighbors_of_v = set(G.all_neighbors(v))
        for w in neighbors_of_v:
            C+=local_constraint(G,v,w)
            c[w]=local_constraint(G,v,w)
        if n>1:
            hierarchy[v]=sum(c[w]/C*n*math.log(c[w]/C*n)/(n*math.log(n)) for w in neighbors_of_v)
=======

    if n_workers is not None:
        from multiprocessing import Pool
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
        from functools import partial
        import random
        nodes = list(nodes)
        random.shuffle(nodes)
        nodes = split(nodes, 4)
        local_function = partial(hierarchy_parallel, G=G)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        res = [x for i in ret for x in i]
        hierarchy = dict(res)
    else:
        for v in G.nodes:
            E = G.ego_subgraph(v)
            n=len(E)-1
            C=0
            c={}
            neighbors_of_v = set(G.all_neighbors(v))
            for w in neighbors_of_v:
                C+=local_constraint(G,v,w)
                c[w]=local_constraint(G,v,w)
            if n>1:
                hierarchy[v]=sum(c[w]/C*n*math.log(c[w]/C*n)/(n*math.log(n)) for w in neighbors_of_v)

>>>>>>> 880991f... parallel_almost
=======

    print("-------pool-----------")
    from multiprocessing import Pool
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    from functools import partial
    import random
    nodes = list(nodes)
    random.shuffle(nodes)
    nodes = split(nodes, 4)
    local_function = partial(hierarchy_parallel, G=G)
    with Pool(4) as p:
        ret = p.map(local_function, nodes)
    res = [x for i in ret for x in i]
    hierarchy = dict(res)

>>>>>>> 17dcc1e... parallel_partial
    return hierarchy

