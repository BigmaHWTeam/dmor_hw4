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
subject to node09: x['WingSpar'] <= 168;
subject to node23: x['WingRib'] <= 105;
subject to node24: x['FuselagePanel'] >= 1;
subject to node30: x['WingRib'] <= 104;
subject to node31: x['FuselagePanel'] >=2;
subject to node32: x['WingRib'] >=104;
