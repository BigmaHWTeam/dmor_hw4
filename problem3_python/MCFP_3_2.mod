set NODES;		    # set of nodes
set ARCS; 		    # set of arcs
set POWERSTATIONS;  # set of nodes with powerstations
# cost of traversing arc a in ARCS
param c {ARCS};		                    
# tail node of arc a : if a=(k,m) then i(a)=k
param i {ARCS} symbolic in NODES;		
# head node of arc a : if a=(k,m) then j(a)=m
param j {ARCS} symbolic in NODES;		
# minimum flow on arc a in ARCS
param lb {ARCS};	                    
# maximum flow (capacity) on arc a in ARCS
param ub {ARCS};	                    
# number of repair crews available
param number_of_crews;                  

var x{a in ARCS};	# flow on arc a in A
var supply {NODES} >= 0; # outflow from Nodes where repair crews at

minimize TotalCost: sum{a in ARCS} c[a]*x[a];

subject to balance {n in NODES}:
    ((n in POWERSTATIONS) and sum{a in ARCS: i[a]=n}x[a]-sum{a in ARCS: j[a]=n}x[a]=-1)
    or
    ((n not in POWERSTATIONS) and sum{a in ARCS: i[a]=n}x[a]-sum{a in ARCS: j[a]=n}x[a]=supply[n]);
subject to lower_b {a in ARCS}: x[a] >= lb[a];
subject to upper_b {a in ARCS}: x[a] <= ub[a];

subject to crew_limit: count{n in NODES} (supply[n] > 0) <= number_of_crews;
