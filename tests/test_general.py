import hmis
import unittest
import datetime as datetime
import pandas as pd
import StringIO
import sys
    
filename = 'save_dicts_June16.pkl'
master_dictionary = hmis.read_dictionary_file(filename)


def test_calc_age():

    ex_birthdate = '1995-05-30'
    ex_age = hmis.calc_age(ex_birthdate)

    assert ex_age == 22 
    assert isinstance(ex_age, int)    
        
        
        
        
def test_get_date_from_string():
    ex_date = '1995-05-30'
    
    ex_date = hmis.get_date_from_string(ex_date)
    assert ex_date.year == 1995
    assert isinstance(ex_date, pd.Timestamp)
    
        
        
        
        
def test_convert_to_coordinates():
    
    zip_code = 12211
    lat, long = hmis.convert_to_coordinates(zip_code)
    
    assert isinstance(lat, float)
    assert isinstance(long, float)
    
    assert abs(lat-42.7066463925) < 0.0001
    assert abs(long-(-73.7668615445)) < 0.0001
        
        
        
def test_pretty_print():
    
    capturedOutput = StringIO.StringIO() 
    sys.stdout = capturedOutput      
    hmis.pretty_print(master_dictionary[0])               
    sys.stdout = sys.__stdout__             
    #print 'Captured', capturedOutput.getvalue() 
    
    ex_print = '================================/n 110378941/n 1968-05-04/n Transitional Housing                In/Out: 5/7/2013   - 5/3/2014   (361 days)/t  Zip code: 12202'
    #assert ex_print == capturedOutput.getvalue()
        
        
        
        
        
        
def test_calc_average_age():
    
    ages_list = hmis.calc_average_age(master_dictionary)
    age_earlier, age2013, age2014, age2015, age2016 = ages_list
    for a in ages_list:
        assert isinstance(a, list)
        
        
    assert age_earlier== [55, 43]     
    assert age2013 == [45, 15, 33, 21, 0, 41, 28, 18, 32, 28, 0, 28, 34, 6, 4, 31, 29]
    assert age2014 ==[29, 30, 20, 29, 46, 24, 18, 32, 24, 5, 4]
    assert age2015 == [44, 30, 23, 27, 0, 35, 24] 
    assert age2016 == [23, 21, 0, 3, 23, 32, 3, 1, 44, 38, 26, 49, 40, 37, 45, 36, 32]
    
        
    capturedOutput = StringIO.StringIO() 
    sys.stdout = capturedOutput      
    hmis.calc_average_age(master_dictionary)               
    sys.stdout = sys.__stdout__             
    #print 'Captured', capturedOutput.getvalue()     
    
    #assert 'Average age for all years before 2013: 49 /n Average age for the year 2013: 23 /n Average age for the year 2014: 23 /n Average age for the year 2015: 26 /n Average age for the year 2016: 26' == capturedOutput.getvalue()  
        
        
def test_organize_ages_by_admission_dates():
    
    dictionaries = hmis.organize_ages_by_admission_dates(master_dictionary)
        
    assert isinstance(dictionaries, dict)
    #print(dictionaries)
    
    assert dictionaries == {2016: [23, 21, 0, 3, 23, 32, 3, 1, 44, 38, 26, 49, 40, 37, 45, 36, 32], 2012: [55, 43], 2013: [45, 15, 33, 21, 0, 41, 28, 18, 32, 28, 0, 28, 34, 6, 4, 31, 29], 2014: [29, 30, 20, 29, 46, 24, 18, 32, 24, 5, 4], 2015: [44, 30, 23, 27, 0, 35, 24]}
    
    
    
def test_print_average_ages():    
    
    year_dictionary =  hmis.organize_ages_by_admission_dates(master_dictionary)
    
    hmis.print_average_ages(year_dictionary)
    
    
    #print(list_of_average_ages)
    
    
    
    
     #Average age for all years before 2013: 49 
#Average age for the year 2013: 23 
#Average age for the year 2014: 23 
#Average age for the year 2015: 26 
#Average age for the year 2016: 26 
    
    
    
    
    
    
    
    
    
    
    
        
        
        