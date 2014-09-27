import gengraph as gg

class ListGraph(gg.GenGraph):
    """
    A subclass of GenGraph for graphs given as a list of arrows.
    
    Parameters
    __________
    
    :param list arrows_list: a list of the arrows in the graph; each\
    arrow is an ordered list of 2 vertices (any type) where the first\
    vertex is the tail of the arrow and the second is the head.
    
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
        
        :param vertex vert: the vertex to count the neighbors of
        
        Returns
        _______
        
        :return: the number of out neighbors of *vert*
        :rtype: int
        
        """
        
        return [a[1] for a in self.arrows_list if a[0] == vert]

    def neighbors_in(self, vert):
        """Return the list of in neighbors of vertex *vert*.
        
        Parameters
        __________
        
        :param vertex vert: the vertex to count the neighbors of
        
        Returns
        _______
        
        :return: the number of in neighbors of *vert*
        :rtype: int
        
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

