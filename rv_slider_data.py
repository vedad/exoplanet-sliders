#!/usr/bin/env python

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Whisker
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
#from ell.utils import models
from models import get_radial_velocity

data_path = "/Users/vxh710/PhD/outreach/in2science/exoplanet-sliders/rv_data.csv"
xdat, ydat, yerrdat = np.loadtxt(data_path, unpack=True, delimiter=',')

upper = ydat + yerrdat
lower = ydat - yerrdat

x = np.linspace(xdat.min(), xdat.max(), 1000)

#x = np.linspace(0, 10, 500)
#x = np.arange(0, 20, 0.002)


P_start = 2
t0_start = 5
incl_start = 90
K_start = 10


y = get_radial_velocity(x, P_start, t0_start, incl_start, K_start)

source = ColumnDataSource(data = dict(x = x, y = y))

source_dat = ColumnDataSource(data = dict(x = xdat, y = ydat, upper=upper,
    lower=lower, base=xdat))

plot = figure(plot_height = 500, plot_width = 1600, 
            title = "exoplanet radial velocity data modelling",
        y_range=(-20, 20))
plot.scatter('x', 'y', line_color=None, color='black', fill_alpha=0.8, size=5,
        source=source_dat)

plot.add_layout(
    Whisker(base='base', source=source_dat, upper="upper", lower="lower", level="overlay")
)

plot.line('x', 'y', source = source, line_width = 3, line_alpha = 1)

t_zero = Slider(start=0,
                end=10,
                value=t0_start,
                step = 0.001,
                title="transit mid-point, T0",
                format = '0.000')

period = Slider(start=1, 
                end=10,
                value=P_start, 
                step=0.001,
                title="orbital period, P",
                format = '0.000')

amplitude = Slider(start=0.0, 
                          end=20, 
                          value=K_start, 
                          step=0.05, 
                          title="semi-amplitude, K")


def update_data(attrname, old, new):
    _x = x

    t0 = t_zero.value
    P = period.value
    K = amplitude.value

    _y = get_radial_velocity(_x, P, t0, 90, K)
    source.data = dict(x = _x, y = _y)


t_zero.on_change('value', update_data)
period.on_change('value', update_data)
amplitude.on_change('value', update_data)

curdoc().add_root(column(t_zero, period, amplitude,
    plot, width = 1600))

#curdoc().add_root(row(plot, column(t_zero, period, radius_ratio,
#    impact_parameter, scaled_separation), width = 500))

#curdoc().add_root(column(period, radius_ratio, width = 100))
curdoc().title = "Sliders"

