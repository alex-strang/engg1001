
"""
Assignment 2
Semester 1, 2022
ENGG1001
"""

# NOTE: Do not import any other libraries!

import csv

import numpy as np
import matplotlib.pyplot as plt

from numpy import ndarray

HELP = """
    'h' - Help message
    'l' - Load a given event file for analysis
    's' - Smooth the raw data
    'p <gauges>' - Plot the data for strain gauges (separated by spaces)
    'a' - Analyse all event files
    'q' - Quit the program
"""

__author__ = "Alexander Strang,47423510"
__email__ = "<a.strang@uqconnect.edu.au>"


def file_import(file_name: str):
    '''
    file_import is a function to import, read and reformate the .dat file
    as a csv file. file_import then does basic data processing to extract the 
    raw data of the original file.

    Parameters
    ----------
    file_name : str


    Returns
    -------
    linecount : int
    headers : ndarray
    timestamps : ndarray
    data : ndarray

    '''

    # Use the CSV module to read the file provided as input
    with open(file_name) as csv_file:
        data_list = list(csv.reader(csv_file, delimiter=','))

        # Create empty lists to store timestamp and data_points in raw form
        timestamp = []
        data_points = []

        # As headers appear in the same location each time, extract headers
        # from the data and store them for later use as a list
        headers = data_list[1][2:]

        # The linecount is defined in all data sets at the last index of
        # the second column
        linecount = int(data_list[-1][1])

        # Define where the data starts, constant across all data sets
        data_initial = 4

        # Loop through the lines of the file to extract timestamps and data
        for index, row in enumerate(data_list):
            if index >= data_initial:
                # Extract the raw timestamp data of each column
                timestamp_raw = row[0]
                # Convert the raw timestamp data to datetime64 format
                timestamp_data = np.datetime64(timestamp_raw)
                # append the timestamps and data rows to thier respective lists
                timestamp.append(timestamp_data)
                data_points.append(row[2:])
            else:
                continue
        # Add the individual timestamp lists to the timestamps array
        timestamps = np.array(timestamp)
        # Add the data points as float data point to the data array
        data = np.array(data_points, dtype=float)
    return linecount, headers, timestamps, data


def plot_data(times, headers, data, gauges):
    '''
    plot_data is a function to plot the data outputted by file_import. It
    takes the data from file_import and plots it against the difference in time
    for a given set of gauges.

    Parameters
    ----------
    times : ndarray
    headers : ndarray
    data : ndarray
    gauges : list[str]

    Returns
    -------
    None.

    '''
    # Assign the objects figure (fig) and axis (ax)
    fig, ax = plt.subplots()
    # Develop a new array that consists of the timedelta64 of each value
    time_diff_raw = times - times[0]
    time_diff = (time_diff_raw.astype(float))/1000000
    # Loop over the data to cycle through what needs to be plotted
    for index, header in enumerate(headers):
        # Check to see if the string in gauges appears in headers
        if header in gauges:
            # Gather and plot the relevant data from the datalist
            # NOTE that the time_diff array will share the data array's index
            plt.plot(time_diff, data[:, index], label=header)
    # Plot the titles, legend, the data grid and then show line plot
    fig.suptitle('Event Start: '+str(times[0]))
    plt.xlabel('Time From Event Start (s)')
    plt.ylabel('Strain(\u03BC\u03B5)')
    plt.legend()
    plt.grid()
    plt.show()


def centre_average(data, window):
    '''
    centre_average is a function to smooth the dataset, taking the existing
    data outputted by file_import and a window inputted by the user and using
    them to apply a moving average, smoothing and then returning the dataset.
    Anywhere where smoothing cannot be applied is left as a 0 value.

    Parameters
    ----------
    data : ndarray
    window : int

    Returns
    -------
    avg_data : ndarray

    '''

    # Find the first and last indexes that are not 0 values
    lim = window//2
    first_index = lim
    last_index = data.shape[0] - lim - 1
    # Generate an array that shares the dimensions of data
    avg_data = np.zeros_like(data)
    # loop through the values in data
    for row, row_value in enumerate(data):
        for col, value in enumerate(row_value):
            # Check to see if the row is within the first and last index
            # Anywhere that is not within the index limits will remain a 0
            if last_index >= row >= first_index:
                # Amend the averaged data array with the moving average value
                avg_data[row, col] = np.average(data[row-lim: row+lim+1, col])
    return avg_data


