import gengraph as gg

class ListGraph(gg.GenGraph):
    """A subclass of GenGraph for graphs given as a list of arrows."""

    def __init__(self, arrows_list):
        """Initialze the object."""
        
        gg.GenGraph.__init__(self)

        self.arrows_list = arrows_list
        
        self.vert_list = self.get_vert_list()
        
        self.rankdict = {vert : 0 for vert in self.vert_list}
        """
        The rank dictionary; keys are the vertices 
        and values are the ranks.
        """
        
    def get_num_arrows(self):
        
        return len(self.arrows_list)
    
    def get_vert_list(self):

        return list(set([a[0] for a in self.arrows_list] + [a[1] for a in self.arrows_list]))


    def get_rank(self, vert):

        return self.rankdict[vert]

    def set_rank(self, vert, newrank):
        
        self.rankdict[vert] = newrank
        
    def neighbors_out(self, vert):
        """return the list of out neighbors of vertex vert."""
        
        return [a[1] for a in self.arrows_list if a[0] == vert]

    def neighbors_in(self, vert):
        """return the list of in neighbors of vertex vert."""
        
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

