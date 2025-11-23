set NODES;		# set of nodes
set ARCS; 		# set of arcs

param c {ARCS};		# cost of traversing arc a in ARCS
param i {ARCS};		# tail node of arc a : if a=(k,m) then i(a)=k
param j {ARCS};		# head node of arc a : if a=(k,m) then j(a)=m
param b {NODES};	# demand/supply of node i in NODES
param lb {ARCS};	# minimum flow on arc a in ARCS
param ub {ARCS};	# maximum flow (capacity) on arc a in ARCS

var x{a in ARCS};	# flow on arc a in A

minimize Cost: sum{a in ARCS} c[a]*x[a];
subject to balance {n in NODES}: sum{a in ARCS: i[a]=n}x[a]-sum{a in ARCS: j[a]=n}x[a]=b[n];
subject to lower_b {a in ARCS}: x[a] >= lb[a];
subject to upper_b {a in ARCS}: x[a] <= ub[a];


