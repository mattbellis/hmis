#'''
import os
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta, datetime
import pickle
import matplotlib.pyplot as plt
from hmis.general import calc_age
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
    namesEN = enrollment_data['PersonalID']
  
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

    return enrollment_data, exit_data, project_data, client_data, site_data






################################################################################
# Make the large list of dictionaries.
################################################################################
def create_dictionary_list(directory='~/hmis_data/',filenames=None,max_people=None):
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
    enrollment_data,exit_data,project_data,client_data,site_data = read_in_data(directory=directory,verbose=True)
    
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
    pidEN = enrollment_data['PersonalID']
    pidEX = exit_data['PersonalID']
    pidCL=client_data['PersonalID']
            
    # Get entry and exit dates from each file.
    entry_date=enrollment_data['EntryDate']
    exit_date=exit_data['ExitDate']

    # Get project IDs for each file.
    project_entry_ID_EN=enrollment_data['ProjectEntryID']
    project_entry_ID_EX = exit_data['ProjectEntryID']
    projectID_EN=enrollment_data['ProjectID']
    
    # Get info from client file.
    client_dob= client_data['DOB']
    
    
    # Get site zip codes.
    zip_codes=site_data['ZIP']
    projectID_site=site_data['ProjectID']  
    
    # List of all of the projects in the CoC.
    project_index=project_types()

    # Keep track of how much time has passed
    start_processing = time.time()
    icount = 0
    for pid in personalids:

        if icount%100==0:
            print("Processed %d out of %d Personal IDs - %0.2f minutes" % (icount,npersonalids,(time.time()-start_processing)/60.))

        if max_people is not None:
            if icount >= max_people:
                break

        unames = np.unique(pidEN) 

        # Get all Enrollment, Exit and Client indices from each respective file.
        enroll_idx = pidEN==pid 
        exit_idx   = pidEX==pid 
        client_idx = pidCL==pid

        # Gets the entry dates, exit dates, and DOB for all of the indicies.
        indate = entry_date[enroll_idx] 
        outdate = exit_date[exit_idx] 
        dob_date = client_dob[client_idx]
        dob_date = str(dob_date.values[0])
        
        # Calculates the age of the individual.
        #dob = calc_age(str(dob_date.values[0]))
        
        # Get the Project IDs 
        peid = projectID_EN[enroll_idx]  
        
        program_list=[]
        
        # Loop through the entry date, exit date and project ID for each project that an individual has.
        for num,(idate, odate, projid) in enumerate(zip(indate, outdate, peid)):
            
            # Get the project type
            project_num = projectID_PR[projectID_PR==projid].index[0]

            '''
            print("---------")
            print("icount: ",icount)
            print("pid: ",`pid)
            print("project_num: ",project_num)
            print("projid: ",projid)
            print(projectID_PR[projectID_PR==projid])
            print(projectID_PR[projectID_PR==projid].index[0])
            print(project_type[project_num])
            print(int(project_type[project_num])-1)
            print(len(project_index))
            '''

            this_proj_type = project_index[int(project_type[project_num])-1]

            # Get the Zip code for the project
            if (len(zip_codes[projid==projectID_site])>0):
                num_for_zip = zip_codes[projid==projectID_site].index[0]

            this_zip=zip_codes[num_for_zip]

            # Get the entry and exit dates.
            thisindate = indate[indate.index[num]]
            thisoutdate = outdate[outdate.index[num]]
            
            # If there is an exit date split the date: else, use today's date as the end date.
            if len(thisoutdate)>0:
                
                if thisoutdate.find('/')>=0:
                    month,day,year = thisoutdate.split('/')
                elif thisoutdate.find('-')>=0:
                    year,month,day = thisoutdate.split('-')
                else:
                    print("Can't recognize date format...")
                    print(thisoutdate)
                    exit(-1)
                
            else:
                now = datetime.now()
                year,month,day = now.year, now.month, now.day

            end = dt.datetime(int(year),int(month),int(day))
            
            if thisindate.find('/')>=0:
                month,day,year = thisindate.split('/')
            elif thisindate.find('-')>=0:
                year,month,day = thisindate.split('-')
            else:
                print("Can't recognize date format...")
                print(thisindate)
                exit(-1)
            


            start = dt.datetime(int(year),int(month),int(day))

            los=(end-start)

            program_list.append({'Admission date': thisindate, 'Discharge date':thisoutdate, 'Length of stay':los, 'Project type': this_proj_type, 'Project Zip Code':this_zip})
            
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
    dictionary_list = pickle.load(infile)
    
    return dictionary_list







    
    














