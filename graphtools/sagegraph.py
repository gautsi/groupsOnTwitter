import gengraph as gg

class SageGraph(gg.GenGraph):
    """
    A subclass of GenGraph which wraps a `Sage DiGraph`_ object.
    
    .. _Sage DiGraph: http://www.sagemath.org/doc/reference/graphs/sage/graphs/digraph.html#sage.graphs.digraph.DiGraph  
    
    Parameters
    __________
    
    :param sage.graphs.digraph.DiGraph dg: the Sage DiGraph to run descent on
    
    """
    
    def __init__(self, dg):
        """Initialize the object."""
        
        gg.GenGraph.__init__(self)
        
        self.dg = dg
        
        self.vert_list = self.get_vert_list()
        
        #The rank dictionary; keys are the vertices
        #and values are the ranks.
        self.rankdict = {vert : 0 for vert in self.vert_list}

        
    def get_num_arrows(self):

        return len(self.dg.edges())

    def get_vert_list(self):

        return self.dg.vertices()        

    def get_rank(self, vert):
        
        return self.rankdict[vert]
    
    def set_rank(self, vert, newrank):
        
        self.rankdict[vert] = newrank
    
    
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):

        num_neighbors = None
        if not cond:
            num_neighbors = self.dg.out_degree(vert) if out else self.dg.in_degree(vert)

        else:
            if less:
                num_neighbors = len([neigh for neigh in self.dg.neighbors_out(vert) if self.get_rank(neigh) <= cutoff])
                
            else:
                num_neighbors = len([neigh for neigh in self.dg.neighbors_in(vert) if self.get_rank(neigh) >= cutoff])
        
        return num_neighbors                

