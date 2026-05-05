import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ── helpers ───────────────────────────────────────────────────────────────────

def add_exit(G: nx.DiGraph, return_nodes: list) -> str:
    """Add a single EXIT node and wire all return_nodes to it."""
    G.add_node("EXIT", label="EXIT")
    for rn in return_nodes:
        G.add_edge(rn, "EXIT", label="")
    return "EXIT"


def cyclomatic_complexity(G: nx.DiGraph) -> int:
    """M = E - N + 2P  (P=1 for single strongly-connected component)."""
    return G.number_of_edges() - G.number_of_nodes() + 2


def draw_cfg(G: nx.DiGraph, title: str, filename: str,
             decision_nodes: list = None, exit_nodes: list = None,
             cyclomatic: int = None) -> None:
    decision_nodes = decision_nodes or []
    exit_nodes = exit_nodes or []

    plt.figure(figsize=(14, 9))
    full_title = f"{title}  (M = {cyclomatic})" if cyclomatic is not None else title
    plt.title(full_title, fontsize=13, fontweight="bold")

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except Exception:
        pos = nx.spring_layout(G, seed=42, k=2.5)

    node_colors = []
    nodes = list(G.nodes())
    for n in nodes:
        if n == "EXIT":
            node_colors.append("#ff6b6b")
        elif n in exit_nodes:
            node_colors.append("#ff6b6b")
        elif n in decision_nodes:
            node_colors.append("#ffd93d")
        elif n == nodes[0]:
            node_colors.append("#6bcb77")
        else:
            node_colors.append("#4d96ff")

    labels = nx.get_node_attributes(G, "label")
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=2200, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7,
                            font_weight="bold")
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=18,
                           connectionstyle="arc3,rad=0.08",
                           edge_color="#333333", width=1.4)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=6, label_pos=0.3)

    legend = [
        mpatches.Patch(color="#6bcb77", label="Entry"),
        mpatches.Patch(color="#4d96ff", label="Action"),
        mpatches.Patch(color="#ffd93d", label="Decision"),
        mpatches.Patch(color="#ff6b6b", label="Exit / Return"),
    ]
    plt.legend(handles=legend, loc="upper right", fontsize=8)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filename}")


