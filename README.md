# hmis
A set of Python tools to parse files from a standard dump of [HMIS (Homeless Management Information System)](https://www.hudexchange.info/resource/3824/hmis-data-dictionary/) data and do some simple analysis and visualization.

hmis is written in python and developed by Sara Mahar (now at the University of San Francisco) and Matthew Bellis at Siena College. 

More complete documentation can be found at [readthedocs](http://hmis.readthedocs.io/en/latest/).



## Requirements 

* Python 2.7, 3.5, or 3.6
* NumPy >= 1.11.2
* Plotly >= 2.0.0
* Pandas >= 0.19.1
* Folium >= 0.3.0
* Geopy >= 1.10.0

# Install

Install the latest version from Github.

    git clone git@github.com:mattbellis/hmis.git
    cd hmis
    python setup.py install




# Usage

This repository also contains a [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/index.html) where you can see some examples of the visualizations and analysis features of hmis-python.

## Basic example 


```
import hmis

people = hmis.read_dictionary_file('save_dicts_June13.pkl')

subset = hmis.select_by_age(people,lo=1,hi=5)

hmis.pretty_print(subset)

```













