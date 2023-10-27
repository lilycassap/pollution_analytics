def sumvalues(values):
    '''
    Returns the sum of the values in a sequence, raises an exception if non-numerical values are present.
    
    Parameters:
        values (list): list of values
    Returns:
        sum (float): sum of all values in list
    '''
    sum = 0
    for value in values:

        # Exception if value is not a number
        try:
            sum += float(value)
        except:
            raise TypeError("Numerical values only.")
    return sum


def maxvalue(values):
    """
    Returns the index of the maximum value in a sequence, raises an exception if non-numerical values are present.

    Parameters:
        values (list): list of values
    Returns:
        max_index (int): index of maximum value in list
    """    

    max = values[0]
    max_index = 0
    for i in range(1, len(values)):
        # Exception if list is not 1D, or not a list of numbers
        try:
            if values[i] > max:
                max = values[i]
                max_index = i
        except:
            raise TypeError("Numerical values only.")

    return max_index


def minvalue(values):
    """
    Returns the index of the minimum value in a sequence, raises an exception if non-numerical values are present.

    Parameters:
        values (list): list of values
    Returns:
        min_index (int): index of minimum value in list
    """    
    min = values[0]
    min_index = 0
    for i in range(1, len(values)):
        # Exception if list is not 1D, or not a list of numbers
        try:
            if values[i] < min:
                min = values[i]
                min_index = i
        except:
            raise TypeError("Numerical values only.")

    return min_index


def meannvalue(values):
    """
    Returns the arithmetic mean value in a list/array, raises an exception if non-numerical values are present.

    Parameters:
        values (list): list of values
    Returns:
        sumvalues(values) / len(values): mean value of list
    """    
    # Exception if list is empty or values are not numerical
    try:
        return sumvalues(values) / len(values)
    except:
        raise TypeError("Numerical values only.")


def countvalue(values, x):
    """
    Returns the number of occurrences of the value x in the list/array values, returns 0 if the value is 
    not present in the list/array.

    Parameters:
        values (list): list of values
        x: value to be found
    Returns:
        sumvalues(values) / len(values): mean value of list
    """    
    count = 0
    for value in values:
        if value == x:
            count += 1
    return count
