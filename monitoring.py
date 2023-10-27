from matplotlib import pyplot as mat_plot
import numpy as np
import requests
import datetime


def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"


    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)

    return res.json()



def graph_past_24_hrs(site_code, species_code):
    """
    Displays a graph of the pollution data from the past 24 hours for a given site and pollutant and returns this
    data in a dictionary.

    Parameters:
        site_code (str): string that corresponds to the site
        species_code (str): string that corresponds to the pollutant
    
    Returns:
        pollution_data (dict): dictionary of hour: data pairs
    """
    
    # Set start date to yesterday (latest data)
    start = str(datetime.datetime.today() - datetime.timedelta(days=1))[:14] + '00:00'
    end = str(datetime.datetime.today() + datetime.timedelta(days=1))[:14] + '00:00'

    # Extract dates from datetime
    start_date, end_date = [start[:10], end[:10]]

    # Extract time from datetime
    start_time = start[11:]

    url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
    res = requests.get(url)

    data = res.json()['RawAQData']['Data']
    x_values = []
    y_values = []
    started = False
 
    for row in data:
        if row['@MeasurementDateGMT'][11:] == start_time:
            started = True

        # Check row does not contain an empty value
        if started and row['@Value'] != '':

            # Add x (hour) and y (pollution data) values
            x_values.append(row['@MeasurementDateGMT'][11:13])
            y_values.append(float(row['@Value']))
    
    # Check there is available data
    if not y_values:
        return 'No available data for this site / pollutant.'
    
    # Format graph
    mat_plot.plot(x_values, y_values)
    mat_plot.title('Pollution Levels Over the Past 24 Hours')
    mat_plot.xlabel('Hour')
    mat_plot.ylabel('Value')
    mat_plot.savefig('past_24_hrs_data.png')
    mat_plot.show()

    pollution_data = {x_values[i]: y_values[i] for i in range(len(x_values))}
    return pollution_data



def yearly_data(site_code, species_code, year):
    """
    Displays a graph of the average pollution data from each month the past year on a monthly basis for a given 
    site and pollutant and returns this data in a dictionary.

    Parameters:
        site_code (str): string that corresponds to the site
        species_code (str): string that corresponds to the pollutant
        year (int): chosen year for pollution data
    Returns:
        pollution_data (dict): dictionary of month: data pairs
    """

    # Format start and end of year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year+1, 1, 2)

    url = f'https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json'
    res = requests.get(url)

    data = res.json()['RawAQData']['Data']

    x_values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    y_values = []
    month = 0
    sum = 0
    count = 0

    for i in data:

        # Check row is desired month
        if i['@MeasurementDateGMT'][5:7] == f'{month:02}':

            # Check row does not contain an empty string value
            if i['@Value'] != '':
                sum += float(i['@Value'])
                count += 1
        else:
            if count != 0:
                # Calculate mean of values for each month
                y_values.append(sum/count)
            sum = 0
            count = 0
            month += 1

    # Check there is 12 months of data
    if len(y_values) < 12:
        return 'Insufficient data for this site / pollutant.'
    
    # Format graph
    mat_plot.plot(x_values, y_values)
    mat_plot.xticks(x_values)
    mat_plot.title('Pollution Levels Over the Year')
    mat_plot.xlabel('Month')
    mat_plot.ylabel('Value')
    mat_plot.savefig('year_data.png')
    mat_plot.show()

    pollution_data = {x_values[i]: y_values[i] for i in range(len(x_values))}
    return pollution_data
    


def met_objectives(site_code, year):
    """
    Displays whether or not a given site met all of its objectives for the year. If not, the objectives it did
    not meet will be listed.

    Parameters:
        site_code (str): string that corresponds to the site
        year (int): chosen year for pollution data
    Returns:
        print objectives that have not been met
    """

    url = f'https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/SiteCode={site_code}/Year={year}/Json'
    res = requests.get(url)

    # Check there is valid data for the given site and year
    try:
        data = res.json()['SiteObjectives']['Site']
    except:
        print('No available data for this site / year.')
        return None
    
    sitename = data['@SiteName']
    objectives = []   

    for i in data['Objective']:
        if i['@Achieved'] == 'NO':
            # Add to list of failed objectives
            objectives.append([i['@SpeciesDescription'], i['@ObjectiveName'], i['@Value']])

    # Output whether or not the site met its goals
    if objectives:
        print(sitename,  'did not achieve all its goals. The following objectives were not met:\n')

        # Format the headers and results
        print(f"{'Pollutant:':<30} {'Objective:':<80} Value:")
        for i in objectives:
            print(f"{i[0]:<30} {i[1]:<80} {i[2]}")
    else:
        print(sitename, 'achieved all goals.')



