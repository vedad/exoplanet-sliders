#!/usr/bin/env python

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from ell.utils import models

# TODO:
# * red line across y axis to indicate location of T0
# * phased transit data in separate plot, including binned data
# * reduced chi^2 shown
# * separate plot showing residuals

transit_data_path = "/Users/vxh710/PhD/outreach/in2science/exoplanet-sliders/transit_data.csv"


x, ydat = np.loadtxt(transit_data_path, unpack=True, delimiter=',',
        usecols=(0,1))
x = np.linspace(x.min(), x.max(), 10000)

y = models.get_light_curve(x, 2, 5, 4, 0.1, 90, 
#                            ld='quad',
#                            ustar=[0.4,0.3],
                            grid_1='very_sparse', grid_2='very_sparse')

source = ColumnDataSource(data = dict(x = x, y = y))

#source_dat = ColumnDataSource(data = dict(x = x, y = ydat))

plot = figure(plot_height = 500, plot_width = 1600,
        title = "exoplanet transit modelling",
        y_range=(0.95, 1.01))
#plot.scatter('x', 'y', line_color=None, color='black', fill_alpha=0.8, size=5,
#        source=source_dat)
plot.line('x', 'y', source = source, line_width = 3, line_alpha = 1)

t_zero = Slider(start=0,
                end=10,
                value=5,
                step = 0.001,
                title="transit mid-point, T0",
                format = '0.000')

period = Slider(start=1, 
                end=10,
                value=2, 
                step=0.001,
                title="orbital period, P",
                format = '0.000')

radius_ratio = Slider(start=0.01, 
                      end=0.2, 
                      value=0.1, 
                      step=0.0005, 
                      title="radius ratio, r/R",
                      format = '0.000')

impact_parameter = Slider(start=0, 
                          end=1+0.2, 
                          value=0.2, 
                          step=0.01, 
                          title="impact parameter, b")

scaled_separation = Slider(start=2, 
                          end=20, 
                          value=5, 
                          step=0.02, 
                          title="scaled separation, a/R")

def get_transit_width(period, aor, ror, b):
    incl = np.arccos(b / aor)
    return period / np.pi * np.arcsin(1/aor * np.sqrt((1 + ror)**2 - b**2) / 
                                                np.sin(incl)
                                                )
def update_data(attrname, old, new):
    _x = x

    t0 = t_zero.value
    P = period.value

    ror = radius_ratio.value
    b = impact_parameter.value
    if b >= (1 + ror):
        _y = np.ones_like(_x)
    else:
        aor = scaled_separation.value
        incl = np.rad2deg(np.arccos(b / aor))

        # calculate transit model only on points close to transit to reduce
        # computation time, the rest is interpolated
        t14 = get_transit_width(P, aor, ror, b)
        phase = (_x - t0) % P / P
        phase[phase > 0.5] -= 1
        
        in_transit = np.array((phase > -0.7*t14/P) & (phase < 0.7*t14/P), dtype=int)

        _y = models.get_light_curve(_x, P, t0, aor, ror, incl,
#                            ld='quad',
#                            ustar=[0.4,0.3],
                            grid_1='very_sparse',
                            grid_2='very_sparse', oversample=in_transit)
    source.data = dict(x = _x, y = _y)


t_zero.on_change('value', update_data)
period.on_change('value', update_data)
radius_ratio.on_change('value', update_data)
impact_parameter.on_change('value', update_data)
scaled_separation.on_change('value', update_data)

# sliders and plots in one column
curdoc().add_root(column(t_zero, period, radius_ratio, impact_parameter,
    scaled_separation, plot, width = 1600))

# sliders in separate column to plot
#curdoc().add_root(row(plot, column(t_zero, period, radius_ratio,
#    impact_parameter, scaled_separation), width = 500))

curdoc().title = "Sliders"

