import numpy as np
import pickle




################################################################################
# Read in the pickled dictionary file.
################################################################################
def read_dict_file(filename):
    """ This function finds the individuals within the age range and returns the dictionaries of those individuals. 
    
    Args:
        **filename** (str): The name of the file that will be pickled.
    
    Return:
        **dict_file** (list): All individual dictionaries in the file passed in.
   
        
    """
    
    # Open and pickle the file. 
    infile = open(filename)
    dict_file = pickle.load(infile)
    
    return dict_file








################################################################################
# Gets IDs within a certain age range.
################################################################################
def get_subset_with_age_range(filename,lo=0, hi=1e9, matching_key='Personal ID'):
    """ This function finds the individuals within the age range and returns the dictionaries of those individuals. 
    
    Args:
        **filename** (string): The name of the file that holds all of the dictionaries.
        
        **lo** (int): The lower bound of the targeted age range.
        Defaults to: 0
        
        **hi** (int): The upper bound of the targeted age range.
        Defaults to: 1e9
        
        **matching_key** (string): The value that determines the cross referencing between the files. 
        Defaults to: 'Personal ID'
    
    Returns: 
        **people** (list): The list of personal IDs that are within the range inputted. 
        
    """
    fn = read_dict_file(filename)
    
    # Gets the personal IDs within the age range specified. 
    people=[]
    for num,ind in enumerate(fn):
        if ind['Age']>=lo and ind['Age']<=hi:
            people.append(ind['Personal ID'])
    people=np.unique(people)
    people.sort()
    print((len(people)))
    
    ppl = get_subset_from_dictionary(people,fn)
    
    return ppl



################################################################################
# Gets information from the selected personal IDs passed through
################################################################################
def get_subset_from_dictionary(names,full_dictionary,matching_key='Personal ID'):
    """ This function gets the subset of dictionaries from the personal IDs that are passed in.
    
    Args:
        **names** (list): The list of personal IDs for analysis.
        
        **full_dictionary** (): The file of dictionaries that has been made.
        
        **matching_key** (string): The value that determines the cross referencing between the files. 
        Defaults to: 'Personal ID'
    
    Returns: 
        **inds** (list): The dictionaries of the individuals with the personal IDs inputted. 
        
    """

    inds = []

    for name in names:
        for client in full_dictionary:
            if client[matching_key]==name:
                inds.append(client)
                break

    return inds

