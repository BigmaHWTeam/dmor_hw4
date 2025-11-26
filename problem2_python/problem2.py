# problem1.py

import os
import random
from amplpy import AMPL
import matplotlib.pyplot as plt

def generate_gantt_chart(sequence, s_param, p_param, title="Production Schedule Gantt Chart", filename="gantt_chart.pdf"):
    """
    Generates and saves a Gantt chart for a given production sequence.

    Args:
        sequence (list): A list of engine numbers in the order of production.
        s_param (dict): A dictionary of switchover times from AMPL.
        p_param (dict): A dictionary of processing times from AMPL.
        title (str): The title for the Gantt chart.
        filename (str): The name of the output PDF file.
    """
    gantt_data = []
    total_time = 0.0
    current_time = 0.0

    engine_types = {1: 'C', 2: 'C', 3: 'C', 4: 'M', 5: 'M'}
    type_colors = {'C': '#0021A5', 'M': '#FA4616'}

    # Start from the dummy node 0
    for i in range(len(sequence) - 1):
        start_engine = sequence[i]
        end_engine = sequence[i+1]

        # Ensure keys are integers for dictionary lookup
        switchover_time = s_param.get((start_engine, end_engine), 0)
        processing_time = p_param.get(end_engine, 0)

        setup_start_time = current_time
        task_start_time = current_time + switchover_time
        task_end_time = task_start_time + processing_time

        if end_engine != 0:
            engine_type = engine_types.get(end_engine)
            gantt_data.append({
                'Task': f"Engine {end_engine}",
                'Setup_Start': setup_start_time,
                'Setup_Duration': switchover_time,
                'Task_Start': task_start_time,
                'Task_Duration': processing_time,
                'Type': engine_type,
                'Color': type_colors.get(engine_type)
            })
        
        current_time = task_end_time
    
    total_time = current_time

    if not gantt_data:
        print(f"No tasks with processing time > 0 to plot for {filename}.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    
    tasks = [item['Task'] for item in gantt_data]
    
    setup_starts = [item['Setup_Start'] for item in gantt_data]
    setup_durations = [item['Setup_Duration'] for item in gantt_data]
    
    task_starts = [item['Task_Start'] for item in gantt_data]
    task_durations = [item['Task_Duration'] for item in gantt_data]
    colors = [item['Color'] for item in gantt_data]

    # Plotting setup times
    ax.barh(tasks, setup_durations, left=setup_starts, height=0.5, 
            edgecolor="black", color='grey', alpha=0.5, label='Setup Time')

    # Plotting processing times
    ax.barh(tasks, task_durations, left=task_starts, height=0.5, 
            edgecolor="black", color=colors, alpha=0.7)

    ax.set_xlabel("Time")
    ax.set_ylabel("Engine")
    
    full_title = f"{title}\nTotal Time: {total_time:.2f}"
    ax.set_title(full_title)
    ax.grid(True, which='major', axis='x', linestyle='--', linewidth=0.5)

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='grey', edgecolor='black', alpha=0.5, label='Setup Time'),
                       Patch(facecolor=type_colors['C'], edgecolor='black', alpha=0.7, label='Commercial'),
                       Patch(facecolor=type_colors['M'], edgecolor='black', alpha=0.7, label='Military')]
    ax.legend(handles=legend_elements)

    for i, task in enumerate(tasks):
        if setup_durations[i] > 0:
            ax.text(setup_starts[i] + setup_durations[i] / 2, i, f"{setup_durations[i]}",
                    ha='center', va='center', color='black', fontweight='bold')
        if task_durations[i] > 0:
            ax.text(task_starts[i] + task_durations[i] / 2, i, f"{task_durations[i]}", 
                    ha='center', va='center', color='white', fontweight='bold')
    
    plt.savefig(filename, format="pdf", bbox_inches="tight")
    print(f"\nGantt chart saved as {filename}")


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
    ampl.option["gurobi_options"] = "solnsens=1"
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
        [engine for engine, order in visit_order.items() if order > 0], 
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

def generate_greedy_sequence(s_param, engines):
    """Generates a sequence using a greedy shortest-path heuristic."""
    print("\nGenerating greedy sequence...")
    unvisited = list(engines)
    current_engine = 0
    sequence = [current_engine]

    while unvisited:
        # Find minimum switchover time to all unvisited engines
        min_time = float('inf')
        next_engine_candidates = []
        for next_engine in unvisited:
            time = s_param.get((current_engine, next_engine), float('inf'))
            if time < min_time:
                min_time = time
                next_engine_candidates = [next_engine]
            elif time == min_time:
                next_engine_candidates.append(next_engine)
        
        # Select next engine (randomly if tied)
        chosen_engine = random.choice(next_engine_candidates)
        sequence.append(chosen_engine)
        unvisited.remove(chosen_engine)
        current_engine = chosen_engine

    sequence.append(0) # Return to start
    print(f"Greedy Sequence: {' -> '.join(map(str, sequence))}")
    return sequence

def generate_batch_sequences():
    """Generates fixed sequences for batch processing."""
    commercial_first = [0, 1, 2, 3, 4, 5, 0]
    print("\nGenerated batch sequences.")
    print(f"Commercial First: {' -> '.join(map(str, commercial_first))}")
    return {"commercial_first": commercial_first}


if __name__ == "__main__":
    MODEL_FILE = "problem2.mod"
    DATA_FILE = "problem2.dat"
    
    # --- Solve the Model for the Optimal Solution ---
    ampl, optimal_sequence, output = solve_model(MODEL_FILE, DATA_FILE)
    
    # --- Print to console ---
    print("--- Results ---")
    for line in output:
        print(line)

    # --- Get Parameters for Heuristics ---
    s = ampl.get_parameter("s").get_values().to_dict()
    p = ampl.get_parameter("p").get_values().to_dict()
    all_engines = ampl.get_set("E").get_values().to_list()
    # Filter out the dummy engine '0' for sequencing heuristics
    production_engines = [e for e in all_engines if e != 0]

    # --- 1. Generate Visualization for Optimal Sequence ---
    generate_gantt_chart(
        optimal_sequence, s, p,
        title="Optimal Production Schedule",
        filename="problem2_optimal_gantt.pdf"
    )

    # --- 2. Generate Visualization for Greedy Heuristic ---
    greedy_sequence = generate_greedy_sequence(s, production_engines)
    generate_gantt_chart(
        greedy_sequence, s, p,
        title="Greedy (Shortest Setup Time) Heuristic",
        filename="problem2_greedy_gantt.pdf"
    )

    # --- 3. Generate Visualizations for Batch Heuristics ---
    batch_sequences = generate_batch_sequences()
    generate_gantt_chart(
        batch_sequences["commercial_first"], s, p,
        title="Batch Heuristic (Commercial First)",
        filename="problem2_commercial_first_gantt.pdf"
    )

    # --- Conditionally write to file ---
    if os.getenv("AMPLHW_OUTPUT"):
        output_filename = "problem2.amplout"
        with open(output_filename, "w") as f:
            f.write("\n".join(output))
        print(f"\nOutput also written to {output_filename}")