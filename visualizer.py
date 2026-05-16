import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from tequila.objective.objective import Variable, FixedVariable

_FONT = "DejaVu Sans"
_LOGIC_GATES = {"X", "Y", "Z", "H", "Phase"}
_DEFAULT_STYLE = {
    "logic": "white",
    "pauli": "#3C2673",
    "parametrized": "#8c358b",
    "logic_label": "black",
    "pauli_label": "white",
    "parametrized_label": "white",
}

_UNIA_STYLE = {
    "logic": "white",
    "pauli": "#3C2673",
    "parametrized": "#8c358b",
    "logic_label": "black",
    "pauli_label": "white",
    "parametrized_label": "white",
}

_FAI_STYLE = {
    "logic": "white",
    "pauli": "white",
    "parametrized": "#66c39e",
    "logic_label": "black",
    "pauli_label": "black",
    "parametrized_label": "black",
}

_TORONTO_STYLE = {
    "logic": "#007FA3",
    "pauli": "#1E3765",
    "parametrized": "#6D247A",
    "logic_label": "black",
    "pauli_label": "#F2F4F7",
    "parametrized_label": "#F2F4F7",
}

_TEQUILA_STYLE = {
    "logic": "white",
    "pauli": "#08293D",
    "parametrized": "#FC24C1",
    "logic_label": "black",
    "pauli_label": "white",
    "parametrized_label": "black",
}

_KNOWN_STYLES = {"default": _DEFAULT_STYLE, "fai": _FAI_STYLE, "unia": _UNIA_STYLE, "toronto": _TORONTO_STYLE, "tequila": _TEQUILA_STYLE}


def _param_label(gate):
    p = gate.parameter
    if isinstance(p, (Variable, FixedVariable)):
        return str(p)
    return "f({})".format(gate.extract_variables())


def _gate_label(gate):
    if gate.is_parameterized():
        return f"{gate.name}({gate.parameter})"
    return gate.name


def _assign_columns(gates):
    n = len(gates)
    return list(range(n)), n, [0.0] * n

def _resolve_style(style):
    if hasattr(style, "lower"):
        if style.lower() in _KNOWN_STYLES: return _KNOWN_STYLES[style.lower()]
    s = dict(_DEFAULT_STYLE)
    if style:
        s.update(style)
    return s


def _gate_color(gate, style):
    if gate.extract_variables():
        return style["parametrized"]
    if gate.name in _LOGIC_GATES:
        return style["logic"]
    if gate.name in ("Rx", "Ry", "Rz") or hasattr(gate, "paulistring"):
        return style["pauli"]
    return style["logic"]


def _label_color(gate, style):
    if gate.extract_variables():
        return style["parametrized_label"]
    if gate.name in _LOGIC_GATES:
        return style["logic_label"]
    if gate.name in ("Rx", "Ry", "Rz") or hasattr(gate, "paulistring"):
        return style["pauli_label"]
    return style["logic_label"]


def _draw_exp_pauli(ax, gate, x, qy, style=None, show_variables=True):
    pauli_items = list(gate.paulistring.items())  # [(qubit, 'X'/'Y'/'Z'), ...]
    qubits = [q for q, _ in pauli_items]

    # Connecting vertical line
    if len(qubits) > 1:
        y_top = qy(min(qubits))
        y_bot = qy(max(qubits))
        ax.plot([x, x], [y_bot, y_top], color="black", lw=1.5, zorder=2)

    resolved = _resolve_style(style)
    color = _gate_color(gate, resolved)
    lcolor = _label_color(gate, resolved)
    r = 0.28
    for q, pauli in pauli_items:
        y = qy(q)
        ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor="black", lw=1.5, zorder=3))
        ax.text(x, y, pauli.lower(), ha="center", va="center", fontfamily=_FONT, fontsize=10, color=lcolor, zorder=4)

    # Parameter label above the topmost qubit
    if show_variables and gate.is_parameterized():
        y_top = qy(min(qubits))
        d = (r + 0.12) / math.sqrt(2)
        ax.text(x + d, y_top + d, _param_label(gate),
                ha="left", va="bottom", fontfamily=_FONT, fontsize=8, color="#444444", zorder=4)


