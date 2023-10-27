from reporting import *  
from intelligence import * 
from monitoring import *


def main_menu():
    """
    Executed upon the initialisation of the program, showing the main menu of the program allowing the user 
    to navigate through the different options.
    """
    
    print('\nR - Pollution Reporting')
    print('I - Mobility Intelligence')
    print('M - Real-time Monitoring')
    print('A - About')
    print('Q - Quit\n')

    choice = input('Choose an option: ').lower()
    print()

    if choice == 'r':
        reporting_menu()
    elif choice == 'i':
        intelligence_menu()
    elif choice == 'm':
        monitoring_menu()
    elif choice == 'a':
        about()
    elif choice == 'q':
        quit()
    else:
        print('Invalid choice, try again.\n')
        main_menu()


    
def reporting_menu():
    """
    Executed when the user chooses the 'R' option in the main menu, allows the user to perform the reporting
    functions and return to the main menu.
    """
   
   # Extract data from each data file and place in a dictionary
    data = {}
    for filename in ['Pollution-London Harlington', 'Pollution-London Marylebone Road', 'Pollution-London N Kensington']:
        f = open(f'data/{filename}.csv')
        data[filename] = [line.strip().split(',') for line in f]   
        f.close()
    
    print('Monitoring stations:')
    print('H - Harlington')
    print('M - Marylebone Road')
    print('N - N. Kensington\n')

    choice = input('Choose a monitoring station: ').lower()
    print()

    if choice == 'h':
        station = 'Pollution-London Harlington'
    elif choice == 'm':
        station = 'Pollution-London Marylebone Road'
    elif choice == 'n':
        station = 'Pollution-London N Kensington'
    else:
        print('Invalid choice, try again.\n')
        reporting_menu()

    print('Pollutants:')
    print('1 - Nitric Oxide')
    print('2 - PM10')
    print('3 - PM2.5\n')

    choice = input('Choose a pollutant: ')
    print()

    if choice == '1':
        pollutant = 'no'
    elif choice == '2':
        pollutant = 'pm10'
    elif choice == '3':
        pollutant = 'pm25'
    else:
        print('Invalid choice, try again.\n')
        reporting_menu()

    print('Functions:')
    print('1 - Daily average')
    print('2 - Daily median')
    print('3 - Hourly average')
    print('4 - Monthly average')
    print('5 - Peak hour date')
    print('6 - Count missing data')
    print('7 - Fill missing data\n')

    choice = input('Choose a function: ')
    print()

    if choice == '1':
        print('Daily averages are:\n', daily_average(data, station, pollutant))
    elif choice == '2':
        print('Daily medians are:\n', daily_median(data, station, pollutant))
    elif choice == '3':
        print('Hourly averages are:\n', hourly_average(data, station, pollutant))
    elif choice == '4':
        print('Monthly averages are:\n', monthly_average(data, station, pollutant))
    elif choice == '5':
        date = input('Enter a date in the format YYYY-MM-DD: ')
        print('Peak hour data is:', peak_hour_date(data, date, station, pollutant))
    elif choice == '6':
        print('Missing data:', count_missing_data(data, station, pollutant))
    elif choice == '7':
        new_value = float(input('Enter a new value to fill the missing data: '))
        print('Copy of the new data:', fill_missing_data(data, new_value, station, pollutant))
    else:
        print('Invalid choice, try again.\n')
        reporting_menu()
    
    main_menu()
    
    

def intelligence_menu():
    """
    Executed when the user chooses the 'I' option in the main menu, allows the user to perform the intelligence
    functions and return to the main menu.
    """

    print('1 - Find red pixels')
    print('2 - Find cyan pixels\n')

    choice = input('Find red or cyan pixels? ')
    map_filename = input('\nEnter the file name: ')
    upper_threshold = int(input('Enter an upper threshold (recommended 100): '))
    lower_threshold = int(input('Enter a lower threshold (recommended 50): '))

    if choice == '1':
        IMG = find_red_pixels(map_filename, upper_threshold, lower_threshold)
    elif choice == '2':
        IMG = find_cyan_pixels(map_filename, upper_threshold, lower_threshold)
    
    choice = input('\nDetect connected components? Y/N: ')

    if choice.lower() == 'y':
        MARK = detect_connected_components(IMG)
    else:
        main_menu()
    
    choice = input('\nSort detected components and display top two components? Y/N: ')

    if choice.lower() == 'y':
        detect_connected_components_sorted(MARK)
    else:
        main_menu()



def monitoring_menu():
    """
    Executed when the user chooses the 'M' option in the main menu, allows the user to perform the monitoring
    functions and return to the main menu.
    """
    
    print('Functions:')
    print('1 - Data for the past 24 hours')
    print('2 - Data for the past year')
    print('3 - Check site has met objectives')
    print('4 - Recommend locations to live\n')

    choice = input('Choose a function: ')
    print()

    if choice == '1':
        print_examples('site')
        site_code = input('Enter a site code: ')
        print_examples('species')
        species_code = input('Enter a species code: ')
        print(graph_past_24_hrs(site_code, species_code))
    elif choice == '2':
        print_examples('site')
        site_code = input('Enter a site code: ')
        print_examples('species')
        species_code = input('Enter a species code: ')
        year = int(input('Choose a year: '))
        print(yearly_data(site_code, species_code, year))
    elif choice == '3':
        print_examples('site')
        site_code = input('Enter a site code: ')
        year = int(input('Choose a year: '))
        met_objectives(site_code, year)
    elif choice == '4':
        print_examples('group')
        group_name = input('Enter a group name: ')
        find_valid_locations(group_name)

    main_menu()



def about():
    """
    Executed when the user chooses the 'A' option in the main menu, prints a string containing the module code
    and my candidate number, returning to the main menu afterwards
    """
    
    print('ECM1400')
    print('245496')

    main_menu()



def quit():
    """
    Executed when the user chooses the 'Q' option in the main menu, terminates the program.
    """
    exit()



if __name__ == '__main__':
    main_menu()