def find_valid_locations(group_name):
    """
    Accepts information from user (age, health issues, preferred site type) and uses it to generate a list of
    recommended sites the user could potentially live in, given a certain group.

    Parameters:
        group_name (str): string that corresponds to the group
    Returns:
        prints list of possible sites to live in
    """

    # Use the most recently updated data
    date = datetime.date.today() - datetime.timedelta(days=2)

    url = f'https://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/GroupName={group_name}/Date={date}/Json'

    res = requests.get(url)
    data = res.json()['DailyAirQualityIndex']['LocalAuthority']

    age = input('Enter your age: ')
    if float(age) >= 65:
        health_issue = 7 

    print('\n1 - Asthma')
    print('2 - Cough')
    print('3 - Heart problem without symptoms')
    print('4 - Heart problem with symptoms')
    print('5 - Lung problem')
    print('6 - None\n')

    # More major health issues will overwrite previous one
    health_issue = int(input('Do you suffer from any of the above health issues? '))

    # Asthma, cough, heart problem no symptoms and elderly people can accept a max index of 6
    if health_issue in [1, 2, 3, 7]:
        max_index = 6

    # General population can accept a max index of 9
    elif health_issue == 6:
        max_index = 9
    
    # Heart problems with symptoms and lung problems can accept a max index of 3
    else:
        max_index = 3

    print('\n1 - Urban background')
    print('2 - Suburban')
    print('3 - Kerbside')
    print('4 - Roadside\n')
    choice = input('Pick a preferred site type: ')

    if choice == '1':
        sitetype = 'Urban Background'
    elif choice == '2':
        sitetype = 'Surburban'
    elif choice == '3':
        sitetype = 'Kerbside'
    elif choice == '4':
        sitetype = 'Roadside'

    valid_sites = []



    # I was very tired when I wrote this part
    # Sorry

    for row in data:
        if 'Site' in row:
            if type(row['Site']) == list:
                for site in row['Site']:
                    if site['@SiteType'] == sitetype:
                        valid = True
                        if type(site['Species']) == list:
                            for species in site['Species']:
                                if int(species['@AirQualityIndex']) > max_index: 
                                    valid = False
                        elif type(site['Species']) == dict:
                            if int(site['Species']['@AirQualityIndex']) > max_index: 
                                    valid = False
                        if valid:
                            valid_sites.append(f"{site['@SiteName']} ({site['@SiteCode']})")


            elif type(row['Site']) == dict:

                if row['Site']['@SiteType'] == sitetype:
                    valid = True
                    if type(row['Site']['Species']) == list:
                        for species in row['Site']['Species']:
                            if int(species['@AirQualityIndex']) > max_index: 
                                valid = False
                    elif type(row['Site']['Species']) == dict:
                        if int(row['Site']['Species']['@AirQualityIndex']) > max_index:
                                valid = False
                    if valid:
                        valid_sites.append(f"{row['Site']['@SiteName']} ({row['Site']['@SiteCode']})")

    print('\nRecommended locations for you:')

    for site in valid_sites:
        print(site)



def print_examples(example):
    '''
    Used in the main module to display options for the user such as types of group, site and pollutant to make it
    easier for them to navigate the program.

    Parameters:
        example (str): string of the type of example needed (e.g. 'group', 'site', 'species')
    Returns:
        prints the list of examples
    '''

    if example == 'group':
        print('Some examples of groups you can use include:')
        print('- All')
        print('- AroundLondon')
        print('- Essex')
        print('- Leicester')
        print('- London\n')

    elif example == 'site':
        print('Some examples of sites you can use include:')
        print('BG1: Barking and Dagenham - Rush Green')
        print('BN3: Barnet - Strawberry Vale')
        print('CT1: City of London - Senator House')
        print('MY1: Westminster - Marylebone Road\n')
    
    elif example == 'species':
        print('Some examples of pollutants you can use include:')
        print('CO: Carbon monoxide')
        print('NO2: Nitrogen Dioxide')
        print('O3: Ozone')
        print('PM10: Particulate Matter\n')
    

