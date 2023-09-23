import itertools
import DSGRN
import dsgrn_utilities.parameter_building as pb
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def apply_thresholding_to_datasets(data, m):
    '''
    data :: dictionary of DSGRN samples from random_parameter_sample_mg_type. Keys are parameter graph index
            and values are the stable MG sets in format 'FP { a, b, c, d }'.
    '''
    data_w_thresholding = {}
    for pgi,fps in data.items():
        data_w_thresholding[pgi] = []
        for fp in fps:
            if 'FP' in fp:
                new_fp = 'FP { '
                for i in [5, 8, 11]:
                    if int(fp[i]) < m/2:
                        new_fp += '0, '
                    else:
                        new_fp += '3, '
                if int(fp[14]) < m/2:
                    new_fp += '0 }'
                else:
                    new_fp += '3 }'
                data_w_thresholding[pgi].append(new_fp)
            else:
                data_w_thresholding[pgi].append(fp)

    return data_w_thresholding

def get_inequalities_for_FPs(ssd,fp_list,network, net_name):
    # put desired fps in canonical order
    fp_list = sorted(fp_list)
    # load results (string of hexcodes : list of FPs)
    #ssd = json.load(open(stable_set_file))
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
    #output = {"(Multistable) Fixed Points" : fp_list, "Parameter inequalities" : all_inequalities}
    #json.dump(output,open("results/{}_inequalities.json".format(net_name),"w"))
    return all_inequalities

def get_inequalities_for_FPs_DSGRN(ssd,fp_list,network,net_name):

    pg = DSGRN.ParameterGraph(network)
    # put desired fps in canonical order
    fp_list = sorted(fp_list)
    # load results (string of hexcodes : list of FPs)
    #ssd = json.load(open(stable_set_file))
    all_inequalities = []
    for pgi,fps in ssd.items():
        fps = sorted(fps) 
        if fps == fp_list:
            parameter = pg.parameter(pgi)
            all_inequalities.append(parameter.partialorders('T'))
    return all_inequalities
    
def get_parameter_inequalities(network,hexcodes,orders):
    param = pb.construct_parameter(network,hexcodes,orders)
    return param.partialorders('T')

def all_state_phase_freq(data, all_states, n = 1):
    '''
    data :: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states :: list of tuples representing FP types
    n :: n=1 if wanting counts, n=sample_size if wanting fequencies
    '''
    fequency_of_state = {}
    for a,b,c,d in all_states:
        count = 0
        for p in data:
            for MS in data[p]:
                if f'{a}, {b}, {c}, {d}' in MS:
                    count += 1
                    continue
        if n == 1:
            fequency_of_state[(a,b,c,d)] = count #this way we get an integer when wanting a count
        else:
            fequency_of_state[(a,b,c,d)] = count/n

    return fequency_of_state

def mono_state_phase_freq(data, all_states, n = 1):
    '''
    data :: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states :: list of tuples representing FP types
    n :: n=1 if wanting counts, n=sample_size if wanting fequencies
    '''
    fequency_of_state = {}
    for a,b,c,d in all_states:
        count = 0
        for p in data:
            Mono = [MS for MS in data[p] if 'FP' in MS]
            if len(Mono) == 1:
                for MS in data[p]:
                    if f'{a}, {b}, {c}, {d}' in MS:
                        count += 1
                        continue
        if n == 1:
            fequency_of_state[(a,b,c,d)] = count #this way we get an integer when wanting a count
        else:
            fequency_of_state[(a,b,c,d)] = count/n

    return fequency_of_state

def bi_state_phase_freq(data, all_states, n = 1):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_single_states_to_plot: list of tuples representing singlular FP type wanting to plot.
    all_pairs_states_to_plot: 2-combinations of all_single_states_to_plot wanting to plot, use 'None' if wanting all. 
    fig_title: title of pie chart.
    fig_name: name of saved figure.
    '''

    bi_stable = list(itertools.combinations(all_states, 2))

    fequency_of_state = {}
    for a,b in bi_stable:
        if a!=b:
            a1,a2,a3,a4 = a
            b1,b2,b3,b4 = b
            count = 0
            for p in data:
                bi = [MS for MS in data[p] if 'FP' in MS]
                a_true = False
                b_true = False
                if len(bi) == 2:
                    for MS in data[p]:
                        if f'{a1}, {a2}, {a3}, {a4}' in MS:
                            a_true = True
                        if f'{b1}, {b2}, {b3}, {b4}' in MS:
                            b_true = True
                    if a_true == True and b_true == True:
                            count += 1
            if n == 1:
                fequency_of_state[(a,b)] = count #this way we get an integer when wanting a count
            else: 
                fequency_of_state[(a,b)] = count/n

    return fequency_of_state

def plot_regression_single_fp(frequency1, frequency2, title, xlabel, ylabel, figname, figsize = (5,5)):
    fig, ax = plt.subplots(figsize = figsize)

    ax.scatter(frequency1, frequency2, color = 'k')

    X = np.array(frequency1).reshape((-1, 1))
    Y = np.array(frequency2)
                
    model = LinearRegression()
    model.fit(X,Y)
    r_sq = model.score(X,Y)
    print(f"coefficient of determination: {r_sq}")
    print(f"intercept: {model.intercept_}")
    print(f"slope: {model.coef_}")
    b = model.intercept_
    m = model.coef_[0]

    lims = [0, np.max([ax.get_xlim(), ax.get_ylim()])]
    print(lims)
    # now plot both limits against eachother
    ax.set_aspect('equal')
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    plt.xticks(np.arange(0, lims[1], step=round(lims[1]/5,3))) 
    plt.yticks(np.arange(0, lims[1], step=round(lims[1]/5,3))) 
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.axline((0, b), slope=m, color='C0', label='by slope')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(figname)
    plt.show()