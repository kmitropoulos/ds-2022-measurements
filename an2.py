fpfiles = ["fp1.txt", "fp2.txt", "fp3.txt", "fp4.txt"]
fpddfiles = ["fpdd1.txt", "fpdd2.txt", "fpdd3.txt", "fpdd4.txt"]
fffiles = ["ff1.txt", "ff2.txt", "ff3.txt", "ff4.txt"]
ddfiles = ["dd1.txt", "dd2.txt", "dd3.txt", "dd4.txt"]
labelsize = 14
titlesize = 16


import matplotlib.pyplot as plt
import numpy as np
import statistics as st


def get_measurements(files):
    res = dict()
    for file in files:
        with open(file,"r") as fd:
            c = 0
            tw = 0
            ms = []
            for line in fd:
                if "Forking" in line:
                    if tw == 1:
                        if (c in res):
                            res[c] += ms.copy()
                        else:
                            res[c] = ms.copy()
                        c = 0
                        tw = 0
                        ms = []
                elif "Duration" in line:
                    tw = 1
                    c += 1
                    time = float(line.split()[-1][:-1])
                    ms.append(time)
            if tw == 1:
                if (c in res):
                    res[c] += ms.copy()
                else:
                    res[c] = ms.copy()
    print(res)
    return res


def latency_plot(res, exp):
    x = np.array(list(res.keys()))
    y = np.array([st.mean(res[x]) for x in res.keys()]) # Effectively y = x**2
    e = np.array([st.stdev(res[x]) for x in res.keys()])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    ax.errorbar(xpos, y, yerr=e, fmt='-o', ecolor="red", capsize=5, barsabove=False)
    ax.set_ylabel("Average latency (s)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Execution Latency - exp {exp}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    plt.savefig(f'images/lat_av_{exp}.png')
    plt.show()


def joined_latency(res1,res2, exp1, exp2):
    mn = min([len(res1), len(res2)])
    x = np.array(list(res1.keys())[:mn])
    y1 = np.array([st.mean(res1[x]) for x in res1.keys()][:mn]) # Effectively y = x**2
    e1 = np.array([st.stdev(res1[x]) for x in res1.keys()][:mn])
    y2 = np.array([st.mean(res2[x]) for x in res2.keys()][:mn])
    e2 = np.array([st.stdev(res2[x]) for x in res2.keys()][:mn])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    ax.errorbar(xpos, y1, yerr=e1, label={exp1},  fmt='-o', ecolor="red", capsize=5, barsabove=False)
    ax.errorbar(xpos, y2, yerr=e2, label={exp2}, fmt='--s', ecolor="green", capsize=5, barsabove=False)
    ax.set_ylabel("Average latency (s)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Execution Latency - exp {exp1} / {exp2}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    plt.legend()
    plt.savefig(f'images/lat_av_comp_{exp1}_{exp2}.png')
    plt.show()

def pd(res,exp):
    x = np.array(list(res.keys()))
    y = np.array([sum([abs(j - st.mean(res[x]))/st.mean(res[x]) for j in res[x]])/len(res[x]) for x in res.keys()])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    bars = ax.bar(xpos, y)
    ax.set_ylabel("Deviation (ratio)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Percentage Deviation of Execution latency - exp {exp}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.savefig(f'images/cm_pd_{exp}.png')
    plt.show()

def ad(res,exp):
    x = np.array(list(res.keys()))
    y = np.array([sum([abs(j - st.mean(res[x])) for j in res[x]])/len(res[x]) for x in res.keys()])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    bars = ax.bar(xpos, y)
    ax.set_ylabel("Deviation (s)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Absolute Deviation of Execution latency - exp {exp}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.savefig(f'images/cm_ad_{exp}.png')
    plt.show()

def joined_pd(res1,res2, exp1, exp2):
    mn = min([len(res1), len(res2)])
    x = np.array(list(res1.keys())[:mn])
    y1 = np.array([sum([abs(j - st.mean(res1[x]))/st.mean(res1[x]) for j in res1[x]])/len(res1[x]) for x in list(res1.keys())[:mn]])
    y2 = np.array([sum([abs(j - st.mean(res2[x]))/st.mean(res2[x]) for j in res2[x]])/len(res2[x]) for x in list(res1.keys())[:mn]])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    bars1 = ax.bar(xpos-0.2, y1, width=0.4, label=exp1)
    bars2 = ax.bar(xpos+0.2, y2, width=0.4, label=exp2)
    ax.set_ylabel("Deviation (ratio)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Percentage Deviation of Execution latency - exp {exp1}/{exp2}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.legend()
    # ax.bar_label(bars, ['%.2f' % i for i in y], padding=2, color='r', fontsize=10)
    plt.savefig(f'images/joined_pd_{exp1}_{exp2}.png')
    plt.show()

def joined_ad(res1,res2, exp1, exp2):
    mn = min([len(res1), len(res2)])
    x = np.array(list(res1.keys())[:mn])
    y1 = np.array([sum([abs(j - st.mean(res1[x])) for j in res1[x]])/len(res1[x]) for x in list(res1.keys())[:mn]])
    y2 = np.array([sum([abs(j - st.mean(res2[x])) for j in res2[x]])/len(res2[x]) for x in list(res1.keys())[:mn]])
    xpos = np.arange(len(x))
    fig, ax = plt.subplots()
    bars1 = ax.bar(xpos-0.2, y1, width=0.4, label=exp1)
    bars2 = ax.bar(xpos+0.2, y2, width=0.4, label=exp2)
    ax.set_ylabel("Deviation (s)", fontsize=labelsize)
    ax.set_xlabel("Parallel requests", fontsize=labelsize)
    ax.set_xticks(xpos)
    ax.set_xticklabels(x)
    ax.set_title(f"Average Absolute Deviation of Execution latency - exp {exp1}/{exp2}", fontsize=titlesize, wrap=True)
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.legend()
    # ax.bar_label(bars, ['%.2f' % i for i in y], padding=2, color='r', fontsize=10)
    plt.savefig(f'images/joined_ad_{exp1}_{exp2}.png')
    plt.show()
    


fpres = get_measurements(fpfiles)
fpddres = get_measurements(fpddfiles)
ffres = get_measurements(fffiles)
ddres = get_measurements(ddfiles)



latency_plot(fpres, "fp")
latency_plot(fpddres, "fp-dd")
latency_plot(ffres, "ff")
latency_plot(ddres, "dd")

joined_latency(fpres, fpddres, "fp", "fp-dd")

pd(fpres, "fp")
pd(fpddres, "fp-dd")
pd(ffres, "ff")
pd(ddres, "dd")

ad(fpres, "fp")
ad(fpddres, "fp-dd")
ad(ffres, "ff")
ad(ddres, "dd")

joined_pd(fpres, fpddres, "fp", "fp-dd")
joined_ad(fpres, fpddres, "fp", "fp-dd")
