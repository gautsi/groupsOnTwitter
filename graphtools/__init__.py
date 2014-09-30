"""
This package includes :class:`graphtools.gengraph.GenGraph`, a superclass implementing the descent algorithm, and subclasses of ``GenGraph`` which accomodate various graph data structures. Namely

* :class:`graphtools.dbgraph.DBGraph` reads graph data stored in a sqlalchemy-supported database,
* :class:`graphtools.sagegraph.SageGraph` wraps a ``sage.graphs.digraph.DiGraph`` object, and
* :class:`graphtools.listgraph.ListGraph` reads graph data stored as a list of arrows.

Multiple types for the vertices are supported. The type *vertextype* refers to the instance-specific type of the vertices.

"""

import gengraph
import listgraph
import sagegraph
import dbgraph
