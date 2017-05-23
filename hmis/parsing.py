#'''
import os
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta, datetime
import pickle
import matplotlib.pyplot as plt
#from collections import OrderedDict
#'''


# There are two ways to get the individuals to visualize and analyze. 
# The first method is to read in all of the data and create a dictionary file. This file holds every individual but can easily and quickly be read in once made.

# The second method is to create the dictionary of the individuals at analysis-time. 


################################################################################
# The following functions are to read in all of the data and create the all individuals dictionaries first.
################################################################################


################################################################################
# Get all of the personal IDs
################################################################################
def get_pids(enrollment_file):
    """ This function gets all of the personal ID in the enrollment file
    
    Args: 
        enrollment_file (Data Frame): the enrollment file that has been read in with pandas
        
    Returns:
        personalids (array): 
    
    """
    namesEN = enrollment_file['PersonalID']
    return np.array(namesEN)


################################################################################
# Read in the file names only when we call this function.
################################################################################
def read_in_data(directory='~/hmis_data/',filenames=None,verbose=False):
    """ This function reads all of the HMIS files.
    
    Args: 
        directory (string, optional): The directory where all of the HMIS files are stored. 
            Defaults to '~/hmis_data/'. 
        filesname (string, optional): The name of the files to get information from. 
            Defaults to None. 
        
    Returns:
        enrollment_file (Data Frame): All of the information from the enrollment file.
        exit_file (Data Frame): All of the information from the exit file.
        project_file (Data Frame): All of the information from the project file.
        client_file (Data Frame): All of the information from the client file.
        site_file (Data Frame): All of the information from the site file.
    
    """
    print(directory)
    # This takes care of things if the user passes in a tilde '~' which you want to expand to /home/USER/.
    directory = os.path.expanduser(directory)

    if filenames==None:
        filenames = ['Enrollment.csv','Exit.csv','Project.csv','Client.csv','Site.csv']

    enrollment_file,exit_file,project_file,client_file,site_file = None,None,None,None,None

    for i,filename in enumerate(filenames):

        fullpath = "%s/%s" % (directory,filename)
        
        # Prints the file that is being read in
        if verbose:
            print(("Reading in %s..." % (fullpath)))

        # If the path is not correct, statements will be printed to help identify the problem.
        if not os.path.isfile(fullpath):
            print(("Yikes!\n%s does not exist!" % (fullpath)))
            print("\nCheck to see if the filename or directory is incorrectly given")
            print("\nWill return None for all files so don't go any further!\n")
            return None,None,None,None

        # Actually reads the files.
        if i==0:
            enrollment_file = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==1:
            exit_file = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==2:
            project_file = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==3:
            client_file = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==4:
            site_file=pd.read_csv(fullpath,delimiter=',',dtype=str)

    return enrollment_file,exit_file,project_file,client_file, site_file



################################################################################
# Get age from birthdate.
################################################################################
def calc_age(birthdate):
    """ This function converts the birthdate to a datetime object and subtracts today's date. This calculates the age of an individual.
    
    Args:
        birthdate (string): The birthday of the individual.
            
    Returns:
        age (string): The age of the individual.
    
    
    """
    
    birth_year,birth_month,birth_day = birthdate.split('-')
    born = dt.datetime(int(birth_year),int(birth_month),int(birth_day))
    today = datetime.now()
    age= today.year-born.year - ((today.month,today.day) < (born.month, born.day))

    return age


