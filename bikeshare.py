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
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). 
    valid_city = CITY_DATA.keys()
    city=''
    while city not in valid_city:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in valid_city:
            break
        else:
            print('Invalid input. Check spelling')

    #Get user input for time filters
    valid_filter = ['month', 'day','none']
    time_filter = ''
    while time_filter not in valid_filter:
        time_filter = input("Would you like to filter the data by month, day, or not at all? Type 'none' for no time filter ").lower()
        if time_filter in valid_filter:
            break
        else:
            print('Invalid input. Check spelling')

    # if time filter is month, get user input for month (all, january, february, ... , june)
    if time_filter=='month':
        day='all'
        valid_month = ['january', 'february', 'march', 'april', 'may', 'june']
        month = ''
        while month not in valid_month:
            month = input("Which month? January, February, March, April, May, June ").lower()
            if month in valid_month:
                break
            else:
                print('Invalid input. Check spelling')

    # if time filter is day get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter=='day':
        month='all'
        valid_day = ['1','2','3','4','5','6','7']
        day = 0
        while day not in valid_day:
            day = input("Which day? Please type your response as an integer (1=Sunday) ")
            if day in valid_day:
                break
            else:
                print('Invalid input. Make sure response is an integer value between 1 and 7')

    #If time filter is none, set month and day to 'all'
    if time_filter=='none':
        month='all'
        day='all'


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

    #Read in city's data
    orig_df = pd.read_csv(CITY_DATA[city])

    #Create time columns
    orig_df['Start Time'] = pd.to_datetime(orig_df['Start Time'])
    orig_df['hour'] = orig_df['Start Time'].dt.hour
    orig_df['day'] = orig_df['Start Time'].dt.day
    orig_df['month'] = orig_df['Start Time'].dt.month

    #Create lists to call from later
    valid_month = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_day = ['1','2','3','4','5','6','7']

    #Filter dataframe
    if month != 'all':
        df = orig_df[(orig_df['month']==valid_month.index(month)+1)]

    if day != 'all':
        df = orig_df[(orig_df['day']==valid_day.index(day)+1)]

    if day=='all' and month=='all':
        df=orig_df

    #See if user wants 5 lines of raw data
    valid_see_data = ['yes', 'no']
    see_data = 'yes'
    #Initialize variable i for indexing datafram
    i=0
    #Use this in input statement to print first for first 5 lines and next after that
    first_next = 'first'

    #Keep asking unitil the answer is no or there is no data left
    while see_data != 'no':
        see_data = input('Would you like to see the {} 5 lines of raw data? Answer "Yes" or "No" '.format(first_next)).lower()
        if see_data == 'yes':
            print(df.iloc[i:i+5])
            i=i+5
            first_next = 'next'
        elif see_data == 'no':
            print('Okay! Please see below for statistics about the data selected')
            break
        elif see_data != 'yes' and see_data != 'no':
            print('Please check spelling')
        elif i not in df.index:
            print('No more data to print')
            break


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The most popular month is {}'.format(months[popular_month-1]).title())

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    print('The most popular day is {}'.format(days[(popular_day)%7-1]))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station is {}'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most popular end station is {}'.format(popular_end))

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('The most popular route is {}'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = sum(df['Trip Duration'])
    print('The total trip duration is {}'.format(total_time))

    # display mean travel time
    mean_time = np.mean(df['Trip Duration'])
    print('The average trip duration is {}'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_count = df['User Type'].value_counts()
    print('Number of each user type:\n',type_count)

    # Display counts of gender if column exists
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Number of each gender:\n',gender_count)
    else:
        print('The city you selected does not have gender data')

    # Display earliest, most recent, and most common year of birth if birth year column exists
    if 'Birth Year' in df.columns:
        recent_birth = df['Birth Year'].max()
        print('The most recent date of birth is {}'.format(int(recent_birth)))
        oldest_birth = df['Birth Year'].min()
        print('The oldest date of birth is {}'.format(int(oldest_birth)))
        common_birth = df['Birth Year'].mode()[0]
        print('The most common date of birth is {}'.format(int(common_birth)))
    else:
        print('The city you selected does not have birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
