import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from general import *
from collections import OrderedDict
import plotly.graph_objs as go
from plotly.offline import iplot
from plotly.graph_objs import Scatter, Figure, Layout


    

################################################################################
# Converts a string to a datetime object.
################################################################################
def get_plotting_style(ptype):
    """ This function gets the plotting styles depending on the type of program. 
    
    Args:
        **ptype** (string): The project type.
    
    Returns: 
        **color** (string): The color of the program in RGB.
        
        **width** (int): The width of the line of the program.
        
        **alpha** (float): The opaque value of the program.
        
        **style** (string): The marker style of the program.
        
    """


    
    
    programs_new = [{'name':'Emergency Shelter',                'color':'rgba(152, 150, 0, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Day Shelter',                      'color':'rgba(152, 0, 150, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'PH - Permanent Supportive Housing','color':'rgba(52, 0, 255, .8)','width':2,'style':'-','alpha':1.0},
                {'name':'Transitional Housing',             'color':'rgba(255, 20, 10, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Services Only',            'color':'rgba(152, 255, 0, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'PH - Rapid Re-Housing',            'color':'rgba(0, 255, 0, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Homelessness Prevention',          'color':'rgba(152, 200, 200, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Street Outreach',                  'color':'rgba(20, 20, 20, .8)','width':10,'style':'-','alpha':0.5},
                {'name':'RETIRED',             'color':'rgba(0, 20, 10, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Other Safe Haven',            'color':'rgba(10, 200, 0, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'PH - Housing Only',            'color':'rgba(0, 90, 90, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'PH - Housing with Services',          'color':'rgba(12, 20, 200, .8)',      'width':2,'style':'-','alpha':1.0},
                {'name':'Coordinated Assesment',                  'color':'rgba(99, 109, 240, .8)','width':10,'style':'-','alpha':0.1}
                ]
    
    color,width,alpha,style = 0,0,0,0
    for pt in programs_new:
        if ptype == pt['name']:
            color = pt['color']
            width = pt['width']
            alpha = pt['alpha']
            style = pt['style']
            
            
    return color,width,alpha,style   




################################################################################
################################################################################
def plot_time_series_from_dict_list_new(inds, image_name, exploded_view=False, plot_w_plotly=False):  
    """ This function plots the time-series for each individual that is inputted.
    
    Args:
        **inds** (list): The list of dictionaries that are going to be plotted.
        
        **image_name** (string): The name of the figure that will be saved.
        
        **exploded_view** (bool, optional): If True: each program for each individual will be plotted on the y-axis. If False: each individual will be plotted on the y-axis with multiple programs on one line.
        Defaulted to: False.
        
        **plot_w_plotly** (bool, optional): If True: this time-series plot will plot with plotly. This has a mouse-over feature that is useful for understanding the data that is visualized. If False: this time-series plot will be plotted with matplotlib. 
        Defaulted to: False.

    """
    
    # If there is only one individual, make their dictionary a list with one item.
    if type(inds) != list:
        inds = [inds]

    totlens=[]
    color_index=0
    if plot_w_plotly==False:
        plt.figure(figsize=(12,5))
    min_date = dt.datetime(2100,1,1)
    max_date = dt.datetime(1800,1,1)
    
    # Set the y-axis
    y = 0.0
    program_list=[]
    
    # Get the information for each individual
    for i in inds:

        projID = i['Personal ID']
        proj_type=[]
        start_dates=[]
        end_dates=[]
        lengths=[]
        
        for entry in i['Programs']:
            start_dates.append(entry['Admission date'])
            end_dates.append(entry['Discharge date'])
            lengths.append(entry['Length of stay'])
            proj_type.append(entry['Project type'])
        
        program_count = 0
        for start,end,l,ptype in zip(start_dates,end_dates,lengths,proj_type):
            
            # Handles nan
            if str(start)=='nan' or str(end)=='nan':
                1
            else:
                
                # Convert dates to datetime format.
                s = get_date_from_string(start)
                e = get_date_from_string(end)

                
                # Get plotting styles depending on what the program is. 
                color,width,alpha,style = get_plotting_style(ptype)
                
                # Starting point on the x-axis.
                x_point = [s,e]
                
                # Determining if it is a one day entry or an extended stay.
                l = np.timedelta64(1,'ns')
                length= (l / np.timedelta64(1, 'D')).astype(int)
                
                # Dependent on the length of stay, the marker plotted will change.
                if length > 1:
                    m_type='o'
                else:
                    m_type='*'

                y_point = [y,y]
                
                # Exploded view with make every program be on a separate line. Defaulted to have each program for one individual to be on one line. 
                if exploded_view==True:
                    y_point=[s,s]
                
                # If plotly is True, then plotly is used to plot instead of matplotlib. 
                if plot_w_plotly==True:
                    
                    showlegend_bool = True
                    if program_count>0:
                        showlegend_bool = False
                    
                    prog = go.Scatter(
                        x = x_point,
                        y= y_point,
                        legendgroup = projID,
                        name = projID,
                        text = projID+"<br>"+ptype,
                        showlegend = showlegend_bool,
                        marker = dict(size = 10,color = color,line = dict(width = 2,))
                    )
                    program_list.append(prog)

                else:

                    # Need to do this to convert the rgba string.
                    color = color[5:-1]
                    color = color.split(',')
                    color = '#%02x%02x%02x' % (int(color[0]),int(color[1]),int(color[2]))
                    plt.plot(x_point,y_point,marker=m_type,linewidth=width,color=color,alpha=alpha,linestyle=style, label=ptype)
                    plt.plot([0,1],[0,1])
                    

                # Keep track of max and min time to rescale axes later.
                if s<min_date:
                    min_date = s
                if e>max_date:
                    max_date = e
            program_count += 1
        
        y += 1
        
    if plot_w_plotly==False:
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(list(zip(labels, handles)))
        plt.legend(list(by_label.values()), list(by_label.keys()), loc='upper left')
        plt.xlim(min_date-dt.timedelta(365),max_date)
        #plt.gcf().tight_layout()
        #plt.gcf().savefig(image_name,dpi=300)
        

    if exploded_view==False and plot_w_plotly==False:
        plt.ylim(-1,y+1)

    if plot_w_plotly ==True:
        iplot(program_list)
        #iplot.image.save_as(program_list, filename=image_name)
        
        
        
        
        
        
        
        
        
        
        
        
