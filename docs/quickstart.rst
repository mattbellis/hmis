=============
 Quick start
=============

hmis provides functions to parse the data dump of an HMIS database (11 .csv files)
and produces a python pickle file which contains a list of dictionaries. Each 
dictionary represents an individual who has been helped somewhere in the 
Continuum of Care (CoC) with additional information about their date-of-birth
and the support they have received. More information can be pulled out from 
the original .csv files. 

A script to build this pickle file is provided. 

Once the file is created, additional hmis tools can be used to visualize the
data or perform simple selections on the dataset. 

Requirements 
------------

These are the additional requirements. They can be installed with 
conda (if you have the Anaconda installation) or pip for folium, geopy, 
and zipcode.

* Python 3.5, or 3.6 (tested with)
* NumPy >= 1.11.2
* Pandas >= 0.19.1
* Plotly >= 2.0.0
* Geopy >= 1.10.0
* Folium >= 0.3.0

If you have the Anaconda distribution installed with Python 3.x,
you can get your system ready for hmis with

.. code-block:: bash

    $ conda update --all
    $ conda install numpy
    $ conda install pandas
    $ conda install plotly

    $ pip install geopy
    $ pip install folium
    $ pip install zipcode



Installation
------------

To install hmis, clone the source repository from Github and install
with setup.py.

On the command line, enter:

.. code:: bash

    $ git clone git@github.com:mattbellis/hmis.git
    $ cd hmis
    $ python setup.py install

You may need to have root (sudo) permissions for the last step, depending
on your installation.







