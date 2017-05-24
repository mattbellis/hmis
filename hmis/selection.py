







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
    
    # Gets the personal IDs within the age range specified. 
    people=[]
    for num,ind in enumerate(filename):
        if ind['Age']>=lo and ind['Age']<=hi:
            people.append(ind['Personal ID'])
    people=np.unique(people)
    people.sort()
    print((len(people)))
    
    ppl = get_subset_from_dictionary(people,filename)
    
    return ppl




