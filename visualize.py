import tequila as tq
from visualizer import show
import numpy

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

HF = 1.0-tq.paulis.Projector(wfn="|001>")
UF = tq.gates.GeneralizedRotation(angle=2.0*numpy.pi, generator=HF)

print(tq.compile_circuit(UF))
show(tq.compile_circuit(UF))

for i1 in range(2):
    for i2 in range(2):
        for i3 in range(2):
            wfn=tq.QubitWaveFunction.from_string(f"|{i1}{i2}{i3}>")
            wfn2 = tq.simulate(UF, initial_state=wfn, backend="qulacs")
            print(f"{wfn} --> {wfn2}")
            wfn3 = HF(wfn)
            print(f"{wfn} --> {wfn3}")