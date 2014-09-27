import gengraph as gg
from sqlalchemy.sql import select
from sqlalchemy import func

class DBGraph(gg.GenGraph):
    """
    A subclass of GenGraph for graphs stored in databases. 
    
    The vertices are stored in a table called **users** with columns
    
    * *user_id* (any type) and
    * *rank* (int)
    
    (the name comes from the original motivation which was Twitter user subgraphs). The table may also have a column *group* (any type) specifying the particular graph that the user belongs to if the database contains multiple graphs. If the table has no *group* column, *user_id* should be a unique identifier; if there is a *group* column, *user_id* and *group* together should be unique. 
    
    The arrows are stored in a table called **arrows** with columns
    
    * *follow_id* and 
    * *lead_id*
    
    both refering to **users**.\ *user_id*. If **users** has a *group* column then **arrows** should have a corresponding *group* column.
    
    Parameters
    __________
    
    :param sqlalchemy.schema.Table users: the table of vertices, described above
    
    :param sqlalchemy.schema.Table arrows: the table of arrows, described above
    
    :param sqlalchemy.engine.base.Connection conn: a connection to the database
    
    :param any group: an optional identifier, described above
    
    The initializer sets all entries in **user**.\ *rank* to 0.
    
    """
    
    def __init__(self, users, arrows, conn, group = None):
        """Initialize the object."""
        
        gg.GenGraph.__init__(self)
        
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

        
    def reset_ranks(self):
        """Set all ranks to zero."""
        
        stmt = self.users.update().where(self.ucheckgroup).values(rank = 0)
        self.conn.execute(stmt)
        

    def get_num_arrows(self):
        
        countarrows = select([func.count()]).select_from(self.arrows).where(self.acheckgroup)
        result = self.conn.execute(countarrows)
        return result.fetchone()[0]
        
    def get_vert_list(self):
        
        getuserids = select([self.users.c.user_id]).where(self.ucheckgroup)
        results = self.conn.execute(getuserids)
        return [result[0] for result in results.fetchall()]

        
    def check_id(self, vert):
    
        return self.users.c.user_id == vert
    
    def get_rank(self, vert):

        stmt = select([self.users.c.rank]).where((self.check_id(vert)) & (self.ucheckgroup))
        result = self.conn.execute(stmt)
        return result.fetchone()[0]

    def set_rank(self, vert, newrank):
        
        stmt = self.users.update().where((self.check_id(vert)) & (self.ucheckgroup)).values(rank = newrank)
        self.conn.execute(stmt)

        
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):
        """See :func:`graphtools.gengraph.GenGraph.count_neighbors`."""
 
        genstmt = select([func.count()]).select_from(self.users).select_from(self.arrows)
        if out:
            inoutstmt = genstmt.where(self.arrows.c.follow_id == vert).where(self.users.c.user_id == self.arrows.c.lead_id)
        else:
            inoutstmt = genstmt.where(self.arrows.c.lead_id == vert).where(self.users.c.user_id == self.arrows.c.follow_id)
            
        if cond:
            if less:
                finalstmt = inoutstmt.where(self.users.c.rank <= cutoff)
            else:
                finalstmt = inoutstmt.where(self.users.c.rank >= cutoff)
        else:
            finalstmt = inoutstmt
            
        result = self.conn.execute(finalstmt)
        return result.fetchone()[0]
        

