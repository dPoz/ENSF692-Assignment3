# school_data.py
# Author: David Pozniak
#
# A terminal-based application for computing and printing statistics based on given input.
#

# Note: there are no classes, methods, or fucntions created to document with docstrings, so only comments will be used throughout.

import numpy as np
import pandas as pd # pandas used to easily read csv file
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

def main():
    
    # using the given imported arrays for convenience
    data = np.array([year_2013, 
                     year_2014, 
                     year_2015, 
                     year_2016, 
                     year_2017, 
                     year_2018, 
                     year_2019, 
                     year_2020, 
                     year_2021, 
                     year_2022])
    
    # reshaping the data so that each year represnes the third dimention of the array.
    data = data.reshape(10, 20, 3)
    
    # reading csv file to access School Names and School Code columns.
    try:
        dataraw = pd.read_csv('Assignment3Data.csv')
    except:
        print("\nPlease make sure the Assignment3Data.csv file is in the same directory as with this python script.\n"*4)
        exit()
    
    # storing the School Names and School Code columns into a dictionary to validate user input.
    school_and_code = dict(zip(np.array(dataraw['School Name']), np.array(dataraw['School Code'], dtype = str)))
    
    print("\nENSF 692 School Enrollment Statistics:\n")

    # Stage 1 requirements:
    # shape and ndim provide the shape and the number of dimentions, respectively, the array has.
    print("Shape of full data array: {}".format(data.shape))
    print("Dimensions of full data array: {}".format(data.ndim))

    # Prompt for user input
    user_input = input("Please enter the highschool name or school code: ")
    
    # this is used in favor of a try and except method, it keeps looping until the users input is inside either the keys or the values of the school_and_code dictionary.
    while(user_input not in school_and_code.keys() and user_input not in school_and_code.values()):
        print("\nYou must enter a valid school name or code.\n")
        # although not expressly asked for in the README2.md file or screenshot, printing out the school_and_code dictionary allows the user know what is valid.
        print("School Name: School Code")
        for school, code in school_and_code.items():
            print("{}: {}".format(school,code))
        user_input = input("\nPlease enter the highschool name or school code: ")

    # the main part of this is the enumeration, it provides the index from the school_and_code dictionary that is used to filter the data such that only the intended school data is used.
    index, schoolinfo = zip(*((i, (key, val)) for (i, (key, val)) in enumerate(school_and_code.items()) if key == user_input or val == user_input))

    school_name, school_code = schoolinfo[0]

    # Stage 2 requirements:
    print("\n***Requested School Statistics***\n")
    
    # subarray view of data filtering out all but the intended school, also applying an ~isnan mask onto it to eliminate NaN values from throwing errors.
    school_data = data[:,index,:][~np.isnan(data[:,index,:])]
    # reshaping required after mask, this is not very robust, it generally only works when entire row of data is NaN.
    school_data = school_data.reshape(int(school_data.size/3),3) 
    
    # Prints out all stage 2 required stats:
    print("School Name: {}, School code: {}".format(school_name, school_code))
    print("Mean enrollment for Grade 10: {}".format(int(np.mean(school_data[:,0]))))
    print("Mean enrollment for Grade 11: {}".format(int(np.mean(school_data[:,1]))))
    print("Mean enrollment for Grade 12: {}".format(int(np.mean(school_data[:,2]))))
    print("Highest enrollment for a single grade: {}".format(int(np.max(school_data))))
    print("Lowest enrollment for a single grade: {}".format(int(np.min(school_data))))
    # loops through all years printing the sum of enrollment for all grades.
    for x in range(13,(int(school_data.size/3)+13)):
        print("Total enrollment for 20{}: {}".format(x, int(np.sum(school_data[x-13,:]))))
    print("Total ten year enrollment: {}".format(int(np.sum(school_data[:,:]))))
    # python was giving a rounding error here with the floored int, 9.99999 vs 10 corrected the issue
    print("Mean total enrollment over 10 years: {}".format(int(np.sum(school_data[:,:]/9.99999)))) 
    # checks to see if any Trues in the mask, and if so, then applies it to calculate the mediam, otherwise prints "No enrollments over 500.".
    if(np.any(school_data[:,:] > 500)):
        print("For all enrollment over 500, the median value was: {}".format(int(np.median(school_data[:,:][school_data[:,:] > 500]))))
    else:
        print("No enrollments over 500.")

    # Prints out all stage 3 requirements:
    print("\n***General Statistics for All Schools***\n")
    print("Mean enrollment in 2013: {}".format(int(np.mean(data[0,:,:][~np.isnan(data[0,:,:])]))))
    print("Mean enrollment in 2022: {}".format(int(np.mean(data[9,:,:][~np.isnan(data[9,:,:])]))))
    print("Total graduation class of 2022: {}".format(int(np.sum(data[9,:,2][~np.isnan(data[9,:,2])]))))
    print("Highest enrollment for a single grade: {}".format(int(np.max(data[~np.isnan(data)]))))
    print("Lowest enrollment for a single grade: {}\n".format(int(np.min(data[~np.isnan(data)]))))

if __name__ == '__main__':
    main()

