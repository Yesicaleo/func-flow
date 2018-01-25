import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, datetime, timedelta


def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1). Parameter: d for date object,
    years for added or subtracted years

    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


def is_multiple_date_data(df):
    two_digit_year = '/' in df.iloc[4,0][-4:]
    year_in_front = '-' in df.iloc[4,0][-4:]
    try:
        if two_digit_year:
            datetime.strptime(df.iloc[4,0], "%m/%d/%y")
            datetime.strptime(df.iloc[4,2], "%m/%d/%y")
        elif year_in_front:
            datetime.strptime(df.iloc[4,0], "%Y-%m-%d")
            datetime.strptime(df.iloc[4,2], "%Y-%m-%d")
        else:
            datetime.strptime(df.iloc[4,0], "%m/%d/%Y")
            datetime.strptime(df.iloc[4,2], "%m/%d/%Y")
        return True

    except Exception as e:
        return False

def is_two_digit_year(date):
    if '/' in date[-3:]:
        return True
    else:
        return False

def year_in_front(date):
    if '-' in date[-3:]:
        return True
    else:
        return False


def get_date_from_offset_julian_date(row_number, year, start_date):
    start_year = year
    end_year = year + 1
    julian_start_date_start_year = datetime.strptime("{}/{}".format(start_date, start_year), "%m/%d/%Y").timetuple().tm_yday
    julian_start_date_end_year = datetime.strptime("{}/{}".format(start_date, end_year), "%m/%d/%Y").timetuple().tm_yday

    if start_year % 4 == 0:
        days_in_year_start = 366
    else:
        days_in_year_start = 365

    if end_year % 4 == 0:
        days_in_year_end = 366
    else:
        days_in_year_end = 365


    if row_number <= days_in_year_start - julian_start_date_start_year:
        current_year = start_year
        date_delta = julian_start_date_start_year + row_number
        current_date = datetime(current_year, 1, 1) + timedelta(date_delta - 1)
    else:
        current_year = end_year
        date_delta = row_number - days_in_year_start + julian_start_date_start_year - 1
        current_date = datetime(current_year, 1, 1) + timedelta(date_delta)

    return current_date

def moving_average(data_array):
    result_data = []
    for index, data in enumerate(data_array):
        if index <= 3:
            result_data.append(data_array[index])
        else:
            result_data.append((data_array[index] + data_array[index - 1] + data_array[index - 2] + data_array[index - 3] + data_array[index - 4])/5)
    return result_data


def get_nan_fraction_in_array(data_array):
    length_array = len(data_array)
    counter = 0
    for data in data_array:
        if pd.isnull(data):
            counter = counter + 1
    return counter / length_array


def smart_plot(result_matrix, metrics_array):

    metrics = {}

    for metric in metrics_array:
        metrics[metric] = []
        metrics[metric].append([])

def plot_matrix(result_matrix):

    boxplot_color = ['#0D47A1','#80DEEA','#FF9800','#FFEB3B','#F44336','#8BC34A','#F48FB1','#7E57C2','#C51162', '#212121']
    metrics = ['Gauge_Class','Gauge_Number','Average_of_Average','Ten_Percentile_Average','Fifty_Percentile_Average','Ninty_Percentile_Average','Ten_Percentile_COV','Fifty_Percentile_COV','Ninty_Percentile_COV']


    current_class_index = 0

    average_average_array = []
    average_average_array.append([])

    ten_percentile_average_array = []
    ten_percentile_average_array.append([])

    fifty_percentile_average_array = []
    fifty_percentile_average_array.append([])

    ninty_percentile_average_array = []
    ninty_percentile_average_array.append([])

    ten_percentile_cov_array = []
    ten_percentile_cov_array.append([])

    fifty_percentile_cov_array = []
    fifty_percentile_cov_array.append([])

    ninty_percentile_cov_array = []
    ninty_percentile_cov_array.append([])

    for index, class_number in enumerate(result_matrix[0]):

        average_average_array[current_class_index].append(result_matrix[2][index])
        ten_percentile_average_array[current_class_index].append(result_matrix[3][index])
        fifty_percentile_average_array[current_class_index].append(result_matrix[4][index])
        ninty_percentile_average_array[current_class_index].append(result_matrix[5][index])
        ten_percentile_cov_array[current_class_index].append(result_matrix[6][index])
        fifty_percentile_cov_array[current_class_index].append(result_matrix[7][index])
        ninty_percentile_cov_array[current_class_index].append(result_matrix[8][index])

        if index == len(result_matrix[0]) - 1:
            plt.ion()
            
            plt.figure(metrics[2])
            plt.title('Average of Average')
            box1 = plt.boxplot(average_average_array, notch=True, patch_artist=True)
            for patch, color in zip(box1['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[2]))
                       

            plt.figure(metrics[3])
            plt.title('10th Percentile of the Average')
            box2 = plt.boxplot(ten_percentile_average_array, notch=True, patch_artist=True)
            for patch, color in zip(box2['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[3]))
            

            plt.figure(metrics[4])
            plt.title('50th Percentile of the Average')
            box3 = plt.boxplot(fifty_percentile_average_array, notch=True, patch_artist=True)
            for patch, color in zip(box3['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[4]))
            

            plt.figure(metrics[5])
            plt.title('90th Percentile of the Average')
            box4 = plt.boxplot(ninty_percentile_average_array, notch=True, patch_artist=True)
            for patch, color in zip(box4['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[5]))
            

            plt.figure(metrics[6])
            plt.title('10th Percentile of COV')
            box5 = plt.boxplot(ten_percentile_cov_array, notch=True, patch_artist=True)
            for patch, color in zip(box5['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[6]))
            
  
            plt.figure(metrics[7])
            plt.title('50th Percentile of COV')
            box6 = plt.boxplot(fifty_percentile_cov_array, notch=True, patch_artist=True)
            for patch, color in zip(box6['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[7]))
            
  
            plt.figure(metrics[8])
            plt.title('90th Percentile of COV')
            box7 = plt.boxplot(ninty_percentile_cov_array, notch=True, patch_artist=True)
            for patch, color in zip(box7['boxes'], boxplot_color):
                patch.set_facecolor(color)
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metrics[8]))

        elif result_matrix[0][index + 1] != class_number:
            current_class_index = current_class_index + 1

            average_average_array.append([])
            ten_percentile_average_array.append([])
            fifty_percentile_average_array.append([])
            ninty_percentile_average_array.append([])
            ten_percentile_cov_array.append([])
            fifty_percentile_cov_array.append([])
            ninty_percentile_cov_array.append([])