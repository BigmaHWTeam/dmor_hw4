set Suppliers;
set Tiers;

param demand;
param Tier_Quantities {s in Suppliers, t in Tiers};
param Tier_Costs {s in Suppliers, t in Tiers};

# x[s,t] is the quantity purchased from supplier s relevant to tier t.
# For supplier A, x['A',t] is the total purchase, active only if in that tier's range.
# For suppliers B and C, x[s,t] is the incremental quantity within that tier.
var x {s in Suppliers, t in Tiers} integer >= 0;

# y[s,t] = 1 if we purchase from supplier s using tier t's rules.
# For A, this is for mutually exclusive quantity ranges.
# For C, this is for enabling the second incremental tier.
var y {s in Suppliers, t in Tiers} binary;


# Demand Constraint
# The total amount from all suppliers must meet the demand.
subject to Demand: sum{s in Suppliers, t in Tiers} x[s,t] = demand;


# Supplier A: All-units discount. Tiers are mutually exclusive.
# The total quantity from A is x['A',1] + x['A',2], but only one can be non-zero.
subject to A_OnlyOneTier: sum {t in Tiers} y['A',t] <= 1;

# Tier 1 for A: quantity is x['A',1], up to Tier_Quantities['A',1]
subject to A_Tier1_Amount: x['A',1] <= Tier_Quantities['A',1] * y['A',1];

# Tier 2 for A: quantity is x['A',2], between lower and upper bounds.
subject to A_Tier2_Lower: x['A',2] >= (Tier_Quantities['A',1] + 1) * y['A',2];
subject to A_Tier2_Upper: x['A',2] <= Tier_Quantities['A',2] * y['A',2];


# Supplier B: Single price.
# Only tier 1 is used. Quantity is unlimited in practice.
subject to B_No_Tier2: x['B',2] = 0;


# Supplier C: Incremental discount.
# x['C',1] is amount in tier 1, x['C',2] is amount in tier 2.
subject to C_Tier1_Limit: x['C',1] <= Tier_Quantities['C',1];
subject to C_Tier2_Limit: x['C',2] <= (Tier_Quantities['C',2] - Tier_Quantities['C',1]) * y['C',2];
# To buy from tier 2, tier 1 must be full.
subject to C_Fill_Tier1: x['C',1] >= Tier_Quantities['C',1] * y['C',2];


# Objective Function
minimize Cost: sum{s in Suppliers, t in Tiers} Tier_Costs[s,t] * x[s,t];
