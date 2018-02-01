import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_winter_highflow import calculate_timing_duration_frequency_annual

np.warnings.filterwarnings('ignore')

def timing_duration_frequency_annual(start_date, directoryName, endWith):
    exceedance_percent = [2, 5, 10, 20, 50]
    percentilles = [10, 50, 90]

    gauge_class_array = []
    gauge_number_array = []

    timing = {}
    duration = {}
    freq = {}

    for percent in exceedance_percent:
        timing[percent] = {}
        duration[percent] = {}
        freq[percent] = {}
        for percentille in percentilles:
            timing[percent][percentille] = []
            duration[percent][percentille] = []
            freq[percent][percentille] = []


    for root,dirs,files in os.walk(directoryName):
        for file in files:
           if file.endswith(endWith):

               fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
               step = is_multiple_date_data(fixed_df);


               current_gaguge_column_index = 1

               while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):
                   current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                   """General Info"""
                   gauge_class_array.append(current_gauge_class)
                   gauge_number_array.append(current_gauge_number)


                   current_timing, current_duration, current_freq = calculate_timing_duration_frequency_annual(flow_matrix, year_ranges, start_date, exceedance_percent)

                   for percent in current_timing:
                       for percentille in percentilles:

                           timing[percent][percentille].append(np.nanpercentile(np.array(current_timing[percent], dtype=np.float), percentille))
                           duration[percent][percentille].append(np.nanpercentile(current_duration[percent], percentille))
                           freq[percent][percentille].append(np.nanpercentile(current_freq[percent], percentille))

                   flow_matrix = np.vstack((year_ranges, flow_matrix))

                   np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")

                   current_gaguge_column_index = current_gaguge_column_index + step


    column_header = ['Class', 'Gauge #']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in current_timing:
        for percentille in percentilles:
            column_header.append('Timing:{}% exceedance-{}%'.format(percent, percentille))
            column_header.append('Duration:{}% exceedance-{}%'.format(percent, percentille))
            column_header.append('Freq:{}% exceedance-{}%'.format(percent, percentille))

            result_matrix.append(timing[percent][percentille])
            result_matrix.append(duration[percent][percentille])
            result_matrix.append(freq[percent][percentille])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/winter_highflow_properties_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
