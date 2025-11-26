import os
from amplpy import AMPL


def safe_str(val):
    """Converts AMPL values to normalized strings (removing .0 for integers)."""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


def solve_model(model_file, data_file):
    """
    Runs the AMPL model and returns the cost and path.
    """
    ampl = AMPL()
    ampl.option["solver"] = "gurobi"

    # Suppress solver output to keep console clean for the table
    ampl.option["solver_msg"] = 0

    ampl.read(model_file)
    ampl.read_data(data_file)

    if os.getenv("AMPLHW_OUTPUT"):
        ampl.eval(r"solve;")
    else:
        ampl.solve()

    # Check if solved successfully
    result = ampl.get_value("solve_result")
    if result != "solved":
        return {
            # "start": crew_node,
            # "end": power_node,
            "cost": float("inf"),
            "path": "Infeasible/Error",
        }

    objective_value = ampl.get_objective("TotalCost").value()
    print(f"Objective Value: {objective_value}")

    supply_var = ampl.get_variable("supply").get_values().to_dict()

    # Identify source nodes (crews) and their supply amount
    sources = {}
    for node, val in supply_var.items():
        if val > 1e-5: # Tolerance for float
            sources[safe_str(node)] = int(round(val))
            print(f"Crew at {node} with supply {val}")

    # --- Path Reconstruction ---
    # Get flow on arcs
    x = ampl.get_variable("x").get_values().to_dict()

    # Get arc topology and costs
    param_i = ampl.get_parameter("i").get_values().to_dict()
    param_j = ampl.get_parameter("j").get_values().to_dict()
    param_c = ampl.get_parameter("c").get_values().to_dict()

    power_stations_set = ampl.get_set("POWERSTATIONS").get_values().to_list()
    power_stations = set(safe_str(p) for p in power_stations_set)

    # Build adjacency with flow and costs
    # adj[u][v] = {'flow': f, 'cost': c, 'arc_id': a}
    adj = {}
    for arc_id, flow in x.items():
        if flow > 1e-5:
            u = safe_str(param_i[arc_id])
            v = safe_str(param_j[arc_id])
            if u not in adj: adj[u] = {}
            # Handle potential parallel edges? AMPL model has simple arcs, but let's be safe.
            # We assume one arc from u to v.
            adj[u][v] = {'flow': flow, 'cost': param_c[arc_id], 'arc_id': arc_id}

    paths = []

    # Decompose flow into paths
    for s, supply_amt in sources.items():
        remaining_supply = supply_amt
        while remaining_supply >= 0.9: # Treat as integer units
            # Find a path from s to a power station
            path_nodes = [s]
            curr = s
            path_cost = 0

            # Simple DFS/Traversal to find a sink with available flow capacity
            # Since this is a valid flow solution, a path must exist.
            while curr not in power_stations:
                if curr not in adj:
                    path_nodes.append("(stuck)")
                    break

                # Pick next node with flow
                next_node = None
                for v, edge_data in adj[curr].items():
                    if edge_data['flow'] > 1e-5:
                        next_node = v
                        break

                if next_node:
                    # Record move
                    edge_data = adj[curr][next_node]
                    path_cost += edge_data['cost']

                    # Decrement flow to mark as used for this unit
                    adj[curr][next_node]['flow'] -= 1.0
                    # Clean up if flow is effectively 0
                    if adj[curr][next_node]['flow'] < 1e-5:
                        del adj[curr][next_node]

                    curr = next_node
                    path_nodes.append(curr)
                else:
                    path_nodes.append("(dead end)")
                    break

            paths.append({
                "start": s,
                "end": curr,
                "cost": path_cost,
                "path": "->".join(path_nodes)
            })
            remaining_supply -= 1.0

    return paths


if __name__ == "__main__":
    MODEL_FILE = "MCFP_3_2.mod"
    DATA_FILE = "MCFP_3_2.dat"

    # Print a loading message if running interactively
    if not os.getenv("AMPLHW_OUTPUT"):
        print("Calculating optimal paths...")

    all_paths = solve_model(MODEL_FILE, DATA_FILE)

    # --- Build Table ---
    header = f"{'Start':<6} | {'End':<6} | {'Time':<6} | {'Travel Sequence'}"
    separator = "-" * 60

    output_lines = []
    output_lines.append(header)
    output_lines.append(separator)

    for r in all_paths:
        start_s = str(r["start"])
        end_s = str(r["end"])
        cost_s = f"{r['cost']:.1f}"
        path_s = r["path"]

        line = f"{start_s:<6} | {end_s:<6} | {cost_s:<6} | {path_s}"
        output_lines.append(line)

    output_content = "\n".join(output_lines)

    print(output_content)

    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem3_2.amplout"
        with open(output_filename, "w") as f:
            f.write(output_content)
        print(f"\nOutput also written to {output_filename}")