def plot_avg_data(times, header, data, avg_data, gauges):
    '''
    plot_avg_data is does the excact same as the plot_data function, however it
    also takes for input the smoothed dataset from centre_average and plots it 
    on the same plot as the previous dataset, however it is done as a dotted 
    black line instead of a solid colour.

    Parameters
    ----------
    times : ndarray
    header : ndarray
    data : ndarray
    avg_data : ndarray
    gauges : list[str]

    Returns
    -------
    None.

    '''

    # Define the fig and ax variables
    fig, ax = plt.subplots()
    # Develop a new array that consists of the timedelta64 of each value
    time_diff_raw = times - times[0]
    time_diff = (time_diff_raw.astype(float))/1000000
    # Produce the data required for the plot
    for index, gauge in enumerate(header):
        # Check to find the index of the inputted gauges
        if gauge in gauges:
            # plot the relevant data on the
            plt.plot(time_diff, data[:, index], label=gauge)
            plt.plot(time_diff, avg_data[:, index], 'k--', label=gauge+'avg')
    # Plot the titles, legend, the data grid and then show line plot
    fig.suptitle('Event Start: '+str(times[0]))
    plt.xlabel('Time From Event Start (s)')
    plt.ylabel('Strain(\u03BC\u03B5)')
    plt.legend()
    plt.grid()
    plt.show()


def analyse_event(times, header, data):
    '''
    analyse_event is further computation of the recorded dataset of a given 
    file, taking for input the times, headers and a dataset, processing them 
    to extract critical information related to the strain gauges.

    Parameters
    ----------
    times : ndaray
    header : ndarray
    data : ndarray

    Returns
    -------
    stats : ndarray
    max_rev_gauge : str
    transit_time : ndarray
    speed : ndarray
    direction : ndarray

    '''

    # Fine the maximum, minimum and measured range of each gauge
    maxi = np.amax(data, axis=0)
    mini = np.amin(data, axis=0)
    meas_range = maxi - mini
    # Combine all 3 arrays from above into a 2d array
    stats = np.stack((maxi, mini, meas_range))
    # Identify the index of the gauge that underwent the most stress
    strain_reversal = np.max(meas_range)
    # Search through the header array for the gauge that matches the index
    max_rev_gauge = header[int(np.where(meas_range == strain_reversal)[0])]

    # Search through the header array for the index of each gauge
    VW_8_index = header.index("VW_8")
    VW_28_index = header.index("VW_28")

    # identify the times where each peak occurs
    maxi_times = times[np.argmax(data, axis=0)]
    # Identify the time of peak associated with both gauges
    VW_8_peaktime = maxi_times[VW_8_index]
    VW_28_peaktime = maxi_times[VW_28_index]
    # Find the difference in time between both peaks and convert to [s]
    transit_time = ((VW_28_peaktime - VW_8_peaktime).astype(float))/1000000
    # calculate averaged speed
    speed = (78.52/abs(transit_time))*3.6

    # Check to see if the difference in time is positive or negative.
    if transit_time > 0:
        # if it is positive then the vehicle hit VW_8 first and is travelling SW
        direction = 'SW'
    else:
        # if it is negative then it hit VW_28 first and is travelling NE
        direction = 'NE'
    return stats, max_rev_gauge, transit_time, speed, direction


def analyse_all(data_dir, file_list):
    '''
    analyse_all intergrates the processes of file_import, centre_average if 
    applicable depending on the user inputs and analyse_event into a singular 
    functions. taking inputs from the user to determine which guage to analyse
    and then anlysing that guage over all recorded events and files within 
    file_list

    Parameters
    ----------
    data_dir : str
    file_list : list

    Returns
    -------
    array_starts : ndarray
    array_speeds : ndarray
    array_directions : ndarray
    array_strains : ndarray
    smoothed : boolean

    '''
    # Generate the lists used for computation
    event_starts = []
    directions = []
    speeds_all = []
    strain = []
    # Prompt the users for inputs
    gauge_input = input('Enter the gauge to analyse: ')
    av_prompt = input('Do you wish to smooth the data (y/[n]): ')

    if av_prompt == 'y':
        # If the user wanted to use averaged data prompt for smoothing window
        wind = int(input('Enter the smoothing window width: '))
    # Loop through each file in file_list
    for file in file_list:
        # Open the file using file_import
        linecount, headers, times, data = file_import(f'{data_dir}/{file}')
        # If smoothing is used call centre_average to convert data
        if av_prompt == 'y':
            # Set the boolean to True for further processing
            smoothed = True
            avg_data = centre_average(data, wind)
            # Analyse each file
            stats, grev_max, t, s, d = analyse_event(times, headers, avg_data)
            # Extract all useful data from each file and add them to lists
            event_starts.append(times[0])
            directions.append(d)
            speeds_all.append(s)
            header_index = headers.index(gauge_input)
            strain.append(stats[2, header_index])
        # Extract the critical information using raw data

        else:
            # Set smoothed to False
            smoothed = False
            # Analyse each file
            stats, grev_max, t, s, d = analyse_event(times, headers, data)
            # Append the lists with the extracted information
            event_starts.append(times[0])
            directions.append(d)
            speeds_all.append(s)
            header_index = headers.index(gauge_input)
            strain.append(stats[2, header_index])

    # Convert all lists to arrays
    array_starts = np.array(event_starts)
    array_speeds = np.array(speeds_all)
    array_directions = np.array(directions)
    array_strains = np.array(strain)

    return array_starts, array_speeds, array_directions, array_strains, smoothed


