import hmis
import unittest
import pandas as pd
import numpy 
from pandas.util.testing import assert_series_equal, assert_frame_equal

filename = 'test_data/hmis_test_data.pkl'

def test_read_in_data():

    #enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = 'test_data')
    org_data = hmis.read_in_data(directory='test_data')
    enrollment_data = org_data["Enrollment"]
    exit_data = org_data["Exit"]
    project_data = org_data["Project"]
    client_data = org_data["Client"]
    site_data = org_data["Site"]



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
    
    #enrollment_data, exit_data, project_data, client_data, site_data = hmis.read_in_data(directory = 'test_data')
    org_data = hmis.read_in_data(directory='test_data')
    enrollment_data = org_data["Enrollment"]
    personalids = hmis.get_pids(enrollment_data)
    
    assert isinstance(personalids, numpy.ndarray)
    assert len(personalids) == 11


        
        
        
        
def test_create_dictionary_list():
    inds = hmis.create_dictionary_list(directory='test_data')
    assert isinstance(inds, list)
    assert len(inds) == 10
    
    
    
    
        
def test_save_file():
    
    inds = hmis.create_dictionary_list(directory='test_data')
    hmis.save_file(inds, filename)
    
    
    people_list = hmis.read_dictionary_file(filename)
    
    assert isinstance(people_list, list)
    assert (people_list[2]['Personal ID'] == '226828041')

        
        

    
        
