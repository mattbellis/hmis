import hmis
import unittest
import datetime as datetime
import pandas as pd
import sys
    
filename = 'test_data/hmis_test_data.pkl'
master_dictionary = hmis.read_dictionary_file(filename)

def test_calc_age():

    ex_birthdate = hmis.get_date_from_string('1995-05-30')
    now = hmis.get_date_from_string('2017-08-22')
    ex_age = hmis.calc_age(ex_birthdate,now)

    assert ex_age.days == 8120 
    assert isinstance(ex_age, datetime.timedelta)    
        
        
        
        
def test_get_date_from_string():
    ex_date = '1995-05-30'
    
    ex_date = hmis.get_date_from_string(ex_date)
    assert ex_date.year == 1995
    assert isinstance(ex_date, datetime.datetime)
    
        
        
        
        
def test_convert_to_coordinates():
    
    zip_code = 12211
    lat, long = hmis.convert_to_coordinates(zip_code)
    
    assert isinstance(lat, float)
    assert isinstance(long, float)
    
    assert abs(lat-42.701752) < 0.01
    assert abs(long-(-73.7576574)) < 0.001
        
        
        
def test_pretty_print():
    
    #capturedOutput = StringIO.StringIO() 
    #sys.stdout = capturedOutput      
    return_val = hmis.pretty_print(master_dictionary[0])               

    assert return_val == 1

    #sys.stdout = sys.__stdout__             
    #print 'Captured', capturedOutput.getvalue() 
    
    #ex_print = '================================/n 110378941/n 1968-05-04/n Transitional Housing                In/Out: 5/7/2013   - 5/3/2014   (361 days)/t  Zip code: 12202'
    #assert ex_print == capturedOutput.getvalue()
        
        
        
        
        
        
def test_calc_average_age_by_year():
    
    ages_list = hmis.calc_average_age_by_year(master_dictionary)
    age_earlier, age2013, age2014, age2015, age2016 = ages_list
    for a in ages_list:
        assert isinstance(a, list)
        
        
    assert age_earlier== [90.13972602739726, 38.02465753424657]
    assert age2013 == []
    assert age2014 == []
    assert age2015 == [35.6, 16.586301369863012]
    assert age2016 == [71.88219178082191, 5.838356164383562]
    
        
    #sys.stdout = capturedOutput      
    #hmis.calc_average_age(master_dictionary)               
    #sys.stdout = sys.__stdout__             
    #print 'Captured', capturedOutput.getvalue()     
    
    #assert 'Average age for all years before 2013: 49 /n Average age for the year 2013: 23 /n Average age for the year 2014: 23 /n Average age for the year 2015: 26 /n Average age for the year 2016: 26' == capturedOutput.getvalue()  
        
        
    
    
    
    
    
    
    
    
    
    
        
        
        
