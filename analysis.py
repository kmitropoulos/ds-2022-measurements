fpfiles = ["fp1.txt", "fp2.txt", "fp3.txt", "fp4.txt"]
fpddfiles = ["fpdd1.txt", "fpdd2.txt", "fpdd3.txt", "fpdd4.txt"]
fffiles = ["ff1.txt", "ff2.txt", "ff3.txt", "ff4.txt"]
ddfiles = ["dd1.txt", "dd2.txt", "dd3.txt", "dd4.txt"]
titles = ["fp"]
labelsize = 14
titlesize = 16


import matplotlib.pyplot as plt
import numpy as np
import statistics as st
import math

def get_measurements(files):
    res = dict()
    for file in files:
        res[file] = dict()
        with open(file,"r") as fd:
            c = 0
            tw = 0
            ms = []
            for line in fd:
                if "Forking" in line:
                    if tw == 1:
                        res[file][c] = ms.copy()
                        c = 0
                        tw = 0
                        ms = []
                elif "Duration" in line:
                    tw = 1
                    c += 1
                    time = float(line.split()[-1][:-1])
                    ms.append(time)
            if tw == 1:
                res[file][c] = ms.copy()

            # print(res[file])
    print(res)
    return res

def latency_plot(res):
    for i in res.keys():
        x = np.array(list(res[i].keys()))
        y = np.array([st.mean(res[i][x]) for x in res[i].keys()]) # Effectively y = x**2
        e = np.array([st.stdev(res[i][x]) for x in res[i].keys()])
        xpos = np.arange(len(x))

        fig, ax = plt.subplots()
        ax.errorbar(xpos, y, yerr=e, fmt='-o', ecolor="red", capsize=5, barsabove=False)
        ax.set_ylabel("Average latency (s)", fontsize=labelsize)
        ax.set_xlabel("Parallel requests", fontsize=labelsize)
        ax.set_xticks(xpos)
        ax.set_xticklabels(x)
        ax.set_title(f"Average execution latency - exp {i}", fontsize=titlesize, wrap=True)
        ax.grid(True)
        plt.savefig(f'images/lat_{i.split(".")[0]}.png')
        plt.show()
        # fig, ax = plt.subplots()
        # plt.title(f"Average completion latency - exp {i}")
        
        # ax.errorbar(x, y, e, ecolor="red", fmt='-o')
        # ax.xlabel("Parallel requests")
        # ax.ylabel("Average latency (s)")
        # plt.grid()
        

def pd(res,titles):
    data = dict()

    for i in res[list(res.keys())[0]].keys():
        data[i] = []
    for i in res.keys():
        x = np.array(list(res[i].keys()))
        y = np.array([sum([abs(j - st.mean(res[i][x]))/st.mean(res[i][x]) for j in res[i][x]])/len(res[i][x]) for x in res[i].keys()])
        for lb, d in zip(list(res[i].keys()), y):
            # print(lb, d)
            data[lb].append(d)
        xpos = np.arange(len(x))

        fig, ax = plt.subplots()
        bars = ax.bar(xpos, y)
        ax.set_ylabel("Deviation (ratio)", fontsize=labelsize)
        ax.set_xlabel("Parallel requests", fontsize=labelsize)
        ax.set_xticks(xpos)
        ax.set_xticklabels(x)
        ax.set_title(f"Average Percentage Deviation of Execution latency - exp {i}", fontsize=titlesize, wrap=True)
        ax.grid(True)
        ax.set_axisbelow(True)
        # ax.bar_label(bars, ['%.2f' % i for i in y], padding=2, color='r', fontsize=10)
        plt.savefig(f'images/pd_{i.split(".")[0]}.png')
        plt.show()

def ad(res,titles):
    data = dict()

    for i in res[list(res.keys())[0]].keys():
        data[i] = []
    for i in res.keys():
        x = np.array(list(res[i].keys()))
        y = np.array([sum([abs(j - st.mean(res[i][x])) for j in res[i][x]])/len(res[i][x]) for x in res[i].keys()])
        for lb, d in zip(list(res[i].keys()), y):
            # print(lb, d)
            data[lb].append(d)
        xpos = np.arange(len(x))

        fig, ax = plt.subplots()
        bars = ax.bar(xpos, y)
        ax.set_ylabel("Deviation (s)", fontsize=labelsize)
        ax.set_xlabel("Number of Parallel requests", fontsize=labelsize)
        ax.set_xticks(xpos)
        ax.set_xticklabels(x)
        ax.set_title(f"Average Absolute Deviation of Execution latency - exp {i}", fontsize=titlesize, wrap=True)
        ax.grid(True)
        ax.set_axisbelow(True)
        # ax.bar_label(bars, ['%.2f' % i for i in y], padding=2, color='r', fontsize=10)
        plt.savefig(f'images/ad_{i.split(".")[0]}.png')
        plt.show()

    
    # print(data)
    # fig, ax = plt.subplots()
    # x = np.array(list(data.keys()))
    # y = np.array([st.mean(data[i]) for i in data.keys()])
    # e = np.array([st.stdev(data[i]) for i in data.keys()])
    # xpos = np.arange(len(x))
    # bars = ax.bar(xpos, y, yerr=e, align='center', alpha=0.7, ecolor='black', capsize=8)
    # ax.set_ylabel("Average Deviation")
    # ax.set_xlabel("Parallel requests")
    # ax.set_xticks(xpos)
    # ax.set_xticklabels(x)
    # ax.set_title(f"Average PDVC - exp: {titles}")
    # ax.grid(True)
    # ax.set_axisbelow(True)
    # plt.savefig(f'images/tot_pdvc_{titles}.png')
    # plt.show()
    



fp = get_measurements(fpfiles)
ff = get_measurements(fffiles)
dd = get_measurements(ddfiles)

latency_plot(fp)
latency_plot(ff)
latency_plot(dd)
pd(fp, "fp")
pd(ff, "ff")
pd(dd, "dd")
ad(fp, "fp")
ad(ff, "ff")
ad(dd, "dd")

