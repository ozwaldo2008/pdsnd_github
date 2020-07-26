import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data you absolute weapons!')

    #define valid user inputs
    valid_inputs = {'city' : ['chicago', 'new york city', 'washington'] , 'month' : ['january','february','march','april','may','june','july','august','september','october','november','december','all'], 'day' :['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']}

    # get user input for city (chicago, new york city, washington).
    city = input('\nWould you like to look at data for Chicago, New York City or Washington?\n').lower()

    #make sure user inputs valid city
    while city not in valid_inputs['city']:
      city = input('\nYour response could not be recognised. \nWould you like to look at data for Chicago, New York City or Washington?\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nWhich month of the year would you like to look at (January, February..etc)?\n').lower()

    #make sure user inputs valid month
    while month not in valid_inputs['month']:
      month = input('\nYour response could not be recognised. \nWhich month of the year would you like to look at (January, February..etc)?\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhich day of the week would you like to look at (Monday, Tuesday...etc)?\n').lower()

    #make sure user inputs valid day
    while day not in valid_inputs['day']:
      day = input('\nYour response could not be recognised. \nWhich day of the week would you like to look at (Monday, Tuesday...etc)?\n').lower()

    print('-'*40)
    return city, month, day

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
         # filter by month to create the new dataframe
        df.drop(df[df['month'] != month].index, inplace = True)

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df.drop(df[df['day'] != day.title()].index, inplace = True)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    popular_month = df['month'].mode()[0]
    print('\nMost common month: ', months[popular_month-1].title())

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print('\nMost common day: ', popular_day)

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour > 11:
      print('\nMost common start hour: {}pm'.format(popular_hour-12))
    elif popular_hour == 12:
      print('\nMost common start hour: {}pm'.format(popular_hour))
    else:
      print('\nMost common start hour: {}am'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_station_combination = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).index[0]
    print('\nThe most frequent station combination is for trips from {} to {}'.format(popular_station_combination[0],popular_station_combination[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['total travel time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    sum_travel_time = df['total travel time'].sum()
    total_days = sum_travel_time.days
    modulo_total_hours = int(sum_travel_time.seconds/(60**2))
    modulo_total_minutes = int(sum_travel_time.seconds/60-modulo_total_hours*60)
    modulo_total_seconds = (sum_travel_time.seconds%60)
    print('\nThe total travel time is {} days, {} hours, {} minutes & {} seconds'.format(total_days, modulo_total_hours, modulo_total_minutes, modulo_total_seconds))

    # display mean travel time
    mean_travel_time = df['total travel time'].mean()
    mean_minutes = int(mean_travel_time.seconds/60)
    mean_seconds = (mean_travel_time.seconds%60)
    print('\nThe mean travel time is {} minutes & {} seconds.'.format(mean_minutes,mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
    except:
        print('\nGender data is not available')
    else:
        gender = df['Gender'].value_counts()
        print(gender)

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
    except:
        print('\nBirth year data is not available')
    else:
        print('\nThe earliest birth year is {}, the most recent birth year is {} & the most common birth year is {}.'.format(int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):
    """Displays individual statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #define valid user responses
    valid_responses = {'positive responses' : ['y','yes','yeah','yep','ok','k','okay','alright'], 'negative responses' : ['n','no','nah','nope']}

    #ask user if they would like to look at 5 rows of individual trip data
    user_preference = input('\nWould you like to look at 5 rows of individual trip data?\n').lower()

    #check user responses & display data
    df.reset_index(drop=True,inplace=True)
    i = 4
    while user_preference not in valid_responses['negative responses']:
      while user_preference not in valid_responses['positive responses'] and user_preference not in valid_responses['negative responses']:
        user_preference = input('\nYour response could not be recognised. \nWould you like to look at 5 rows of individual trip data? (yes or no)\n').lower()
      if user_preference in valid_responses['positive responses']:
        for i in range(i-4,i):
         print('\n')
         print(df.loc[i])
        i += 5
        user_preference = input('\nWould you like to look at the next 5 rows of individual trip data?\n').lower()

def main():
    """
    Loads data & runs all sub-functions of the main program
    """
    while True:
        #prompt user filters & get data
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #display relevant statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip_data(df)

        #ask whether user would like to look at the data with new filters
        valid_responses = {'positive responses' : ['y','yes','yeah','yep','ok','k','okay','alright'], 'negative responses' : ['n','no','nah','nope']}
        restart = input('\nWould you like to look at the data with a new city/time filter?\n').lower()

        #safe guard against incorrect input
        while restart not in valid_responses['positive responses'] and restart not in valid_responses['negative responses']:
          restart = input('\nYour response could not be recognised. \nWould you like to look at the data with a new city/time filter? (yes or no)\n').lower()

        #terminate program if user doesn't want to restart
        if restart in valid_responses['negative responses']:
          print('\n\nProgram terminating...Goodnight you absolute weapons\n')
          break

if __name__ == "__main__":
	main()
