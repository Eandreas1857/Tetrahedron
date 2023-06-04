import dsgrn_utilities.select_boolean_params as sbp
import dsgrn_utilities.parameter_building as pb
import DSGRN, ast, time
import matplotlib.pyplot as plt
import json

def get_stable_Morse_sets(param):
    '''
    Get the stable Morse sets for a parameter
    :param param: DSGRN parameter object
    :return: list of stable Morse set annotations
    '''
    stable_sets = []
    domaingraph = DSGRN.DomainGraph(param)
    morsegraph = DSGRN.MorseGraph(domaingraph)
    for i in range(0, morsegraph.poset().size()):
        if len(morsegraph.poset().children(i)) == 0:
            stable_sets.append(morsegraph.annotation(i)[0])
    return stable_sets


def get_boolean_stable_Morse_sets(network):
    boolean_stable_sets = {}
    net = DSGRN.Network(network)
    boolean_params = sbp.subset_boolean_parameters(net)
    print("Number of strict Boolean parameters: {}".format(len(boolean_params)))
    for p in boolean_params:
        stable_morse_sets = get_stable_Morse_sets(p)
        hexcodes = " ".join(p.logic()[node_index].hex() for node_index in range(net.size()))
        boolean_stable_sets[hexcodes] = sorted(stable_morse_sets)
    return boolean_stable_sets


# def count_Morse_sets(stable_sets,val="3"):
#     fp_counts = {}
#     for ms in stable_sets.values():
#         # count the number of nodes that have desired state in an FP
#         ms_str = "\n".join(ms)
#         if ms_str in fp_counts:
#             fp_counts[ms_str]["count"] += 1
#         else:
#             fp_counts[ms_str] = {}
#             fp_counts[ms_str]["count"] = 1
#             # FIXME: This next line will have to be modified when the number of out-edges is not the same for every node.
#             fps = [str(m.count(val))  if m != "FC" else "FC" for m in ms]        
#             fp_counts[ms_str]["multistability_type"] = " ".join(fps)
#     fp_type_counts = {}
#     for ms,d in fp_counts.items():
#         key = d["multistability_type"]
#         if key in fp_type_counts:
#             fp_type_counts[key] += d["count"]
#         else:
#             fp_type_counts[key] = d["count"]
#     return fp_counts, fp_type_counts


def get_parameter_inequalities(network,hexcodes,orders):
    param = pb.construct_parameter(network,hexcodes,orders)
    return ast.literal_eval(param.inequalities())


def get_inequalities_for_FPs(stable_set_file,fp_list,network,net_name):
    # put desired fps in canonical order
    fp_list = sorted(fp_list)
    # load results (string of hexcodes : list of FPs)
    ssd = json.load(open(stable_set_file))
    all_hexes = []
    for hexcodes,fps in ssd.items():
        fps = sorted(fps) 
        if fps == fp_list:
            all_hexes.append(hexcodes.split())
    # network string to DSGRN network
    net = DSGRN.Network(network)
    # create default order for parameter construction
    orders = [list(range(len(net.outputs(i)))) for i in range(net.size())]
    # get all the parameter inequalities with the correct dynamics
    all_inequalities = []
    for hxcds in all_hexes:
        all_inequalities.append(get_parameter_inequalities(net,hxcds,orders))
    output = {"(Multistable) Fixed Points" : fp_list, "Parameter inequalities" : all_inequalities}
    json.dump(output,open("results/{}_inequalities.json".format(net_name),"w"))
    return all_inequalities


def make_data(network,net_name):
    essential_boolean_stable_sets = get_boolean_stable_Morse_sets(network)
    json.dump(essential_boolean_stable_sets,open("results/{}_boolean_stable_sets.json".format(net_name),"w"))
    #FIXME: count_Morse_sets doesn't work for other networks
    # fp_counts,fp_type_counts = count_Morse_sets(essential_boolean_stable_sets)
    # json.dump(fp_counts,open("results/{}_boolean_morse_set_counts.json".format(net_name),"w"))
    # json.dump(fp_type_counts,open("results/{}_boolean_morse_set_type_counts.json".format(net_name),"w"))


def compute(network,net_name,fp_list):
    make_data(network,net_name)
    datafile = "results/{}_boolean_stable_sets.json".format(net_name)
    all_inequalities = get_inequalities_for_FPs(datafile,fp_list,network,net_name)
    # print(all_inequalities)
    print("Number of inequalities = {}".format(len(all_inequalities)))
    return all_inequalities

    
if __name__ == "__main__":
    import json,os,sys
    import adjacency_matrix_to_network as adj


    # folder = "SUMnetworks"
    # for f in os.listdir(folder):
    #     net_name = "SUM_{}".format(f.split(".")[0])
    #     print("\n")
    #     print(net_name)
    #     network, high_vals = adj.get_network(os.path.join(folder,f))
    #     # if any([h>3 for h in high_vals]):
    #     #     continue
    #     net = DSGRN.Network(network)
    #     pg = DSGRN.ParameterGraph(net)
    #     print(pg.size())
    #     N = len(high_vals)
    #     fp_list = []
    #     for k,h in enumerate(high_vals):
    #         fp = [0]*N
    #         fp[k] = h
    #         FP = "FP { " + ", ".join(str(s) for s in fp) + " }"
    #         fp_list.append(FP)
    #     print(network)
    #     print(fp_list)
    #     start = time.time()
    #     compute(network,net_name,fp_list)
    #     print("\nTime elapsed: {} minutes\n".format(round((time.time()-start)/60,ndigits=2)))

    # network = """
    # A : (~B) + (~C) + (~D) : E
    # B : (~A) + (~C) + (~D) : E
    # C : (~A) + (~B) + (~D) : E
    # D : (~A) + (~B) + (~C) : E
    # """

    # net_name = "essential_tetrahedron"

    network = """
    A : (~B)(~C)(~D) : E
    B : (~A)(~C)(~D) : E
    C : (~A)(~B)(~D) : E
    D : (~A)(~B)(~C) : E
    """

    net_name = "essential_tetrahedron_multiplication_3000"
    fplist1 = ["FP { 3, 0, 0, 0 }"]
    ineqs1 = compute(network,net_name,fplist1)
    print(ineqs1[0])
    print("\n")
   
    net_name = "essential_tetrahedron_multiplication_0300"
    fplist2 = ["FP { 0, 3, 0, 0 }"]
    ineqs2 = compute(network,net_name,fplist2)
    print(ineqs2[0])
    print("\n")

    net_name = "essential_tetrahedron_multiplication_0030"
    fplist3 = ["FP { 0, 0, 3, 0 }"]
    ineqs3 = compute(network,net_name,fplist3)
    print(ineqs3[0])
    print("\n")

    net_name = "essential_tetrahedron_multiplication_0003"
    fplist4 = ["FP { 0, 0, 0, 3 }"]
    ineqs4 = compute(network,net_name,fplist4)
    print(ineqs4[0])
    print("\n")

    # network = """
    # A : B : E
    # B : A + C : E
    # C : (B)(~D) : E
    # D : (~C) : E
    # """

    # net_name = "tomas_triple"




