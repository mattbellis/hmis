#'''
import os
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta, datetime
import pickle
import matplotlib.pyplot as plt
from hmis.general import calc_age,get_date_from_string
import time


################################################################################
# The following functions are used to read in data from the standard HMIS data
# export and then create a master dictionary file containing the individuals
# and information about them and the care they have received. 
#
# By converting the data to a dictionary, the subsequent data exploration is
# *much* faster, even though the initial creation of the dictionary can take
# some time. 
################################################################################

# List of all of the projects in the CoC.
def project_types():

    # This comes from the HMIS Data Dictionary and might need to updated every now and then from their documentation.
    proj_types=['Emergency Shelter', \
                'Transitional Housing', \
                'PH - Permanent Supportive Housing', \
                'Street Outreach', \
                'RETIRED', \
                'Services Only', \
                'Other', \
                'Safe Haven', \
                'PH - Housing Only', \
                'PH - Housing with Services', \
                'Day Shelter', \
                'Homelessness Prevention', \
                'PH - Rapid Re-Housing','Coordinated Assesment']

    return proj_types


################################################################################
# Get all of the personal IDs
################################################################################
def get_pids(enrollment_data):
    """ This function returns the personal IDs of the individuals from the enrollment file.
    
    Args: 
        **enrollment_data** (pandas Data Frame): Data from the enrollment file that has been already read in.
        The file should have been read in with Pandas so we are passing it in as a pandas.DataFrame.
        
    Returns:
        **personalids** (numpy array): All Personal IDs from the individuals in the enrollment file.
        The Personal ID is used to identify individuals.
    
    """
    #namesEN = enrollment_data['PersonalID']
    namesEN = enrollment_data['PIN']
  
    return np.array(namesEN)


################################################################################
# Read in the file names only when we call this function.
################################################################################
def read_in_data(directory='~/hmis_data/',filenames=['Enrollment.csv','Exit.csv','Project.csv','Client.csv','Site.csv'],verbose=False):
    
    """ This function reads all of the HMIS files inputted using pandas.
    
    Args: 
        **directory** (string, optional): The directory where all of the HMIS files are stored. 
        *Defaults to '~/hmis_data/'.*
            
        **filenames** (list, optional): A list of the filenames from which we will be reading the data.
            These files come from the standard HMIS data dump. 
            *Defaults to  ['Enrollment.csv','Exit.csv','Project.csv','Client.csv','Site.csv'].*
            
        **verbose** (bool, optional): If this is True, additional information is printed to the screen.
        *Defaults to False.*
        
    Returns:

        **A dictionary containing the following pieces of information, with keys referenced by the original file names (e.g. Enrollment.csv --> Enrollment)**

        **enrollment_data** (Data Frame): All of the information from the enrollment file.
        
        **exit_data** (Data Frame): All of the information from the exit file.
        
        **project_data** (Data Frame): All of the information from the project file.
        
        **client_data** (Data Frame): All of the information from the client file.
        
        **site_data** (Data Frame): All of the information from the site file.
    
    """
    # This takes care of things if the user passes in a tilde '~' which you want to expand to /home/USER/.
    directory = os.path.expanduser(directory)


    enrollment_data,exit_data,project_data,client_data,site_data = None,None,None,None,None

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
            enrollment_data = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==1:
            exit_data = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==2:
            project_data = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==3:
            client_data = pd.read_csv(fullpath,delimiter=',',dtype=str)
        elif i==4:
            site_data=pd.read_csv(fullpath,delimiter=',',dtype=str)

    # Put original data into one large dictionary
    org_data = {} 
    all_files = [enrollment_data, exit_data, project_data, client_data, site_data]
    for f,a in zip(filenames,all_files):
        key = f.split('.')[0]
        org_data[key] = a

    return org_data






