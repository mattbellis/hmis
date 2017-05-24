import datetime as dt
from datetime import timedelta, datetime
import pandas as pd


################################################################################
# Get age from birthdate.
################################################################################
def calc_age(birthdate):
    """ This function converts the birthdate to a datetime object and subtracts today's date. This calculates the age of an individual.
    
    Args:
        **birthdate** (string): The birthday of the individual.
            
    Returns:
        **age** (string): The age of the individual.
    
    
    """
    
    birth_year,birth_month,birth_day = birthdate.split('-')
    born = dt.datetime(int(birth_year),int(birth_month),int(birth_day))
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

