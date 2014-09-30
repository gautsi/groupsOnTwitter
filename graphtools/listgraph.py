import gengraph as gg

class ListGraph(gg.GenGraph):
    """
    A subclass of GenGraph for graphs given as a list of arrows.
    
    Parameters
    __________
    
    :param list arrows_list: a list of the arrows in the graph; each\
    arrow is an ordered list of 2 vertices (any type) where the first\
    vertex is the tail of the arrow and the second is the head.
    
    We use the following simple example throughout.
    
    >>> from graphtools.listgraph import ListGraph
    >>> graph = ListGraph([['a', 'b'], ['b', 'c']])
    >>> print graph.get_num_arrows()
    2
    >>> set(graph.get_vert_list()) == set(['a', 'b', 'c'])
    True
    >>> print graph.get_rank('a')
    0
    >>> graph.set_rank('b',2)
    >>> graph.get_rank('b')
    2
    >>> graph.reset_ranks()
    >>> graph.descend('a')
    >>> graph.descent(20)
    >>> hl = graph.hierarchy_list #get the list of hierarchy scores
    >>> print len(hl) #descend has been run 21 times, plus the initial score
    22
    >>> print hl[0] #the first score is always 0
    0
    >>> print hl[-1] #the score after 21 descends will probably be 1.0
    1.0
    
    Graphs with isolated vertices (vertices with no neighbors) are not\
    supported. Isolated vertices don't affect the hierarchy of the graph.  
    
    """

    def __init__(self, arrows_list):
        """Initialze the object."""
        
        gg.GenGraph.__init__(self)

        self.arrows_list = arrows_list
        
        self.vert_list = self.get_vert_list()
        
        #The rank dictionary; keys are the vertices 
        #and values are the ranks.
        self.rankdict = {vert : 0 for vert in self.vert_list}

        
    def get_num_arrows(self):
        
        return len(self.arrows_list)
    
    def get_vert_list(self):

        return list(set([a[0] for a in self.arrows_list] + [a[1] for a in self.arrows_list]))


    def get_rank(self, vert):

        return self.rankdict[vert]

    def set_rank(self, vert, newrank):
        
        self.rankdict[vert] = newrank
        
    def neighbors_out(self, vert):
        """Return the list of out neighbors of vertex *vert*.
        
        Parameters
        __________
        
        :param vertextype vert: the vertex to get the neighbors of
        
        Returns
        _______
        
        :return: the list of out neighbors of *vert*
        :rtype: list
        
        For example,
        
        >>> graph.neighbors_out('a')
        ['b']
        >>> graph.neighbors_out('c')
        []
            
        """
        
        return [a[1] for a in self.arrows_list if a[0] == vert]

    def neighbors_in(self, vert):
        """Return the list of in neighbors of vertex *vert*.
        
        Parameters
        __________
        
        :param vertextype vert: the vertex to get the neighbors of
        
        Returns
        _______
        
        :return: the list of in neighbors of *vert*
        :rtype: list
        
        For example,
        
        >>> graph.neighbors_in('a')
        []
        >>> graph.neighbors_in('c')
        ['b']

        """

        
        return [a[0] for a in self.arrows_list if a[1] == vert]

        
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):
 
        num_neighbors = None
        if not cond:
            num_neighbors = len(self.neighbors_out(vert)) if out else len(self.neighbors_in(vert))

        else:
            if less:
                num_neighbors = len([neigh for neigh in self.neighbors_out(vert) if self.get_rank(neigh) <= cutoff])
                
            else:
                num_neighbors = len([neigh for neigh in self.neighbors_in(vert) if self.get_rank(neigh) >= cutoff])
        
        return num_neighbors                

