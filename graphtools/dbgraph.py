import gengraph as gg
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, create_engine, sql

def make_db(arrows_list, name=None):
    """
    Make a SQLite database in the correct format for :class:`DBGraph`.
    
    Parameters
    __________
    
    
    :param list arrow_list: the arrows of the graph as a list of lists of two ints, the first int representing the tail of the arrow and the second the head.
    :param str name: the name of the database; if no name is given, the database will be in-memory-only
    
    Returns
    _______
    
    :returns: the users table, arrows table and database connection as two `sqlalchemy Table`_ objects and a `sqlalchemy Connection`_ object, respectively
    :rtype: tuple
    
    For example,
    
    >>> from graphtools.dbgraph import make_db
    >>> users, arrows, conn = make_db([[1, 2], [2, 3]])
    >>> from sqlalchemy.sql import select
    >>> result = conn.execute(select([users]))
    >>> result.fetchall()
    [(1, 0), (2, 0), (3, 0)]
    >>> result = conn.execute(select([arrows]))
    >>> result.fetchall()
    [(1, 1, 2), (2, 2, 3)]
    
    .. _sqlalchemy Table: http://docs.sqlalchemy.org/en/rel_0_9/core/metadata.html#sqlalchemy.schema.Table
        
    .. _sqlalchemy Connection: http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html?highlight=connection#sqlalchemy.engine.Connection
    
    """
    
    #make the engine and connection
    if name is None:
        engine = create_engine('sqlite://')
    else:
        engine = create_engine('sqlite:///{}.db'.format(name))
    
    conn = engine.connect()
    
    #setup the tables    
    metadata = MetaData()

    users = Table('users', metadata, 
        Column('user_id', Integer, primary_key=True),
        Column('rank', Integer)
    )
    
    arrows = Table('arrows', metadata,
        Column('id', Integer, primary_key=True), 
        Column('follow_id', Integer, ForeignKey('users.user_id')),
        Column('lead_id', Integer, ForeignKey('users.user_id')),
        sqlite_autoincrement=True
    )
    
    #create the tables    
    metadata.create_all(engine)
    
    #add the vertices
    vertices = set([a[0] for a in arrows_list] + [a[1] for a in arrows_list])
    
    user_values = [{'user_id':vertex, 'rank':0} for vertex in vertices]
    
    conn.execute(users.insert(), user_values)
        
    #add the arrows
     
    arrow_values = [{'follow_id':arrow[0], 'lead_id':arrow[1]} for arrow in arrows_list]
     
    conn.execute(arrows.insert(), arrow_values)

    return users, arrows, conn
    
    
def get_tables(engine):
    """
    Get the tables and connections required for :class:`DBGraph` from a `sqlalchemy Engine`_ object.
    
    Parameters:
    ___________
    
    :param sqlalchemy.engine.Engine engine: the database engine

    Returns
    _______
    
    :returns: the users table, arrows table and database connection as two `sqlalchemy Table`_ objects and a `sqlalchemy Connection`_ object, respectively
    :rtype: tuple
    
    .. _sqlalchemy Table: http://docs.sqlalchemy.org/en/rel_0_9/core/metadata.html#sqlalchemy.schema.Table
        
    .. _sqlalchemy Engine: http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.Engine

    .. _sqlalchemy Connection: http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.Connection
    
    """
    pass    
    

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
    
    :param sqlalchemy.engine.Connection conn: a connection to the database
    
    :param group: an optional identifier, described above
    
    The initializer sets all entries in **user**.\ *rank* to 0.
    
    For example,
    
    >>> from graphtools.dbgraph import make_db, DBGraph
    >>> users, arrows, conn = make_db([[1, 2], [2, 3]])
    >>> graph = DBGraph(users=users, arrows=arrows, conn=conn)
    >>> print graph.get_num_arrows()
    2
    >>> set(graph.get_vert_list()) == set([1, 2, 3])
    True
    >>> print graph.get_rank(1)
    0
    >>> graph.set_rank(3,2)
    >>> graph.get_rank(3)
    2
    >>> graph.reset_ranks()
    >>> graph.descend(2)
    >>> graph.descent(20)
    >>> hl = graph.hierarchy_list #get the list of hierarchy scores
    >>> print len(hl) #descend has been run 21 times, plus the initial score
    22
    >>> print hl[0] #the first score is always 0
    0
    >>> print hl[-1] #the score after 21 descends will probably be 1.0
    1.0
    
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
        
        stmt = self.users.update().where(self.ucheckgroup).values(rank = 0)
        self.conn.execute(stmt)
        

    def get_num_arrows(self):
        
        countarrows = sql.select([func.count()]).select_from(self.arrows).where(self.acheckgroup)
        result = self.conn.execute(countarrows)
        return result.fetchone()[0]
        
    def get_vert_list(self):
        
        getuserids = sql.select([self.users.c.user_id]).where(self.ucheckgroup)
        results = self.conn.execute(getuserids)
        return [result[0] for result in results.fetchall()]

        
    def check_id(self, vert):
    
        return self.users.c.user_id == vert
    
    def get_rank(self, vert):

        stmt = sql.select([self.users.c.rank]).where((self.check_id(vert)) & (self.ucheckgroup))
        result = self.conn.execute(stmt)
        return result.fetchone()[0]

    def set_rank(self, vert, newrank):
        
        stmt = self.users.update().where((self.check_id(vert)) & (self.ucheckgroup)).values(rank = newrank)
        self.conn.execute(stmt)

        
    def count_neighbors(self, vert, out=True, cond=False, less=True, cutoff=0):
 
        genstmt = sql.select([func.count()]).select_from(self.users).select_from(self.arrows)
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
        

