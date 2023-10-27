# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification



def daily_average(data, monitoring_station, pollutant):
    """
    Returns a list with the daily averages (i.e., 365 values) for a particular pollutant and 
    monitoring station.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        monitoring_station (str)
        pollutant (str)
    Returns:
        daily_averages (list): list of all 365 values of the mean for each day
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)
    
    daily_averages = []
    sum = 0
    count = 0
    for i in range(len(data[monitoring_station])):
        pollution = data[monitoring_station][i][myindex]

        # Skip any row containing 'no data'
        if pollution != 'No data':
            sum += float(pollution)
            count += 1

        # Add data to daily averages list every 24th row (each day)
        if (i+1) % 24 == 0 and count != 0:
            daily_averages.append(sum/count)
            sum = 0
            count = 0
        
    return daily_averages 

    

def daily_median(data, monitoring_station, pollutant):
    """
    Returns a list with the daily median values (i.e., 365 values) for a particular pollutant and monitoring
    station.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        monitoring_station (str)
        pollutant (str)
    Returns:
        daily_median (list): list of all 365 values of the median for each day
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)

    daily_medians = []
    hourly_data = []
    count = 0

    for i in range(len(data[monitoring_station])):
        row = data[monitoring_station][i][myindex]

        # Skip any row containing 'no data'
        if row != 'No data':
            hourly_data.append(float(row))
            count += 1

        # Add data to daily medians list every 24th row (each day)
        if (i+1) % 24 == 0 and len(hourly_data) != 0:
            hourly_data.sort()
            mid = len(hourly_data)//2

            # If even number of values, find the average of the two middle values
            if len(hourly_data) % 2 == 0:
                median = (hourly_data[mid] + hourly_data[mid-1])/2
            else:
                median = hourly_data[mid]

            daily_medians.append(median)
            hourly_data = []
            count = 0
    
    return daily_medians


    
def hourly_average(data, monitoring_station, pollutant):
    """
    Returns a list with the hourly averages (i.e., 24 values) for a particular pollutant and monitoring station.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        monitoring_station (str)
        pollutant (str)
    Returns:
        hourly_averages (list): list of all 24 values of the average for each hour
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)
    hourly_averages = []

    # Iterate through each hour of the day
    for hour in range(1, 25):
        sum = 0
        count = 0
        for row in data[monitoring_station]:

            # Check row matches given hour
            if row[1][:2] == f'{hour:02}':
                
                # Skip any row containing 'no data'
                if row[myindex] != 'No data':
                    sum += float(row[myindex])
                    count += 1

        hourly_averages.append(sum/count)

    return hourly_averages

        

def monthly_average(data, monitoring_station, pollutant):
    """
    Returns a list with the monthly averages (i.e., 12 values) for a particular pollutant and monitoring station.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        monitoring_station (str)
        pollutant (str)
    Returns:
        monthly_averages (list): list of all 12 values of the average for each month
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)
    monthly_averages = []

    # Iterate through each month of the year
    for month in range(1, 13):
        sum = 0
        count = 0
        for row in data[monitoring_station]:

            # Check row matches given month
            if row[0][5:7] == f'{month:02}':
                
                # Skip any row containing 'no data'
                if row[myindex] != 'No data':
                    sum += float(row[myindex])
                    count += 1

        # Ensure there is data to add
        if count != 0:
            monthly_averages.append(sum/count)
    
    return monthly_averages



def peak_hour_date(data, date, monitoring_station, pollutant): 
    """
    Returns the hour of the day with the highest pollution level for a given date and its corresponding value.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        date (str): date in the format YYYY-MM-DD
        monitoring_station (str)
        pollutant (str)
    Returns:
        (peak_hour, max) (tuple): tuple containing the peak hour (str) and the corresponding pollution value (float)
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)

    max = 0
    for i in range(len(data[monitoring_station])):
        if data[monitoring_station][i][0] == date:
            pollution = float(data[monitoring_station][i][myindex])
            if pollution > max:
                max = pollution
                index = i
        
        # If max has already been defined, return the result to avoid iterating through the rest of the data
        elif max > 0:   
            peak_hour = data[monitoring_station][index][1][:5]
            return (peak_hour, max)



def count_missing_data(data, monitoring_station, pollutant):
    """
    For a given monitoring station and pollutant, returns the number of 'No data' entries in the data.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        monitoring_station (str)
        pollutant (str)
    Returns:
        count (int): number of occurrences of 'No data' in the data
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)

    count = 0
    for row in data[monitoring_station]:
        if row[myindex] == 'No data':
            count += 1
    
    return count
        


def fill_missing_data(data, new_value, monitoring_station, pollutant): 
    """
    For a given monitoring station and pollutant, returns a copy of the data with the missing values
    'No data' replaced by the value in the parameter new value.

    Parameters:
        data (dict): dictionary containing the pollution data for each monitoring station
        new_value (float): the value to replace the 'No data' values
        monitoring_station (str)
        pollutant (str)
    Returns:
        data (list): copy of the original data with missing values replaced by the new value
    """

    # Extract the index of the chosen pollutant from the header of the data
    myindex = data[monitoring_station].pop(0).index(pollutant)

    for i in range(len(data[monitoring_station])):

        # Check if row has a missing value
        if data[monitoring_station][i][myindex] == 'No data':

            # Replace missing value with new value
            data[monitoring_station][i][myindex] = new_value
    
    return data


