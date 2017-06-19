import hmis
import unittest
import pandas as pd
import numpy 
from pandas.util.testing import assert_series_equal, assert_frame_equal


directory = '~/Documents/hmis_data_copy'
filename = 'save_dicts_June16.pkl'


def test_read_in_data():

    enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = directory)


    assert isinstance(enrollment_data, pd.DataFrame)
    assert isinstance(enrollment_data['PersonalID'], pd.Series)
    
    assert isinstance(exit_data, pd.DataFrame)
    assert isinstance(exit_data['PersonalID'], pd.Series)
    
    assert isinstance(project_data, pd.DataFrame)
    assert isinstance(project_data['ProjectID'], pd.Series)
    
    assert isinstance(client_data, pd.DataFrame)
    assert isinstance(client_data['PersonalID'], pd.Series)
    
    assert isinstance(site_data, pd.DataFrame)
    assert isinstance(site_data['ProjectID'], pd.Series)




def test_get_pids():
    
    enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = directory)
    personalids = hmis.get_pids(enrollment_data)
    
    assert isinstance(personalids, numpy.ndarray)
    assert len(personalids) == 99


        
        
        
        
def test_create_dictionary_list():
    inds = hmis.create_dictionary_list(directory=directory)
    assert isinstance(inds, list)
    assert len(inds) == 99
    
    
    
    
        
def test_save_file():
    
    inds = hmis.create_dictionary_list(directory=directory)
    hmis.save_file(inds, filename)
    
    
    people_list = hmis.read_dictionary_file(filename)
    
    assert isinstance(people_list, list)
    assert (people_list[10]['Personal ID'] == '110380741')

        
        

    
        