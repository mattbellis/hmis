"""
Building dictionary file
    Read_in_data 
    Get_pids 
    Calc_age (general)
    Create_dictionary_list
    Save_file 
 
Reading in the dictionary file
    Read_dictionary_file
"""

import hmis
import unittest
import pandas as pd
import numpy as np
from pandas.util.testing import assert_series_equal, assert_frame_equal




#class TestParsingFunctions(unittest.TestCase):


def test_read_in_data():

    #directory='~/hmis_data/'
    directory = '~/Documents/hmis_data'

    enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = directory)


    assert isinstance(enrollment_data, pd.DataFrame)
    assert isinstance(exit_data, pd.DataFrame)
    assert isinstance(project_data, pd.DataFrame)
    assert isinstance(client_data, pd.DataFrame)
    assert isinstance(site_data, pd.DataFrame)




def test_get_pids():
    
    enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = directory)
    personalids = hmis.get_pids(enrollment_data)

    assert isinstance(personalids, np.array)
    print(len(personalids))
    self.assertEqual(len(personalids),100 )


        
        
        
        
def test_create_dictionary_list():
    
    
    
    
    
    
        
def test_save_file():
    
        
        

        
        
        
        
        
def test_read_dictionary_file():
    
        
        
        
        
        