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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'new york city', 'washington']
    city = ''

    while city not in valid_cities:
        city = input("Would you like to see data for Chicago, New York City or Washington? ").lower()
        
    # get user input for month and weekday
    valid_date_level = ['month', 'day', 'both', 'none']
    date_level = ''

    while date_level not in valid_date_level:
        date_level= input("Would you like to filter the data by month, day, both, or not at all? Type none for no time filter. ")
        if date_level == "both":
            month = input("Which month? ").lower()
            day = input("Which day of week? ").lower()
        if date_level == "month":
            month = input("Which month? ").lower()
            day = "all"
        if date_level == "day":
            day = input("Which day of week? ").lower()
            month = "all"
        if date_level == "none":
            day = "all"
            month = "all"

    print(city, month, day)

   
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
    file_path = CITY_DATA[city]
    df = pd.read_csv(file_path)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['day'] = df['Start Time'].dt.strftime('%A').str.lower()
    
    if month != "all":
        df = df[df['month'] == month]
    if day != "all":
        df = df[df['day'] == day]

    print (df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].value_counts().idxmax()
    print("The most common month is:", most_common_month)

    # display the most common day of week
    most_common_weekday = df["day"].value_counts().idxmax()
    print("The most common weekday is:", most_common_weekday)

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df["start_hour"].value_counts().idxmax()
    print("The most common start hour is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df["Start Station"].value_counts().idxmax()
    print("The most popular start station is:", most_popular_start_station)

    # display most commonly used end station
    most_popular_end_station = df["End Station"].value_counts().idxmax()
    print("The most popular end station is:", most_popular_end_station)

    # display most frequent combination of start station and end station trip
    combination_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    most_frequent_combination = combination_counts.sort_values('Count', ascending=False).head(1)
    print("The most frequent station combination is:", most_frequent_combination["Start Station"].to_string(index=False), "and", most_frequent_combination["End Station"].to_string(index=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("The total travel time in", city, "for the selected time is:", total_travel_time)

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("The average travel time in", city, "for the selected time is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_type=df['User Type'].value_counts().to_string(header=False)
    print("The user types are distributed in the following way:\n", counts_user_type,"\n")

    # Display counts of gender
    if city == "washington":
        print("No gender information available for this city.\n")
    else: 
        counts_gender =df['Gender'].value_counts().to_string(header=False)
        print("Gender is distributed in the following way:\n", counts_gender,"\n")

    # Display earliest, most recent, and most common year of birth
    if city == "washington":
        print("No birth year information available for this city.\n")
    else: 
        earliest_birth_year= df['Birth Year'].min().astype(int)
        print("The earliest birth year is:", earliest_birth_year)
    
        df_sorted=df.sort_values('Start Time', ascending=False)
        most_recent_birth_year = df_sorted['Birth Year'].iloc[0].astype(int)
        print("The most recent birth year is:", most_recent_birth_year)
        
        most_common_birthyear = df["Birth Year"].value_counts().idxmax().astype(int)
        print("The most common birth year is:", most_common_birthyear)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
def display_trip_data(df):
    pd.set_option("display.max_columns", None)
    view_data = input("Would you like to view individual trip data? Enter yes or no?")
    start_loc = 0
    while view_data.lower() == "yes":
        print(df[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?").lower()
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df,city)
        user_stats(df, city)
        display_trip_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