################################################################################
# Make the large list of dictionaries.
################################################################################
def create_dictionary_list(directory='~/hmis_data/',filenames=['Enrollment.csv','Exit.csv','Project.csv','Client.csv','Site.csv'],max_people=None):
    """ This function creates a list of all dictionaries in the enrollment file.
    
    Args:
        **directory** (string, optional): The directory where all of the HMIS files are stored. 
        *Defaults to '~/hmis_data/'.*
            
        **filenames** (string, optional): The name of the files to get information from.  
        *Defaults to None.*
            
        **max_people** (int, optional): For debugging. The maximum number of people you
        use to build the file. 
        *Defaults to None which reads in all people.*
            
    Returns:
        **individuals** (list): This is a list of all the individual's dictionaries.
    
    """
    print(directory)
    # Read in all of the given HMIS files.
    org_data = read_in_data(directory=directory,filenames=filenames,verbose=True)
    enrollment_data = org_data["Enrollment"]
    exit_data = org_data["Exit"]
    project_data = org_data["Project"]
    client_data = org_data["Client"]
    #site_data = org_data["Site"]
    site_data = org_data["Geography"] # This might be the name of things as of 081418
    #site_data = org_data["Project"] # 
    
    # Get all of the personal IDs from the enrollment file.
    personalids = get_pids(enrollment_data)
    
    # If the personal ID is not a list make it a list of one variable
    if type(personalids) != list and type(personalids) != np.ndarray:
        personalids = [personalids]

    # Some data will be duplicated as multiple people will appear multiple times.
    # So pull out only the unique personal IDs. 
    personalids = np.unique(personalids)

    npersonalids = len(personalids)
        
    individuals = []
    
    # Get project IDs from the Project.csv file.
    projectID_PR = project_data['ProjectID']
    project_type = project_data['ProjectType']
    
    # Get personal IDs from each file.
    #pidEN = enrollment_data['PersonalID']
    #pidEX = exit_data['PersonalID']
    #pidCL=client_data['PersonalID']

    pidEN = enrollment_data['PIN']
    pidEX = exit_data['PIN']
    pidCL=client_data['PIN']
            
    #unames = np.unique(pidEN) 

    # Get entry and exit dates from each file.
    entry_date=enrollment_data['EntryDate']
    exit_date=exit_data['ExitDate']

    # Get project IDs for each file.
    #project_entry_ID_EN=enrollment_data['ProjectEntryID']
    #project_entry_ID_EX = exit_data['ProjectEntryID']
    project_entry_ID_EN=enrollment_data['EnrollmentID']
    project_entry_ID_EX = exit_data['EnrollmentID']
    projectID_EN=enrollment_data['ProjectID']
    
    # Get info from client file.
    client_dob= client_data['DOB']
    
    # Get site zip codes.
    projectID_site=site_data['ProjectID']  
    zip_codes=site_data['ZIP']
    # Will change this back after Dutchess county stuff. Need to look
    # further down in code as well
    #zip_codes=(12603*np.ones(len(projectID_site),dtype=int)).astype(str)
    
    # List of all of the projects in the CoC.
    project_index=project_types()

    # Keep track of how much time has passed
    start_processing = time.time()
    icount = 0
    for pid in personalids:

        if icount%1000==0:
            print("Processed %d out of %d Personal IDs - %0.2f minutes" % (icount,npersonalids,(time.time()-start_processing)/60.))

        if max_people is not None:
            if icount >= max_people:
                break

        #unames = np.unique(pidEN) 

        # Get all Enrollment, Exit and Client indices from each respective file.
        enroll_idx = pidEN==pid 
        exit_idx   = pidEX==pid 
        client_idx = pidCL==pid

        # Check to make sure we can find the client in the Client.csv file. 
        # If we can't then break and move on. 
        if len(client_idx[client_idx==True]) == 0:
            print("\nCannot find %s in Client.csv!" % (pid))
            print("Skipping and moving on...\n")
            continue

        # Gets the entry dates, exit dates, and DOB for all of the indicies.
        # Save them as datetime.datetime objects
        indate = entry_date[enroll_idx] 
        outdate = exit_date[exit_idx] 

        dob_date = client_dob[client_idx]
        dob_date = get_date_from_string(str(dob_date.values[0]))
        
        # Get the Project IDs 
        peid = projectID_EN[enroll_idx]  
        projentryid = project_entry_ID_EN[enroll_idx]
        
        program_list=[]
        
        # Loop through the entry date, exit date and project ID for each project that an individual has.
        #print(len(indate))
        for num,(idate, odate, projid,projenid) in enumerate(zip(indate, outdate, peid, projentryid)):
            
            # Get the project type
            project_num = projectID_PR[projectID_PR==projid].index[0]

            '''
            print("---------")
            print("icount: ",icount)
            print("pid: ",pid)
            print("project_num: ",project_num)
            print("projid: ",projid)
            print(projectID_PR[projectID_PR==projid])
            print(projectID_PR[projectID_PR==projid].index[0])
            print(project_type[project_num])
            print(int(project_type[project_num])-1)
            print(len(project_index))
            '''

            #print("project_num", project_num)
            #print("project_type[project_num]",project_type[project_num], type(project_type[project_num]))
            #print("project_index", project_index)
            #print(int(float(project_type[project_num]))-1)
            this_proj_type = project_index[int(float(project_type[project_num]))-1]

            # Get the Zip code for the project
            #'''
            if (len(zip_codes[projid==projectID_site])>0):
                num_for_zip = zip_codes[projid==projectID_site].index[0]

            this_zip=zip_codes[num_for_zip]
            #'''
            #this_zip='12603'

            # Get the entry and exit dates.
            thisindate = indate[indate.index[num]]
            thisoutdate = outdate[outdate.index[num]]
            
            # If there is an exit date split the date: else, use today's date as the end date.
            end = None
            if len(thisoutdate)>0:
                end = get_date_from_string(thisoutdate)
            else:
                end = datetime.now()

            start = get_date_from_string(thisindate)
            
            los=(end-start)

            program_list.append({'Admission date': start, 'Discharge date':end, 'Length of stay':los, 'Project type': this_proj_type, 'Project Zip Code':this_zip, 'Project ID':projid, 'Project Entry ID':projenid})
            
            
        individuals.append({'Personal ID':pid, 'DOB': dob_date,'Programs':program_list})

        icount += 1
        
    return individuals



