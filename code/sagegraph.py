import graphtools as gt
import numpy as np

class SageGraph(gt.GenGraph):
    """
    A subclass of GenGraph which wraps a Sage DiGraph object.
    """
    
    def __init__(self, dg):
        """
        Initialize the object.
        
        Parameters:
        ___________
        
        dg: a Sage DiGraph; the graph that this object is wrapping.
        
        """
        gt.GenGraph.__init__(self)
        
        self.dg = dg
        
        self.vertices = self.dg.vertices()
        
        self.rankdict = {vert : 0 for vert in self.vertices}
        """
        The rank dictionary; keys are the vertices 
        and values are the ranks.
        """
        
    def get_num_arrows(self):
        """Return the number of arrows."""
        return len(self.dg.edges())

    def get_rank(self, vert):
        """Return the rank of vertex vert."""
        
        return self.rankdict[vert]
    
    def set_rank(self, vert, newrank):
        self.rankdict[vert] = newrank
    
    
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):
        """
        Return the number of neighbors of a vertex.
        
        Parameters
        __________
        
        vert: a vertex; count this vertex's neighbors
        
        out: a Boolean; if True, count out neighbors, else in
        
        cond: a Boolean; if True, count the neighbors satisfying a condition on rank
        
        less: a Boolean; if True, count the neighbors with rank less than or equal to the cutoff, else more
        
        cutoff: an int; the cutoff rank for the conditional
        
        """
        num_neighbors = None
        if not cond:
            num_neighbors = self.dg.out_degree(vert) if out else self.dg.in_degree(vert)

        else:
            if less:
                num_neighbors = len([neigh for neigh in self.dg.neighbors_out(vert) if self.get_rank(neigh) <= cutoff])
                
            else:
                num_neighbors = len([neigh for neigh in self.dg.neighbors_in(vert) if self.get_rank(neigh) >= cutoff])
        
        return num_neighbors                
                
    def descent(self, num):
        """Run descend num times on random vertices."""
        for __ in xrange(num):
            vert = np.random.choice(self.vertices)
            self.descend(vert)
