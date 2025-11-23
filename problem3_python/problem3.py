# problem1.py

import os
import random
from amplpy import AMPL
import matplotlib.pyplot as plt

def solve_model(model_file, data_file, crew_node, power_node):
    """
    Runs the engine production AMPL model and returns the solved object
    and processed results.

    Args:
        model_file (str): Path to the AMPL model file.
        data_file (str): Path to the AMPL data file.
    
    Returns:
        tuple: A tuple containing the solved AMPL object, the optimal sequence list,
               and the list of output lines for display.
    """
    ampl = AMPL()
    ampl.option["solver"] = "gurobi"
    ampl.option["gurobi_options"] = "solnsens=1"
    ampl.read(model_file)
    ampl.read_data(data_file)

    ampl.getParameter("b").set(crew_node, 1)
    ampl.getParameter("b").set(power_node, -1)
    
    print("Solving model...")
    if os.getenv("AMPLHW_OUTPUT"):
        ampl.eval(r"solve;")
    else:
        ampl.solve()
    print("Solve complete.\n")

    objective_value = ampl.get_objective('Cost').value()
    
    # --- Build up the detailed output ---
    output_lines = []
    output_lines.append(f"Time for crew at Node {crew_node:02d} to get to power station at Node {power_node}:\t{objective_value:,.1f}")
    return output_lines

if __name__ == "__main__":
    MODEL_FILE = "MCFP.mod"
    DATA_FILE = "MCFP.dat"
    
    # --- Solve the Model for the Optimal Solution ---
    output = []

    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node="3p")
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node="3p")
    output.append("-" * 30)
    
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node=5)
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node=5)
    output.append("-" * 30)

    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node="6p")
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node="6p")
    output.append("-" * 30)

    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node=13)
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node=13)
    output.append("-" * 30)

    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node="23p")
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node="23p")
    output.append("-" * 30)

    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=1, power_node=24)
    output += solve_model(MODEL_FILE, DATA_FILE, crew_node=18, power_node=24)
    
    # --- Print to console ---
    print("--- Results ---")
    for line in output:
        print(line)

    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem3.amplout"
        with open(output_filename, "w") as f:
            f.write("\n".join(output))
        print(f"\nOutput also written to {output_filename}")