################################################################################
# Saves the dictionary file by pickling the file.
################################################################################
def save_file(inds,filename):
    """ This function creates a file of the dictionaries that passed in.
    
    Args:
        **inds** (list): The list of dictionaries.
        
        **filename** (string): The name of the file that the dictionaries will be saved as. This should be a .pkl file. 
    
    """
    outfile = open(filename,'wb')
    pickle.dump(inds,outfile,pickle.HIGHEST_PROTOCOL)
    outfile.close()




################################################################################
# Read in the pickled dictionary file.
################################################################################
def read_dictionary_file(filename):
    """ This function returns the list of dictionaries that are in the inputted file.
    
    Args:
        **filename** (str): The file to be read in using pickle.
    
    Return:
        **dictionary_list** (list): List of the dictionaries in the file passed in.
        
    """
    
    # Open and pickle the file. 
    infile = open(filename, 'rb')
    try:
        dictionary_list = pickle.load(infile)
    except ValueError as detail:
        error_string = """%s
        This is most likely caused by the file being pickled with a higher protocol in Python3.x and then trying to open it with a lower protocol in 2.7.\n
        You will want to recreate the file using the same version of python as the one you are using to open it.\n
        File is not read in!""" % detail
        raise ValueError(error_string)
    except UnicodeDecodeError as detail:
        error_string = """%s
        This is most likely caused by the file being pickled with a lower protocol in Python2.7 and then trying to open it with a higher protocol in 3.x.\n
        You will want to recreate the file using the same version of python as the one you are using to open it.\n
        File is not read in!""" % detail
    
    return dictionary_list



