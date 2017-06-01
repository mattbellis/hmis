import hmis
import time

# Location of the 12 files from the HMIS data dump.
hmis_data_location = '~/hmis_data/'
start=time.time()

# Put together a dictionary of all the individuals in the HMIS
# data dump and determine the connections and relationships between
# the different entries in the different files.
print("Reading in and determining relationships in HMIS data...")
print("This might take a while...up to an hour, depending on your machine.")
inds = hmis.create_dictionary_list(directory=hmis_data_location)

# Write this dictionary to a pickled file.
print("Writing pickle file...")
hmis.save_file(inds, 'save_dicts_June1.pkl')


print("Done!")
print(time.time()-start)