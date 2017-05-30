import numpy as np


################################################################################
# Gets IDs within a certain age range.
################################################################################
def get_subset_with_age_range(dict_list,lo=0, hi=1e9, matching_key='Personal ID'):
    """ 
    This function returns the dictionaries of the individuals within the age range. 
    
    :param list dict_list: Full list of the dictionaries
    
    Args:
        **dict_list** (list): Full list of the dictionaries.

        **lo** (int): The lower bound of the targeted age range.
            Defaults to: 0
        
        **hi** (int): The upper bound of the targeted age range.
            Defaults to: 1e9
        
        **matching_key** (string): The value that determines the cross referencing between the files. 
            Defaults to: 'Personal ID'
    
    Returns: 
        **dict_subset** (list): The list of dictionaries of the individuals that are within the age range. 
        
    """
    
    # Gets the personal IDs within the age range specified. 
    personal_IDs=[]
    for num,ind in enumerate(dict_list):
        if ind['Age']>=lo and ind['Age']<=hi:
            personal_IDs.append(ind['Personal ID'])
    personal_IDs=np.unique(personal_IDs)
    personal_IDs.sort()
    print((len(personal_IDs)))
    
    dict_subset = get_subset_from_dictionary(personal_IDs,dict_list)
    
    return dict_subset




################################################################################
# Gets information from the selected personal IDs passed through
################################################################################
def get_subset_from_dictionary(personal_IDs,full_dictionary,matching_key='Personal ID'):
    """ This function gets the subset of dictionaries from the personal IDs that are passed in.
    
    Args:
        **personal_IDs** (array): The list of personal IDs to get the dictionaries. 
        
        **full_dictionary** (list): The full list of dictionaries that has been made.
        
        **matching_key** (string): The key that determines the cross referencing between the files. 
            Defaults to: 'Personal ID'
    
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




def get_subset_with_program_num(dict_list, num_of_programs, matching_key='Personal ID'):
    """ 
    This function returns the dictionaries of the individuals that have at least the number of programs entered. 
    
    :param list dict_list: Full list of the dictionaries
    
    Args:
        **dict_list** (list): Full list of the dictionaries.
        
        **num_of_programs** (int): The lower number to how many programs an individual must have to be returned.
        
        **matching_key** (string): The value that determines the cross referencing between the files. 
            Defaults to: 'Personal ID'
    
    Returns: 
        **dict_subset** (list): The list of dictionaries of the individuals that have at least the number of programs inputted.
        
    """

    
    personal_IDs = []
    for num,ind in enumerate(dict_list):
        prog_list = ind['Programs']
        if len(prog_list) > (num_of_programs -1):
            personal_IDs.append(ind['Personal ID'])
                                
    personal_IDs=np.unique(personal_IDs)
    personal_IDs.sort()
    print((len(personal_IDs)))
    
    dict_subset = get_subset_from_dictionary(personal_IDs,dict_list)
    
    return dict_subset
    
    
    
    
    
    
    