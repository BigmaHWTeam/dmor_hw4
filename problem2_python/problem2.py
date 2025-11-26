# problem2.py

import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from amplpy import AMPL

# UF Style Guide Colors
UF_ORANGE = "#FA4616"
UF_BLUE = "#0021A5"
SETUP_COLOR = "#B0B0B0"  # Neutral Gray for setup

def solve_model(model_file, data_file):
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
    # Removed Gurobi sensitivity analysis option as requested
    # ampl.option["gurobi_options"] = "solnsens=1" 
    ampl.read(model_file)
    ampl.read_data(data_file)

    print("Solving model...")
    if os.getenv("AMPLHW_OUTPUT"):
        ampl.eval(r"solve;")
    else:
        ampl.solve()
    print("Solve complete.\n")

    objective_value = ampl.get_objective('Time').value()
    visit_order = ampl.get_variable("v").get_values().to_dict()

    # Determine the optimal sequence
    sorted_engines = sorted(
        [engine for engine, order in visit_order.items() if order > 0 and engine != 0], 
        key=lambda e: visit_order[e]
    )
    optimal_sequence = sorted_engines + [0]
    
    # --- Build up the detailed output ---
    output_lines = []
    output_lines.append(f"Objective value (Total Time): {objective_value:,.2f}")
    output_lines.append("-" * 30)
    seq_str = " -> ".join(map(str, optimal_sequence))
    output_lines.append(f"Optimal Production Sequence: {seq_str}")
    return ampl, optimal_sequence, output_lines

def extract_data(ampl):
    """Extracts parameters s, p, t and node list from AMPL object."""
    s = ampl.get_parameter('s').get_values().to_dict()
    p = ampl.get_parameter('p').get_values().to_dict()
    t = ampl.get_parameter('t').get_values().to_dict()
    # Nodes are keys in p, excluding 0 (dummy)
    nodes = [int(i) for i in p.keys() if int(i) != 0]
    return s, p, t, nodes

def get_greedy_sequence(nodes, s):
    """Generates a sequence using a greedy algorithm based on shortest setup time."""
    unvisited = set(nodes)
    current = 0
    sequence = [0]
    
    while unvisited:
        # Find candidates with min setup time
        min_setup = float('inf')
        candidates = []
        
        for node in unvisited:
            setup_time = s.get((current, node), float('inf'))
            if setup_time < min_setup:
                min_setup = setup_time
                candidates = [node]
            elif setup_time == min_setup:
                candidates.append(node)
        
        # Pick random if tie
        if not candidates:
            break # Should not happen given connected graph logic
        
        next_node = random.choice(candidates)
        sequence.append(next_node)
        unvisited.remove(next_node)
        current = next_node
        
    sequence.append(0) # Return to start
    return sequence

def get_comm_mil_sequence(nodes, t):
    """Generates a sequence: all Commercial first, then all Military."""
    # Sort for deterministic output within groups
    commercial = sorted([n for n in nodes if t[n] == 'C'])
    military = sorted([n for n in nodes if t[n] == 'M'])
    
    return [0] + commercial + military + [0]

def calculate_schedule_metrics(sequence, s, p):
    """Calculates total setup time and segments for plotting."""
    total_setup = 0
    current_time = 0
    segments = [] # list of (start, duration, type ('setup' or 'run'), engine_id)
    
    for i in range(len(sequence) - 1):
        u, v = sequence[i], sequence[i+1]
        
        # Setup
        setup_time = s.get((u, v), 0)
        if setup_time > 0:
            segments.append((current_time, setup_time, 'setup', v))
            total_setup += setup_time
            current_time += setup_time
            
        # Processing (only if not returning to 0, usually 0 has p=0 anyway)
        proc_time = p.get(v, 0)
        if proc_time > 0:
            segments.append((current_time, proc_time, 'run', v))
            current_time += proc_time
            
    return total_setup, current_time, segments

