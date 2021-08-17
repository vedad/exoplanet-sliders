import numpy as np
import astropy.units as u
import sys

def get_light_curve(x, period, t0, aor, ror, incl,
                    ustar=None, ld=None, ecc=0, omega=90, sbratio=0,
                    oversample=1, texp=None, **kwargs):
    try:
        from ellc import lc
    except ModuleNotFoundError:
        print("Please install `ellc` to use this function")
        sys.exit()

    if not isinstance(x, np.ndarray):
        x = np.array([x])
    
    r1oa = 1/aor
    r2oa = r1oa * ror
    f_s = np.sqrt(ecc) * np.sin(np.deg2rad(omega))
    f_c = np.sqrt(ecc) * np.cos(np.deg2rad(omega))

    model = lc(x,
            radius_1=r1oa,
            radius_2=r2oa,
            incl=incl,
            sbratio=sbratio,
            period=period,
            t_zero=t0,
            f_s=f_s,
            f_c=f_c,
            light_3=0, 
            ld_1=ld,
            ldc_1=ustar,
            t_exp=texp,
            n_int=oversample,
            **kwargs)
#            grid_1='very_sparse',
#            grid_2='v)

    return model

def get_radial_velocity(x, period, t0, incl, K, ecc=0, omega=90, sbratio=0):
    try:
        from ellc import rv
    except ModuleNotFoundError:
        print("Please install `ellc` to use this function")
        sys.exit()

    K      *= u.m/u.s
    period *= u.day

    a1 = (K * period * np.sqrt(1 - ecc**2) /
            (2*np.pi * np.sin(np.deg2rad(incl)))
            ).to(u.R_sun).value
    q  = 1
    a  = a1 * (1 + 1/q)

    fs = np.sqrt(ecc) * np.sin(np.deg2rad(omega))
    fc = np.sqrt(ecc) * np.cos(np.deg2rad(omega))


    model = rv(x, 
            period=period.value, 
            t_zero=t0, 
            incl=incl, 
            sbratio=0,
            a=a, 
            q=q, 
            f_s=fs, 
            f_c=fc, 
            flux_weighted=False
            )

    return model[0] * 1e3


