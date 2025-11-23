import os
from amplpy import AMPL


def safe_str(val):
    """Converts AMPL values to normalized strings (removing .0 for integers)."""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


def solve_model(model_file, data_file, crew_node, power_node):
    """
    Runs the AMPL model and returns the cost and path.
    """
    ampl = AMPL()
    ampl.option["solver"] = "gurobi"
    ampl.option["gurobi_options"] = "solnsens=1"

    # Suppress solver output to keep console clean for the table
    ampl.option["solver_msg"] = 0

    ampl.read(model_file)
    ampl.read_data(data_file)

    ampl.getParameter("b").set(crew_node, 1)
    ampl.getParameter("b").set(power_node, -1)

    if os.getenv("AMPLHW_OUTPUT"):
        ampl.eval(r"solve;")
    else:
        ampl.solve()

    # Check if solved successfully
    result = ampl.get_value("solve_result")
    if result != "solved":
        return {
            "start": crew_node,
            "end": power_node,
            "cost": float("inf"),
            "path": "Infeasible/Error",
        }

    objective_value = ampl.get_objective("Cost").value()

    # --- Path Reconstruction ---
    # Get flow on arcs
    x = ampl.get_variable("x").get_values().to_dict()

    # Get arc topology
    param_i = ampl.get_parameter("i").get_values().to_dict()
    param_j = ampl.get_parameter("j").get_values().to_dict()

    # Map tail -> head for active arcs
    next_node_map = {}
    for arc_id, flow in x.items():
        if abs(flow) > 0.5:  # Active arc
            u = safe_str(param_i[arc_id])
            v = safe_str(param_j[arc_id])
            next_node_map[u] = v

    # Trace the path
    path_nodes = []
    curr = safe_str(crew_node)
    target = safe_str(power_node)

    path_nodes.append(curr)

    # Limit iterations to avoid infinite loops in case of errors
    max_iter = len(param_i) + 5
    count = 0

    while curr != target and count < max_iter:
        if curr in next_node_map:
            next_n = next_node_map[curr]
            path_nodes.append(next_n)
            curr = next_n
        else:
            # Path broken or destination not reached
            path_nodes.append("(end?)")
            break
        count += 1

    path_str = "->".join(path_nodes)

    return {
        "start": crew_node,
        "end": power_node,
        "cost": objective_value,
        "path": path_str,
    }


if __name__ == "__main__":
    MODEL_FILE = "MCFP_3_1.mod"
    DATA_FILE = "MCFP_3_1.dat"

    scenarios = [
        (1, "3p"),
        (18, "3p"),
        (1, 5),
        (18, 5),
        (1, "6p"),
        (18, "6p"),
        (1, 13),
        (18, 13),
        (1, "23p"),
        (18, "23p"),
        (1, 24),
        (18, 24),
    ]

    results = []

    # Print a loading message if running interactively
    if not os.getenv("AMPLHW_OUTPUT"):
        print("Calculating optimal paths...")

    for start, end in scenarios:
        res = solve_model(MODEL_FILE, DATA_FILE, start, end)
        results.append(res)

    # --- Build Table ---
    header = f"{'Start':<6} | {'End':<6} | {'Time':<6} | {'Travel Sequence'}"
    separator = "-" * 60

    output_lines = []
    output_lines.append(header)
    output_lines.append(separator)

    for r in results:
        start_s = str(r["start"])
        end_s = str(r["end"])
        cost_s = f"{r['cost']:.1f}"
        path_s = r["path"]

        line = f"{start_s:<6} | {end_s:<6} | {cost_s:<6} | {path_s}"
        output_lines.append(line)

    output_content = "\n".join(output_lines)

    print(output_content)

    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem3_1.amplout"
        with open(output_filename, "w") as f:
            f.write(output_content)
        print(f"\nOutput also written to {output_filename}")
