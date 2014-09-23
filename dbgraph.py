import graphtools as gt
from sqlalchemy.sql import select
from sqlalchemy import func
import numpy as np

class DBGraph(gt.GenGraph):
    """
    A subclass of GenGraph for graphs stored in databases.
    
    The vertices are stored in a table called users.
    The arrows are stored in a table called arrows.
    The vertices are identified by the value in the user_id column. 
    
    """
    
    def __init__(self, users, arrows, conn, group = None):
        """Initialize the object."""
        
        gt.GenGraph.__init__(self)
        
        self.users = users
        self.arrows = arrows
        self.conn = conn
        self.group = group
        
        if self.group is None:
            self.ucheckgroup = True
            self.acheckgroup = True
        else:
            self.ucheckgroup = self.users.c.group == self.group
            self.acheckgroup = self.arrows.c.group == self.group
            
        self.reset_ranks()
        self.user_list = self.get_user_list()
        
    def reset_ranks(self):
        """Set all ranks to zero."""
        
        stmt = self.users.update().where(self.ucheckgroup).values(rank = 0)
        self.conn.execute(stmt)
        
    def get_user_list(self):
        """return the list of user_ids."""
        
        getuserids = select([self.users.c.user_id]).where(self.ucheckgroup)
        results = self.conn.execute(getuserids)
        return [result[0] for result in results.fetchall()]

    def get_num_arrows(self):
        """Return the number of arrows."""
        
        countarrows = select([func.count()]).select_from(self.arrows).where(self.acheckgroup)
        result = self.conn.execute(countarrows)
        return result.fetchone()[0]
        
    def check_id(self, vert):
        return self.users.c.user_id == vert
    
    def get_rank(self, vert):
        """Return the rank of vertex vert."""

        stmt = select([self.users.c.rank]).where((self.check_id(vert)) & (self.ucheckgroup))
        result = self.conn.execute(stmt)
        return result.fetchone()[0]

    def set_rank(self, vert, newrank):
        """Set the rank of vertex vert to int newrank."""
        
        stmt = self.users.update().where((self.check_id(vert)) & (self.ucheckgroup)).values(rank = newrank)
        self.conn.execute(stmt)

        
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
 
        genstmt = select([func.count()]).select_from(users).select_from(arrows)
        if out:
            inoutstmt = genstmt.where(arrows.c.follow_id == vert).where(users.c.user_id == arrows.c.lead_id)
        else:
            inoutstmt = genstmt.where(arrows.c.lead_id == vert).where(users.c.user_id == arrows.c.follow_id)
            
        if cond:
            if less:
                finalstmt = inoutstmt.where(users.c.rank <= cutoff)
            else:
                finalstmt = inoutstmt.where(users.c.rank >= cutoff)
        else:
            finalstmt = inoutstmt
            
        result = self.conn.execute(finalstmt)
        return result.fetchone()[0]
        
        
    def descent(self, num = 1):
        """Run descend num times on random vertices."""
        
        for __ in xrange(num):
            vert = np.random.choice(self.user_list)
            print 'descending on vert ' + str(vert)
            self.descend(vert)
