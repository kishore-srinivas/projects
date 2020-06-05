import networkx as nx
import dwave_networkx as dnx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dimod.reference.samplers import ExactSolver

s5 = nx.star_graph(5)

# solve on QPU
sampler = EmbeddingComposite(DWaveSampler())
print(dnx.min_vertex_cover(s5, sampler))

# solve on classical computer
sampler = ExactSolver()
print(dnx.min_vertex_cover(s5, sampler))