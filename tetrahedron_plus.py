import random
from tetrahedron import get_stable_Morse_sets
from tetrahedron import get_boolean_stable_Morse_sets

def random_parameter_sample_mg_type(n,parameter_graph):
    params = random.sample(range(0,parameter_graph.size()),n)
    pi_results = {}
    bar_results = {}
    for p in params:
        stable_MS_type_count = {'FP':0, 'FC':0, 'XC':0}
        parameter = parameter_graph.parameter(p)
        stable_MS = get_stable_Morse_sets(parameter)
        bar_results[p] = stable_MS
        for MS in stable_MS:
            for type in stable_MS_type_count:
                if type in MS:
                    stable_MS_type_count[type] += 1
        stable_MS_type = (stable_MS_type_count['FP'], stable_MS_type_count['FC'], stable_MS_type_count['XC'])
        if stable_MS_type not in pi_results:
            pi_results[stable_MS_type] = [p]
        else:
            pi_results[stable_MS_type] += [p]

        #print(p, stable_MS, stable_MS_type_count)
    return pi_results, bar_results

def stable_mg_type_counts_for_strict_Boolean(network_location):
    strict_Bool_MS = get_boolean_stable_Morse_sets(network_location)

    results = {}
    for hex in strict_Bool_MS:
        stable_MS_type_count = {'FP':0, 'FC':0, 'XC':0}
        for MS in strict_Bool_MS[hex]:
            for type in stable_MS_type_count:
                if type in MS:
                    stable_MS_type_count[type] += 1
        stable_MS_type = (stable_MS_type_count['FP'], stable_MS_type_count['FC'], stable_MS_type_count['XC'])
        if stable_MS_type not in results:
            results[stable_MS_type] = [hex]
        else:
            results[stable_MS_type] += [hex]

        #print(p, stable_MS, stable_MS_type_count)
    return results