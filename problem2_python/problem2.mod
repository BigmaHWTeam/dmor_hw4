set E;
set T;

param s {i in E, j in E} >=0; # Switchover time from engine i to engine j
param p {j in E} >=0;         # Processing time for engine j
param t {i in E} symbolic;    # Type of engine i

var x {i in E, j in E} binary;  # 1 if switchover from engine i to engine j
var v {E} >= 1, <= card(E);     # Order in which engine i is visited


minimize Time:
    sum {i in E} sum {j in E} x[i,j]*(s[i,j] + p[j]);

subject to every_engine_starts_once {j in E}:
    sum {i in E} x[i,j] = 1;

subject to every_engine_ends_once {i in E}:
    sum {j in E} x[i,j] = 1;

subject to no_self_switch {i in E}:
    x[i,i] = 0;

subject to valid_type {i in E}:
    t[i] in T;

subject to no_sub_tours {i in E, j in E: i <> j and j <> 0}:
  ( (v[i] - v[j]) + (card(E) * x[i,j]) ) <= (card(E)-1);