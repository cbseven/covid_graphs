import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates

plt.style.use('seaborn-poster')

COUNTRY_DATA = {'url': 'https://raw.githubusercontent.com/owid/covid-19-data/'
                       'master/public/data/owid-covid-data.csv',
                'source': 'Data on COVID-19 (coronavirus) by Our World in Data'
                }

# Documentation for OWID data source:
# https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data-codebook.md


def main():
    # user chooses one or more countries specified by their ISO codes
    country_codes = choose_countries()
    # user chooses graph to plot
    graph = choose_graph()
    # if graph type is an Over Time (OT) series, plot it
    if graph['type'] == 'TS':
        graph_ts(country_codes, graph)


def choose_countries():
    """
    asks the user for input and accepts one or more country codes (iso_code) separated by commas
    https://www.iban.com/country-codes
    returns a list of codes, default to ['USA', 'ITA', 'FRA', 'GBR']
    :return country_code_list:
    """
    print()
    user_input = input(
        'Enter the country (three letter iso code, '
        'separate multiples with commas): ')\
        or 'USA,ITA,FRA,GBR'
    country_code_list = user_input.split(',')
    return country_code_list


def retrieve_data(url):
    """
    :param url:
    :return data:
    """
    data = pd.read_csv(url)
    # format the date column as date
    data['date'] = pd.to_datetime(data['date'])
    # ensure that the data is sorted by date
    data.sort_values('date', inplace=True)
    return data


def graph_ts(country_codes, graph):
    """
    loops over a list of country codes and generates a plot according to
    the column supplied in graph dictionary (includes column, ylabel, title)
    :param country_codes:
    :param graph:
    :return:
    """

    df = retrieve_data(COUNTRY_DATA['url'])

    # plot a line for each country on the same axes
    for country_code in country_codes:
        df_country = df[df['iso_code'] == country_code]
        country = df_country.at[df_country.index[0], 'location']
        column = graph['column']
        df_country = remove_leading_zeros(df_country, column)
        plt.plot_date('date', column, marker='', linestyle='-', label=country, data=df_country)

    plt.ylabel(graph['ylabel'])
    plt.title(graph['title'])
    plt.legend()  # legend labels defined by label attribute in plot_date() above
    plt.gcf().autofmt_xdate()  # cleans up the x-axis, gcf = 'get current figure'
    date_format = mpl_dates.DateFormatter('%b - %d')  # %b = month abbrev, %d = day number
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=90, ha='center')
    plt.show()


def remove_leading_zeros(df, column):
    """
    remove leading rows from sorted data frame where column values = zero
    :param df:
    :param column:
    :return df:
    """

    # TO DO: Make this function work!!
    # the following does *not* work.
    # length = len(df)
    # for i in range(length):
    #     if df[i][column] > 0:
    #         return df.slice(i, length)
    return df


def choose_graph():
    menu = {1: {'name': ' Total Cases by Date',
                'graph': {'type': 'TS',
                          'column': 'total_cases',
                          'title': 'Total Cases by Date',
                          'ylabel': 'Cases'}},
            2: {'name': ' New Cases by Date',
                'graph': {'type': 'TS',
                          'column': 'new_cases',
                          'title': "New Cases by Date",
                          'ylabel': 'Cases'}},
            3: {'name': ' Total Deaths by Date',
                'graph': {'type': 'TS',
                          'column': 'total_deaths',
                          'title': "Total Deaths by Date",
                          'ylabel': 'Deaths'}},
            4: {'name': ' New Deaths by Date',
                'graph': {'type': 'TS',
                          'column': 'new_deaths',
                          'title': "New Deaths by Date",
                          'ylabel': 'Deaths'}},
            5: {'name': ' Total Tests by Date',
                'graph': {'type': 'TS',
                          'column': 'total_tests',
                          'title': "Total Tests by Date",
                          'ylabel': 'Tests'}},
            6: {'name': ' New Tests by Date',
                'graph': {'type': 'TS',
                          'column': 'new_tests_smoothed',
                          'title': "New Tests by Date",
                          'ylabel': 'Tests'}},
            7: {'name': ' Total Tests per Thousand by Date',
                'graph': {'type': 'TS',
                          'column': 'total_tests_per_thousand',
                          'title': "Total Tests per Thousand by Date",
                          'ylabel': 'Tests/T'}},
            8: {'name': ' New Tests per Thousand by Date',
                'graph': {'type': 'TS',
                          'column': 'new_tests_smoothed_per_thousand',
                          'title': "New Tests per Thousand by Date",
                          'ylabel': 'Tests/T'}},
            9: {'name': ' Total Deaths per Million by Date',
                'graph': {'type': 'TS',
                          'column': 'total_deaths_per_million',
                          'title': "Total Deaths per Million by Date",
                          'ylabel': 'Deaths/M'}},
            10: {'name': 'New Deaths per Million by Date',
                 'graph': {'type': 'TS',
                           'column': 'new_deaths_per_million',
                           'title': "New Deaths per Million by Date",
                           'ylabel': 'Deaths/M'}},
            11: {'name': 'Total Cases per Million by Date',
                 'graph': {'type': 'TS',
                           'column': 'total_cases_per_million',
                           'title': "Total Cases per Million by Date",
                           'ylabel': 'Cases/M'}},
            12: {'name': 'New Cases per Million by Date',
                 'graph': {'type': 'TS',
                           'column': 'new_cases_per_million',
                           'title': "New Cases per Million by Date",
                           'ylabel': 'Cases/M'}}
            }
    print()
    print('    AVAILABLE GRAPHS')
    for item in menu:
        print('(' + str(item) + ')', menu[item]['name'])
    print()
    choice = int(input('    Choose a graph by entering its number from the list above: ') or 1)
    print()
    return menu[choice]['graph']


if __name__ == '__main__':
    main()
