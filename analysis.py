%%file pool.py
# then 
# import sys
# !{sys.executable} pool.py
import pandas as pd
import sncosmo
import redback
# variables
transients = ['ZTF21aciuhqw']
index = 0
while index < len(transients):
    guess_red_shift = 0
    red_shift = 0.065
    transient = transients[index]
    print("\n\t\tPROGRESS:", index, "/", len(transients), "transients\n")

    if index+1 < len(transients) and type(transients[index+1]) is not str:
        red_shift = transients[index+1]
        index+=2
    else:
        guess_red_shift = 1
        index+=1


    data = redback.get_data.get_lasair_data(transient=transient, transient_type='supernova')

    sncosmo_data = pd.DataFrame()
    sncosmo_data["time"] = data["time"]
    sncosmo_data["band"] = data["band"]
    sncosmo_data["flux"] = data["flux_density(mjy)"]
    sncosmo_data["flux_err"] = data["flux_density_error"]
    sncosmo_data["zp"] = [25] * len(data)
    sncosmo_data["zpsys"] = data["system"].str.lower()
    data = sncosmo_data

    data = dict(map(lambda col_kv: (col_kv[0], list(map(lambda row_kv: row_kv[1], col_kv[1].items()))), data.items()))

    print(data)

    summary = ["model", "type", "amplitude", "t0", "logz", "logl", "AIC", "score(logz)", "score(logl)"]
    summary = dict([(i, []) for i in summary])

    cumulative_m = ['hsiao', 'hsiao-subsampled', 'nugent-hyper', 'nugent-sn1a', 'nugent-sn1bc', 'nugent-sn2l', 'nugent-sn2n', 'nugent-sn2p', 'nugent-sn91bg', 'nugent-sn91t'] # for lookup purposes

    x0x1c = ['salt2'] # for lookup purposes

    def analyze_model(msource):
        summary1 = {}
        summary1["model"] = msource

        model = sncosmo.Model(source=msource)
        type = "N/A"
        for m in sncosmo.models._SOURCES.get_loaders_metadata():
            if msource == m["name"]:
                type = m["type"]
        summary1["type"] = type

        salt = msource in x0x1c

        model.set(z=red_shift)

        # run the fit
        bounds={'z':(0.0001, 0.2)}
        fparams = ['z'] if guess_red_shift else []
        fparams+= ['t0', 'amplitude'] if not salt else ['t0', 'x0', 'x1', 'c']
        if salt:
            result, fitted_model = sncosmo.fit_lc(
                data, model,
                fparams, bounds=bounds)
            p = result.parameters
            bounds |= {'x0':(0, p[2]*10), 'x1':(p[3],p[3]), 'c': (p[4],p[4])}

        result, fitted_model = sncosmo.nest_lc(
            data, model,
            fparams, bounds=bounds, guess_amplitude_bound=not salt)

        print("===========RUN 1:=============", msource)
        #print("Number of degrees of freedom in fit:", result.ndof)
        #print("The result contains the following attributes:\n", result.keys())
        #print("logZ", result.logz)
        #print("h", result.h)
        #print("logl", result.logl)
        #print("parameters", result.parameters)


        summary1["logz"] = result.logz
        if not salt:
            summary1["amplitude"] = str(result.param_dict["amplitude"]) + " ± " + str(result.errors["amplitude"])
        else:
            summary1["amplitude"] = "x0=" + str(result.param_dict["x0"]) + " ± " + str(result.errors["x0"]) + "; x1=" + str(result.param_dict["x1"]) + " ± " + str(result.errors["x1"]) + "; c=" + str(result.param_dict["c"]) + " ± " + str(result.errors["c"])
        summary1["t0"] = str(result.param_dict["t0"]) + " ± " + str(result.errors["t0"])

        #sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)

        # create a model ================== 2
        bounds2={}
        for p in fparams:
            bounds2[p]=(result.param_dict[p],result.param_dict[p])
        model.set(z=red_shift)
        # run the fit
        result, fitted_model = sncosmo.nest_lc(
            data, model,
            fparams,
            bounds=bounds2)

        print("===========RUN 2:=============", msource)
        #print("Number of degrees of freedom in fit:", result.ndof)
        #print("The result contains the following attributes:\n", result.keys())
        #print("logZ", result.logz)
        #print("h", result.h)
        #print("logl", result.logl[0])
        #print("parameters", result.parameters)


        summary1["logl"] = result.logl[0]
        summary1["AIC"] = 2*result.ndof-2*result.logl[0]

        #sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)
        return summary1


    import multiprocessing
    pool = multiprocessing.Pool(4)
    summary0 = pool.map(analyze_model,  ['salt2', 'hsiao', 'hsiao-subsampled', 'nugent-hyper', 'nugent-sn1a', 'nugent-sn1bc', 'nugent-sn2l', 'nugent-sn2n', 'nugent-sn2p', 'nugent-sn91bg', 'nugent-sn91t', 's11-2004hx', 's11-2005gi', 's11-2005hl', 's11-2005hm', 's11-2005lc', 's11-2006fo', 's11-2006jl', 's11-2006jo', 'snana-04d1la', 'snana-04d4jv', 'snana-2004fe', 'snana-2004gq', 'snana-2004gv', 'snana-2004hx', 'snana-2004ib', 'snana-2005gi', 'snana-2005hm', 'snana-2006ep', 'snana-2006ez', 'snana-2006fo', 'snana-2006gq', 'snana-2006iw', 'snana-2006ix', 'snana-2006jl', 'snana-2006jo', 'snana-2006kn', 'snana-2006kv', 'snana-2006lc', 'snana-2006ns', 'snana-2007iz', 'snana-2007kw', 'snana-2007ky', 'snana-2007lb', 'snana-2007ld', 'snana-2007lj', 'snana-2007ll', 'snana-2007lx', 'snana-2007lz', 'snana-2007md', 'snana-2007ms', 'snana-2007nc', 'snana-2007nr', 'snana-2007nv', 'snana-2007og', 'snana-2007pg', 'snana-2007y', 'snana-sdss004012', 'snana-sdss014475', 'snf-2011fe', 'v19-1987a', 'v19-1987a-corr', 'v19-1993j', 'v19-1993j-corr', 'v19-1994i', 'v19-1994i-corr', 'v19-1998bw', 'v19-1998bw-corr', 'v19-1999dn', 'v19-1999dn-corr', 'v19-1999em', 'v19-1999em-corr', 'v19-2002ap', 'v19-2002ap-corr', 'v19-2004aw', 'v19-2004aw-corr', 'v19-2004et', 'v19-2004et-corr', 'v19-2004fe', 'v19-2004fe-corr', 'v19-2004gq', 'v19-2004gq-corr', 'v19-2004gt', 'v19-2004gt-corr', 'v19-2004gv', 'v19-2004gv-corr', 'v19-2005bf', 'v19-2005bf-corr', 'v19-2005hg', 'v19-2005hg-corr', 'v19-2006aa', 'v19-2006aa-corr', 'v19-2006ep', 'v19-2007gr', 'v19-2007gr-corr', 'v19-2007od', 'v19-2007od-corr', 'v19-2007pk', 'v19-2007pk-corr', 'v19-2007ru', 'v19-2007ru-corr', 'v19-2007uy', 'v19-2007uy-corr', 'v19-2007y', 'v19-2007y-corr', 'v19-2008aq', 'v19-2008aq-corr', 'v19-2008ax', 'v19-2008ax-corr', 'v19-2008bj', 'v19-2008bj-corr', 'v19-2008bo', 'v19-2008bo-corr', 'v19-2008d', 'v19-2008d-corr', 'v19-2008fq', 'v19-2008fq-corr', 'v19-2008in', 'v19-2008in-corr', 'v19-2009bb', 'v19-2009bb-corr', 'v19-2009bw', 'v19-2009bw-corr', 'v19-2009dd', 'v19-2009dd-corr', 'v19-2009ib', 'v19-2009ib-corr', 'v19-2009ip', 'v19-2009ip-corr', 'v19-2009iz', 'v19-2009iz-corr', 'v19-2009jf', 'v19-2009jf-corr', 'v19-2009kr', 'v19-2009kr-corr', 'v19-2009n', 'v19-2009n-corr', 'v19-2010al', 'v19-2010al-corr', 'v19-2011bm', 'v19-2011bm-corr', 'v19-2011dh', 'v19-2011dh-corr', 'v19-2011ei', 'v19-2011ei-corr', 'v19-2011fu', 'v19-2011fu-corr', 'v19-2011hs', 'v19-2011hs-corr', 'v19-2011ht', 'v19-2011ht-corr', 'v19-2012a', 'v19-2012a-corr', 'v19-2012ap', 'v19-2012ap-corr', 'v19-2012au', 'v19-2012au-corr', 'v19-2012aw', 'v19-2012aw-corr', 'v19-2013ab', 'v19-2013ab-corr', 'v19-2013am', 'v19-2013am-corr', 'v19-2013by', 'v19-2013by-corr', 'v19-2013df', 'v19-2013df-corr', 'v19-2013ej', 'v19-2013ej-corr', 'v19-2013fs', 'v19-2013fs-corr', 'v19-2013ge', 'v19-2013ge-corr', 'v19-2014g', 'v19-2014g-corr', 'v19-2016bkv', 'v19-2016bkv-corr', 'v19-2016gkg', 'v19-2016gkg-corr', 'v19-2016x', 'v19-2016x-corr', 'v19-asassn14jb', 'v19-asassn14jb-corr', 'v19-asassn15oz', 'v19-asassn15oz-corr', 'v19-iptf13bvn', 'v19-iptf13bvn-corr', 'whalen-z15b', 'whalen-z15d', 'whalen-z15g', 'whalen-z25b', 'whalen-z25d', 'whalen-z25g', 'whalen-z40b', 'whalen-z40g'\
                                        ] )

    # collect results and fill in the blanks
    summary = {}
    for i, d in enumerate(summary0):
        for k in d.keys():
            if not k in summary:
                summary[k]=[type(d[k])()] * i
            if len(summary[k])<i:
                summary[k]+=[type(d[k])()] * (i-len(summary[k]))
            if len(summary[k])>i:
                raise Exception(f'Somehow got more rows than had data ({len(summary[k])} > {i})')
            summary[k]+=[d[k]]
        for k in summary.keys():
            if len(summary[k])<(i+1):
                summary[k]+=[type(summary[k][0])()] * (i-len(summary[k]))
            if len(summary[k])>(i+1):
                raise Exception(f'Somehow got more rows than had data ({len(summary[k])} > {i})')
        

    import math
    ltot = sum([math.exp(i) for i in summary["logl"]])
    summary["score(logl)"] = [math.exp(i)/ltot for i in summary["logl"]]
    ztot = sum([math.exp(i) for i in summary["logz"]])
    summary["score(logz)"] = [math.exp(i)/ztot for i in summary["logz"]]

    summary = pd.DataFrame(summary).sort_values(by=['score(logl)'], ascending=False)
    print(summary.to_string())
    summary.to_csv(transient+"_guessed_"+summary["type"][0]+".csv", index=False)
    summary.to_excel(transient+"_guessed_"+summary["type"][0]+".xlsx")
print("DONE")
