# -*- coding: utf-8 -*-
import numpy as np

class GenGraph:
    """A general graph."""

    def __init__(self):
        """Initialze the object."""

        self.num_arrows = None
        
        self.vert_list = None
        
        self.hierarchy_list = [0]
        
        self.passes = 0

    def get_num_arrows(self):
        """Return the number of arrows."""
        
        pass
        
    def get_vert_list(self):
        """Return a list of vertices."""

        pass

    def get_rank(self, vert):
        """Return the rank of vertex vert."""

        pass

    def set_rank(self, vert, newrank):
        """Set the rank of vertex vert to int newrank."""
        
        pass

        
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):
        """
        Count the number of neighbors of a vertex.
        
        :param vert: the vertex to count the neighbors of 
        :type vert: vertex
        
        :param out: if True, count out neighbors, else in
        :type out: Boolean
                
        :param cond: if True, count the neighbors satisfying a condition on rank
        :type cond: Boolean
        
        :param less: if True, count the neighbors with rank less than or equal to the cutoff, else more
        :type less: Boolean
        
        :param cutoff: the cutoff rank for the conditional
        :type cutoff: int
        
        """
 
        pass
        
        
        

    def descent(self, num = 1, debug = False):
        """Run descend num times on random vertices."""
        
        if self.vert_list is None:
            self.vert_list = self.get_vert_list()
        
        for __ in xrange(num):
            vert = type(self.vert_list[0])(np.random.choice(self.vert_list))
            if debug:
                print "{}/{}: descending on {}".format(__+1, num, vert)
            self.descend(vert, debug)


    def descend(self, vert, debug = False):
        """
        Run one iteration of the descend algorithm.

        Parameters
        __________

        vert: the vertex whose rank may change
        
        """
        
        #If haven't done so yet, get the number of arrows
        if not self.num_arrows:
            self.num_arrows = self.get_num_arrows()

        #get the rank of the vertex
        rank = self.get_rank(vert)

        if debug:
            print '*******\nDescending on {} with rank {}'.format(vert, rank)

        #count the relevant in and out neighbors:
        #out neighbors with rank <= rank + 1
        small_out = self.count_neighbors(vert, out=True, cond=True, less=True, cutoff=rank+1)
        
        #out neighbors with rank <= rank
        smaller_out = self.count_neighbors(vert, out=True, cond=True, less=True, cutoff=rank)
        
        #in neighbors with rank >= rank - 1
        large_in = self.count_neighbors(vert, out=False, cond=True, less=False, cutoff=rank-1)
        
        #in neighbors with rank >= rank
        larger_in = self.count_neighbors(vert, out=False, cond=True, less=False, cutoff=rank)
        
        #pressure_down is the decrease in agony
        #if the rank of this vertex is decreased by 1
        pressure_down = smaller_out - large_in

        #pressure_up is the decrease in agony
        #if the rank of this vertex is increased by 1
        pressure_up = larger_in - small_out
        
        if debug:
            print 'small out {}\nsmaller out {}\nlarge in {}\nlarger in {}\npressure down {}\npressure up {}'.format(small_out, smaller_out, large_in, larger_in, pressure_down, pressure_up)
        
        #if there is pressure down greater
        #than the pressure up, 
        #and pressure down is positive
        #or pressure down is zero and vert is not a source
        #go down
        if pressure_down > pressure_up and (pressure_down > 0 or (pressure_down == 0 and self.count_neighbors(vert, out = False) > 0)):
            
            #decrease the rank of this user
            self.set_rank(vert, rank-1)
            
            if debug:
                print 'rank down to {}'.format(rank - 1)
            
            #add the new hierarchy score to the list
            hier_change = pressure_down/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]
            
        #else if there is nonnegative pressure up greater
        #than the pressure up, go up
        elif pressure_up > pressure_down and (pressure_up > 0 or (pressure_up == 0 and self.count_neighbors(vert, out = True) > 0)):

            #increase the rank of this user
            self.set_rank(vert, rank+1)
            
            if debug:
                print 'rank up to {}'.format(rank + 1)
            
            #add the new hierarchy score to the list
            hier_change = pressure_up/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]

        #otherwise, changing the rank doesn't help and add the current
        #hierarchy score to the list
        else:
            self.hierarchy_list += [self.hierarchy_list[-1]]
            