def plot_gantt(sequence, s, p, t, filename, title):
    """Generates and saves a Gantt chart with each engine on its own line."""
    total_setup, total_time, segments = calculate_schedule_metrics(sequence, s, p)
    
    # Identify all engines involved (excluding 0)
    engines = sorted([n for n in t.keys() if n != 0])
    
    # Create figure with dynamic height based on number of engines
    # Height: header + (rows * height_per_row)
    fig_height = max(4, len(engines) * 0.8 + 2)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    
    # Map engines to Y-axis positions (using index)
    engine_indices = {e: i for i, e in enumerate(engines)}
    
    # Track all time points for vertical lines
    time_points = {0}
    
    for start, duration, seg_type, engine_id in segments:
        if engine_id == 0: continue
        
        row_idx = engine_indices[engine_id]
        end_time = start + duration
        time_points.add(end_time)
        time_points.add(start)
        
        if seg_type == 'setup':
            color = SETUP_COLOR
            # Draw Setup bar
            ax.broken_barh([(start, duration)], (row_idx - 0.3, 0.6), 
                         facecolors=color, edgecolor='black', linewidth=0.5)
            
            # Label with setup time
            if duration >= 1:
                ax.text(start + duration/2, row_idx, f"{int(duration)}", 
                       ha='center', va='center', color='black', fontsize=8)
                
        else: # Run
            engine_type = t.get(engine_id, 'None')
            color = UF_ORANGE if engine_type == 'C' else UF_BLUE if engine_type == 'M' else 'black'
            
            # Draw Run bar
            ax.broken_barh([(start, duration)], (row_idx - 0.3, 0.6), 
                         facecolors=color, edgecolor='black', linewidth=0.5)
             
            # Label with run time
            if duration >= 2:
                ax.text(start + duration/2, row_idx, f"{int(duration)}", 
                       ha='center', va='center', color='white', fontsize=9, fontweight='bold')

    # Add vertical lines for all significant time points
    for tp in sorted(list(time_points)):
        ax.axvline(x=tp, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Formatting
    ax.set_yticks(range(len(engines)))
    ax.set_yticklabels([f"Engine {e}" for e in engines])
    ax.invert_yaxis() # Top to bottom
    
    ax.set_xlim(0, total_time * 1.05)
    ax.set_xlabel('Time', fontsize=12)
    
    # X-ticks at specific points
    sorted_ticks = sorted(list(time_points))
    ax.set_xticks(sorted_ticks)
    ax.set_xticklabels([str(int(x)) if x.is_integer() else str(x) for x in sorted_ticks], rotation=45)
    
    # Title with Total Setup Highlight
    full_title = f"{title}\nTotal Setup Time: {total_setup}"
    ax.set_title(full_title, fontsize=14, pad=15)
    
    # Legend
    patches = [
        mpatches.Patch(color=UF_ORANGE, label='Commercial (C)'),
        mpatches.Patch(color=UF_BLUE, label='Military (M)'),
        mpatches.Patch(color=SETUP_COLOR, label='Setup')
    ]
    ax.legend(handles=patches, loc='upper right')
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Generated chart: {filename}")

if __name__ == "__main__":
    MODEL_FILE = "problem2.mod"
    DATA_FILE = "problem2.dat"
    
    # --- Solve the Model for the Optimal Solution ---
    ampl, optimal_sequence, output = solve_model(MODEL_FILE, DATA_FILE)
    
    # --- Print to console ---
    print("--- Results ---")
    for line in output:
        print(line)


    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem2.amplout"
        with open(output_filename, "w") as f:
            f.write("\n".join(output))
        print(f"\nOutput also written to {output_filename}")
        
    # --- Generate Gantt Charts ---
    print("\nGenerating Gantt Charts...")
    s, p, t, nodes = extract_data(ampl)
    
    # 1. Optimal Sequence
    plot_gantt(optimal_sequence, s, p, t, "problem2_optimal_gantt.pdf", "Optimal Production Schedule")
    
    # 2. Greedy Sequence
    greedy_seq = get_greedy_sequence(nodes, s)
    plot_gantt(greedy_seq, s, p, t, "problem2_greedy_gantt.pdf", "Greedy Algorithm Schedule")
    
    # 3. Commercial First Sequence
    comm_mil_seq = get_comm_mil_sequence(nodes, t)
    plot_gantt(comm_mil_seq, s, p, t, "problem2_commercial_first_gantt.pdf", "Commercial First Schedule")
