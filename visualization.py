import pandas as pd
import numpy as np
import os, io
import math

w = os.get_terminal_size()[0]

cumulative_m = ['hsiao', 'hsiao-subsampled', 'nugent-hyper', 'nugent-sn1a', 'nugent-sn1bc', 'nugent-sn2l', 'nugent-sn2n', 'nugent-sn2p', 'nugent-sn91bg', 'nugent-sn91t']
with open("./Telegram Desktop/Ib.txt", "r") as f:
    summary = f.read()
summary = pd.read_csv(io.StringIO(summary.replace(" -", "  -")), sep='\s\s+', engine='python')
summary["l"] = np.exp(summary["logl"])
summary["z"] = np.exp(summary["logz"])
summary["aicscore"] = np.exp(-summary["AIC"])

def right_pad(msg, w, c=' '):
    return msg+c*(w-len(msg)) if w-len(msg) > 0 else msg

def left_pad(msg, w, c=' '):
    return c*(w-len(msg))+msg if w-len(msg) > 0 else msg

def center_pad(msg, w, c=' '):
    return c*(math.floor((w-len(msg))/2))+msg+c*(math.ceil((w-len(msg))/2)) if w-len(msg) > 0 else msg

def print_bar_chart(name, data, metric, normalize=True, maxnum=None, minval=None, printmodel=True):
    data=data[:]
    tot = sum(data[metric])
    data[metric]=data[metric]/tot
    print(center_pad(name+(f' (normalized by {tot*100:.2f}%)' if tot>0.0001 else ""), w, '='))
    if minval:
        data=data[data[metric] >= minval]
    data.sort_values(by=[metric], ascending=False, inplace=True)
    if maxnum and len(data) > maxnum:
        data=data[:maxnum]
    if printmodel: wmodel = max([len(i) for i in data["model"]]) + 1
    wtype = max([len(i) for i in data["type"]]) + 1
    maxval = max(data[metric])

    for i in range(len(data)):
        d = data.iloc[i]
        s1 = (right_pad(d["model"], wmodel) if printmodel else '') + left_pad(d["type"], wtype) + left_pad(f'{d[metric]*100:.2f}% ', 9)
        print(s1, round((w-len(s1))*(d[metric]/maxval))*'❚', sep='')
    print()

summary_c = summary[summary["model"].isin(cumulative_m)]
print_bar_chart("Likelihood, 1+", summary_c, "l")
print_bar_chart("Evidence, 1+", summary_c, "z")
print_bar_chart("Likelihood, top 15", summary, "l", maxnum=15, minval=0.0001)
print_bar_chart("Evidence, top 15", summary, "z", maxnum=15, minval=0.0001)
print_bar_chart("AIC, top 15", summary, "aicscore", maxnum=15, minval=0.0001)

summary_s = {}
for i in range(len(summary)):
    d = summary.iloc[i]
    key = d["type"]
    if key not in summary_s: summary_s[key] = [0, 0]
    summary_s[key][0] += d["l"]
    summary_s[key][1] += d["z"]
summary_s = pd.DataFrame([["Σ", i[0], i[1][0], i[1][1]] for i in summary_s.items()], columns=["model", "type", "l", "z"])

print_bar_chart("Likelihood, Σ", summary_s, "l", printmodel=False)
print_bar_chart("Evidence, Σ", summary_s, "z", printmodel=False)
print_bar_chart("Likelihood, Σ1", summary_s[summary_s["type"].isin(["SN Ia", "SN Ib", "SN Ic", "SN Ic-BL", "SN IIL", "SN IIP", "SN IIn"])], "l", printmodel=False)
summary_s2 = {"SN I a  ": ["SN Ia"], "SN I b/c": ["SN Ib", "SN Ic", "SN Ib/c"], "SN IIL/P": ["SN IIL/P", "SN IIP", "SN IIL"], "SN IIn  ": ["SN IIn"]}
summary_s3 = {"SN Ia  ": ["SN Ia"], "SN Ib/c": ["SN Ib", "SN Ic", "SN Ib/c"], "SN II  ": ["SN IIL/P", "SN IIP", "SN IIL", "SN IIn", "SN II", "SN II-pec"]}
summary_s2 = {i[0]: [sum(summary_s[summary_s["type"].isin(i[1])]["l"]), sum(summary_s[summary_s["type"].isin(i[1])]["z"])] for i in summary_s2.items()}
summary_s3 = {i[0]: [sum(summary_s[summary_s["type"].isin(i[1])]["l"]), sum(summary_s[summary_s["type"].isin(i[1])]["z"])] for i in summary_s3.items()}
summary_s2 = pd.DataFrame([["Σ", i[0], i[1][0], i[1][1]] for i in summary_s2.items()], columns=["model", "type", "l", "z"])
summary_s3 = pd.DataFrame([["Σ", i[0], i[1][0], i[1][1]] for i in summary_s3.items()], columns=["model", "type", "l", "z"])
print_bar_chart("Likelihood, Σ2", summary_s2, "l", printmodel=False)
print_bar_chart("Likelihood, Σ3", summary_s3, "l", printmodel=False)
