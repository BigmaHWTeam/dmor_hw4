import os
from amplpy import AMPL


def run_ampl_model(model_file, data_file, output_filename=None):
    """
    Runs the product mix AMPL model (Problem 4) and prints a detailed
    breakdown of the results.

    Args:
        model_file (str): Path to the AMPL model file.
        data_file (str): Path to the AMPL data file.
        output_filename (str, optional): Filename to write output to.
    """
    print(f"Running model: {model_file}...")
    ampl = AMPL()

    # Set solver and options
    ampl.option["solver"] = "gurobi"

    # Read the model and data files
    ampl.read(model_file)
    ampl.read_data(data_file)

    # --- Build up the detailed output ---
    output_lines = []

    # Solve the model
    print("Solving model...")
    solve_success = False
    try:
        if os.getenv("AMPLHW_OUTPUT"):
            ampl.eval(r"solve;")
        else:
            ampl.solve()
        solve_success = True
        print("Solve complete.\n")
    except Exception as e:
        print(f"Solve failed: {e}\n")
        output_lines.append(f"Status: Infeasible/Error - {str(e)}")

    # --- Build up the detailed output ---
    if solve_success:
        # Get objective value
        try:
            objective_value = ampl.get_objective("Profit").value()
            output_lines.append(
                f"Objective value (Total Profit): ${objective_value:,.2f}"
            )
            output_lines.append("-" * 30)
            output_lines.append("Production Plan:")

            # Get variables and sets
            x = ampl.get_variable("x")
            products = ampl.get_set("P")

            # Iterate through products
            for p in products:
                val = x[p].value()
                if val > 0.001:
                    output_lines.append(f"  - Product {p}: {val:,.2f} units")

            # output_lines.append("-" * 30)
            # output_lines.append("Resource Usage (Slack):")

            # slack_hours = ampl.get_variable("SlackHours").value()
            # slack_alum = ampl.get_variable("SlackAlum").value()
            #
            # output_lines.append(f"  - Unused Hours: {slack_hours:,.2f}")
            # output_lines.append(f"  - Unused Aluminum: {slack_alum:,.2f}")
        except Exception as e:
            output_lines.append(f"Error extracting results: {e}")

    # --- Print to console ---
    print(f"--- Results for {model_file} ---")
    for line in output_lines:
        print(line)
    print("\n")

    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT") and output_filename:
        with open(output_filename, "w") as f:
            f.write("\n".join(output_lines))
        print(f"Output also written to {output_filename}")


if __name__ == "__main__":
    import glob

    DATA_FILE = "problem4.dat"
    run_ampl_model("integer.mod", DATA_FILE, "integer.amplout")
    run_ampl_model("relaxation.mod", DATA_FILE, "relaxation.amplout")

    # Find and run all node*.mod files in lexicographical order
    node_models = sorted(glob.glob("node*.mod"))
    for model_file in node_models:
        output_file = model_file.replace(".mod", ".amplout")
        run_ampl_model(model_file, DATA_FILE, output_file)
