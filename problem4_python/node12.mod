set P;
param sellValue {p in P};
param hours {p in P};
param alum {p in P};
param maxHour;
param maxAlum;

var x{p in P} >=0;
var SlackHours >=0;
var SlackAlum >=0;

maximize Profit: sum{p in P}sellValue[p]*x[p];
subject to CtrAlum: sum {p in P} alum[p]*x[p]+SlackAlum=maxAlum;
subject to CtrHour: sum {p in P} hours[p]*x[p]+SlackHours=maxHour;

# Branch and Bound Constraints
subject to node04: x['WingSpar'] <= 169;
subject to node05: x['WingRib'] >= 106;
subject to node07: x['WingSpar'] <= 167;
subject to node08: x['WingRib'] >= 107;
subject to node10: x['WingSpar'] <= 166;
subject to node12: x['WingRib'] <= 107;
