# hmis
A set of Python tools to parse files from a standard dump of HMIS (Homeless Management Information System) data and do some simple analysis and visualization.


hmis-python is written in python and developed by Sara Mahar and Matthew Bellis at Siena College. 

See the hmis-python repository and readthedocs for further information.



# Install

Install the latest version (from GitHub): `pip install git+git://github.com/rasbt/biopandas.git#egg=biopandas`



## Requirements 

* Python 2.7, 3.5, or 3.6
* NumPy >= 1.11.2
* Pandas >= 0.19.1
* Folium >= 0.3.0
* Geopy >= 1.10.0


# Usage

This repository also contains a [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/index.html) where you can see some examples of the visualizations and analysis features of hmis-python.

## Basic example 


```
import hmis

people = hmis.read_dictionary_file('save_dicts_June13.pkl')

people_selected_by_age = hmis.select_by_age(people,lo=1,hi=5)

map1 =hmis.plot_program_locations(people_selected_by_age, cluster=True, exploded=True)

map1

```













