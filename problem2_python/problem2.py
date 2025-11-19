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
    ampl.option["gurobi_options"] = "solnsens=1"

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
    objective_value = ampl.get_objective('Time').value()
    output_lines.append(f"Objective value (Total Time): {objective_value:,.2f}")
    output_lines.append("-" * 30)
    output_lines.append("Test Plan:")

    # Get all necessary variables and parameters as dictionaries for easy access
    x = ampl.get_variable("x").get_values().to_dict()
    for (i, j), val in x.items():
        if val == 1:
            output_lines.append(f"  - Switch from Engine {i} to Engine {j}")
            output_lines.append(f"      - Switchover Time: {ampl.get_parameter('s').get(i,j)}")
            output_lines.append(f"      - Processing Time: {ampl.get_parameter('p').get(j)}")
    # x_a_tier = ampl.get_variable("x_A_Tier").get_values().to_dict()
    # x_c_tier = ampl.get_variable("x_C_Tier").get_values().to_dict()
    # tier_costs = ampl.get_parameter("Tier_Costs").get_values().to_dict()

    # # --- Supplier A Details ---
    # if x.get('A', 0) > 0.001:
    #     output_lines.append(f"  - Supplier A: {int(round(x['A']))} units")
    #     if x_a_tier.get(1, 0) > 0.001:
    #         cost = tier_costs.get(('A', 1), 0)
    #         output_lines.append(f"      - Tier 1 Active: {int(round(x_a_tier[1]))} units @ ${cost:.2f}/unit")
    #     if x_a_tier.get(2, 0) > 0.001:
    #         cost = tier_costs.get(('A', 2), 0)
    #         output_lines.append(f"      - Tier 2 Active: {int(round(x_a_tier[2]))} units @ ${cost:.2f}/unit")

    # # --- Supplier B Details ---
    # if x.get('B', 0) > 0.001:
    #     cost = tier_costs.get(('B', 1), 0)
    #     output_lines.append(f"  - Supplier B: {int(round(x['B']))} units")
    #     output_lines.append(f"      - Fixed Rate: ${cost:.2f}/unit")

    # # --- Supplier C Details ---
    # if x.get('C', 0) > 0.001:
    #     output_lines.append(f"  - Supplier C: {int(round(x['C']))} units")
    #     if x_c_tier.get(1, 0) > 0.001:
    #         cost = tier_costs.get(('C', 1), 0)
    #         output_lines.append(f"      - Purchased in Tier 1: {int(round(x_c_tier[1]))} units @ ${cost:.2f}/unit")
    #     if x_c_tier.get(2, 0) > 0.001:
    #         cost = tier_costs.get(('C', 2), 0)
    #         output_lines.append(f"      - Purchased in Tier 2: {int(round(x_c_tier[2]))} units @ ${cost:.2f}/unit")
    
    # --- Print to console ---
    print("--- Results ---")
    for line in output_lines:
        print(line)

    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem2.amplout"
        with open(output_filename, "w") as f:
            f.write("\n".join(output_lines))
        print(f"\nOutput also written to {output_filename}")


if __name__ == "__main__":
    # --- Define Problem Specifics ---
    MODEL_FILE = "problem2.mod"
    DATA_FILE = "problem2.dat"
    
    # --- Run the AMPL model ---
    run_ampl_model(MODEL_FILE, DATA_FILE)