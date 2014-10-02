Introduction
============

Hierarchy on Twitter
____________________

Who are the power players on Twitter (or in a Twitter community)? A good indicator of power is the number of followers a user has. But an identification of the powerful users based solely on the number of followers would miss the users with few but powerful followers. We describe a measure of a user's power which incorporates the power of the user's followers.

Consider the directed graph with vertices the users in a Twitter community and an arrow from user :math:`A` to user :math:`B` if and only if :math:`A` follows :math:`B`. In this graph, the powerful users will have many in neighbors (followers), and many of their out neighbors (friends) will be powerful themselves. On the other hand, the average user will have many out nieghbors but few in neighbors. Thus the Twitter graph may exhibit high hierarchy as defined below.

Let :math:`G = (V, E)` be a directed graph. Write :math:`n = |V|`, :math:`m = |E|`. All of the following definitions are (directly or adapted) from [FHSN]_.

Definition
    A **ranking** of :math:`G` is a map :math:`V \to {\bf N}` where :math:`{\bf N}` is the natural numbers, and the value of a vertex under the map is called the **rank** of the vertex. Denote the set of rankings of :math:`G` by :math:`R(G)`.

Definition
    The **agony** of a ranking :math:`r \in R(G)` is
     
    .. math::
    
       A(r) := \sum_{(u, v) \in E} \max \{ r(u) - r(v) + 1, 0\}.

Definition   
    The **hierarchy** of a ranking :math:`r \in R(G)` is
     
    .. math::
    
       h(r) := 1 - (1/m)A(r).

The agony of a ranking counts the arrows in the graph which don't go up in rank (counted with one more than the difference in ranks). The naive ranking by the zero map has agony :math:`m`, so any ranking at least as good as the naive one has hierarchy between 0 and 1.

If a ranking of the graph of a Twitter community has high hierarchy, then the graph exhibits hierarchal structure and rank is a good indicator of power. In the next section, we describe an algorithm to find a ranking of a graph with high hierarchy. In the next chapter, we document an implementation of that algorithm.

.. Definition
    The **agony** of :math:`G` is :math:`$A(G) := \min_{r \in R(G)}A(r),$`
    and the **hierarchy** of :math:`G` is :math:`$h(G) := 1 - (1/m)A(G).$`    

.. By [FHSN]_, :math:`A(G)` is at most :math:`m`, so :math:`0 \leq h(G) \leq 1`.

.. [FHSN] M\. Gupte, P\. Shankar, J\. Li, S\. Muthukrishnan, L\. Iftode, `Finding hierarchy in directed online social networks.`_

.. _`Finding hierarchy in directed online social networks.`: http://www.cs.rutgers.edu/~iftode/www11_socialhierarchy.pdf




The descent algorithm
_____________________

Let :math:`G = (V,E)` be a directed graph and let :math:`r` be a ranking of :math:`G`. Pick a vertex :math:`v \in V`. Will updating :math:`r` by increasing or decreasing the rank of :math:`v` by 1 decrease the agony of :math:`r`? The change in agony if the rank of :math:`v` is increased by 1 is 

.. math::
   i(v) := \big|\{w \in V\ |\ v \to w \in E \ \& \ r(w) \leq r(v) + 1\}\big| - \big|\{w \in V\ |\ w \to v \in E \ \& \ r(w) \geq r(v)\}\big|
   
while the change in agony if the rank of :math:`v` is decreased by 1 is 

.. math::
   d(v) := \big|\{w \in V\ |\ w \to v \in E\ \& \ r(w) \geq r(v) - 1\}\big| - \big|\{w \in V\ |\ v \to w \in E\ \& \ r(w) \leq r(v)\}\big|. 
   
If :math:`i(v) \leq -1`, then increasing the rank of the vertex by 1 will decrease the agony of the ranking, as will decreasing the rank by 1 if :math:`d(v) \leq -1`.

Our algorithm, which we call the descent algorithm, starts with the naive ranking (all ranks are 0) and iteratively picks a vertex at random and changes its rank by 1 if doing so will decrease the agony of the ranking.
