import time
import pandas as pd

CITY_DATA = { 'C': 'chicago.csv',
              'N': 'new_york_city.csv',
              'W': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    city = input("\nplease type one of the following 3 symbols n,c,w \njust type the first letter of the city it doesn't matter capital or small letter we will deal with it \n n for  New York City \n c for Chicago\n w for Washington?\n").title()
    city = city[0]
    while city not in ('N', 'C', 'W'):
        print("Sorry, your input has no match. Try again.")
        city = input("\nplease retype the city symbool \njust type the first letter of the city it doesn't matter capital or small letter we will deal with it \n n for  New York City \n c for Chicago\n w for Washington?\n").title()
        city = city[0]
    
    month = input("\nplease type the month you want to see from these months [january, february, march, april, may, june or 'all'] for all months\nyou can typy the first letter only \n").lower()
    
    while month not in ['january', 'february', 'march', 'april', 'may', 'june','all','a']:
        print("Sorry, your input has no match. Try again.")
        month = input("\nplease retype the month you want to see from these months [january, february, march, april, may, june or 'all'] for all months\nyou can typy the first letter only \n").lower()
        
    
    day = input("\nplease enter the day that you want to analyse of the following: sunday, monday, tuesday, wednesday, thursday, friday, allfor all days or usr symbol a for all \n").lower()
    while day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all','a'):
        print("Sorry, your input has no match. Try again.")
        day = input("\nplease retype the day that you want to analyse of the following: sunday, monday, tuesday, wednesday, thursday, friday, allfor all days or usr symbol a for all \n").lower()
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
    # load data file into a dataframe
   
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all' and month != 'a':
   	 	# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if selected
    if day != 'all' and day != "a":
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].value_counts().idxmax()
    print('The most Commonly used start station:', start_station)

    end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most Commonly used end station:', end_station)

    print('\nthe most frequent combination of start station and end station trip:', start_station, " & ", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = sum(df['Trip Duration'])
    print('The total travel time in days:', total_travel_time/24/60/60, " Days")

    mean_travel_time = df['Trip Duration'].mean()
    #convert to days
    print('The mean travel time:', mean_travel_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    
    print('User Types:\n', user_types)
    
    if  "Gender" in df.columns:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
        
        earliest_year = df['Birth Year'].min()
        print('\nEarliest Year:',int( earliest_year))
        
        most_recent_year = df['Birth Year'].max()
        print('\nThe most Recent Year:', int(most_recent_year))
        
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nThe most common year: ' ,int( most_common_year))
        
    else:
        print("\nno avilable gender or birth year data for this city")

        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def raw_data(df):
    ask_user = input('Would you like to view more raw data for the city selected? \nPrint y for yes or no: ').lower()
    if ask_user[0] == 'y':
        print( df.iloc[:5])
        
    else:
        pass

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter y for yes or any key for no.\n')
        if restart[0].lower() != 'y':
            break


if __name__ == "__main__":
	main()