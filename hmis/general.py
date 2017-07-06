import datetime as dt
from datetime import timedelta, datetime
import pandas as pd
from geopy.geocoders import Nominatim
import collections


################################################################################
# Get age from birthdate.
################################################################################
def calc_age(birthdate, admission_date = 0):
    """ This function calculates the age of an individual using their birthdate.
    
    Args:
        **birthdate** (string): The birthday of the individual.
            
    Returns:
        **age** (int): The age of the individual.
    
    
    """
    birth_year,birth_month,birth_day = birthdate.split('-')
    born = dt.datetime(int(birth_year),int(birth_month),int(birth_day))
    if admission_date !=0:
        today = get_date_from_string(admission_date)
    else:
        today = datetime.now()
    
    age= today.year-born.year - ((today.month,today.day) < (born.month, born.day))

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
    
    date=pd.to_datetime(datestring)
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

    # Make sure inds is a list.
    if type(inds)==dict:
        inds = [inds]
        
    for ind in inds: 
        print("================================")
        print((ind['Personal ID']))
        print((ind['DOB']))
        
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
                    output += "%s: %-10s - %-10s " % ("In/Out",program["Admission date"], program["Discharge date"])
                    output += "(%s days) " % (program["Length of stay"].days)
                    output += "\t Zip code: %s" % (program['Project Zip Code'])

                print(output)

################################################################################
################################################################################

def calc_average_age_by_year(ppl):
    """ Calculates the average age split up by year. The years are split up from 2013, 2014, 2015, 2016 and earlier than 2013. 
    
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


    for person in ppl:

        for program in person['Programs']:
            ad_date = program['Admission date']
            
            if (get_date_from_string(ad_date)).year == 2013:
                age = calc_age(person['DOB'], program['Admission date'])
                age2013.append(age)

            elif (get_date_from_string(ad_date)).year == 2014:
                age = calc_age(person['DOB'], program['Admission date'])
                age2014.append(age)
                
            elif (get_date_from_string(ad_date)).year == 2015:
                age = calc_age(person['DOB'], program['Admission date'])
                age2015.append(age)
                
            elif (get_date_from_string(ad_date)).year == 2016:
                age = calc_age(person['DOB'], program['Admission date'])
                age2016.append(age)
                
            else:
                age = calc_age(person['DOB'], program['Admission date'])
                age_earlier.append(age)
               

                
          
    average_age_earlier = sum(age_earlier)/len(age_earlier)
    print("Average age for all years before 2013: %i " % average_age_earlier)
    
    average_age2013 = sum(age2013)/len(age2013)
    print("Average age for the year 2013: %i " % average_age2013)

    average_age2014 = sum(age2014)/len(age2014)
    print("Average age for the year 2014: %i " % average_age2014)

    average_age2015 = sum(age2015)/len(age2015)
    print("Average age for the year 2015: %i " % average_age2015)

    average_age2016 = sum(age2016)/len(age2016)
    print("Average age for the year 2016: %i " % average_age2016)
    
    average_age_list = [age_earlier, age2013, age2014, age2015, age2016]

    return average_age_list
    






################################################################################
################################################################################

def organize_ages_by_admission_dates(ppl):
    """ Organizes the ages in a dictionary depending on when they entered the program. The years are split up from 2013, 2014, 2015, 2016 and earlier than 2013. 
    
    Args:
        **ppl** (list): The list of dictionaries of the individuals to be analyzed.
        
        
    Return:    
        **yeah_dictionary** (dict): The dictionaries of the ages of individuals for the appropriate year they entered a specific program.

    """


    year_dictionary = {}
    
    # Loop through each individual
    for person in ppl:

        # Loop through each program of each individual
        for program in person['Programs']:
            ad_date = program['Admission date']
            
            if get_date_from_string(ad_date).year in year_dictionary:
                year_dictionary[get_date_from_string(ad_date).year].append(calc_age(person['DOB'], program['Admission date']))
            else:
                year_dictionary[get_date_from_string(ad_date).year] = [calc_age(person['DOB'], program['Admission date'])]

    # Sort the years in order
    year_dictionary = collections.OrderedDict(sorted(year_dictionary.items()))
    return year_dictionary




def print_average_ages(year_dictionary):
    """ Prints the average age for each year that someone has visited a program. 
    
    Args:
        **year_dictionary** (dict): The dictionaries of the ages of individuals for the appropriate year they entered a specific program.

    """
    
    
    for year in year_dictionary:
        print("Average age for the year %i : %i " % (year, sum(year_dictionary[year])/len(year_dictionary[year] )))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