def print_paths(G: nx.DiGraph, entry: str, exit_node: str = "EXIT",
                cutoff: int = 12) -> None:
    try:
        paths = list(nx.all_simple_paths(G, source=entry,
                                         target=exit_node, cutoff=cutoff))
        labels = nx.get_node_attributes(G, "label")
        print(f"  Execution paths (source→EXIT): {len(paths)} found")
        for i, path in enumerate(paths, 1):
            readable = " → ".join(labels.get(n, n) for n in path)
            print(f"    P{i}: {readable}")
    except Exception as e:
        print(f"  Path enumeration skipped: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# CFG definitions
# ══════════════════════════════════════════════════════════════════════════════

def build_cfg_task1() -> nx.DiGraph:
    """
    process_data – 2 nested loops + 2 conditions.
    Decision points: n2 (outer loop), n3 (if <0), n5 (inner loop), n6 (if %2)
    M = E - N + 2 = 13 - 9 + 2 = 6  (≈ D+1 = 4+1 = 5 simplified)

    NOTE: back-edges (n4→n2, n5↔n2, n7→n5, n6→n5) create cycles;
    all_simple_paths cannot traverse cycles – basis paths listed manually.
    """
    G = nx.DiGraph()
    nodes = {
        "n1": "total = 0",
        "n2": "i<len(data)?\n[outer loop]",
        "n3": "data[i] < 0?",
        "n4": "continue",
        "n5": "j<data[i]?\n[inner loop]",
        "n6": "j % 2 == 0?",
        "n7": "total += j",
        "n8": "return total",
    }
    for nid, lbl in nodes.items():
        G.add_node(nid, label=lbl)

    edges = [
        ("n1", "n2", ""),
        ("n2", "n3", "T"),
        ("n2", "n8", "F"),
        ("n3", "n4", "T"),
        ("n3", "n5", "F"),
        ("n4", "n2", "continue"),
        ("n5", "n6", "T"),
        ("n5", "n2", "F"),
        ("n6", "n7", "T"),
        ("n6", "n5", "F"),
        ("n7", "n5", ""),
    ]
    for u, v, lbl in edges:
        G.add_edge(u, v, label=lbl)
    add_exit(G, ["n8"])
    return G


def build_cfg_task2() -> nx.DiGraph:
    """
    check_access – 1 compound condition (A∧B)∨C → M=2.
    With short-circuit expansion: 3 atomic checks → M=4 (decision-point method).
    """
    G = nx.DiGraph()
    nodes = {
        "n1": "role=='user'?",
        "n2": "is_active?",
        "n3": "is_admin?",
        "n4": "return True",
        "n5": "return False",
    }
    for nid, lbl in nodes.items():
        G.add_node(nid, label=lbl)

    # Short-circuit: if role!='user' skip is_active, go straight to is_admin
    G.add_edge("n1", "n2", label="T")
    G.add_edge("n1", "n3", label="F")
    G.add_edge("n2", "n4", label="T")      # role='user' AND active → True
    G.add_edge("n2", "n3", label="F")      # role='user' BUT NOT active → check admin
    G.add_edge("n3", "n4", label="T")      # is_admin → True
    G.add_edge("n3", "n5", label="F")      # none → False
    add_exit(G, ["n4", "n5"])
    return G

def build_cfg_task3() -> nx.DiGraph:
    """
    process_matrix – 3 nested loops + 1 condition.
    Decision points: n2, n3, n4, n5 → M = E-N+2 = 12-9+2 = 5
    """
    G = nx.DiGraph()
    nodes = {
        "n1": "count = 0",
        "n2": "i<len(matrix)?\n[outer]",
        "n3": "j<len(matrix[i])?\n[middle]",
        "n4": "matrix[i][j] > 0?",
        "n5": "k<matrix[i][j]?\n[inner]",
        "n6": "count += k % 3",
        "n7": "return count",
    }
    for nid, lbl in nodes.items():
        G.add_node(nid, label=lbl)

    edges = [
        ("n1", "n2", ""),
        ("n2", "n3", "T"),
        ("n2", "n7", "F"),
        ("n3", "n4", "T"),
        ("n3", "n2", "F"),          # middle loop exhausted → next outer iter
        ("n4", "n5", "T"),
        ("n4", "n3", "F"),          # condition false → next j
        ("n5", "n6", "T"),
        ("n5", "n3", "F"),          # inner loop done → next j
        ("n6", "n5", ""),           # next k
    ]
    for u, v, lbl in edges:
        G.add_edge(u, v, label=lbl)
    add_exit(G, ["n7"])
    return G

def build_cfg_task4() -> nx.DiGraph:
    """
    validate_input – 3 sequential guards, last with compound AND.
    Decision points: n1, n3, n5 → M = E-N+2 = 10-8+2 = 4
    """
    G = nx.DiGraph()
    nodes = {
        "n1": "not user?",
        "n2": "return 'Missing user'",
        "n3": "len(pwd) < 8?",
        "n4": "return 'Weak password'",
        "n5": "any(digit)?",
        "n6": "any(upper)?",
        "n7": "return 'Valid'",
        "n8": "return 'Invalid'",
    }
    for nid, lbl in nodes.items():
        G.add_node(nid, label=lbl)

    G.add_edge("n1", "n2", label="T")
    G.add_edge("n1", "n3", label="F")
    G.add_edge("n3", "n4", label="T")
    G.add_edge("n3", "n5", label="F")
    G.add_edge("n5", "n6", label="T (digit found)")
    G.add_edge("n5", "n8", label="F (no digit)")
    G.add_edge("n6", "n7", label="T (upper found)")
    G.add_edge("n6", "n8", label="F (no upper)")
    add_exit(G, ["n2", "n4", "n7", "n8"])
    return G

def build_cfg_task5() -> nx.DiGraph:
    """
    update_task_status – 3 if-guards, last with compound AND.
    With compound expansion: 4 decision nodes → M = E-N+2 = 14-11+2 = 5
    """
    G = nx.DiGraph()
    nodes = {
        "n1": "valid_transitions\n= {...}",
        "n2": "status==\nnew_status?",
        "n3": "return 'No change'",
        "n4": "new_status not in\nvalid_transitions?",
        "n5": "return 'Invalid\ntransition'",
        "n6": "role not in\n[admin,mgr]?",
        "n7": "new_status\n=='closed'?",
        "n8": "return 'Permission\ndenied'",
        "n9": "task.status\n= new_status",
        "n10": "return 'Updated'",
    }
    for nid, lbl in nodes.items():
        G.add_node(nid, label=lbl)

    edges = [
        ("n1",  "n2",  ""),
        ("n2",  "n3",  "T"),
        ("n2",  "n4",  "F"),
        ("n4",  "n5",  "T"),
        ("n4",  "n6",  "F"),
        ("n6",  "n7",  "T (not admin)"),
        ("n6",  "n9",  "F (admin/mgr)"),
        ("n7",  "n8",  "T (closing)"),
        ("n7",  "n9",  "F (not closing)"),
        ("n9",  "n10", ""),
    ]
    for u, v, lbl in edges:
        G.add_edge(u, v, label=lbl)
    add_exit(G, ["n3", "n5", "n8", "n10"])
    return G

# ══════════════════════════════════════════════════════════════════════════════
# Analysis runner
# ══════════════════════════════════════════════════════════════════════════════

CONFIGS = [
    {
        "name":      "Task 1 – process_data",
        "builder":   build_cfg_task1,
        "entry":     "n1",
        "decisions": ["n2", "n3", "n5", "n6"],
        "exits":     ["n8"],
        "filename":  "cfg_images/cfg_task1.png",
        "basis_paths": [
            "P1 [empty data]: n1→n2(F)→n8→EXIT",
            "P2 [negative]:   n1→n2(T)→n3(T)→n4→n2(F)→n8→EXIT",
            "P3 [zero value]: n1→n2(T)→n3(F)→n5(F)→n2(F)→n8→EXIT",
            "P4 [even j]:     n1→n2(T)→n3(F)→n5(T)→n6(T)→n7→n5(F)→n2(F)→n8→EXIT",
            "P5 [odd j]:      n1→n2(T)→n3(F)→n5(T)→n6(F)→n5(F)→n2(F)→n8→EXIT",
        ],
    },
    {
        "name":      "Task 2 – check_access",
        "builder":   build_cfg_task2,
        "entry":     "n1",
        "decisions": ["n1", "n2", "n3"],
        "exits":     ["n4", "n5"],
        "filename":  "cfg_images/cfg_task2.png",
    },
    {
        "name":      "Task 3 – process_matrix",
        "builder":   build_cfg_task3,
        "entry":     "n1",
        "decisions": ["n2", "n3", "n4", "n5"],
        "exits":     ["n7"],
        "filename":  "cfg_images/cfg_task3.png",
        "basis_paths": [
            "P1 [empty outer]:  n1→n2(F)→n7→EXIT",
            "P2 [empty middle]: n1→n2(T)→n3(F)→n2(F)→n7→EXIT",
            "P3 [cond false]:   n1→n2(T)→n3(T)→n4(F)→n3(F)→n2(F)→n7→EXIT",
            "P4 [inner=1 iter]: n1→n2(T)→n3(T)→n4(T)→n5(T)→n6→n5(F)→n3(F)→n2(F)→n7→EXIT",
            "P5 [inner>1 iter]: extends P4 with additional n6→n5 back-edges",
        ],
    },
    {
        "name":      "Task 4 – validate_input",
        "builder":   build_cfg_task4,
        "entry":     "n1",
        "decisions": ["n1", "n3", "n5", "n6"],
        "exits":     ["n2", "n4", "n7", "n8"],
        "filename":  "cfg_images/cfg_task4.png",
    },
]


def main():
    os.makedirs("cfg_images", exist_ok=True)

    for cfg in CONFIGS:
        G = cfg["builder"]()
        M = cyclomatic_complexity(G)

        print(f"\n{'='*60}")
        print(f" {cfg['name']}")
        print(f"{'='*60}")
        print(f"  Nodes (N) : {G.number_of_nodes()}")
        print(f"  Edges (E) : {G.number_of_edges()}")
        print(f"  M = E - N + 2 = {G.number_of_edges()} - "
              f"{G.number_of_nodes()} + 2 = {M}")
        print(f"  → Minimum {M} independent test cases for full path coverage.")

        if "basis_paths" in cfg:
            print("  Basis paths (loop graphs – listed manually):")
            for bp in cfg["basis_paths"]:
                print(f"    {bp}")
        else:
            print_paths(G, entry=cfg["entry"])

        draw_cfg(
            G,
            title=cfg["name"],
            filename=cfg["filename"],
            decision_nodes=cfg["decisions"],
            exit_nodes=cfg["exits"] + ["EXIT"],
            cyclomatic=M,
        )

    print("\n✓ All CFG images written to cfg_images/")


if __name__ == "__main__":
    main()
