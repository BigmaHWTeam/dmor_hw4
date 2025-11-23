import matplotlib.pyplot as plt
import networkx as nx
import random
from dataclasses import dataclass, field
from typing import Dict, Optional, List


@dataclass
class BranchNode:
    node_id: str
    parent_id: Optional[str] = None
    branch_constraint: str = ""  # e.g., "x1 <= 3"
    z_value: Optional[float] = None
    x_values: Dict[str, float] = field(default_factory=dict)
    pruned_reason: Optional[str] = None  # e.g., "Infeasible", "Bound", "Integer Opt"
    is_integer_solution: bool = False
    is_dominated: bool = False

    @property
    def label(self) -> str:
        lines = [f"{self.node_id}"]
        if self.branch_constraint:
            # Shorten constraint for display if too long
            c = self.branch_constraint
            if len(c) > 20:
                c = (
                    c.replace("WingSpar", "WS")
                    .replace("WingRib", "WR")
                    .replace("FuselagePanel", "FP")
                )
            lines.append(c)

        if self.pruned_reason == "Infeasible":
            lines.append("Infeasible")
        else:
            if self.z_value is not None:
                lines.append(f"Z = {self.z_value:,.2f}")

            # Format x values compactly
            # Use short names
            short_names = {"WingSpar": "WS", "WingRib": "WR", "FuselagePanel": "FP"}
            x_strs = []
            for k, v in self.x_values.items():
                sn = short_names.get(k, k)
                x_strs.append(f"{sn}={v:.2f}")

            # Split into lines of 2 variables
            for i in range(0, len(x_strs), 2):
                lines.append(", ".join(x_strs[i : i + 2]))

        if self.pruned_reason and self.pruned_reason != "Infeasible":
            lines.append(f"[{self.pruned_reason}]")

        return "\n".join(lines)

    @property
    def color(self) -> str:
        if self.pruned_reason == "Infeasible":
            return "#E0E0E0"  # Light Gray
        if self.is_integer_solution and not self.is_dominated:
            return "#90EE90"  # Light Green
        if self.is_dominated:
            return "#FFB347"  # Pastel Orange (Suboptimal)
        return "#ADD8E6"  # Light Blue (Continuous)


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Positions nodes in a hierarchical layout, allocating width based on subtree size (number of leaves).
    """
    if not nx.is_tree(G):
        # Fallback for non-perfect trees
        return nx.shell_layout(G)

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = random.choice(list(G.nodes))

    def count_leaves(node):
        children = list(G.successors(node))
        if not children:
            return 1
        return sum(count_leaves(c) for c in children)

    def _hierarchy_pos(node, left, right, vert_loc, pos):
        pos[node] = ((left + right) / 2, vert_loc)
        children = list(G.successors(node))
        if not children:
            return pos

        total_leaves = sum(count_leaves(c) for c in children)

        # Distribute width based on leaf count
        current_left = left
        width_per_leaf = (right - left) / total_leaves

        for child in children:
            child_leaves = count_leaves(child)
            child_width = child_leaves * width_per_leaf
            _hierarchy_pos(
                child,
                current_left,
                current_left + child_width,
                vert_loc - vert_gap,
                pos,
            )
            current_left += child_width

        return pos

    return _hierarchy_pos(root, xcenter - width / 2, xcenter + width / 2, vert_loc, {})


def draw_tree():
    # AUTOMATICALLY GENERATED DATA
    nodes_data = [
        BranchNode(
            node_id="relaxation",
            parent_id=None,
            branch_constraint="Relaxation",
            z_value=6510631.58,
            x_values={"WingSpar": 168.42, "WingRib": 105.26},
            is_integer_solution=False,
        ),
        BranchNode(
            node_id="node01",
            parent_id="relaxation",
            branch_constraint="x['WingSpar'] >= 169",
            z_value=6473861.67,
            x_values={"WingSpar": 169.0, "WingRib": 103.33},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node02",
            parent_id="node01",
            branch_constraint="x['WingRib'] >= 104",
            z_value=None,
            x_values={},
            pruned_reason="Infeasible",
        ),
        BranchNode(
            node_id="node03",
            parent_id="node01",
            branch_constraint="x['WingRib'] <= 103",
            z_value=6471358.2,
            x_values={"FuselagePanel": 0.2, "WingSpar": 169.0, "WingRib": 103.0},
            is_integer_solution=False,
            is_dominated=False,
        ),
        BranchNode(
            node_id="node09",
            parent_id="relaxation",
            branch_constraint="x['WingSpar'] <= 168",
            z_value=6509841.6,
            x_values={"WingSpar": 168.0, "WingRib": 105.6},
        ),
        BranchNode(
            node_id="node10",
            parent_id="node09",
            branch_constraint="x['WingRib'] >= 106",
            z_value=6508903.5,
            x_values={"WingSpar": 167.5, "WingRib": 106.0},
        ),
        BranchNode(
            node_id="node11",
            parent_id="node10",
            branch_constraint="x['WingSpar'] >= 168",
            z_value=None,
            x_values={},
            pruned_reason="Infeasible",
        ),
        BranchNode(
            node_id="node12",
            parent_id="node10",
            branch_constraint="x['WingSpar'] <= 167",
            z_value=6507965.4,
            x_values={"WingSpar": 167.0, "WingRib": 106.4},
        ),
        BranchNode(
            node_id="node13",
            parent_id="node12",
            branch_constraint="x['WingRib'] >= 107",
            z_value=6506558.25,
            x_values={"WingSpar": 166.25, "WingRib": 107.0},
        ),
        BranchNode(
            node_id="node14",
            parent_id="node13",
            branch_constraint="x['WingSpar'] >= 167",
            z_value=None,
            x_values={},
            pruned_reason="Infeasible",
        ),
        BranchNode(
            node_id="node15",
            parent_id="node13",
            branch_constraint="x['WingSpar'] <= 166",
            z_value=6506089.2,
            x_values={"WingSpar": 166.0, "WingRib": 107.2},
        ),
        BranchNode(
            node_id="node16",
            parent_id="node15",
            branch_constraint="x['WingRib'] >= 108",
            z_value=6504213.0,
            x_values={"WingSpar": 165.0, "WingRib": 108.0},
            is_integer_solution=True,
        ),
        BranchNode(
            node_id="node17",
            parent_id="node15",
            branch_constraint="x['WingRib'] <= 107",
            z_value=6506010.5,
            x_values={"FuselagePanel": 0.17, "WingSpar": 166.0, "WingRib": 107.0},
        ),
        BranchNode(
            node_id="node18",
            parent_id="node17",
            branch_constraint="x['FuselagePanel'] >= 1",
            z_value=6503271.75,
            x_values={"FuselagePanel": 1.0, "WingSpar": 164.75, "WingRib": 107.0},
            pruned_reason="Node 16",
            is_dominated=True,
        ),
        BranchNode(
            node_id="node19",
            parent_id="node17",
            branch_constraint="x['FuselagePanel']<=0",
            z_value=6500927.00,
            x_values={"WingSpar": 166, "WingRib": 107},
            is_dominated=True,
            pruned_reason="Node 16",
        ),
        BranchNode(
            node_id="node20",
            parent_id="node12",
            branch_constraint="x['WingRib'] <= 106",
            z_value=6507808.00,
            x_values={"FuselagePanel": 0.33, "WingSpar": 167.00, "WingRib": 106.0},
        ),
        BranchNode(
            node_id="node21",
            parent_id="node20",
            branch_constraint="x['FuselagePanel'] >= 1",
            z_value=6505617.00,
            x_values={"FuselagePanel": 1, "WingSpar": 166.00, "WingRib": 106.0},
            is_integer_solution=True,
        ),
        BranchNode(
            node_id="node22",
            parent_id="node20",
            branch_constraint="x['FuselagePanel'] <= 0",
            z_value=6497641.00,
            x_values={"WingSpar": 167.00, "WingRib": 106.0},
            is_dominated=True,
            pruned_reason="Node 21",
        ),
        BranchNode(
            node_id="node23",
            parent_id="node09",
            branch_constraint="x['WingRib'] <= 105",
            z_value=6509841.60,
            x_values={"FuselagePanel": 0.5, "WingSpar": 168.00, "WingRib": 105.6},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node24",
            parent_id="node23",
            branch_constraint="x['FuselagePanel'] >= 1",
            z_value=6509369.4,
            x_values={"FuselagePanel": 1, "WingSpar": 168.00, "WingRib": 104.4},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node25",
            parent_id="node24",
            branch_constraint="x['WingRib'] >= 105",
            z_value=6507962.25,
            x_values={"FuselagePanel": 1, "WingSpar": 167.25, "WingRib": 105},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node26",
            parent_id="node25",
            branch_constraint="x['WingSpar'] >= 168",
            pruned_reason="Infeasible",
        ),
        BranchNode(
            node_id="node27",
            parent_id="node25",
            branch_constraint="x['WingSpar'] <= 167",
            z_value=6507414.5,
            x_values={"FuselagePanel": 1.17, "WingSpar": 167, "WingRib": 105},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node28",
            parent_id="node27",
            branch_constraint="x['FuselagePanel'] >= 2",
            z_value=6504675.75,
            x_values={"FuselagePanel": 2, "WingSpar": 165.75, "WingRib": 105},
            is_dominated=True,
            pruned_reason="Node 21",
        ),
        BranchNode(
            node_id="node29",
            parent_id="node27",
            branch_constraint="x['FuselagePanel'] <= 1",
            z_value=6502331.00,
            x_values={"FuselagePanel": 1, "WingSpar": 167, "WingRib": 105},
            is_dominated=True,
            pruned_reason="Node 21",
        ),
        BranchNode(
            node_id="node30",
            parent_id="node24",
            branch_constraint="x['WingRib'] <= 104",
            z_value=6509212.00,
            x_values={"FuselagePanel": 1.33, "WingSpar": 168, "WingRib": 104},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node31",
            parent_id="node30",
            branch_constraint="x['FuselagePanel'] >= 2",
            z_value=6508897.20,
            x_values={"FuselagePanel": 2, "WingSpar": 168, "WingRib": 103.2},
            is_dominated=False,
        ),
        BranchNode(
            node_id="node32",
            parent_id="node31",
            branch_constraint="x['WingRib'] >= 104",
            z_value=6507021.00,
            x_values={"FuselagePanel": 2, "WingSpar": 167, "WingRib": 104},
            is_dominated=False,
            is_integer_solution=True,
            pruned_reason="Optimal Solution",
        ),
        BranchNode(
            node_id="node33",
            parent_id="node31",
            branch_constraint="x['WingRib'] <= 103",
            z_value=6508818.50,
            x_values={"FuselagePanel": 2.17, "WingSpar": 168, "WingRib": 103},
        ),
        BranchNode(
            node_id="node34",
            parent_id="node33",
            branch_constraint="x['FuselagePanel'] >= 3",
            z_value=6508178.13,
            x_values={"FuselagePanel": 3, "WingSpar": 167.87, "WingRib": 102.11},
        ),
        BranchNode(
            node_id="node35",
            parent_id="node34",
            branch_constraint="x['WingSpar'] >= 168",
            z_value=6499821.33,
            x_values={"FuselagePanel": 3, "WingSpar": 168, "WingRib": 101.67},
            is_dominated=True,
            pruned_reason="Node 32",
        ),
        BranchNode(
            node_id="node36",
            parent_id="node34",
            branch_constraint="x['WingSpar'] <= 167",
            z_value=6506548.8,
            x_values={"FuselagePanel": 3, "WingSpar": 167, "WingRib": 102.80},
            is_dominated=True,
            pruned_reason="Node 32",
        ),
        BranchNode(
            node_id="node37",
            parent_id="node33",
            branch_constraint="x['FuselagePanel'] <= 2",
            z_value=6503735.00,
            x_values={"FuselagePanel": 2, "WingSpar": 168, "WingRib": 103},
            is_dominated=True,
            pruned_reason="Node32",
        ),
        BranchNode(
            node_id="node38",
            parent_id="node30",
            branch_constraint="x['FuselagePanel'] <= 1",
            z_value=6499045.00,
            x_values={"FuselagePanel": 1, "WingSpar": 168, "WingRib": 104},
            is_integer_solution=True,
            is_dominated=True,
            pruned_reason="Node 32",
        ),
        BranchNode(
            node_id="node39",
            parent_id="node23",
            branch_constraint="x['FuselagePanel'] <= 0",
            z_value=6494355.00,
            x_values={"FuselagePanel": 0, "WingSpar": 168, "WingRib": 105},
            is_integer_solution=True,
            is_dominated=True,
            pruned_reason="Node32",
        ),
        BranchNode(
            node_id="node04",
            parent_id="node03",
            branch_constraint="x['FuselagePanels'] >= 1",
            z_value=6461344.33,
            x_values={"FuselagePanel": 1, "WingSpar": 169, "WingRib": 101.67},
        ),
        BranchNode(
            node_id="node05",
            parent_id="node04",
            branch_constraint="x['WingRib'] >= 102",
            z_value=6461344.33,
            x_values={"FuselagePanel": 1, "WingSpar": 169, "WingRib": 101.67},
            pruned_reason="Infeasible",
        ),
        BranchNode(
            node_id="node06",
            parent_id="node04",
            branch_constraint="x['WingRib'] <= 101",
            z_value=6456337.4,
            x_values={"FuselagePanel": 1.4, "WingSpar": 169, "WingRib": 101},
        ),
        BranchNode(
            node_id="node07",
            parent_id="node06",
            branch_constraint="x['FuselagePanel'] >= 2",
            z_value=6448827.0,
            x_values={"FuselagePanel": 2, "WingSpar": 169, "WingRib": 100},
            is_integer_solution=True,
        ),
        BranchNode(
            node_id="node08",
            parent_id="node06",
            branch_constraint="x['FuselagePanel'] <= 1",
            z_value=6448642.00,
            x_values={"FuselagePanel": 1, "WingSpar": 169.2, "WingRib": 101},
            is_dominated=True,
            pruned_reason="Node 07",
        ),
    ]

    # Create Graph
    G = nx.DiGraph()
    node_map = {n.node_id: n for n in nodes_data}

    edges = []
    for n in nodes_data:
        if n.parent_id and n.parent_id in node_map:
            edges.append((n.parent_id, n.node_id))

    G.add_nodes_from([n.node_id for n in nodes_data])
    G.add_edges_from(edges)

    # Layout
    try:
        # We calculate a vertical layout first, then rotate it.
        # width=total_vertical_span_in_rotated_view
        pos = hierarchy_pos(G, root="relaxation", width=25.0, vert_gap=0.2)
        # Rotate to horizontal: x_new = -y_old (depth), y_new = x_old (spread)
        pos = {u: (-y * 20, x) for u, (x, y) in pos.items()}
    except Exception:
        pos = nx.spring_layout(G, k=0.9, iterations=50)

    # Draw
    # Taller figure for horizontal layout
    fig, ax = plt.subplots(figsize=(20, 25))

    # Draw edges
    nx.draw_networkx_edges(
        G, pos, ax=ax, arrows=True, arrowstyle="-|>", node_size=2000, edge_color="gray"
    )

    # Draw nodes
    for node_id, (x, y) in pos.items():
        node_info = node_map.get(node_id)
        if not node_info:
            continue

        label = node_info.label
        color = node_info.color

        bbox_props = dict(boxstyle="round,pad=0.3", fc=color, ec="black", alpha=0.9)

        ax.text(x, y, label, ha="center", va="center", size=9, bbox=bbox_props)

    # Custom Legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="#90EE90", edgecolor="black", label="Integer Solution"),
        Patch(
            facecolor="#ADD8E6", edgecolor="black", label="Candidate (Bound >= Best)"
        ),
        Patch(
            facecolor="#FFB347", edgecolor="black", label="Suboptimal (Bound < Best)"
        ),
        Patch(facecolor="#E0E0E0", edgecolor="black", label="Infeasible"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=12)

    ax.set_title("Branch and Bound Search Tree (Problem 4)")
    plt.axis("off")

    output_file = "binary_search_tree.pdf"
    plt.savefig(output_file, format="pdf", bbox_inches="tight")
    print(f"Tree visualization saved to {output_file}")


if __name__ == "__main__":
    draw_tree()
