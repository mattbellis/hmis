import hmis
from datetime import datetime

filename = 'test_data/hmis_test_data.pkl'
master_dictionary = hmis.read_dictionary_file(filename)

def test_select_by_age():

    people = hmis.read_dictionary_file(filename)
    
    lo=10
    hi=20

    ppl_based_on_age = hmis.select_by_age(people,lo=lo,hi=hi)
    
    assert isinstance(ppl_based_on_age, list)

    
    
    
    
def test_subset_from_dictionary():

    personal_IDs = ['226828041','230978041']
    dictionary_subset = hmis.subset_from_dictionary(personal_IDs,master_dictionary)
    
    assert (len(dictionary_subset)==2)
    assert isinstance(dictionary_subset, list)
    assert isinstance(dictionary_subset[0], dict)
    assert (dictionary_subset[0]['DOB']==datetime(1945,1,1))


def test_select_by_number_of_programs():
    
    num_of_programs=1
    ppl_based_on_programs = hmis.select_by_number_of_programs(master_dictionary, num_of_programs)

    assert (len(ppl_based_on_programs)==6)
    
    assert isinstance(ppl_based_on_programs, list)
    
    for person in ppl_based_on_programs:
        assert isinstance(person, dict)
        
    
    
    
    
def test_select_by_program_type():
    
    program_type = 'Emergency Shelter'
    
    ppl_based_on_program_type = hmis.select_by_program_type(master_dictionary, program_type)
    assert (len(ppl_based_on_program_type) == 6)
    
    assert isinstance(ppl_based_on_program_type, list)
    
    
    for person in ppl_based_on_program_type:
        assert isinstance(person, dict)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
