import numpy as np
import pandas as pd
import os 

# read data.txt, this assumes it is in the same directory as restaurant.py
dir_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(dir_path + "/data.txt", encoding='latin-1')

# drop NA zipcodes
data_dropna = data.dropna(subset = ['ZIPCODE'])

# sort dataframe by ascending inspection date
data_gradesort = data_dropna.sort_values('GRADEDATE')

# remove duplicate restaurants using unique CAMIS value, keeping most recent inspection date
dataset = data_gradesort.drop_duplicates(subset = 'CAMIS', keep = 'last')

# use groupby to find zipcodes with more than 100 restaurants
group = dataset.groupby('ZIPCODE').count().reset_index()
group100 = group[group.CAMIS > 100]

# obtain unique zipcode list
ziplist = group100['ZIPCODE'].tolist()

# filter the dataframe of unique restaurants by the zipcodes in the zipcode list
restaurants = dataset[dataset['ZIPCODE'].isin(ziplist)]

outputlist = []

# for every zipcode, do the following:
# obtain a list of restaurants in that zipcode
# calculate the mean score for that list
# append to outputlist a tuple containing the zipcode, mean score, and # of restaurants
for zipcode in ziplist:
    restaurantzip = restaurants[restaurants.ZIPCODE == zipcode]
    averagescore = restaurantzip['SCORE'].mean()
    tuple = (zipcode, averagescore, len(restaurantzip))
    outputlist.append(tuple)
    
# sort the output list by second value of each tuple, which happens to be mean score
outputlist = sorted(outputlist, key=lambda tup: tup[1], reverse = True)
print(outputlist)

# write list of tuples to text file
with open('output.txt', 'w') as file:
    for output in outputlist:
        file.write(str(output) + "\n")
        
# write slightly modified list of tuples to text file
# this list has parantheses removed to allow as input into CARTO
with open('carto_output.txt', 'w') as file:
    for output in outputlist:
        file.write(str(output)[1:-1] + "\n")