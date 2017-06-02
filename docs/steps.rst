======
 Steps
======

These are the steps in order to visualize individuals.

Create primary dictionary file
------------------------------

Put together a dictionary of all the individuals in the HMIS data dump and determine the connections and relationships between the different entries in the different files.

First create the .pkl file:

.. code-block:: bash

    $ python build_primary_dictionary_file.py
    
To change the directory or file name, edit build_primary_dictionary_file.py.


Import necessary packages
-------------------------

.. doctest::

    >>> import hmis
    >>> import plotly
    >>> import matplotlib.pylab as plt
    >>> import folium
    
    
If you are using a Jupyter notebook make sure to include the following in order to plot within the kernel:

.. doctest:: 

    >>> plotly.offline.init_notebook_mode()
    >>> %matplotlib notebook


Read the dictionary file
------------------------

Once you have made the master dictionary file, you can read it in at 

.. doctest::

    >>> filename = 'example.pkl'
    >>> master_dictionary = hmis.read_dictionary_file(filename)


Select individuals to visualize
-------------------------------

From this list of dictionaries ``master_dictionary``, you can select individuals that are within a certain  age range:

.. doctest:: 

    >>> lo = 31
    >>> hi = 33
    >>> selected_people = hmis.select_by_age(master_dictionary,lo=lo,hi=hi)
    
    
Additionally, you can select individuals from ``master_dictionary`` that have been to at least a certain number of progams:

.. doctest::
    
    >>> num_of_programs = 27
    >>> selected_people = hmis.select_by_number_of_programs(mast-dictionary,num_of_programs)


Visualize time-series plots
---------------------------

From the ``selected_people``, you can plot their time-series plots:

.. doctest:: 

    >>> image_name = 'example.png'
    >>> hmis.plot_time_series_from_dict_list_new(selected_people, image_name, plot_w_plotly=True)
    
    
    
Visualize program locations
----------------------------

From the ``selected_people``, you can plot the location of their programs:

.. doctest:: 

    >>> map2 =hmis.plot_program_locations(selected_people)
    >>> map2














