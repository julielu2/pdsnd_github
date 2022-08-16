import time
import numpy as np
import pandas as pd

# Lists and Dictionaries
city_list = ['chicago.csv', 'new_york_city.csv', 'washington.csv']
city_dict = {}
month_list = ['January', 'February', 'March', 'April', 'May', 'June']
day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for cityval in city_list:
    '''Loop which takes all csv files and turns them into a dictionary, with the city name being their index'''
    city_name = cityval[0:-4]
    city_dict[city_name] = cityval

#Functions
def get_values():
    """Prompts user to enter a city, month and a day
    
    Returns: 
        (str) city - name of the city
        (str) month - name of the month, or 'all' if no month filter
        (str) day - name of the day of the week, or 'all' if no day filter
    """
    print("\033[1mHello! To begin exploring this US bikeshare data, please enter in some values!\033[0m")
    #Get user input for city
    cityvalid = False
    while cityvalid == False:
        city = str(input("\033[1mPlease enter in Chicago, New York City or Washington: \033[0m")).lower()
        city = city.replace(" ", "_")
        if city in city_dict:
            cityvalid = True
        else:
            print("\033[1mPlease select a city from the list and check your spelling!\033[0m")
    #Get user input for month
    monthvalid = False
    while monthvalid == False:
        month = str(input("P\033[1mlease input the month you'd like to filter by, or else input 'all': \033[0m")).title()
        if month in month_list or month == 'All':
            monthvalid = True
        else:
            print("\033[1mPlease input a valid month and check your spelling!\033[0m")
    #Get user input for day of the week
    dayvalid = False
    while dayvalid == False:
        day = str(input("\033[1mPlease input the day of the week you'd like to filter by, or else input 'all': \033[0m")).title()
        if day in day_list or day == 'All':
            dayvalid = True
        else:
            print("\033[1mPlease input a valid day of the week and check your spelling!\033[0m")
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
    df = pd.read_csv(city_dict[city])
    # Start Time column is converted into datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # month, week and starting hour is extracted into new columns in the DataFrame
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if month != 'All':
    # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        
    # filter by day of week if applicable
    if day != 'All':
    # filter by day of week to create the new dataframe
        df = df[df['Day'] == day]
    return df
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel, including month, day, and starting hour"""

    print('\033[1m\nCalculating The Most Frequent Times of Travel...\n\033[0m')
    start_time = time.time()

    # display the most common month
    month_common = df['Month'].mode()[0]
    print('The most popular month of travel is {}'.format(month_common))

    # display the most common day of week
    day_common = df['Day'].mode()[0]
    print('The most popular day of travel is {}'.format(day_common))

    # display the most common start hour
    start_hour_common = df['Start Hour'].mode()[0]
    print('The most popular starting hour to travel is {}'.format(start_hour_common))

    # calculates the time taken for this to function to return the appropriate information - a note to turn this into a function that can be repeatedly called would be a good idea to prevent the code from being repetitive as this timing process is called multiple times.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\033[1m\nCalculating The Most Popular Stations and Trip...\n\033[0m')
    start_time = time.time()

    # display most commonly used start station
    start_station_common = df['Start Station'].mode()[0]
    print('The most common station to leave from is {}'.format(start_station_common))

    # display most commonly used end station
    end_station_common = df['End Station'].mode()[0]
    print('The most common station to arrive at is {}'.format(end_station_common))
    
    # display the most common combation of stations left from and arrived at
    combination_station_common = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most common combintion of travel of departing from {} and arriving at {}'.format(combination_station_common[0],combination_station_common[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\033[1m\nCalculating Trip Duration...\n\033[0m')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total time travelled for this period is {} seconds ({} minutes, {} hours, or {} days)!'.format(round(total_time), round(total_time/60), round(total_time/3600), round(total_time/86400)))
    print('-'*10)
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean time travelled during this period is {} seconds ({} minutes)'.format(round(mean_time), round(mean_time/60)))
    print('-'*10)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\033[1m\nCalculating User Stats...\n\033[0m')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    
    # Display counts of gender
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('For the users travelling within this period:')
    print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
    print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
    print('Most common year of birth: {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_data(city):
    '''Data which shows users lines of data from the database in increments of 5'''
    raw = pd.read_csv(city_dict[city])
    while True:
        see = str(input('\033[1mDo you want to see the first 5 lines of data for {}?: \033[0m'.format(city.title()))).lower()
        if see == 'yes':
            print(raw.head(5))
            line = 0
            while True:
                next = str(input('\033[1mDo you want to see the next 5 lines?: \033[0m')).lower()
                if next == 'yes':
                    line += 5
                    print(raw.iloc[line: line+5])
                elif next == 'no':
                    break
                else:
                    print('\033[1mPlease enter a valid input.\n\033[0m')
        elif see == 'no':
            break
        else:
            print("\033[1mPlease type in a valid response\n\033[0m")
        break

def bikeshare():    
    '''Main function which calls the other functions for the purpose of being able to loop the entire process if users which to restart.'''
    while True:
        city, month, day = get_values()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        #Washington does not have user statistics, so a conditional is used to prevent users selecting user stats from Washington.
        if city == 'chicago' or city == 'new_york_city':
            user_stats(df)
        see_data(city)
        
        '''Prompting whether users would like to restart or not'''
        restart_valid = False
        while restart_valid == False:
            restart = input('\033[1m\nWould you like to restart? Type in yes or no.\n\033[0m').lower()
            if restart == 'yes' or restart == 'no':
                restart_valid = True
            #Error checking in case the user's response cannot be read, so that they are re-prompted to provide another answer.
            else:
                print('\033[1m\nPlease input a valid response\n\033[0m')
        if restart == 'no':
            break
bikeshare()
print('\033[1m\nThanks for interacting!\033[0m')
