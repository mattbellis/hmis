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
    
    
def test_get_additional_info():

    alldata = hmis.read_in_data(directory='test_data')

    vals = hmis.get_additional_info('230978041',idtype='Personal',org_data=alldata,info='WorldWarII')
    assert isinstance(vals,dict)
    assert isinstance(vals['230978041'],dict)
    assert vals['230978041']['WorldWarII'] == 'EMPTY'

    vals = hmis.get_additional_info('230978041',idtype='Personal',org_data=alldata,info=['Gender','Ethnicity','WorldWarII'])
    assert isinstance(vals,dict)
    assert vals['230978041']['Gender'] == '0'

    vals = hmis.get_additional_info('552310',idtype='ProjectEntry',org_data=alldata,info=['HouseholdID','RelationshipToHoH','ResidencePrior'])
    assert isinstance(vals,dict)
    assert vals['552310']['RelationshipToHoH'] == '2'

    vals = hmis.get_additional_info(['567519','561729'],idtype='ProjectEntry',org_data=alldata,info=['MonthsHomelessPastThreeYears'])
    assert isinstance(vals,dict)
    assert vals['567519']['MonthsHomelessPastThreeYears'] == '101'
    assert vals['561729']['MonthsHomelessPastThreeYears'] == '110'

    
    
    
    
    
    
    
    
    
    
    
    
    
