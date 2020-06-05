from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

Q = {('x','x'): -1, ('x','z'): 2, ('z','x'): 0, ('z','z'): -1}
response = sampler.sample_qubo(Q, num_reads=5000)

for d in response.data(['sample', 'energy', 'num_occurrences']):
    print(d.sample, "Energy:", d.energy, "Ocurrences:", d.num_occurrences)