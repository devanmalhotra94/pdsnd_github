import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November',
          'December']

WEEK_DAYS = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Enter a city ({}) :'.format(', '.join(CITY_DATA.keys()))).lower()
    while city not in CITY_DATA.keys():
        city = input('Invalid city name. {} Please enter the city : '.format(city)).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter a month ({}) :'.format(', '.join(MONTHS))).title()
    while month not in MONTHS:
        month = input('Invalid month name ({}). Please enter a month : '.format(month)).title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter a day ({}) :'.format(', '.join(WEEK_DAYS))).title()
    while day not in WEEK_DAYS:
        day = input('Invalid day ({}). Please enter a day : '.format(day)).title()

    print('-' * 40)
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

    # convert the start time to a datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # additional columns to make the filtering easier
    df['Day'] = df['Start Time'].dt.day_name()
    df['Month'] = df['Start Time'].dt.month_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'All':
        df = df[df['Month'] == month]

    if day != 'All':
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df.size > 0:
        # TO DO: display the most common month
        print('Most common month: ', df.Month.value_counts().sort_values(ascending=False).head(1).keys()[0])

        # TO DO: display the most common day of week
        print('Most common day: ', df.Day.value_counts().sort_values(ascending=False).head(1).keys()[0])

        # TO DO: display the most common start hour
        print('Most common hour', df.Hour.value_counts().sort_values(ascending=False).head(1).keys()[0])
    else:
        print('There is no data matching for the given filter. ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.size > 0:

        # TO DO: display most commonly used start station
        print('Most common Start Station: ',
              df['Start Station'].value_counts().sort_values(ascending=False).head(1).keys()[0])

        # TO DO: display most commonly used end station
        print('Most common End Station: ',
              df['End Station'].value_counts().sort_values(ascending=False).head(1).keys()[0])

        # TO DO: display most frequent combination of start station and end station trip
        start_end_combo = df.groupby(['End Station', 'Start Station']).size().reset_index(name="Time").sort_values(
            ascending=False, by="Time").head(1)
        print('Most Common Start & End Station:  ', start_end_combo.iloc[0]['Start Station'], ' - ',
              start_end_combo.iloc[0]['End Station'])
    else:
        print('There is no data matching for the given filter. ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.size > 0:
        # TO DO: display total travel time
        print('Total Travel Time', time.strftime("%Hh:%Mm:%Ss", time.gmtime(df['Trip Duration'].sum())))

        # TO DO: display mean travel time
        print('Mean Travel Time', time.strftime("%Hh:%Mm:%Ss", time.gmtime(df['Trip Duration'].mean())))
    else:
        print('There is no data matching for the given filter. ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.size > 0:

        # TO DO: Display counts of user types
        if 'User Type' in df:
            print(df['User Type'].value_counts().to_string())
        else:
            print('No User Type info available in the data set')
        # TO DO: Display counts of gender
        if 'Gender' in df:
            print(df['Gender'].value_counts().to_string())
        else:
            print('No Gender info available in the data set')

        # TO DO: Display earliest, most recent, and most common year of birth
        if 'Birth Year' in df:
            print('Youngest Birth Year: ', int(df['Birth Year'].min()))
            print('Oldest Birth Year: ', int(df['Birth Year'].max()))
            print('Most Common Birth Year: ',
                  int(df['Birth Year'].value_counts().sort_values(ascending=False).head(1).keys()[0]))
        else:
            print('No Birth Year info available in the data set')
    else:
        print('There is no data matching for the given filter. ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    """Display raw dat based on the users request"""
    choice = input("Do you like to see the raw dat? (Yes/No)? ").lower()

    # starting index of the raw data
    slicer = 0
    while choice == 'yes':

        # if we have five more raws to print
        if slicer + 5 < df.shape[0]:
            print(df.iloc[slicer:slicer + 5])
            # move the cursor
            slicer += 5
        # otherwise print the remaining row
        else:
            print(df.iloc[slicer:])
            break

        choice = input("Do you like to see the raw dat? (Yes/No)? ").lower()
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
