#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[2]:


num_months = ['{}'.format(i) for i in range(1,13) ]
lettered_months = ['january','february','march','april','may','june','july', 'august','september','october', 'november', 'december']
short_months = [i[:3]for i in lettered_months]

Datazippedmonths_ = dict(zip(short_months,num_months))
Inzippedmonths_ = dict(zip(short_months,lettered_months))
LetteredZippedmonths_ = dict(zip(num_months,lettered_months))

lettered_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
days_short = ['mon','tue','wed','thu','fri','sat','sun']
zippeddays_ = dict(zip(days_short,lettered_days))

weekdays_ ={'0':'monday','1':'tuesday','2':'wednesday','3':'thursday','4':'friday','5':'saturday','6':'sunday'} 
weekdays_reverse = dict(zip(days_short, list(weekdays_.keys())))


"""num_days = ['{}'.format(i) for i in range(1,29) ]

days_in_month = days_short*4

daysmonth_dict = dict(zip(num_days, days_in_month))


monthlydict= {'mon':[], 'tue':[] ,'wed':[],'thur':[],'fri':[],'sat':[],'sun':[]}
for key,value in daysmonth_dict.items():
    if value in monthlydict.keys():
        monthlydict[value].append(key)

"""

city_ = {'ch':'chicago','nyc':'new york city','w':'washington'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cit = input('\n which city  ch=chigago , nyc = new york city, w = washington would you like to analyze? ')
    return cit
    print('-'*40)


# In[3]:


def load_data(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame containing city data
    """
    df = pd.read_csv(CITY_DATA[city_[city]])
    
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', inplace=True, axis=1)
             
        return df
    else:
        return df


# In[4]:


def filter_df(city,df):
    """
    function responsible to taking inputs about user filtering data
    Args:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        df - Returns a filtered city DataFrame 
    """
    if city in city_.keys():
    
        filt = input('\n Would you like to filter by month, date,  both:(month & date), weekday(mon..etc), if none, type no? ')
        if filt =='month' or filt == 'date' or filt =='both' or filt =='weekday' or filt =='No' or filt =='no' or filt =='none' :
            
            if filt == 'month':
                # get user input for month (all, january, february, ... , june)
                month = input('\n which month would you like to analyze,eg:jan ?'.upper())

                if len(df.loc[df['Start Time'].str.contains('-0{}-'.format(Datazippedmonths_[month])),:]) != 0:
                    print("You'd like to analyze {} bikeshare travels in the month of {}".format(city_[city], 
                                                                         Inzippedmonths_[month]))

                    df =df.loc[df['Start Time'].str.contains('-0{}-'.format(Datazippedmonths_[month])),:]
                    return df
                else:
                    print('no bike travels were recorded in this month, restart process and Enter another month to filter!!\n'.upper())


            elif filt == 'date':
        # get user input for day of week (all, monday, tuesday, ... sunday)
                date = input('\n what date would you like to analyze,eg:1-31? '.upper())


                if len(df.loc[df['Start Time'].str.contains('-{} '.format(date)),:]) != 0:
                    print("\n You'd like to analyze {} bikeshare travels on the {}th".format(city_[city],date))

                    df = df.loc[df['Start Time'].str.contains('-{} '.format(date)),:]
                    return df
                else:
                    print('no bike travels were recorded on this date, restart process and Enter another date to filter!!\n'.upper())


            elif filt == 'both':
        # get user input for day of week (all, monday, tuesday, ... sunday)
                date = input('\n what date would you like to analyze,eg:1....etc? '.upper())
                month = input('\n which month would you like to analyze?: eg:jan...etc '.upper())

                if len(df.loc[df['Start Time'].str.contains('-0{}-{}'.format(Datazippedmonths_[month],date)),:]) != 0 :
                    print("\n You'd like to analyze {} bikeshare travels in the month of {} specifically on the {}th".format(city_[city],
                                                                                            Inzippedmonths_[month],
                                                                                            date))

                    df = df.loc[df['Start Time'].str.contains('-0{}-{}'.format(Datazippedmonths_[month],date)),:]
                    return df
                else:
                    print('no bike travels were recorded in this month and date combination, restart process and Enter another month & date to filter !!\n'.upper()) 

            elif filt == 'weekday':
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input('\n what day mon,tue,wed,thu,sat,sun would you like to analyze,eg:mon? '.upper())

                df['Start Time'] = [pd.Timestamp(i) for i in list(df['Start Time'])]
                df['Start Time'] = [i for i in list(df['Start Time'].convert_dtypes(datetime))]

                if len(df.iloc[[weekdays_reverse[day] =='{}'.format(datetime.date(i).weekday()) for i in df['Start Time']] ,:]) != 0 :

                    print("\n You'd like to analyze {} bikeshare travels on {}s".format(city_[city], zippeddays_[day]))


                    df =df.iloc[[weekdays_reverse[day] =='{}'.format(datetime.date(i).weekday()) for i in df['Start Time']] ,:]
                    return df
                else:
                    print('no bike travels were recorded on this day, restart process and Enter another weekday to filter !!\n'.upper())

            elif filt=='No' or filt=='no' or filt=='none' :
                print('filtering on all data points')
                return df
        else:
            print("enter either 'month' or 'date' or 'both' or 'weekday' or and for no filter:'No' or 'no' or 'none'  ")
    else:
        ('Enter right the abbreviation:  ch=chigago , nyc = new york city, w = washington')


# In[5]:


def time_prep(df):
    """
    Converts start time and end time into datetime object
    Args:
        df- with datetime columns
        
    Returns:
        df - Returns a city DataFrame with cdatetime columns 
    """

    df['Start Time'] = [pd.Timestamp(i) for i in list(df['Start Time'])]
    df['End Time'] = [pd.Timestamp(i) for i in list(df['End Time'])]
    print('Just a few secs more...')
    
    df['Start Time'] = [i for i in list(df['Start Time'].convert_dtypes(datetime))]
    print('Almost there..')
    df['End Time'] = [i for i in list(df['End Time'].convert_dtypes(datetime))]
    
    return


# In[6]:


def time_stats(df, ):
    """Displays statistics on the most frequent times of travel."""
    years_ = Counter(['{}'.format(datetime.date(i).year) for i in df['Start Time'][:]])
    months_ = Counter(['{}'.format(datetime.date(i).month) for i in df['Start Time'][:]])
    days_ = Counter(['{}'.format(datetime.date(i).weekday()) for i in df['Start Time'][:]])
    hours_ = Counter(['{}'.format(datetime.time(i).hour) for i in df['Start Time'][:]])
    print('Done.. Results coming right up!!!')
    
    print('\n Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print('most common month: {}'.format(LetteredZippedmonths_[months_.most_common(1)[0][0]]))

    # display the most common day of week
    print('most common day of the week: {}'.format(weekdays_[days_.most_common(1)[0][0]]))

    # display the most common start hour
    print('most common hour: {}'.format(max(hours_.most_common(1)[0][0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    startstation = [i for i in df['Start Station']]
    endstation = [i for i in df['End Station']]
    
    A = df['Start Station'].to_list()
    B = df['End Station'].to_list()
    CombAB = tuple(zip(A,B))
    
    start_time = time.time()

    # display most commonly used start station
    sc = Counter(startstation)
    print('most commonly used start station: {} , Count:{}'.format(sc.most_common(1)[0][0],
                                                                   sc.most_common(1)[0][1])) #1st change

    # display most commonly used end station
    ec = Counter(endstation)
    print('most commonly used end station: {} , Count:{}'.format(ec.most_common(1)[0][0],
                                                                 ec.most_common(1)[0][1]))

    # display most frequent combination of start station and end station trip
    Cc = Counter(CombAB)
    print('most liked combination of start station and end station: {}, Count:{}'.format(Cc.most_common(1)[0][0], 
                                                                                                 Cc.most_common(1)[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def raw_data(df,length = 4):
    que = input("Would you like to see 5 raw inputs, Y/N? or yes/ no ")
    if que.lower() == 'y' or  que.lower() =='yes':
        return ['{} '.format(value) for key,value in {i:df.iloc[i,:].to_dict() for i in range(length)}.items()]
        pass
#{ i:{key:value[i] for key ,value in data.loc[0:4,:].to_dict().items() for key2,value2 in value.items() if key2 in value.keys() } for i in range(1)}
    else:
        return df


# In[9]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    df['total'] = df['End Time'] - df['Start Time']

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #print('total travel time: {}'.format(df['Trip Duration'].sum()))
    print('total travel time: {} \t total travel time in secs {} '.format(df['total'].sum(), df['Trip Duration'].sum()))

    # display mean travel time
    #print('mean travel time: {}'.format(df['Trip Duration'].mean()))
    print('mean travel time: {} \t mean travel time in secs {} '.format(df['total'].mean(), df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[10]:


def NanReplacer(df):
    null_cols = [df.isnull().sum().index[[i 
                                          for i in df.isnull().sum()].index(v)] 
                 for v in [i for i in df.isnull().sum()]
                 if v != 0]
    for i in null_cols:
        df[i] = df[i].fillna('{}'.format(df[i].mode()[0]))
    return df


# In[11]:


#Counter(data['User Type']).most_common(3)[0][1]


# In[12]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for i,v in dict(Counter(df['User Type']).most_common(3)).items():
        print('{}:{}'.format(i,v))
        
    #Display counts of gender    
    while 'Gender' in df.columns:
        print('\n counts of gender'.upper())
        for i,v in dict(Counter(df['Gender']).most_common(3)).items():
            print('{}:{}'.format(i,v))
        break
        

    while 'Birth Year' in df.columns:
        BY_ = Counter(df['Birth Year'])
        # Display earliest, most recent, and most common year of birth
        print('\n Earliest years of births'.upper())
        for i,v in BY_.items():
            if float(i) < 1905:
                print(i)
                

        print('\n Most Recent Births'.upper())
        for i,v in BY_.items():
            if float(i) > 2000:
                print(i)


#         print('\n most common year of birth'.upper())
        Myc = [i for i in df['Birth Year']]
        McyB = Counter(Myc)
        print('\n MOST COMMON YEAR OF BIRTH: {} count:{}'.format(McyB.most_common(1)[0][0], McyB.most_common(1)[0][1]))
        break
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[13]:


#user_stats(data)


# In[14]:


def main():
    while True:
        try:
            city= get_filters()
            df = load_data(city)
            print('Setting things up.....')
            
            df = filter_df(city,df)
            time_prep(df)
            NanReplacer(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            df = raw_data(df, 4)
            for i in df:
                print('\n {}'.format(i))
        except TypeError:
            print("Oops...wrong filter entered.Restart process!Remember to type either month, day, both or none")
        except KeyError:
            print("Oops..Wrong month or day value.Restart process!Remember to enter first 3 letters and also they're not case senitive!")  

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a nice day!..GoodBye')
            break


if __name__ == "__main__":
	main()