def plot1_bar(array_starts, array_strains, smoothed):
    '''
    plot1_bar is a simple function dedicated to plotting a bar graph of the
    max strain on the gauge outlined in analyse_all against time, taking 
    data outputted by analyse_all and plotting it. 

    Parameters
    ----------
    array_starts : ndarray
    array_strains : ndarray
    smoothed : boolean

    Returns
    -------
    None.

    '''
    time_diff = (array_starts - array_starts[0])/np.timedelta64(1, 'm')
    # Define the fig1 and ax variables
    fig1, ax = plt.subplots()
    # Set the graph as a bar and the bar graph width to 10 then plot the data
    ax.bar(time_diff, array_strains, 10)
    # Plot the axis labels grid and graph title
    ax.set(xlabel='Time from first event (min)', ylabel='Strain reversal\
           (\u03BC\u03B5)')
    ax.grid()
    # Change the figure title depending on what dataset was used
    if smoothed == True:
        fig1.suptitle(
            'Timing and magnitude of measured strain reversal [averaged data]')
    elif smoothed == False:
        fig1.suptitle(
            'Timing and magnitude of measured strain reversal [raw data]')
    # Show the plot
    plt.show
    return None


def plot2_hist(array_starts, array_speeds, array_strains, smoothed):
    '''
    plot2_hist takes the outputs of analyse_all and plots 2 histograms that 
    share the same y axis, one of the frequency of a range of speeds, and the 
    other of the frequency of maximum strain expereiced by the gauge inputted 
    in analyse_all.

    Parameters
    ----------
    array_starts : ndarray
    array_speeds : ndarray
    array_strains : ndarray
    smoothed : boolean

    Returns
    -------
    None.

    '''
    # Set the values for fig2, ax1, ax2, defining that they share the y-axis
    fig2, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    # Set the data lists for both graphs and thier respective bins and width
    ax1.hist(array_speeds, bins=np.arange(35, 70, 5))
    ax2.hist(array_strains, bins=np.arange(80, 190, 10))
    # Generate the axis labels and graph title
    ax1.set(xlabel='Speed(km/hr)', ylabel='Frequency')
    ax2.set(xlabel='Strain reversal(\u03BC\u03B5)')
    # Deter,ome graph title depending on what data set was used in processing
    if smoothed == True:
        fig2.suptitle('Frequency of speed and loading events [averaged data]')
    if smoothed == False:
        fig2.suptitle('Frequency of speed and loading events [raw data]')
    # Show the plot
    plt.show
    return None


