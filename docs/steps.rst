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

    >>> from hmis import selection
    >>> from hmis import general
    >>> from hmis import visualizing 
    >>> from hmis import parsing
    >>> import plotly
    
    
If you are using a Jupyter notebook make sure to include the following in order to plot within the kernel:

.. doctest:: 

    >>> plotly.offline.init_notebook_mode()
    >>> %matplotlib notebook


Read the dictionary file
------------------------

To read in the entire primary dictionary file:

.. doctest::

    >>> filename = 'example.pkl'
    >>> dict_list = parsing.read_dict_file(filename)


Select individuals to visualize
-------------------------------

From this list of dictionaries ``dict_list``, you can define an age range to select the individuals to visualize. 




Visualize time-series plots
---------------------------

















