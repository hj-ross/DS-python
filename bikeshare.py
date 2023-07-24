#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import calendar


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = list(calendar.month_name[1:7])
DAY_DATA = list(calendar.day_name)

def get_one_filter(ask_time_filter, filters):
    
    time_filter = ""
    
    while time_filter not in filters:
        time_filter = input(ask_time_filter).lower()
        if time_filter in filters[2:]:
            time_filter = 'all'
            
    return time_filter


def ask_for_other_filter(time_filter):
    choices = ['month', 'day']
    choice = ''
    yes_no = ['yes', 'y', 'no', 'n']
    
    ask_other_filter = "\nWould you like to also filter by {}\n?"
    if time_filter == choices[0]:
        while choice not in yes_no:
            choice = input(ask_other_filter.format(choices[1])).lower()
        print("choice was:", choice)
        if choice in yes_no[:2]:
            print("\nEntered getting day if statement. Choice was:", choice)
            return get_day()
    else: #day
        while choice not in yes_no:
            choice = input(ask_other_filter.format(choices[0])).lower()
        if choice in yes_no[:2]:
            return get_month()
    return 'all' # default if they don't want the second filter

def get_filters():

    """

    Asks user to specify a city, month, and day to analyze.

    Returns:

        (str) city - name of the city to analyze

        (str) month - name of the month to filter by, or "all" to apply no month filter

        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    ask_city = "Would you like to see data for Chicago, New York, or Washington?\n"
    city = ""
    
    while city not in CITY_DATA.keys():
        city = input(ask_city).lower()
        if city == 'new york':
            city += ' city'

    ask_time_filter = "Would you like to filter the data by month, day, or not at all?\n"
    filters = ['month', 'day', 'not at all', 'all', 'see all', 'none', 'no filter']
    time_filter = get_one_filter(ask_time_filter, filters)       
   
    
    month = "all"
    day = "all"
    if time_filter == filters[0]:
        month = get_month()
        day = ask_for_other_filter(time_filter)
    elif time_filter == filters[1]:
        day = get_day()
        month = ask_for_other_filter(time_filter)
    print('-'*40)

    return     city, month, day



def get_month():
    """Get the month for analysis."""
    
    ask_month = "Which month - January, February, March, April, May, or June?\n"
    month = ""
    
    # get user input for month ( january, february, ... , june)
    while month not in MONTH_DATA:
        month = input(ask_month).title()
        
    print("\nThe month chosen for analysis is: {}".format(month))
    
    return month



def get_day():
    """Get the day of the week for analysis."""
    
    ask_day = "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n"
    day = ""
    
    # get user input for day of week (monday, tuesday, ... sunday)
    while day not in DAY_DATA:
        day = input(ask_day).title()
        
    print("\nThe month chosen for analysis is: {}".format(day))
    
    return day



def load_data(city, month, day):

    """

    Loads data for the specified city and filters by month and day if applicable.



    Args:

        (str) city - name of the city to analyze

        (str) month - name of the month to filter by, or "all" to apply no month filter

        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

        df - Pandas DataFrame containing city data filtered by month and day

    """
    print("\nAnalyzing data for {}, for month: {}, and day of week: {}".format(city.title(), month, day))
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

   # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df

def gender(df, city):
    '''.
    Question: What are the counts of gender?
    
    Args: 
        (df) df - dataframe of filtered data
        (str) city - city analyzing
        
    Returns:
        none
    '''
    if city in ['new york city', 'chicago']:
        gender_data = df['Gender'].value_counts()
        print("\nGender distribution of riders:\n", gender_data.apply(lambda x: '{:,}'.format(x)))


def birth_years(df, city):
    '''
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    
    Args: 
        (df) df - dataframe of filtered data
        (str) city - city analyzing
        
    Returns:
        none
    '''
    if city in ['new york city', 'chicago']:
        print("\nEarliest rider birth year:", int(df['Birth Year'].min()))
        print("\nLatest rider birth year:", int(df['Birth Year'].max()))
        print("\nMost common rider birth year:", int(df['Birth Year'].mode()[0]))
    
def show_raw(df, row_start=0):
    '''
    Question: Allow user to view 5 rows of raw data at a time
    
    Args: 
        (df) df - dataframe of filtered data
        
    Returns:
        none
    '''
    raw_choices = ['yes', 'y', 'no', 'n']
    
    ask_raw = "\nWould you like to see{} raw data?\n".format(' more' if row_start else '')   
    raw_choice = ''

    # get user's choice
    while raw_choice not in raw_choices:
        raw_choice = input(ask_raw).lower()
    
    if raw_choice in raw_choices[:2]:
        pd.set_option('display.max_columns',200)
        print(df.iloc[row_start:row_start+5])
        show_raw(df, row_start+5)

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    city, month, day = get_filters()
    
    #print("Analyzing data for {}, for month: {}, and day of week: {}".format(city.title(), month, day))
    df = load_data(city, month, day)
    
    
    #1 Popular times of travel (i.e., occurs most often in the start time)
    
    if month == 'all':
        print('\nMost Popular Month:', MONTH_DATA[df.month.mode()[0]-1])
    
    
    if day == 'all':
        print('\nMost Popular Day:', df.day_of_week.mode()[0])
    
    
    # get most popular time
    
    popular_hour = df.hour.mode()[0]
    is_am = popular_hour < 12
    print('\nMost Popular Hour:', popular_hour if is_am else popular_hour -12, '{}'.format('AM' if is_am else 'PM'))
    
    #2 Popular stations and trip
    
    
    print('\nMost Popular Start Station:', df['Start Station'].mode()[0])
    print('\nMost Popular End Station:', df['End Station'].mode()[0])
    
    df['Trip'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    print('\nMost Popular Trip:', df.Trip.mode()[0])
    
    #3 Trip duration
    # formatted using advice from: https://www.geeksforgeeks.org/print-number-commas-1000-separators-python/
    
    total_time = df['Trip Duration'].sum() / 60
    print('\nTotal time biked:', '{:,.2f}'.format(total_time), ' minutes')
    
    print('\nAverage trip duration:', '{:,.2f}'.format(total_time / df.shape[0]), ' minutes')
    
    
    ## print value counts for each user type
    user_types = df['User Type'].value_counts()
    
    print("\nDistribution of user types:")
    print(user_types.apply(lambda x: '{:,}'.format(x)))
    
    gender(df, city)
    birth_years(df, city)    
    
    show_raw(df)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()

        

if __name__ == "__main__":
	statistics()

