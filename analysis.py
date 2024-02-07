import pandas as pd
import sncosmo


data = pd.read_csv('ZTF23abhvrhm.txt', sep=',')

data = dict(map(lambda col_kv: (col_kv[0], list(map(lambda row_kv: row_kv[1], col_kv[1].items()))), data.items()))

print(data)

summary = ["model", "type", "amplitude", "t0", "logz", "logl", "AIC", "score(logz)", "score(logl)"]
summary = dict([(i, []) for i in summary])

cumulative_m = ['hsiao', 'hsiao-subsampled', 'nugent-hyper', 'nugent-sn1a', 'nugent-sn1bc', 'nugent-sn2l', 'nugent-sn2n', 'nugent-sn2p', 'nugent-sn91bg', 'nugent-sn91t']

x0x1c = ['salt2']

for msource in ['hsiao', 'hsiao-subsampled', 'nugent-hyper', 'nugent-sn1a', 'nugent-sn1bc', 'nugent-sn2l', 'nugent-sn2n', 'nugent-sn2p', 'nugent-sn91bg', 'nugent-sn91t', 's11-2004hx', 's11-2005gi', 's11-2005hl', 's11-2005hm', 's11-2005lc', 's11-2006fo', 's11-2006jl', 's11-2006jo', 'snana-04d1la', 'snana-04d4jv', 'snana-2004fe', 'snana-2004gq', 'snana-2004gv', 'snana-2004hx', 'snana-2004ib', 'snana-2005gi', 'snana-2005hm', 'snana-2006ep', 'snana-2006ez', 'snana-2006fo', 'snana-2006gq', 'snana-2006iw', 'snana-2006ix', 'snana-2006jl', 'snana-2006jo', 'snana-2006kn', 'snana-2006kv', 'snana-2006lc', 'snana-2006ns', 'snana-2007iz', 'snana-2007kw', 'snana-2007ky', 'snana-2007lb', 'snana-2007ld', 'snana-2007lj', 'snana-2007ll', 'snana-2007lx', 'snana-2007lz', 'snana-2007md', 'snana-2007ms', 'snana-2007nc', 'snana-2007nr', 'snana-2007nv', 'snana-2007og', 'snana-2007pg', 'snana-2007y', 'snana-sdss004012', 'snana-sdss014475', 'snf-2011fe', 'v19-1987a', 'v19-1987a-corr', 'v19-1993j', 'v19-1993j-corr', 'v19-1994i', 'v19-1994i-corr', 'v19-1998bw', 'v19-1998bw-corr', 'v19-1999dn', 'v19-1999dn-corr', 'v19-1999em', 'v19-1999em-corr', 'v19-2002ap', 'v19-2002ap-corr', 'v19-2004aw', 'v19-2004aw-corr', 'v19-2004et', 'v19-2004et-corr', 'v19-2004fe', 'v19-2004fe-corr', 'v19-2004gq', 'v19-2004gq-corr', 'v19-2004gt', 'v19-2004gt-corr', 'v19-2004gv', 'v19-2004gv-corr', 'v19-2005bf', 'v19-2005bf-corr', 'v19-2005hg', 'v19-2005hg-corr', 'v19-2006aa', 'v19-2006aa-corr', 'v19-2006ep', 'v19-2007gr', 'v19-2007gr-corr', 'v19-2007od', 'v19-2007od-corr', 'v19-2007pk', 'v19-2007pk-corr', 'v19-2007ru', 'v19-2007ru-corr', 'v19-2007uy', 'v19-2007uy-corr', 'v19-2007y', 'v19-2007y-corr', 'v19-2008aq', 'v19-2008aq-corr', 'v19-2008ax', 'v19-2008ax-corr', 'v19-2008bj', 'v19-2008bj-corr', 'v19-2008bo', 'v19-2008bo-corr', 'v19-2008d', 'v19-2008d-corr', 'v19-2008fq', 'v19-2008fq-corr', 'v19-2008in', 'v19-2008in-corr', 'v19-2009bb', 'v19-2009bb-corr', 'v19-2009bw', 'v19-2009bw-corr', 'v19-2009dd', 'v19-2009dd-corr', 'v19-2009ib', 'v19-2009ib-corr', 'v19-2009ip', 'v19-2009ip-corr', 'v19-2009iz', 'v19-2009iz-corr', 'v19-2009jf', 'v19-2009jf-corr', 'v19-2009kr', 'v19-2009kr-corr', 'v19-2009n', 'v19-2009n-corr', 'v19-2010al', 'v19-2010al-corr', 'v19-2011bm', 'v19-2011bm-corr', 'v19-2011dh', 'v19-2011dh-corr', 'v19-2011ei', 'v19-2011ei-corr', 'v19-2011fu', 'v19-2011fu-corr', 'v19-2011hs', 'v19-2011hs-corr', 'v19-2011ht', 'v19-2011ht-corr', 'v19-2012a', 'v19-2012a-corr', 'v19-2012ap', 'v19-2012ap-corr', 'v19-2012au', 'v19-2012au-corr', 'v19-2012aw', 'v19-2012aw-corr', 'v19-2013ab', 'v19-2013ab-corr', 'v19-2013am', 'v19-2013am-corr', 'v19-2013by', 'v19-2013by-corr', 'v19-2013df', 'v19-2013df-corr', 'v19-2013ej', 'v19-2013ej-corr', 'v19-2013fs', 'v19-2013fs-corr', 'v19-2013ge', 'v19-2013ge-corr', 'v19-2014g', 'v19-2014g-corr', 'v19-2016bkv', 'v19-2016bkv-corr', 'v19-2016gkg', 'v19-2016gkg-corr', 'v19-2016x', 'v19-2016x-corr', 'v19-asassn14jb', 'v19-asassn14jb-corr', 'v19-asassn15oz', 'v19-asassn15oz-corr', 'v19-iptf13bvn', 'v19-iptf13bvn-corr', 'whalen-z15b', 'whalen-z15d', 'whalen-z15g', 'whalen-z25b', 'whalen-z25d', 'whalen-z25g', 'whalen-z40b', 'whalen-z40g', \
    'salt2']:
    summary["model"].append(msource)

    model = sncosmo.Model(source=msource)
    type = "N/A"
    for m in sncosmo.models._SOURCES.get_loaders_metadata():
        if msource == m["name"]:
            type = m["type"]
    summary["type"].append(type)

    salt = msource in x0x1c

    model.set(z=0.065)
    # run the fit
    fparams= [ 't0', 'amplitude'] if not salt else ['t0', 'x0', 'x1', 'c']
    result, fitted_model = sncosmo.nest_lc(
        data, model,
        fparams,{},guess_amplitude_bound=1)

    print("===========RUN 1:=============", msource)
    print("Number of degrees of freedom in fit:", result.ndof)
    print("The result contains the following attributes:\n", result.keys())
    print("logZ", result.logz)
    print("h", result.h)
    print("logl", result.logl)
    print("parameters", result.parameters)


    summary["logz"].append(result.logz)
    if not salt:
        summary["amplitude"].append(str(result.param_dict["amplitude"]) + " ± " + str(result.errors["amplitude"]))
    else:
        summary["amplitude"].append("x0=" + str(result.param_dict["x0"]) + " ± " + str(result.errors["x0"]) + "; x1=" + str(result.param_dict["x1"]) + " ± " + str(result.errors["x1"]) + "; c=" + str(result.param_dict["c"]) + " ± " + str(result.errors["c"]))
    summary["t0"].append(str(result.param_dict["t0"]) + " ± " + str(result.errors["t0"]))

    sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)

    # create a model ================== 2
    bounds2={}
    for p in fparams:
        bounds2[p]=(result.param_dict[p],result.param_dict[p])
    model.set(z=0.065)
    # run the fit
    result, fitted_model = sncosmo.nest_lc(
        data, model,
        fparams,
        bounds=bounds2)

    print("===========RUN 2:=============", msource)
    #print("Number of degrees of freedom in fit:", result.ndof)
    #print("The result contains the following attributes:\n", result.keys())
    print("logZ", result.logz)
    print("h", result.h)
    print("logl", result.logl[0])
    print("parameters", result.parameters)


    summary["logl"].append(result.logl[0])
    summary["AIC"].append(2*result.ndof-2*result.logl[0])

    sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)

import math
ltot = sum([math.exp(i) for i in summary["logl"]])
summary["score(logl)"] = [math.exp(i)/ltot for i in summary["logl"]]
ztot = sum([math.exp(i) for i in summary["logz"]])
summary["score(logz)"] = [math.exp(i)/ztot for i in summary["logz"]]

summary = pd.DataFrame(summary).sort_values(by=['score(logl)'], ascending=False)
print(summary.to_string())
summary.to_csv("Iabc_test.csv", index=False)
summary.to_excel("output.xlsx")
