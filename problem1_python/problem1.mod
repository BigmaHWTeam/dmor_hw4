set Suppliers;
set Tiers;

param demand;
param Tier_Quantities {s in Suppliers, t in Tiers};
param Tier_Costs {s in Suppliers, t in Tiers};

var x{s in Suppliers} integer >=0; # Buy x from supplier s.
var A_Tier {t in Tiers} binary; # Which tier
var x_A_Tier {t in Tiers} integer >=0; # How much in the tier
var C_Tier2 binary; # Can use tier 2
var x_C_Tier {t in Tiers} integer >=0; # How much in the tier

##########
# Demand #
##########
subject to Demand: sum{s in Suppliers} x[s]=demand;

##############
# Supplier A #
##############
# Total bought is sum of each tier bought
subject to Link_x_A: x['A'] = sum {t in Tiers} x_A_Tier[t];
# Only 1 tier
subject to Select_Tier_A: sum {t in Tiers} A_Tier[t] <=1;
# Enforce Tier 1
subject to x_A_t1: x_A_Tier[1] <= Tier_Quantities['A',1] * A_Tier[1];
# Lower 
subject to x_A_t2_lower: x_A_Tier[2] >= (Tier_Quantities['A',1]+1)*A_Tier[2];
subject to x_A_t2_upper: x_A_Tier[2] <= Tier_Quantities['A',2]*A_Tier[2];
##############
# Supplier B #
##############
subject to Max_B: x['B'] <= Tier_Quantities['B',1];

##############
# Supplier C #
##############
subject to Link_x_C: x['C'] = sum {t in Tiers} x_C_Tier[t];
subject to Tier_Limit_C1:
  x_C_Tier[1] <= Tier_Quantities['C',1];
subject to Tier_Limit_C2:
  x_C_Tier[2] <= (Tier_Quantities['C',2] - Tier_Quantities['C',1]) * C_Tier2;
subject to Fill_C1:
  x_C_Tier[1] >= Tier_Quantities['C',1] * C_Tier2;

#############
# Objective #
#############
minimize Cost:
  (Tier_Costs['A',1]*x_A_Tier[1] + Tier_Costs['A',2]*x_A_Tier[2])
  + (Tier_Costs['B',1]*x['B'])
  + (Tier_Costs['C',1]*x_C_Tier[1] + Tier_Costs['C',2]*x_C_Tier[2]);