################################################################################
# Make the large dictionary file.
################################################################################
def get_all_info_for_individuals_new(directory='~/hmis_data/',filenames=None):
    """ This function creates a file of all of the dictionaries in the given HMIS files.
    
    Args:
        directory (string, optional): The directory where all of the HMIS files are stored. 
            Defaults to '~/hmis_data/'. 
        filesname (string, optional): The name of the files to get information from.  
            Defaults to None. 
            
    Returns:
        individuals ()
    
    """
    print(directory)
    # Read in all of the given HMIS files.
    enrollment_file,exit_file,project_file,client_file,site_file = read_in_data(directory=directory,filenames=filenames,verbose=True)
    
    # Get all of the personal IDs from the enrollment file.
    personalids = get_pids(enrollment_file)
    

    # If the personal ID is not a list make it a list of one variable
    if type(personalids) != list and type(personalids) != np.ndarray:
        personalids = [personalids]
        
    individuals = []
    
    # Get project IDs from the Project.csv file.
    project_ID_from_file = project_file['ProjectID']
    project_type = project_file['ProjectType']
    
    # Get personal IDs from each file.
    namesEN = enrollment_file['PersonalID']
    namesEX = exit_file['PersonalID']
    namesCL=client_file['PersonalID']
            
    # Get entry and exit dates from each file.
    entry_date=enrollment_file['EntryDate']
    exit_date=exit_file['ExitDate']

    # Get project IDs for each file.
    project_entry_ID_EN=enrollment_file['ProjectEntryID']
    project_entry_ID_EX = exit_file['ProjectEntryID']
    projectID=enrollment_file['ProjectID']
    
    # Get info from client file.
    client_dob= client_file['DOB']
    
    
    # Get site zip codes.
    zip_codes=site_file['ZIP']
    projectID_site=site_file['ProjectID']
    
    
    
    # List of all of the projects in the CoC.
    project_index=['Emergency Shelter','Transitional Housing', 'PH - Permanent Supportive Housing', 'Street Outreach','RETIRED','Services Only','Other Safe Haven','PH - Housing Only','PH - Housing with Services','Day Shelter','Homelessness Prevention','PH - Rapid Re-Housing','Coordinated Assesment']

    
    icount = 0
    for pid in personalids:

        if icount%1000==0:
            print(icount)
        

        unames = np.unique(namesEN) 

        # Get all Enrollment, Exit and Client indices from each respective file.
        enroll_idx = namesEN==pid 
        exit_idx   = namesEX==pid 
        client_idx = namesCL==pid

        # Gets the entry dates, exit dates, and DOB for all of the indicies.
        indate = entry_date[enroll_idx] 
        outdate = exit_date[exit_idx] 
        dob_date = client_dob[client_idx]
        
        # Calculates the age of the individual.
        dob=calc_age(str(dob_date.values[0]))
        
        # Get the actual project entry IDs and project exit IDs to match up with the 
        #inpeid = project_entry_ID_EN[enroll_idx] 
        #outpeid = project_entry_ID_EX[exit_idx] 
        
        # Get the Project IDs 
        peid = projectID[enroll_idx]  
        
        program_list=[]
        
        # Loop through the entry date, exit date and project ID for each project that an individual has.
        for num,(idate,odate,projid) in enumerate(zip(indate,outdate,peid)):
            
            # Get the project type
            num_for_project= project_ID_from_file[project_ID_from_file==projid].index[0]
            this_proj_type= project_index[int(project_type[num_for_project])-1]
            
            # Get the Zip code for the project
            #num_for_zip=projectID_site[projid==projectID_site].index[0]
            #this_zip=zip_codes[num_for_zip]
            
            # Get the entry and exit dates.
            thisindate = indate[indate.index[num]]
            thisoutdate = outdate[outdate.index[num]]
            
            # If there is an exit date split the date: else, use today's date as the end date.
            if len(thisoutdate)>0:
                
                month,day,year = thisoutdate.split('/')
                
            else:
                now = datetime.now()
                year,month,day = now.year, now.month, now.day

            end = dt.datetime(int(year),int(month),int(day))
            month,day,year = thisindate.split('/')
            start = dt.datetime(int(year),int(month),int(day))

            los=(end-start)

            
            program_list.append({'Admission date': thisindate, 'Discharge date':thisoutdate, 'Length of stay':los, 'Project type': this_proj_type})
            #program_list.append({'Admission date': thisindate, 'Discharge date':thisoutdate, 'Length of stay':los, 'Project type': this_proj_type, 'Project Zip Code':this_zip})
            
        individuals.append({'Personal ID':pid, 'Age': dob,'Programs':program_list})

        icount += 1
        
    return individuals



################################################################################
# Saves the dictionary file with pickle.
################################################################################
def save_file(inds,filename):
    """ This function creates a file of all the dictionaries that are passed into this function.
    
    Args:
        inds (): All of the dictionaries from the people in the enrollment file.
        filename (string): The name of the file that the dictionaries will be saved as. Must be a .txt file. 
    
    """
    outfile = open(filename,'wb')
    pickle.dump(inds,outfile,pickle.HIGHEST_PROTOCOL)
    outfile.close()


################################################################################
# Gets IDs within a certain age range.
################################################################################
def get_subset_with_age_range(filename,lo=0, hi=1e9, matching_key='Personal ID'):
    """ This function finds the individuals within the age range and returns the dictionaries of those individuals. 
    
    Args:
        filename (string): The name of the file that holds all of the dictionaries.
        lo (int): The lower bound of the targeted age range.
            Defaults to: 0
        hi (int): The upper bound of the targeted age range.
            Defaults to: 1e9
        matching_key (string): The value that determines the cross referencing between the files. 
            Defaults to: 'Personal ID'
    
    Returns: 
        people (list): The list of personal IDs that are within the range inputted. 
        
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


################################################################################
# Gets information from the selected personal IDs passed through
################################################################################
def get_subset_from_dictionary(names,full_dictionary,matching_key='Personal ID'):
    """ This function gets the subset of dictionaries from the personal IDs that are passed in.
    
    Args:
        names (list): The list of personal IDs for analysis.
        full_dictionary (): The file of dictionaries that has been made.
        matching_key (string): The value that determines the cross referencing between the files. 
            Defaults to: 'Personal ID'
    
    Returns: 
        inds (list): The dictionaries of the individuals with the personal IDs inputted. 
        
    """

    inds = []

    for name in names:
        for client in full_dictionary:
            if client[matching_key]==name:
                inds.append(client)
                break

    return inds








    
    
 
    
    
    
    
    
    
################################################################################
# The following functions are to read in the data for the specified personal IDs.
################################################################################


################################################################################
# Get all of the personal IDs within an age range.
################################################################################
def get_dictionaries_with_age_range(lo=0,hi=1e9):
    """ This function finds the individuals within the age range and returns the personal IDs of those individuals. 
    
    Args:
        filename (string): The name of the file that holds all of the dictionaries.
        lo (int): The lower bound of the targeted age range.
            Defaults to: 0
        hi (int): The upper bound of the targeted age range.
            Defaults to: 1e9
    
    Returns: 
        people (list): The list of personal IDs that are within the range inputted. 
        
    """
    
    filename = read_in_data(filenames=['Client.csv'])
    filename = filename[0]
    namesCL = filename['PersonalID']
     
    client_dob = filename['DOB']
    people=[]
    for num,x in enumerate(client_dob):

        month,day,year = x.split('-')
        birthdate = dt.datetime(int(month),int(day),int(year))

        age = dt.datetime.now() - birthdate
        age_in_years = np.floor(np.abs(age.days/365.))

        if age_in_years>=lo and age_in_years<=hi:
            people.append(namesCL[num])
    return people
    
    
    
    
    
    
    
    













