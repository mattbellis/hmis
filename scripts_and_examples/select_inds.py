import hmis


# The name of the dictionary file that must be read in.
filename = 'save_dicts_May22.txt'

# The range of ages to be analyzed.
lo=15
hi=16


# Open and pickle the file. 
infile = open(filename)
read_dict_file = pickle.load(infile)

# Gets the subset of the individuals within the range specified. 
ppl = hmis.get_subset_with_age_range(read_dict_file,lo=lo,hi=hi)