set N;  # Nodes (in this case the road intersections)
set A;  # Arcs (in this case the roads)
set C;  # Crews
set P;  # Power stations
set L;  # Locations (where Location is made up of two coordinates:
    # if on a Node then both coordinates are the Node id
    # otherwise if on an Arc then first coordinate is the tail Node id and second is the head Node id) 

#------------

param b {l in L} >= 0;              # Supply/demand at location l in L
param t {l1 in L, l2 in L} >= 0;    # Time to travel from location l1 to location l2
param crew_location {c in C} in L;  # Starting location of crew c in C
param power_location {p in P} in L; # Location of power station p in P

#------------

var x {l1 in L, l2 in L} >= 0;    # Number of times road from location 1 to location 2 used.

#------------

# For each power station, minimize the total time to reach it
minimize Time {p in P}:
    sum {l1 in L} sum {l2 in L} x[l1,l2] * t[l1,l2];

#------------

subject to balance {l in L}: sum{a in ARCS: i[a]=l}x[a]-sum{a in ARCS: j[a]=l}x[a]=b[n];