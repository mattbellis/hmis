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
    
    
################################################################################
# Get information from the original data
################################################################################
def get_additional_info(IDs,idtype='Personal',org_data=None,info=None):
    """ This function gets additional information on an individual,
    project, or an indiviuals entry into a project based on their PersonalID,
    ProjectID, or ProjectEntryID respectively.
    
    Args:
        **IDs** (list or string): The list of IDs as strings or a single ID.
        
        **idtype** (string): 'Personal' or 'Project' or 'ProjectEntry' which 
        tells the program what type of data to retrieve.

        **org_data**: (dictionary of Panda data frames) This is the output of the 
        read_in_data command. 

        **info** (list or string): This is a string or list of strings, where
        the strings are the headers of the Pandas dataframes and the information
        to be returned. 

    Return:
        **information** (dictionary) This is a dictionary with the keys representing
        the IDs passed in and the values are dictionaries with those keys being
        the different pieces of information passed in with the info variable. 

     """

    # Error checking
    if idtype != 'Personal' and idtype != 'Project' and idtype != 'ProjectEntry':
        print("type must be \'Personal\' or \'Project\' or \'ProjectEntry\'!!!")
        print("Instead, idtype is %s" % (idtype))
        print("Returning from get_additional_info() without doing anything")
        return None

    if org_data is None:
        print("org_data must be passed in!")
        print("Instead, org_data is %s" % (org_data))
        print("This is the original data as returned by the read_in_data() function")
        print("Returning from get_additional_info() without doing anything")
        return None

    if info is None:
        print("info must be passed in!")
        print("Instead, info is %s" % (info))
        print("This should be a header or headers (as a list) for the original files.")
        print("Returning from get_additional_info() without doing anything")
        return None


    # Get the list of original .csv files from which we'll look for this info. 
    # We can add to this list later, if there is interest.
    list_of_files = []
    idkey = "%sID" % (idtype)
    if idtype=='Personal':
        list_of_files.append('Client')
    elif idtype=='ProjectEntry':
        list_of_files.append('Enrollment')
        list_of_files.append('Exit')
    elif idtype=='Project':
        list_of_files.append('Site')
        list_of_files.append('Project')

    if type(IDs)==str:
        IDs = [IDs]

    if type(info)==str:
        info = [info]

    # Check that the info keys are actually in the headers, including the idkey
    # which will be PersonalID or ProjectID or ProjectEntry.
    for header in info + [idkey]:

        found_header = False
        for name in list_of_files:

            # List of headers from dataframe
            headers = list(org_data[name].columns.values)

            if header in headers:
                found_header = True
                break

        if found_header==False:
            print("%s not found in any of the headers in the files!" % (header))
            print("Returning from get_additional_info() without doing anything")
            return None

    values = {}

    for ID in IDs:

        # For the person or project
        values[ID] = {}

        for header in info:

            # Loop over the different files in which to look.
            for name in list_of_files:
                filedata = org_data[name]
                # We are going to assume that the ID only appears once!
                index = filedata[filedata[idkey] == ID].index.tolist()

                if len(index)==1:
                    index = index[0]
                elif len(index)==0:
                    break
                else:
                    print("%s appears more than once in the %s file!!!" % (header, name))
                    print("Using only the first appearence, but this might not be right!")
                    index = index[0]

                if header in list(filedata.columns.values):
                    value = filedata.iloc[index][header] 
                    if value != value:
                        value = "EMPTY"
                    values[ID][header] = value

    return values

    
    















