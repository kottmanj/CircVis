import tequila as tq
from visualizer import show

circuit = tq.gates.H(0)
circuit+= tq.gates.X(1)
circuit+= tq.gates.Y(2)
circuit+= tq.gates.X(3,control=1)
circuit+= tq.gates.Rz(1.0, 2)
circuit+= tq.gates.CNOT(0,1)
circuit+= tq.gates.Ry("a",0,1)
circuit+= tq.gates.ExpPauli(paulistring="X(0)Y(1)", angle="b")
circuit+= tq.gates.X(3)
circuit+= tq.gates.Rx(angle=tq.Variable("c")+1.0, target=3, control=0)
show(circuit, show_variables=True, style="unia")
