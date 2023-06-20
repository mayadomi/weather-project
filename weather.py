import csv
from datetime import datetime
import statistics

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"


def convert_date(iso_string: str) -> str:
    """Converts and ISO formatted date into a human readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """

    # Assumptions:
    # Argument string is always a correctly formatted iso string
    # Python v3 onwards being used (datetime.fromisoformat is from v3 onwards)

    # Create datetime object type
    iso_date = datetime.fromisoformat(iso_string)

    # Format it using the string format time function with desired format
    formatted_date = iso_date.strftime("%A %d %B %Y")

    return formatted_date


def convert_f_to_c(temp_in_fahrenheit: float) -> float:
    """Converts a temperature from fahrenheit to celsius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees celsius, rounded to 1dp.
    """

    temp_in_celsius = round(((float(temp_in_fahrenheit) - 32) * 5/9), 1)

    return temp_in_celsius


def calculate_mean(weather_data: list) -> float:
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """

    # Cast all elements to type float
    weather_data_float = [float(data_point) for data_point in weather_data]

    # Use python's statistics library to get the mean
    weather_mean = statistics.mean(weather_data_float)

    # Alternative would be to add up the values of the list using a loop
    # and then divide by len(list) to get the mean.

    # weather_mean = sum(weather_data_float)/len(weather_data_float)

    return weather_mean


def load_data_from_csv(csv_file: str) -> list:
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    csv_file_data = []

    with open(csv_file, mode="r") as weather_csv_file:
        csv_reader = csv.DictReader(weather_csv_file)
        for data_row in csv_reader:
            csv_file_data.append([data_row['date'], int(data_row['min']), int(data_row['max'])])

    return csv_file_data


# The find_min and find_max functions could maybe be combined to single function? With a flag
# to use 'min' or 'max' function, eg

# def find_temp_limits(weather_data: list, limit_type: str) -> tuple:
#     weather_data_float = [float(data_point) for data_point in weather_data]
#     if len(weather_data_float) == 0:  # check for empty weather data
#         return ()
#     else:
#         if limit_type == 'max':
#             limit_value = max(weather_data_float)
#
#         elif limit_type == 'min':
#             limit_value = min(weather_data_float)
#
#         # find the highest index for multiple occurrences of limit_value
#         limit_value_index = max(index for index, item in enumerate(weather_data_float) if item == limit_value)
#
#         return limit_value, limit_value_index


def find_min(weather_data: list) -> tuple:
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list.
    """
    # Cast to float to use python's min/max functions
    weather_data_float = [float(data_point) for data_point in weather_data]

    if len(weather_data_float) == 0:  # check for empty weather data
        return ()
    else:
        min_value = min(weather_data_float)
        # find the highest index for multiple occurrences of min_value
        min_value_index = max(index for index, item in enumerate(weather_data_float) if item == min_value)

        return min_value, min_value_index


def find_max(weather_data: list) -> tuple:
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list.
    """
    # Cast to float to use python's min/max functions
    weather_data_float = [float(data_point) for data_point in weather_data]

    if len(weather_data_float) == 0: # check for empty weather data
        return ()
    else:
        max_value = max(weather_data_float)
        max_value_index = max(index for index, item in enumerate(weather_data_float) if item == max_value)
        return max_value, max_value_index


def generate_summary(weather_data: list) -> str:
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.

    Returns:
        A string containing the summary information.

    """
    min_temps = []
    max_temps = []

    for day in weather_data:
        min_temps.append(day[1])
        max_temps.append(day[2])

    # Assumes no duplicate min or max days - otherwise probs 
    # need some logic to either choose one instance (eg the 'earliest' day)
    # or collect => concatenate dates with same min/max eg
    # 'The lowest temperature will be 10.0C, and will occur on 
    # Tuesday 10 July 2023 and Wednesday 11 July 2023' etc

    # Get the max temperature information
    max_temp_value, max_value_index = find_max(max_temps)
    max_temp_formatted_date = convert_date(weather_data[max_value_index][0])
    mean_max_temp = calculate_mean(max_temps)

    # Get the min temperature information
    min_temp_value, min_value_index = find_min(min_temps)
    min_temp_formatted_date = convert_date(weather_data[min_value_index][0])
    mean_min_temp = calculate_mean(min_temps)

    # Compile a single string for the temperature information whilst converting temp units/getting celsius symbol
    summary_string = f"{str(len(weather_data))} Day Overview\n" \
                    f"  The lowest temperature will be {format_temperature(convert_f_to_c(min_temp_value))}, and will occur on {min_temp_formatted_date}.\n" \
                    f"  The highest temperature will be {format_temperature(convert_f_to_c(max_temp_value))}, and will occur on {max_temp_formatted_date}.\n" \
                    f"  The average low this week is {format_temperature(convert_f_to_c(mean_min_temp))}.\n" \
                    f"  The average high this week is {format_temperature(convert_f_to_c(mean_max_temp))}.\n"

    return summary_string


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """

    daily_summary = []

    # Loop through the weather data and compile list of summary strings with formatted date and temperature units
    for day in weather_data:
        daily_summary.append(
                f"---- {convert_date(day[0])} ----\n"
                f"  Minimum Temperature: {format_temperature(convert_f_to_c(day[1]))}\n"
                f"  Maximum Temperature: {format_temperature(convert_f_to_c(day[2]))}\n")

    # Compile summary strings list to a single string
    summary_string = "\n".join(daily_summary) + "\n"  # seems to be extra newlines at end of the text files :)

    return summary_string
