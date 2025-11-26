# problem1.py

import os
from amplpy import AMPL

def run_ampl_model(model_file, data_file):
    """
    Runs the supplier selection AMPL model and prints a detailed
    breakdown of the results.

    Args:
        model_file (str): Path to the AMPL model file.
        data_file (str): Path to the AMPL data file.
    """
    ampl = AMPL()

    # Set solver and options
    ampl.option["solver"] = "gurobi"

    # Read the model and data files
    ampl.read(model_file)
    ampl.read_data(data_file)

    # Solve the model
    print("Solving model...")
    if os.getenv("AMPLHW_OUTPUT"):
        ampl.eval(r"solve;")
    else:
        ampl.solve()
    print("Solve complete.\n")

    # --- Build up the detailed output ---
    output_lines = []

    # Get objective value
    objective_value = ampl.get_objective('Cost').value()
    output_lines.append(f"Objective value (Total Cost): ${objective_value:,.2f}")
    output_lines.append("-" * 30)
    output_lines.append("Purchase Plan:")

    # Get all necessary variables and parameters as dictionaries for easy access
    x = ampl.get_variable("x").get_values().to_dict()
    tier_costs = ampl.get_parameter("Tier_Costs").get_values().to_dict()

    # --- Supplier A Details ---
    total_A = x.get(('A', 1), 0) + x.get(('A', 2), 0)
    if total_A > 0.001:
        output_lines.append(f"  - Supplier A: {int(round(total_A))} units")
        if x.get(('A', 1), 0) > 0.001:
            cost = tier_costs.get(('A', 1), 0)
            output_lines.append(f"      - Tier 1 Active: {int(round(x[('A', 1)]))} units @ ${cost:.2f}/unit")
        if x.get(('A', 2), 0) > 0.001:
            cost = tier_costs.get(('A', 2), 0)
            output_lines.append(f"      - Tier 2 Active: {int(round(x[('A', 2)]))} units @ ${cost:.2f}/unit")

    # --- Supplier B Details ---
    total_B = x.get(('B', 1), 0)
    if total_B > 0.001:
        cost = tier_costs.get(('B', 1), 0)
        output_lines.append(f"  - Supplier B: {int(round(total_B))} units")
        output_lines.append(f"      - Fixed Rate: ${cost:.2f}/unit")

    # --- Supplier C Details ---
    total_C = x.get(('C', 1), 0) + x.get(('C', 2), 0)
    if total_C > 0.001:
        output_lines.append(f"  - Supplier C: {int(round(total_C))} units")
        if x.get(('C', 1), 0) > 0.001:
            cost = tier_costs.get(('C', 1), 0)
            output_lines.append(f"      - Purchased in Tier 1: {int(round(x[('C', 1)]))} units @ ${cost:.2f}/unit")
        if x.get(('C', 2), 0) > 0.001:
            cost = tier_costs.get(('C', 2), 0)
            output_lines.append(f"      - Purchased in Tier 2: {int(round(x[('C', 2)]))} units @ ${cost:.2f}/unit")

    # --- Print to console ---
    print("--- Results ---")
    for line in output_lines:
        print(line)

    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem1.amplout"
        with open(output_filename, "w") as f:
            f.write("\n".join(output_lines))
        print(f"\nOutput also written to {output_filename}")


if __name__ == "__main__":
    # --- Define Problem Specifics ---
    MODEL_FILE = "problem1.mod"
    DATA_FILE = "problem1.dat"

    # --- Run the AMPL model ---
    run_ampl_model(MODEL_FILE, DATA_FILE)
