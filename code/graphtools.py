# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 21:58:23 2014

@author: gautam
"""

class GenGraph:
    """A general graph."""

    def __init__(self):
        """Initialze the object."""

        self.num_arrows = None
        
        self.hierarchy_list = [0]
        
        self.passes = 0

    def get_num_arrows(self):
        """Return the number of arrows."""
        
        pass


    def get_rank(self, vert):
        """Return the rank of vertex vert."""

        pass

    def set_rank(self, vert, newrank):
        """Set the rank of vertex vert to int newrank."""
        
        pass

        
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
 
        pass
        



    def descend(self, vert):
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
        
        #if there is nonnegative pressure down greater
        #than the pressure up, go down
        if pressure_down > pressure_up and pressure_down >= 0:
            
            #decrease the rank of this user
            self.set_rank(vert, rank-1)
            
            #add the new hierarchy score to the list
            hier_change = pressure_down/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]
            
        #else if there is nonnegative pressure up greater
        #than the pressure up, go up
        elif pressure_up > pressure_down and pressure_up >= 0:

            #increase the rank of this user
            self.set_rank(vert, rank+1)
            
            #add the new hierarchy score to the list
            hier_change = pressure_up/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]

        #otherwise, changing the rank doesn't help and add the current
        #hierarchy score to the list
        else:
            self.hierarchy_list += [self.hierarchy_list[-1]]
            

