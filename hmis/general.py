import datetime as dt
from datetime import timedelta, datetime
import pandas as pd
from geopy.geocoders import Nominatim
import collections
import numpy as np


################################################################################
# Get age from birthdate.
################################################################################
def calc_age(birthdate, date_to_calc_age=None):
    """ This function calculates the age of an individual using their birthdate.
    
    Args:
        **birthdate** (datetime.datetime): The birthday of the individual.
            
        **age_at_date** (datetime.datetime or string): The date on which you want to know the individual's age. 
            
    Returns:
        **age** (int): The age of the individual.
    
    
    """
    '''
    birth_year,birth_month,birth_day = birthdate.split('-')
    born = dt.datetime(int(birth_year),int(birth_month),int(birth_day))
    '''

    # Put the date_to_calc_age into a datetime.datetime object
    if date_to_calc_age is not None:
        if type(date_to_calc_age) == str:
            date_to_calc_age = get_date_from_string(date_to_calc_age)
    else:
        date_to_calc_age = datetime.now()
    
    age = date_to_calc_age - birthdate

    return age



################################################################################
# Converts a string to a datetime object.
################################################################################
def get_date_from_string(datestring):
    """ This function converts the date as a string to a datetime object.
    
    Args:
        **datestring** (string): the date as a string.
    
    Returns: 
        **date** (datetime object): the date as a datetime object.
        
    """
    
    date = pd.to_datetime(datestring)

    # Convert to datetime.datetime object for more standard
    # manipulation
    date = date.to_pydatetime()

    return date



################################################################################
# Converts zip code to coordinates.
################################################################################
def convert_to_coordinates(zip_code):
    """ Converts the list of zip codes to latitude and ongitude coordinates. 
    
    Args:
        **zip_code** (string): The zip code to be converted.
        
        
    Return:    
        **location.latitude** (float): The latitude corrdinate of the zip code.
        
        **location.longitude** (float): The longitude coordinate of the zip code.

    """
    geolocator = Nominatim()

    zc=str(int(zip_code))

    zipState=zc + ", New York"
    location = geolocator.geocode(zipState, timeout=10)
    if (location !=None):
        return location.latitude, location.longitude        
        
        
################################################################################
################################################################################
def pretty_print(inds, dump_all=False):
    """ This function prints the dictionaries passed to it in a way that is very easy to read.
    
    Args:
        **inds** (list): The list of dictionaries that 
        **dump_all** (bool): If True, this shows the category name. If False, this function just prints out the numerical values without the decription.
        
        
    """

    #dateformat = "%Y-%m-%d"
    dateformat = "%m/%d/%Y"

    # Make sure inds is a list.
    if type(inds)==dict:
        inds = [inds]
        
    for ind in inds: 
        print("================================")
        print((ind['Personal ID']))
        print((ind['DOB']).strftime(dateformat))
        
        if ind['Programs'] != list:
            
            for program in ind['Programs']:
                
                output = ""
                
                # Adds the keys to the programs along with the values in all of the programs. 
                if dump_all:
                    for key in program:
                        output += "%-15s: %-15s " % (key, program[key])

                # Adds only the values of all the programs.        
                else:
                    output += "%-35s " % (program["Project type"])
                    output += "%s: %-10s - %-10s " % ("In/Out",program["Admission date"].strftime(dateformat), program["Discharge date"].strftime(dateformat))
                    output += "(%s days) " % (program["Length of stay"].days)
                    output += "\t Zip code: %s" % (program['Project Zip Code'])

                print(output)

    return 1 # For success

################################################################################
################################################################################

def calc_average_age_by_year(ppl):
    """ Calculates the average age split up by year. The years are split up from 2013, 2014, 2015, 2016 and earlier than 2013. 
    This is primarily an example of how a semi-standard analysis could be added to the libraries in this hmis module. 
    
    Args:
        **ppl** (list): The list of dictionaries of the individuals to be analyzed.
        
        
    Return:    
        **average_age_list** (list): The list of average ages, starting with 2013, 2014, 2015, and 2016 and then the average age for the years before 2013. 

    """
    
    
    age_earlier =[]
    age2013 =[]
    age2014 = []
    age2015 =[]
    age2016=[]

    years = ["before 2013","2013","2014","2015","2016"]


    for person in ppl:

        for program in person['Programs']:
            ad_date = program['Admission date']
            
            if (get_date_from_string(ad_date)).year == 2013:
                age = calc_age(person['DOB'], program['Admission date'])
                age2013.append(age.days/365.0)

            elif (get_date_from_string(ad_date)).year == 2014:
                age = calc_age(person['DOB'], program['Admission date'])
                age2014.append(age.days/365.0)
                
            elif (get_date_from_string(ad_date)).year == 2015:
                age = calc_age(person['DOB'], program['Admission date'])
                age2015.append(age.days/365.0)
                
            elif (get_date_from_string(ad_date)).year == 2016:
                age = calc_age(person['DOB'], program['Admission date'])
                age2016.append(age.days/365.0)
                
            else:
                age = calc_age(person['DOB'], program['Admission date'])
                age_earlier.append(age.days/365.0)
                
          
    age_list = [age_earlier, age2013, age2014, age2015, age2016]

    for age,year in zip(age_list,years):

        if len(age)>0:
            ave_age = np.mean(age)
            print("Average age   for %-12s: %4.2f " % (year,ave_age))
        else:
            print("No indviduals for %-12s" % (year))
    
    return age_list
    






################################################################################
################################################################################