def to_matplotlib(circuit, filename=None, show_variables=True, style=None):
    n_qubits = circuit.n_qubits
    gates = circuit.gates

    style = _resolve_style(style)
    gate_cols, n_cols, gate_offsets = _assign_columns(gates)

    col_spacing = 1.6
    left_margin = 0.8
    right_margin = 0.8
    total_width = left_margin + n_cols * col_spacing + right_margin

    fig_w = max(4.0, total_width * 0.9)
    fig_h = max(2.0, (n_qubits + 1) * 0.9)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_aspect("equal")
    ax.axis("off")

    def qy(q):
        return float(n_qubits - 1 - q)

    def cx(col):
        return left_margin + col * col_spacing + col_spacing / 2

    # Draw qubit wires
    for q in range(n_qubits):
        y = qy(q)
        ax.plot([0, total_width], [y, y], color="black", lw=1.5, zorder=1)
        ax.text(-0.05, y, f"q{q}", ha="right", va="center", fontfamily=_FONT, fontsize=11)

    # Draw gates
    for gate, col, x_off in zip(gates, gate_cols, gate_offsets):
        x = cx(col) + x_off
        targets = gate.target
        controls = gate.control
        name = gate.name

        if hasattr(gate, "paulistring"):
            _draw_exp_pauli(ax, gate, x, qy, style=style, show_variables=show_variables)
        else:
            color = _gate_color(gate, style)
            lcolor = _label_color(gate, style)
            all_qubits = list(targets) + list(controls)
            if len(all_qubits) > 1:
                y_top = qy(min(all_qubits))
                y_bot = qy(max(all_qubits))
                ax.plot([x, x], [y_bot, y_top], color="black", lw=1.5, zorder=2)

            for c in controls:
                ax.add_patch(Circle((x, qy(c)), 0.13, color="black", zorder=3))

            for t in targets:
                y = qy(t)
                if name == "X" and controls:
                    # CNOT-style ⊕ target
                    ax.add_patch(
                        Circle((x, y), 0.28, facecolor="white", edgecolor="black", lw=1.5, zorder=3)
                    )
                    ax.plot([x - 0.28, x + 0.28], [y, y], color="black", lw=1.5, zorder=4)
                    ax.plot([x, x], [y - 0.28, y + 0.28], color="black", lw=1.5, zorder=4)
                elif name in ("Rx", "Ry", "Rz"):
                    axis = name[1].lower()
                    r = 0.28
                    ax.add_patch(
                        Circle((x, y), r, facecolor=color, edgecolor="black", lw=1.5, zorder=3)
                    )
                    ax.text(x, y, axis, ha="center", va="center", fontfamily=_FONT, fontsize=10, color=lcolor, zorder=4)
                    if show_variables and gate.is_parameterized():
                        d = (r + 0.12) / math.sqrt(2)
                        ax.text(x + d, y + d, _param_label(gate),
                                ha="left", va="bottom", fontfamily=_FONT, fontsize=8, color="#444444", zorder=4)
                else:
                    label = name if name in _LOGIC_GATES else _gate_label(gate)
                    box_w = max(0.55, len(label) * 0.115 + 0.15)
                    box_h = 0.5
                    ax.add_patch(
                        FancyBboxPatch(
                            (x - box_w / 2, y - box_h / 2),
                            box_w,
                            box_h,
                            boxstyle="round,pad=0.04",
                            facecolor=color,
                            edgecolor="black",
                            lw=1.5,
                            zorder=3,
                        )
                    )
                    ax.text(x, y, label, ha="center", va="center", fontfamily=_FONT, fontsize=9, color=lcolor, zorder=4)

    ax.set_xlim(-0.6, total_width + 0.2)
    ax.set_ylim(-0.8, n_qubits - 0.2)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=150, bbox_inches="tight")
    else:
        plt.show()

def show(*args, **kwargs):
    to_matplotlib(*args, **kwargs)