def  laplacian(G):
    """Returns the laplacian centrality of each node in the weighted graph

    Parameters
    ---------- 
    G : graph
        weighted graph
    
    Returns
    -------
    CL : dict
        the laplacian centrality of each node in the weighted graph

    Examples
    --------
    Returns the laplacian centrality of each node in the weighted graph G

    >>> laplacian(G)

    Reference
    ---------
    .. [1] Xingqin Qi, Eddie Fuller, Qin Wu, Yezhou Wu, Cun-Quan Zhang. 
    "Laplacian centrality: A new centrality measure for weighted networks." 
    Information Sciences, Volume 194, Pages 240-253, 2012.

    """
<<<<<<< HEAD
<<<<<<< HEAD
    adj=G.adj
    X={}
    W={}
    CL={}
    Xi={}
    for i in G:
        X[i]=0
        W[i]=0
        CL[i]=0
        Xi[i]=0
=======
    adj = G.adj
    from collections import defaultdict
    X=defaultdict(int)
    W = defaultdict(int)
    CL = {}
    
    print("-------pool-----------")
    from multiprocessing import Pool
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    from functools import partial
    import random
    nodes = list(G.nodes)
    random.shuffle(nodes)
    def split(nodes, n):
        ret = []
        length = len(nodes)  # 总长
        step = int(length / n) + 1  # 每份的长度
        for i in range(0, length, step):
            ret.append(nodes[i:i + step])
        return ret
    nodes = split(nodes, 4)

    local_function = partial(initialize_parallel, G=G, adj=adj)
    with Pool(4) as p:
        ret = p.map(local_function, nodes)
    res = [x[0] for i in ret for x in i]
    X = dict(res)
    res = [x[1] for i in ret for x in i]
    W = dict(res)
    ELG=sum(X[i]*X[i] for i in G)+sum(W[i] for i in G)

    local_function = partial(laplacian_parallel, G=G, X=X, W=W, adj=adj, ELG=ELG)
    with Pool(4) as p:
        ret = p.map(local_function, nodes)
    res = [x for i in ret for x in i]
    CL = dict(res)
    """
    print("-------no-parallel-----------")
>>>>>>> 17dcc1e... parallel_partial
    for i in G:
        for j in G:
            if i in G and j in G[i]:
                X[i]+=adj[i][j].get('weight', 1)
                W[i]+=adj[i][j].get('weight', 1)*adj[i][j].get('weight', 1)
    ELG=sum(X[i]*X[i] for i in G)+sum(W[i] for i in G)
    for i in G:
        import copy
        Xi=copy.deepcopy(X)
        for j in G:
            if j in adj.keys() and i in adj[j].keys():
                Xi[j]-=adj[j][i].get('weight', 1)
        Xi[i]=0
        ELGi=sum(Xi[i]*Xi[i] for i in G)+sum(W[i] for i in G)-2*W[i]
        if ELG:
            CL[i]=(float)(ELG-ELGi)/ELG
<<<<<<< HEAD
    return CL
=======
    adj = G.adj
    from collections import defaultdict
    X=defaultdict(int)
    W = defaultdict(int)
    CL = {}

    if len(G) >= 1000:
        # use the parallel version for large graph 
        from multiprocessing import Pool
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
        from functools import partial
        import random
        nodes = list(G.nodes)
        random.shuffle(nodes)

        def split(nodes, n):
            ret = []
            length = len(nodes)  # 总长
            step = int(length / n) + 1  # 每份的长度
            for i in range(0, length, step):
                ret.append(nodes[i:i + step])
            return ret
        nodes = split(nodes, 4)

        local_function = partial(initialize_parallel, G=G, adj=adj)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        res = [x[0] for i in ret for x in i]
        X = dict(res)
        res = [x[1] for i in ret for x in i]
        W = dict(res)
        ELG=sum(X[i]*X[i] for i in G)+sum(W[i] for i in G)

        local_function = partial(laplacian_parallel, G=G, X=X, W=W, adj=adj, ELG=ELG)
        with Pool(4) as p:
            ret = p.map(local_function, nodes)
        res = [x for i in ret for x in i]
        CL = dict(res)
    
    else:
        # use np-parallel version for small graph
        for i in G:
            for j in G:
                if i in G and j in G[i]:
                    X[i]+=adj[i][j].get('weight', 1)
                    W[i]+=adj[i][j].get('weight', 1)*adj[i][j].get('weight', 1)
        ELG=sum(X[i]*X[i] for i in G)+sum(W[i] for i in G)
        for i in G:
            import copy
            Xi=copy.deepcopy(X)
            for j in G:
                if j in adj.keys() and i in adj[j].keys():
                    Xi[j]-=adj[j][i].get('weight', 1)
            Xi[i]=0
            ELGi=sum(Xi[i]*Xi[i] for i in G)+sum(W[i] for i in G)-2*W[i]
            if ELG:
                CL[i]=(float)(ELG-ELGi)/ELG
    return CL

def initialize_parallel(nodes, G, adj):
=======
    """
    return CL


def initialize_parallel(nodes, G, adj):
    import time, os
    print('Run initial %s (%s)...' % (len(nodes), os.getpid()))
    start = time.time()
>>>>>>> 17dcc1e... parallel_partial
    ret = []
    for i in nodes:
        X = 0
        W = 0
        for j in G:
            if j in G[i]:
                X+=adj[i][j].get('weight', 1)
                W+=adj[i][j].get('weight', 1)*adj[i][j].get('weight', 1)
        ret.append([[i, X], [i, W]])
<<<<<<< HEAD
    return ret

def laplacian_parallel(nodes, G, X, W, adj, ELG):
=======
    end = time.time()
    print('Task %s finish %0.2f seconds.' % (len(nodes), (end - start)))
    return ret

def laplacian_parallel(nodes, G, X, W, adj, ELG):
    import time, os
    print('Run task %s (%s)...' % (len(nodes), os.getpid()))
    start = time.time()
>>>>>>> 17dcc1e... parallel_partial
    ret = []
    for i in nodes:
        import copy
        Xi=copy.deepcopy(X)
        for j in G:
            if j in adj.keys() and i in adj[j].keys():
                Xi[j]-=adj[j][i].get('weight', 1)
        Xi[i]=0
        ELGi=sum(Xi[i]*Xi[i] for i in G)+sum(W[i] for i in G)-2*W[i]
        if ELG:
            ret.append([i, (float)(ELG-ELGi)/ELG])
<<<<<<< HEAD
=======
    end = time.time()
    print('Task %s finish %0.2f seconds.' % (len(nodes), (end - start)))
>>>>>>> 17dcc1e... parallel_partial
    return ret

def sort(data):
    return dict(sorted(data.items(), key = lambda x: x[0], reverse = True))

def output(data, path):
    import json
    data = sort(data)
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    with open(path, 'w', encoding='utf-8') as json_file:
<<<<<<< HEAD
        json_file.write(json_str)
>>>>>>> 880991f... parallel_almost
=======
        json_file.write(json_str)
>>>>>>> 17dcc1e... parallel_partial
