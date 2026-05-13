# CircuitVisualizer

A matplotlib-based quantum circuit visualizer for [Tequila](https://github.com/tequilahub/tequila) circuits. Draws gates as styled boxes and circles, handles controlled operations, and annotates symbolic parameters.

## Requirements

```
tequila-basic
matplotlib
```

## FAQ

```python
import tequila as tq
from visualizer import show

circuit = tq.gates.H(0)
circuit += tq.gates.X(target=1, control=0)  # CNOT
show(circuit)
```

![Bell state circuit](docs/bell_state.png)

## API

```python
show(circuit, filename=None, show_variables=True, style=None)
```

| Parameter | Type | Description |
|---|---|---|
| `circuit` | `tq.QCircuit` | The Tequila circuit to draw |
| `filename` | `str \| None` | Save to file instead of displaying (e.g. `"out.png"`) |
| `show_variables` | `bool` | Annotate symbolic parameters next to gates (default `True`) |
| `style` | `str \| dict \| None` | Color theme — see [Styles](#styles) below |

`to_matplotlib` is an alias for `show` with identical parameters.

---

## Gate Types

Gates are classified into three visual categories: **logic**, **Pauli rotation**, and **parametrized**. Each category gets its own color in the chosen style.
- Logic Gates: `H`, `X`, `Y`, `Z`, ...  drawn as rectangles
- CNOT gets the special treatment
- Pauli Gates: $e^{-i \frac{\theta}{2} P}$ where $P$ Is a PauliString. Drawn as (connected) circles.

Example:
```python
circuit  = tq.gates.H(0)
circuit += tq.gates.H(1)
circuit += tq.gates.ExpPauli(paulistring="X(0)Y(1)Z(2)", angle="alpha")
show(circuit)
```

![ExpPauli gate](docs/exp_pauli.png)

---

## Styles

Severall colorstyles available (`unia`, `toronto`, `fai`, `tequila`). Pass the name as a string to `show()`.  
Create your own as simple dictionaries (see source code for more).
```python
show(circuit, style={"parametrized": "orange", "parametrized_label": "black"})
```
The other keys are:

| Key | Description                                   |
|---|-----------------------------------------------|
| `logic` | Fill color for H, X, Y, Z, Phase boxes        |
| `logic_label` | Text color inside logic boxes                 |
| `pauli` | Fill color for Rx/Ry/Rz circles (fixed angle) |
| `pauli_label` | Text color inside pauli circles               |
| `parametrized` | Fill color for gates with symbolic angles     |
| `parametrized_label` | Text color inside parametrized gates          |

---

### `default` / `unia`

White logic gates, deep purple Pauli rotations, medium purple parametrized gates.

| Key | Color |
|---|---|
| `logic` | `white` |
| `pauli` | `#3C2673` |
| `parametrized` | `#8c358b` |

![default style](docs/style_default.png)

---

### `fai`

Minimal black-and-white logic and Pauli gates; soft green parametrized gates.

| Key | Color |
|---|---|
| `logic` | `white` |
| `pauli` | `white` |
| `parametrized` | `#66c39e` |

![fai style](docs/style_fai.png)

---

### `toronto`

University of Toronto palette: teal logic gates, dark navy Pauli rotations, royal purple parametrized gates.

| Key | Color |
|---|---|
| `logic` | `#007FA3` |
| `pauli` | `#1E3765` |
| `parametrized` | `#6D247A` |

![toronto style](docs/style_toronto.png)

---

### `tequila`

Tequila project palette: white logic gates, near-black Pauli rotations, hot pink parametrized gates.

| Key | Color |
|---|---|
| `logic` | `white` |
| `pauli` | `#08293D` |
| `parametrized` | `#FC24C1` |

![tequila style](docs/style_tequila.png)

---

## Full Example

The circuit in `visualize.py` exercises every gate type at once:

```python
import tequila as tq
from visualizer import show

circuit  = tq.gates.H(0)
circuit += tq.gates.X(1)
circuit += tq.gates.Y(2)
circuit += tq.gates.X(3, control=1)           # controlled-X
circuit += tq.gates.Rz(1.0, 2)               # fixed rotation
circuit += tq.gates.CNOT(0, 1)
circuit += tq.gates.Ry("a", 0, 1)            # parametrized, controlled
circuit += tq.gates.ExpPauli("X(0)Y(1)", "b") # multi-qubit Pauli exp
circuit += tq.gates.X(3)
circuit += tq.gates.Rx(tq.Variable("c") + 1.0, target=3, control=0)  # expression

show(circuit, show_variables=True, style="toronto")
```

![Full example — toronto style](docs/style_toronto.png)
