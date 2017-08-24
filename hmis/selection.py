import numpy as np
from hmis.general import calc_age
from datetime import datetime

################################################################################
# Gets IDs within a certain age range.
################################################################################
def select_by_age(master_dictionary,lo=0, hi=1e9, date_to_calc_age=None):
    """ 
    This function returns the dictionaries of the individuals within the age range. 
    
    Args:
        **master_dictionary** (list): Full list of the dictionaries.

        **lo** (int): The lower bound of the targeted age range.
        *Defaults to: 0*
        
        **hi** (int): The upper bound of the targeted age range.
        *Defaults to: 1e9*
        
    Returns: 
        **dictionary_subset** (list): The list of dictionaries of the individuals that are within the age range. 
        
    """
    
    # Put the date_to_calc_age into a datetime.datetime object
    if date_to_calc_age is not None:
        if type(date_to_calc_age) == str:
            date_to_calc_age = get_date_from_string(date_to_calc_age)
    else:
        date_to_calc_age = datetime.now()

    # Gets the personal IDs within the age range specified. 
    personal_IDs=[]
    
    for num,ind in enumerate(master_dictionary):
        age = calc_age(ind['DOB'],date_to_calc_age)
        age = age.days/365.0 # Convert to years as float
        if age>=lo and age<=hi:
            personal_IDs.append(ind['Personal ID'])
    personal_IDs=np.unique(personal_IDs)
    personal_IDs.sort()
    print("%d people have been selected." % (len(personal_IDs)))
    
    dictionary_subset = subset_from_dictionary(personal_IDs,master_dictionary)
    
    return dictionary_subset




################################################################################
# Gets information from the selected personal IDs passed through
################################################################################
def subset_from_dictionary(personal_IDs,full_dictionary,matching_key='Personal ID'):
    """ This function gets the subset of dictionaries from the personal IDs that are passed in.
    
    Args:
        **personal_IDs** (array): The list of personal IDs to get the dictionaries. 
        
        **full_dictionary** (list): The full list of dictionaries that has been made.
        
        **matching_key** (string): The key that determines the cross referencing between the files. 
        *Defaults to: 'Personal ID'*
    
    Returns: 
        **inds** (list): The subset of dictionaries with the personal IDs inputted. 
        
    """

    inds = []
    
    for pid in personal_IDs:
        for client in full_dictionary:
            if client[matching_key]==pid:
                inds.append(client)
                break

    return inds




# ASK CARES FOLKS IF THIS SHOULD BE NAMED BY PROGRAMS OR PROJECTS
def select_by_number_of_programs(master_dictionary, num_of_programs):
    """ 
    This function returns the dictionaries of the individuals that have at least the number of programs entered. 
    
    
    Args:
        **master_dictionary** (list): Full list of the dictionaries.
        
        **num_of_programs** (int): The lower number to how many programs an individual must have to be returned.
        
    Returns: 
        **dictionary_subset** (list): The list of dictionaries of the individuals that have at least the number of programs inputted.
        
    """
    
    personal_IDs = []
    for num,ind in enumerate(master_dictionary):
        prog_list = ind['Programs']
        if len(prog_list) > (num_of_programs -1):
            personal_IDs.append(ind['Personal ID'])
                                
    personal_IDs=np.unique(personal_IDs)
    personal_IDs.sort()
    print((len(personal_IDs)))
    
    dictionary_subset = subset_from_dictionary(personal_IDs,master_dictionary)
    
    return dictionary_subset
    
    
    
def select_by_program_type(master_dictionary, prog_type):
    """ 
    This function returns the dictionaries of the individuals that have stayed at the inputted program type.
    
    
    Args:
        **master_dictionary** (list): Full list of the dictionaries.
        
        **prog_type** (str): The type of prgram that the individual must have stayed at.
        
    Returns: 
        **dictionary_subset** (list): The list of dictionaries of the individuals that have 
        
    """
    
    personal_IDs = []
    for num, ind in enumerate(master_dictionary):
        prog_list = ind['Programs']
        
        for p in prog_list:
            if (p['Project type'] == prog_type):
                personal_IDs.append(ind['Personal ID'])
    
    
    personal_IDs=np.unique(personal_IDs)
    personal_IDs.sort()
    print((len(personal_IDs)))
    
    dictionary_subset = subset_from_dictionary(personal_IDs,master_dictionary)
    
    return dictionary_subset
    
    

