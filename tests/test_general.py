import hmis
import unittest
import datetime as datetime

    
    
    
# Must create a class to test the functions you want to test. You must pass in the unittest.TestCase object. 

# The functions you want to test must start with the word "test".

# There are two ways to assert that what your function returns and what is expected are equal.



################################################################################
# Pass in a parameter "self" to the function and use the .assertEqual method with the value you want to check with the expected value. 
################################################################################
class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
            
            

            
#class TestParsingFunctions(unittest.TestCase):
    
    #def test_read_in_data(self):
        
        #data = read_hector_input(os.path.join(os.path.dirname(__file__), '../pyhector/emissions/RCP26_emissions.csv'))

        
        
################################################################################
# You can use the built-in assert function with python. 
################################################################################
class TestGeneralFunctions(unittest.TestCase):
    
    def test_calc_age():
        
        ex_birthdate = '1995-05-30'
        ex_age = hmis.calc_age(ex_birthdate)
        
        assert ex_age == 22
        
        
    def test_getting_age():
        
        ex_ind = {'Age': 32, 'Personal ID': '104846641', 'Programs': [{'Project type': 'Services Only', 'Discharge date': '10/20/2014', 'Admission date': '10/4/2016', 'Length of stay': datetime.timedelta(-715), 'Project Zip Code': '12206'}, {'Project type': 'Emergency Shelter', 'Discharge date': '2/28/2014', 'Admission date': '10/6/2014', 'Length of stay': datetime.timedelta(-220), 'Project Zip Code': '12210'}]}
        
        assert ex_ind['Age'] ==32
        #self.assertEqual(ex_ind['Age'], 32)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        