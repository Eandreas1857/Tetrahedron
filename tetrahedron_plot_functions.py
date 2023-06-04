from matplotlib import pyplot as plt
import itertools

def pi_chart_Stable_MS_type(results, n, fig_title, fig_name):
    '''
    results: dict, where key is tuple (#FP, #FC, #PC) and value is list of all params that have that tuple type. 
    Output of random_parameter_sample_mg_type
    fig_title: title of pie chart
    fig_name: name of saved figure
    '''
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(aspect="equal"))
    label = []
    data = []
    A = sorted(results.keys(), key=lambda x: x[0])
    B = sorted(A, key=lambda x: x[1])
    C = sorted(B, key=lambda x: x[2])
    for stable_MS_type in C:
        num = len(results[stable_MS_type])
        perc = round((num/n)*100,1)
        label.append(str(perc) + '% ' +str(stable_MS_type))
        data.append(num)

    wedges, texts = ax.pie(data)
    for w in wedges:
        w.set_linewidth(.5)
        w.set_edgecolor('white')
        
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    ax.legend(wedges, label,
            title="Stable MS Type\n (FP, FC, PC)",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(fig_title)
    plt.savefig(fig_name, dpi=300)
    plt.show()

def all_state_phase_freq_bar_plot(results, all_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states_to_plot: list of tuples representing FP type wanting to plot
    fig_title: title of pie chart
    fig_name: name of saved figure
    '''
    fequency_of_state = {}
    n = len(results)
    for a,b,c,d in all_states_to_plot:
        count = 0
        for p in results:
            for MS in results[p]:
                if f'{a}, {b}, {c}, {d}' in MS:
                    count += 1
                    continue
        fequency_of_state[(a,b,c,d)] = count/n

    labels = [f'{a}, {b}, {c}, {d}' for a,b,c,d in fequency_of_state]
    values = list(fequency_of_state.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(labels, values, width = 0.4)
    plt.xticks(rotation=30)
    plt.title(fig_title)
    plt.savefig(fig_name, dpi=300)
    plt.show()

def mono_state_phase_freq_bar_plot(results, n, all_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states_to_plot: list of tuples representing FP type wanting to plot
    fig_title: title of pie chart
    fig_name: name of saved figure
    '''

    fequency_of_state = {}
    for a,b,c,d in all_states_to_plot:
        count = 0
        for p in results:
            Mono = [MS for MS in results[p] if 'FP' in MS]
            if len(Mono) == 1:
                for MS in results[p]:
                    if f'{a}, {b}, {c}, {d}' in MS:
                        count += 1
                        continue
        fequency_of_state[(a,b,c,d)] = count

    labels = [f'{a}, {b}, {c}, {d}' for a,b,c,d in fequency_of_state]
    values = [i/n for i in fequency_of_state.values()]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(labels, values, width = 0.4)
    plt.xticks(rotation=30)
    plt.title(fig_title)
    plt.savefig(fig_name, dpi=300)
    plt.show()

def bi_state_phase_freq_bar_plot(results, n, all_single_states_to_plot, all_pairs_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_single_states_to_plot: list of tuples representing singlular FP type wanting to plot.
    all_pairs_states_to_plot: 2-combinations of all_single_states_to_plot wanting to plot, use 'None' if wanting all. 
    fig_title: title of pie chart.
    fig_name: name of saved figure.
    '''

    bi_stable = list(itertools.combinations(all_single_states_to_plot, 2))

    fequency_of_state = {}
    for a,b in bi_stable:
        if a!=b:
            a1,a2,a3,a4 = a
            b1,b2,b3,b4 = b
            count = 0
            for p in results:
                bi = [MS for MS in results[p] if 'FP' in MS]
                a_true = False
                b_true = False
                if len(bi) == 2:
                    for MS in results[p]:
                        if f'{a1}, {a2}, {a3}, {a4}' in MS:
                            a_true = True
                        if f'{b1}, {b2}, {b3}, {b4}' in MS:
                            b_true = True
                    if a_true == True and b_true == True:
                            count += 1
            fequency_of_state[(a,b)] = count
    
    labels = []
    values = []
    if all_pairs_states_to_plot == None:
        labels = []
        values = []
        for a,b in fequency_of_state:
            i = fequency_of_state[(a,b)]
            if i != 0:
                labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
                values.append(i/n)
    else: 
        for i in all_pairs_states_to_plot:
            a,b = i
            if i in fequency_of_state:
                values.append(fequency_of_state[i]/n)
            else:
                values.append(fequency_of_state[(b,a)]/n)
            labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
    
    fig = plt.figure(figsize = (12, 6))
    plt.bar(labels, values, width = 0.75)
    plt.xticks(rotation=45, ha='right')
    plt.title(fig_title)
    plt.tight_layout()
    plt.savefig(fig_name, dpi=300)
    plt.show()

#TODO: combine below function with above
def strict_bi_state_phase_freq_bar_plot(results, n, all_single_states_to_plot, all_pairs_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_single_states_to_plot: list of tuples representing singlular FP type wanting to plot.
    all_pairs_states_to_plot: 2-combinations of all_single_states_to_plot wanting to plot, use 'None' if wanting all. 
    fig_title: title of pie chart.
    fig_name: name of saved figure.
    '''

    bi_stable = list(itertools.combinations(all_single_states_to_plot, 2))

    fequency_of_state = {}
    for a,b in bi_stable:
        if a!=b:
            a1,a2,a3,a4 = a
            b1,b2,b3,b4 = b
            count = 0
            for p in results:
                a_true = False
                b_true = False
                if len(results[p]) == 2:
                    for MS in results[p]:
                        if f'{a1}, {a2}, {a3}, {a4}' in MS:
                            a_true = True
                        if f'{b1}, {b2}, {b3}, {b4}' in MS:
                            b_true = True
                    if a_true == True and b_true == True:
                            count += 1
            fequency_of_state[(a,b)] = count
    
    labels = []
    values = []
    if all_pairs_states_to_plot == None:
        labels = []
        values = []
        for a,b in fequency_of_state:
            i = fequency_of_state[(a,b)]
            if i !=0:
                labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
                values.append(i/n)
    else: 
        for i in all_pairs_states_to_plot:
            a,b = i
            if i in fequency_of_state:
                values.append(fequency_of_state[i]/n)
            else:
                values.append(fequency_of_state[(b,a)]/n)
            labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
    
    fig = plt.figure(figsize = (12, 6))
    plt.bar(labels, values, width = 0.75)
    plt.xticks(rotation=45, ha='right')
    plt.title(fig_title)
    plt.tight_layout()
    plt.savefig(fig_name, dpi=300)
    plt.show()

def all_state_phase_freq_bar_plot_w_thresholding(results, theta, all_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states_to_plot: list of tuples representing FP type wanting to plot
    fig_title: title of pie chart
    fig_name: name of saved figure
    '''
    fequency_of_state = {}
    n = len(results)
    for a,b,c,d in all_states_to_plot:
        count = 0
        for p in results:
            for MS in results[p]:
                if 'FP' in MS:
                    if a<theta and int(MS[5])<theta or a>theta and int(MS[5])>theta:
                        if b<theta and int(MS[8])<theta or b>theta and int(MS[8])>theta:
                            if c<theta and int(MS[11])<theta or c>theta and int(MS[11])>theta:
                                if d<theta and int(MS[14])<theta or d>theta and int(MS[14])>theta:
                                    count +=1
        fequency_of_state[(a,b,c,d)] = count/n

    labels = [f'{a}, {b}, {c}, {d}' for a,b,c,d in fequency_of_state]
    values = list(fequency_of_state.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    plt.bar(labels, values, width = 0.4)
    plt.xticks(rotation=30)
    plt.title(fig_title)
    plt.savefig(fig_name, dpi=300)
    plt.show()

def mono_state_phase_freq_bar_plot_w_thresholding(results, n, theta, all_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_states_to_plot: list of tuples representing FP type wanting to plot
    fig_title: title of pie chart
    fig_name: name of saved figure
    '''

    fequency_of_state = {}
    for a,b,c,d in all_states_to_plot:
        count = 0
        for p in results:
            Mono = [MS for MS in results[p] if 'FP' in MS]
            if len(Mono) == 1:
                for MS in results[p]:
                    if 'FP' in MS:
                        if a<theta and int(MS[5])<theta or a>theta and int(MS[5])>theta:
                            if b<theta and int(MS[8])<theta or b>theta and int(MS[8])>theta:
                                if c<theta and int(MS[11])<theta or c>theta and int(MS[11])>theta:
                                    if d<theta and int(MS[14])<theta or d>theta and int(MS[14])>theta:
                                        count +=1
        fequency_of_state[(a,b,c,d)] = count

    labels = [f'{a}, {b}, {c}, {d}' for a,b,c,d in fequency_of_state]
    values = [i/n for i in fequency_of_state.values()]
    
    fig = plt.figure(figsize = (10, 5))

    plt.bar(labels, values, width = 0.4)
    plt.xticks(rotation=30)
    plt.title(fig_title)
    plt.savefig(fig_name, dpi=300)
    plt.show()

def bi_state_phase_freq_bar_plot_w_thresholding(results, n, theta, all_single_states_to_plot, all_pairs_states_to_plot, fig_title, fig_name):
    '''
    results: dict, where key is parameter or hex code and value is list of stable MS. 
    Output of random_parameter_sample_mg_type.
    all_single_states_to_plot: list of tuples representing singlular FP type wanting to plot.
    all_pairs_states_to_plot: 2-combinations of all_single_states_to_plot wanting to plot, use 'None' if wanting all. 
    fig_title: title of pie chart.
    fig_name: name of saved figure.
    '''

    bi_stable = list(itertools.combinations(all_single_states_to_plot, 2))

    fequency_of_state = {}
    for a,b in bi_stable:
        if a!=b:
            a1,a2,a3,a4 = a
            b1,b2,b3,b4 = b
            count = 0
            for p in results:
                bi = [MS for MS in results[p] if 'FP' in MS]
                a_true = False
                b_true = False
                if len(bi) == 2:
                    for MS in results[p]:
                        if 'FP' in MS:
                            if a1<theta and int(MS[5])<theta or a1>theta and int(MS[5])>theta:
                                if a2<theta and int(MS[8])<theta or a2>theta and int(MS[8])>theta:
                                    if a3<theta and int(MS[11])<theta or a3>theta and int(MS[11])>theta:
                                        if a4<theta and int(MS[14])<theta or a4>theta and int(MS[14])>theta:
                                            a_true = True
                            if b1<theta and int(MS[5])<theta or b1>theta and int(MS[5])>theta:
                                if b2<theta and int(MS[8])<theta or b2>theta and int(MS[8])>theta:
                                    if b3<theta and int(MS[11])<theta or b3>theta and int(MS[11])>theta:
                                        if b4<theta and int(MS[14])<theta or b4>theta and int(MS[14])>theta:
                                            b_true = True
                    if a_true == True and b_true == True:
                            count += 1
            fequency_of_state[(a,b)] = count
    
    labels = []
    values = []
    if all_pairs_states_to_plot == None:
        labels = []
        values = []
        for a,b in fequency_of_state:
            i = fequency_of_state[(a,b)]
            if i != 0:
                labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
                values.append(i/n)
    else: 
        for i in all_pairs_states_to_plot:
            a,b = i
            if i in fequency_of_state:
                values.append(fequency_of_state[i]/n)
            else:
                values.append(fequency_of_state[(b,a)]/n)
            labels.append(f'{a[0]}{a[1]}{a[2]}{a[3]}, {b[0]}{b[1]}{b[2]}{b[3]}')
    
    fig = plt.figure(figsize = (12, 6))
    plt.bar(labels, values, width = 0.75)
    plt.xticks(rotation=45, ha='right')
    plt.title(fig_title)
    plt.tight_layout()
    plt.savefig(fig_name, dpi=300)
    plt.show()
    