def main():
    '''
    main is a function dedicated to the operated of the user interface and the
    user interaction with the code and other functions. It's purpose is to 
    guide the user and avoid potential errors and loops within the function 
    code.

    Parameters
    -------
    None.

    Returns
    -------
    None.

    '''
    # Define the data directory of the live loads .dat files and txt files
    data_dir = 'data'
    # Generate a list called file_list to add the extracted file names too
    file_list = []
    # Open the .txt file as a csv file and loop through all values
    with open(data_dir+'/file_list.txt') as csv_file:
        file_name_list = list(csv.reader(csv_file, delimiter=','))
        # Add extracted list items into a standerdized list
        for file_name_raw in file_name_list:
            file_list.append(file_name_raw[0])

    # Set several boolean variables that will be used to avoid/cause loops
    smooth_avg = False
    data_exists = False
    on = True

    # Define that while the boolean on is True to run the follow code
    while on == True:
        # Prompt the user to input a command within the main functions commands
        option = input('Please enter a command: ')
        # Format the inputted command to avoid computation complications
        option = option.strip()

        # Check that a variable was inputted
        if option != '':

            # if h is inputted display the HELP message
            if option == 'h':
                print(HELP)

            # if l is inputted attempt to run file_import
            elif option == 'l':
                # Set the file_loop boolean to True so the l command loops
                file_loop = True
                # Check to see if the command is looping
                while file_loop == True:
                    # Prompt the user for the name of the file in .dat format
                    file = input('Enter the name of the event file: ')
                    # If the file exists call file_import
                    if file in file_list:
                        linec, head, times, data = file_import(f'{data_dir}/{file}')
                        # Print a statement declaring the number of lines
                        print(str(linec)+' lines of data read from', file+'.')
                        # Run analyse_event on the data from file_import
                        stats, mrg, tt, s, d = analyse_event(times, head, data)
                        # Declare which gauge recorded the most strain
                        print(mrg, 'measured the greatest strain reversal in', file)
                        # Allow the code to break the loop
                        file_loop = False
                        # Declare that data exists now that data is saved
                        data_exists = True
                    # If the file is not within file_list print that it is not
                    else:
                        print('This file does not exist.')

            # If the command s is inputted check to see that data is saved
            elif option == 's':
                if data_exists == True:
                    # Prompt the user for a window width for smoothing
                    window = int(input('Enter the smoothing window width: '))
                    # Callthe centre_average function on the dataset
                    avg_data = centre_average(data, window)
                    # Determine the percentage strain reduction due to smoothing
                    max_index = head.index(mrg)
                    max_old = stats[0, max_index]
                    max_new = np.max(avg_data[:, max_index])
                    red_perc = round(((1-(max_new/max_old))*100), 2)
                    red_rdt = "{:.2f}".format(red_perc)
                    print('The maximum strain measured at', mrg,
                          'has been reduced by', red_rdt+'%')
                    # Declare that smooth_avg = True for further computing
                    smooth_avg = True
                # If data does not exist prompt the user to load a file
                elif data_exists == False:
                    print('You must load a file before proceeding...')
            # Check if the first index in the command is p
            if option[0] == 'p':
                # Check that data exists
                if data_exists == True:
                    # Seperate the inputted command to extract the gauges
                    option_entered = option.split()
                    gauges_entered = option_entered[1:]
                    # Check that guages were inputted
                    if len(option_entered) <= 1:
                        # if no gauges were inputted prompt the users to input
                        print('No gauges selected to plot.')
                    # Check to see if the data has been smoothed
                    elif smooth_avg == True:
                        # Plot using plot_avg_data if data is smoothed
                        print('Creating plots...')
                        plot_avg_data(times, head, data,
                                      avg_data, gauges_entered)
                    elif smooth_avg == False:
                        # Plot using plot_data if data is not smoothed
                        print('Creating plots...')
                        plot_data(times, head, data, gauges_entered)
                # Verifyng that data exists, prompt for a file if it does not
                elif data_exists == False:
                    print('You must load a file before proceeding...')

            # Check if command a was inputted
            elif option == 'a':
                # Call and run analyse_all on all datasets and files
                a_st, a_sp, a_d, a_str, smoothed = analyse_all(
                    data_dir, file_list)
                print('Creating plots...')
                # Generate the graphs from plot1_bar and plot2_hist
                plot1_bar(a_st, a_str, smoothed)
                plot2_hist(a_st, a_sp, a_str, smoothed)
                # Prompt the user to input the speed limit
                speed_limit = float(input('Enter a speed limit to impose: '))
                # Determine the number of cars exceeding the speed limit
                speed_check = a_sp > speed_limit
                speed_lim = str(speed_limit)
                speed_count = sum(speed_check)
                # Determine if smootheed or raw data was used for processing
                if smoothed == True:
                    dtype = 'averaged data.'
                else:
                    dtype = 'raw data.'
                # Print a statement declaring the number of cars speeding
                print(speed_count, 'vehicles detected exceeding the imposed speed limit of',
                      speed_lim+'km/hr using', dtype)
            # If command q was entered, verify the users intent with a prompt
            elif option == 'q':
                answer = input('Are you sure? (y/[n]): ')
                # if y then close program
                if answer == 'y':
                    on = False
                # If not y, continue with main
                else:
                    continue
            # If no known command was entered continue to prompt for a command
            else:
                continue
        # If a empty command was entered continue to prompt for a command
        else:
            continue


if __name__ == "__main__":
    main()
