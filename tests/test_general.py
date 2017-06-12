import hmis
import unittest
import datetime as datetime

    
    
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
    
    
  
    
            
class TestGeneralFunctions(unittest.TestCase):
    
    def test_calc_age(self):
        
        ex_birthdate = '1995-06-30'
        ex_age = hmis.calc_age(ex_birthdate)
        
        self.assertEqual(ex_age, 21)
        
        
    def test_getting_age(self):
        ex_ind = {'Age': 32, 'Personal ID': '104846641', 'Programs': [{'Project type': 'Services Only', 'Discharge date': '10/20/2014', 'Admission date': '10/4/2016', 'Length of stay': datetime.timedelta(-715), 'Project Zip Code': '12206'}, {'Project type': 'Emergency Shelter', 'Discharge date': '2/28/2014', 'Admission date': '10/6/2014', 'Length of stay': datetime.timedelta(-220), 'Project Zip Code': '12210'}]}
        self.assertEqual(ex_ind['Age'], 32)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        