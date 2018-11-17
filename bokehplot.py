import pandas as pd
import numpy as np

from bokeh.io import show, output_file, output_notebook
from bokeh.layouts import WidgetBox, column, row
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
                                  Tabs, CheckboxButtonGroup, 
                                  TableColumn, DataTable, Select)

from bokeh.models import (CategoricalColorMapper, HoverTool, 
                          ColumnDataSource, Panel, CustomJS,
                         FuncTickFormatter, SingleIntervalTicker, LinearAxis)

from bokeh.plotting import figure

from scipy.stats import gaussian_kde
from bokeh.palettes import Category20_16

### this is to plot without using bokeh server
flights = pd.read_csv("flights.csv")
feat_plot = "arr_delay" ##change to fps_stability
group_name = "name" ##change to "model_name"

df = flights.loc[:,[group_name, feat_plot]]
df = df.dropna()

def plot_density_onegame(df, name, feat_plot):
    
    bandwidth = 5
    range_start = -100
    range_end = 180
    r = len(df.groupby(name).count().index)
    l = list(df.groupby(name).count().index)
    l = sorted(l)
    
    def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p
    
    x = np.linspace(range_start, range_end, 100)

    source_dict = dict(x=x)
    line_dict = dict()
    line_colors = Category20_16
    line_colors.sort()

    for i in range(0,r):
        tmp_df = df[df[name] == l[i]]
        tmp_kde = gaussian_kde(tmp_df[feat_plot], bw_method = bandwidth)
        tmp_y = tmp_kde.pdf(x)
        #y_number = "y%s" % i
        y_number = l[i]
        source_dict[y_number] = tmp_y

    source = ColumnDataSource(data=source_dict)
    p = figure(plot_width = 600, plot_height = 400)

    for i in range(0,r):
        #y_number = "y%s" % i
        y_number = l[i]
        line_number = "line%s" % i
        line = p.line('x',y_number,source=source,line_width=3,line_alpha=0.6,line_color=line_colors[i])
        line_dict[line_number] = line

    hover = HoverTool(tooltips=[(feat_plot, '$x'),('Density', '$y')], line_policy = 'next')
    p.add_tools(hover)
    p = style(p)

    checkbox = CheckboxGroup(labels=l, active=list(range(r)))

    checkbox.callback = CustomJS(args=line_dict, code="""
        //console.log(cb_obj.active);
        line0.visible = false;
        line1.visible = false;
        line2.visible = false;
        line3.visible = false;
        line4.visible = false;
        line5.visible = false;
        line6.visible = false;
        line7.visible = false;
        line8.visible = false;
        line9.visible = false;
        line10.visible = false;
        line11.visible = false;
        for (i in cb_obj.active) {
            //console.log(cb_obj.active[i]);
            if (cb_obj.active[i] == 0) {
                line0.visible = true;
            } else if (cb_obj.active[i] == 1) {
                line1.visible = true;
            }
              else if (cb_obj.active[i] == 2) {
                line2.visible = true;
            }
              else if (cb_obj.active[i] == 3) {
                line3.visible = true;
            }
              else if (cb_obj.active[i] == 4) {
                line4.visible = true;
            }
              else if (cb_obj.active[i] == 5) {
                line5.visible = true;
            }
              else if (cb_obj.active[i] == 6) {
                line6.visible = true;
            }
              else if (cb_obj.active[i] == 7) {
                line7.visible = true;
            }
              else if (cb_obj.active[i] == 8) {
                line8.visible = true;
            }
              else if (cb_obj.active[i] == 9) {
                line9.visible = true;
            }
              else if (cb_obj.active[i] == 10) {
                line10.visible = true;
            }
              else if (cb_obj.active[i] == 11) {
                line11.visible = true;
            }
        }
    """)
    
    controls = WidgetBox(checkbox)
    layout = row(controls, p)

    tab = Panel(child = layout, title = "Density Plot of "+feat_plot)

    return tab


tab3 = plot_density_onegame(df,'name', 'arr_delay')
tabs = Tabs(tabs= [tab3])

output_file("testBokeh.html")
show(tabs)



