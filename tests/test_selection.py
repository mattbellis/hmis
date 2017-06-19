import hmis



filename = 'save_dicts_June16.pkl'
master_dictionary = hmis.read_dictionary_file(filename)

def test_select_by_age():

    people = hmis.read_dictionary_file(filename)
    
    lo=10
    hi=20

    ppl_based_on_age = hmis.select_by_age(people,lo=lo,hi=hi)
    

    assert isinstance(ppl_based_on_age, list)

    
    
    
    
def test_subset_from_dictionary():

    personal_IDs = ['110380741']
    dictionary_subset = hmis.subset_from_dictionary(personal_IDs,master_dictionary)
    
    assert (len(dictionary_subset)==1)
    assert isinstance(dictionary_subset, list)
    assert isinstance(dictionary_subset[0], dict)
    assert (dictionary_subset[0]['DOB']=='2013-07-14')
    
    
    
    
def test_select_by_number_of_programs():
    
    num_of_programs=1
    ppl_based_on_programs = hmis.select_by_number_of_programs(master_dictionary, num_of_programs)

    assert (len(ppl_based_on_programs)==54)
    
    assert isinstance(ppl_based_on_programs, list)
    
    for person in ppl_based_on_programs:
        assert isinstance(person, dict)
        
    
    
    
    
def test_select_by_program_type():
    
    program_type = 'Transitional Housing'
    
    ppl_based_on_program_type = hmis.select_by_program_type(master_dictionary, program_type)
    
    #print("the length: %i" %len(ppl_based_on_program_type))
    assert (len(ppl_based_on_program_type) == 46)
    
    assert isinstance(ppl_based_on_program_type, list)
    
    
    for person in ppl_based_on_program_type:
        assert isinstance(person, dict)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    