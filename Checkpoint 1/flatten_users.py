from collections.abc import MutableMapping
from datetime import datetime, date
# from ast import literal_eval
from threading import current_thread
from multiprocessing import current_process

import itertools
import json
import multiprocessing
import os
import numpy as np
import pandas as pd


# import flatdict

# Generic functions for cleaning the data
def convert_epoch_time_to_datetime(epoch_time):
    """
    Takes an epoch timestamp and converts it to datetime format
    Ref: 
    https://www.pythonforbeginners.com/basics/convert-epoch-to-datetime-in-python
    https://stackoverflow.com/questions/49710963/converting-13-digit-unixtime-in-ms-to-timestamp-in-python 
    """

    converted_date = None
    try:
        # Divide by 1,000 to remove ms time
        converted_date = datetime.fromtimestamp(int(epoch_time)/1000).isoformat()
    except ValueError as err:
        # print(f"Cannot convert epoch time {epoch_time} to isodate {err}")

        try:
            date.fromisoformat(str(epoch_time))
        except ValueError as err:
            # Value passed is already in the correct `iso` format. Nothing else to do here.
            return epoch_time
    
    return converted_date

# Testing the epoch time conversion
# convert_epoch_time_to_datetime(1588990000000) # '2020-05-08T22:06:40'
# convert_epoch_time_to_datetime(1588994215395)   # '2020-05-08T23:16:55.395000'


def flatten_json_column(json_col: str): # df: pd.DataFrame, 
    """
    This function flattens JSON columns to individual columns
    It merges the flattened dataframe with expected dataframe to capture missing columns from JSON
    :param df: Crowd Work Data CSV raw dataframe
    :param json_col: custom data columns in JSON format.
    :param custom_df: expected dataframe
    :return: returns df pandas dataframe

    Ref: 
    https://github.com/vvgsrk/ParseCSVContainsJSONUsingPandas/tree/main
    https://avithekkc.medium.com/how-to-convert-nested-json-into-a-pandas-dataframe-9e8779914a24
    """
    # https://sandbox.toloka.yandex.com/es/task/1083120/00001086f0--61e9b9cd825234636baafa59
    # 00001086d6--61e9b930a2d62b2b56644596

    pid = os.getpid()
    threadName = current_thread().name
    processName = current_process().name

    print(f"flatten_json_column json_col {json_col}")

    print(f"flatten_json_column * {pid} * {processName} * {threadName} \
        ---> Start counting...")

    # Make sure to sort the `na_positions` last because this could effect how many columns
    # that the nested column values are shown. If the nested column value is `NaN` first then
    # nothing will get populated for those nested column fields. (e.g. `c4_project.hit_requirements`)
    # Note: Comment out the fields that you don't want to show up in the final dataframe.
    # struct_data_json = {
    #     "task_id": [None],
    #     "assignment_id": [None],
    #     "accepted_at": [None],
    #     "deadline": [None],
    #     "time_to_deadline_in_seconds": [None],
    #     "state": [None],
    #     "question.value": [None],
    #     "question.type": [None],
    #     # "question.attributes": [None],
    #     "question.attributes.FrameSourceAttribute": [None],
    #     "question.attributes.FrameHeight": [None],
    #     "project.hit_set_id": [None],
    #     "project.title": [None],
    #     "project.requester_id": [None],
    #     "project.requester_name": [None],
    #     "project.description": [None],
    #     "project.assignment_duration_in_seconds": [None],
    #     "project.creation_time": [None],
    #     "project.assignable_hits_count": [None],
    #     "project.latest_expiration_time": [None],
    #     "project.caller_meets_requirements": [None],
    #     "project.caller_meets_preview_requirements": [None],
    #     "project.last_updated_time": [None],
    #     "project.monetary_reward.currency_code": [None],
    #     "project.monetary_reward.amount_in_dollars": [None],
    #     # "project.hit_requirements.qualification_type_id": [None],
    #     # "project.hit_requirements.comparator": [None],
    #     # "project.hit_requirements.worker_action": [None],
    #     # "project.hit_requirements.qualification_values": [None],
    #     # "project.hit_requirements.caller_meets_requirement": [None],
    #     # "project.hit_requirements.qualification_type.qualification_type_id": [None],
    #     # "project.hit_requirements.qualification_type.name": [None],
    #     # "project.hit_requirements.qualification_type.visibility": [None],
    #     # "project.hit_requirements.qualification_type.description": [None],
    #     # "project.hit_requirements.qualification_type.has_test": [None],
    #     # "project.hit_requirements.qualification_type.is_requestable": [None],
    #     # "project.hit_requirements.qualification_type.keywords": [None],
    #     # "project.hit_requirements.caller_qualification_value.integer_value": [None],
    #     # "project.hit_requirements.caller_qualification_value.locale_value.country": [None],
    #     # "project.hit_requirements.caller_qualification_value.locale_subdivision": [None],
    #     "project.requester_url": [None],
    #     "expired_task_action_url": [None],
    #     "task_url": [None]
    # }

    def _flatten_dict(d: MutableMapping, sep: str= '.') -> MutableMapping:
        """
        Take in 
        """
        [flat_dict] = pd.json_normalize(data=d, sep=sep, max_level=None).to_dict(orient='records')
        return flat_dict

    try:
        df_temp = pd.DataFrame() # struct_data_json

        # If c4 `nan` value is passed, do nothing except return empty dataframe.
        # If c4 has a string dicionary, then build new dataframe from it.
        if isinstance(json_col, str):
            # Convert the input (str) to (dict) type.
            # Build a flattened dictionary before sending to Pandas to `json_normalize`
            dict_json_flattened = _flatten_dict(json.loads(json_col))

            # Explicitly remove this column because it's a nested list and is hard to flatten.
            # Plus this column doesn't have any values that we need for our model.
            # del dict_json_flattened["project.hit_requirements"]

            # Separate the nested list of values for 'activeAssignments'.
            # For now we're just using the first assignment at index 0.

            # series_active_assignments = pd.Series(
            #     _flatten_dict(dict_json_flattened["activeAssignments"][0])
            # ).add_prefix('active_assignments.')
            # df_active_assignments = series_active_assignments.to_frame().T

            df_temp = pd.DataFrame([dict_json_flattened])
            # df_temp = pd.concat([df_temp, df_active_assignments], axis='columns', ignore_index=False)

            try:
                for a in range(len(dict_json_flattened["activeAssignments"])):
                    series_active_assignments = pd.Series(
                        _flatten_dict(dict_json_flattened["activeAssignments"][a])
                    ).add_prefix(f'activeAssignments.{a}.')
                    df_temp = pd.concat([df_temp, series_active_assignments.to_frame().T], axis='columns', ignore_index=False)
            except KeyError as err:
                # print(f"flatten_json_columns: {err}")
                pass
            else:
                # Remove this because we've flattened the column value out.
                del df_temp["activeAssignments"]

    except json.JSONDecodeError as err:
        print(f"flatten_json_columns: Invalid JSON argument passed - json.JSONDecodeError: {err}")

    print(f"flatten_json_column * {pid} * {processName} * {threadName} \
        ---> Finished counting...")

    # Return dataframe with flatten columns and 'c4.' prefix.
    return df_temp.add_prefix('c4.')


# Ref:
# https://medium.com/analytics-vidhya/multiprocessing-multithreading-involving-2-dataframes-in-python-1f65e3e748b3
# https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/
# https://stackoverflow.com/questions/40357434/pandas-df-iterrows-parallelization
# https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments

def flatten_c4_in_parallel(df_user: pd.DataFrame):
    """
    Use multiprocessing in flattening the 'c4' column for multiple records.
    """
    
    # Merge records that have 'c4' values.
    # df_c4_flattened = pd.DataFrame()
    df_c4_exists = df_user[~df_user['c4'].isna()]

    # create as many processes as there are CPUs on your machine
    # leave one free to not freeze machine
    num_processes = multiprocessing.cpu_count() - 1

    # calculate the chunk size as an integer
    # chunk_size = int(df_c4_exists.shape[0]/num_processes)

    # this solution was reworked from the above link.
    # will work even if the length of the dataframe is not evenly divisible by num_processes
    # chunks_list = [df_c4_exists.iloc[df_c4_exists.index[i:i + chunk_size]] for i in range(0, df_c4_exists.shape[0], chunk_size)]
    chunks_list = np.array_split(df_c4_exists, num_processes)
    list_c4_row = []
    for row in chunks_list:
        for j in row['c4']:
            list_c4_row.append(j)

    # Hold results in this dataframe for 'c4' flattened for the particular user.
    df_c4_flattened = pd.DataFrame()

    # Start worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:

            # try:
                # apply our function to each chunk in the list
                # df_pool_result = pool.map(flatten_json_column, chunks_list).iloc[0].to_frame().T
                # df_c4_flattened = pd.concat([df_c4_flattened, df_pool_result], ignore_index=True)
            
        df_results = pool.starmap( flatten_json_column, zip(list_c4_row) )  # zip(chunks_list, itertools.repeat("c4", len(chunks_list)))
        df_c4_flattened = pd.concat(df_results, axis="index", ignore_index=False, sort=False)

            # except IndexError as err:  # pylint: disable=unused-argument
            #     pass
        
        # closing and joining the pool to make sure that the jobs finished and flushed.
        pool.close()
        pool.join()

    df_c4_user = pd.concat([df_c4_exists, df_c4_flattened], axis="columns", ignore_index=True)

        # for i, j in df_c4_exists.iterrows():
        #     # if isinstance(j["c4"], str):
        #     try:
        #         # https://stackoverflow.com/questions/33094056/is-it-possible-to-append-series-to-rows-of-dataframe-without-making-a-list-first
        #         series_temp = flatten_json_column(j["c4"]).iloc[0].to_frame().T

        #         df_c4_flattened = pd.concat([df_c4_flattened, series_temp], ignore_index=True) 
        #     except IndexError as err:
        #         pass
        #     df_c4_user = pd.concat([df_c4_exists, thread_df_c4_flattened], axis="columns", ignore_index=False)

    return df_c4_user


def flatten_user_to_csv(user_id: int, df_user: pd.DataFrame, csv_output_path: str=""):
    """
    Read in the cleaned Amazon MT dataset and write it out for a particular user (e.g `ae862298385abab2a0a1619f8cedef9d`)
    Convert the `c4` event column by flattening most dict values into separate columns and 
    write out to temporary *.csv to run limited records moving forward.

    Parameters
    user_id (int): c10 (user) field in the original dataset
    df_user (pd.DataFrame): Pandas dataframe information for the user on the original dataset.
    debug (bool): indicate
    """

    # Read the data into a dataframe and flatten 'c4 (event)' column to new columns.

    

    # # Suggest writing this transformed data out to a file to read in that transformed file for further processing.
    # df_temp_user = pd.read_csv(FLATTENED_USER_CSV_PATH, encoding='utf-8', header="infer")

    # df_temp_user.sort_values(by=['user', 'time'], ascending=[True, True]).to_csv(FLATTENED_USER_CSV_PATH,
    #                                                                              encoding='utf-8', header=True, columns=columns, index=False, mode="w")
    
    # Convert the milliseconds c8 (time) to an iso datetime format.
    # For some reason writing out to temporary csv here helps when joining with the c4 (extra) flattened information.
    # If we forget this step the concat of c4 (extra) to the original dataframe gets messed up.
    # ------------------------------------------------------------------------------------
    TIMECONVERTED_USER_CSV_PATH = f"../data/toloka_telemetry_db_{user_id}.csv"

    # Convert the epoch timestamp to datetime and write out to temporary csv file.
    df_user['time'] = df_user.time.map(convert_epoch_time_to_datetime)
    df_user.to_csv(TIMECONVERTED_USER_CSV_PATH, encoding='utf-8', header=True, index=False, mode="w")

    # Droping the Dataframe to avoid duplicates when reading in again from csv after transforming the epic timestamp.
    df_user.drop(df_user.index, inplace=True)

    # Read in the transformed epoch time values and perform further processing with c4 (extra) column.
    df_user = pd.read_csv(TIMECONVERTED_USER_CSV_PATH, encoding='utf-8', header="infer")
    os.remove(TIMECONVERTED_USER_CSV_PATH)
    # print("Removed temporary time converted file {TIMECONVERTED_USER_CSV_PATH}.")
    # ------------------------------------------------------------------------------------

    df_c4_user = flatten_c4_in_parallel(df_user)
    # df_c4_user = pd.read_csv(f"../data/toloka_combine/toloka_telemetry_db_{user_id}_flattened.csv", encoding='utf-8', header="infer")

    # # Merge records that have 'c4' values.
    # df_c4_flattened = pd.DataFrame()
    # df_c4_exists = df_user[~df_user['c4'].isna()]

    # # Calculate the number of 'c4' records to handle per thread
    # num_of_c4_records = len(df_c4_exists) // NUM_THREADS

    # # Loop through the threads and create them
    # for i in range(0, NUM_THREADS):

    #     # Initialize the records for this thread
    #     thread_records = []

    #     # Create a thread to write this chunk of lines to the output file
    #     thread = threading.Thread(target=flatten_json_column, args=(thread_lines, output_file_path))

    #     # Start the thread
    #     thread.start()

    # for i, j in df_c4_exists.iterrows():
    #     # if isinstance(j["c4"], str):
    #     try:
    #         # https://stackoverflow.com/questions/33094056/is-it-possible-to-append-series-to-rows-of-dataframe-without-making-a-list-first
    #         series_temp = flatten_json_column(j["c4"]).iloc[0].to_frame().T

    #         df_c4_flattened = pd.concat([df_c4_flattened, series_temp], ignore_index=True) 
    #     except IndexError as err:
    #         pass
    # df_c4_user = pd.concat([df_c4_exists, df_c4_flattened], axis="columns", ignore_index=False)

    # Merge records that have non 'c4' values.
    df_non_c4_exists = df_user[df_user['c4'].isna()]
    df_user = pd.concat([df_c4_user, df_non_c4_exists], axis="index", ignore_index=False)

    # Delete 'c4' column because it has been flattened.
    # del df_user["c4"]   

    # Data is sorted by c8 (time) field to ensure the events are in order.
    # This sorting by c8 (time) is important before we perform calculations on invisible labor time.
    df_user.sort_values(by=['time'], ascending=[True], inplace=True)

    # Write out the flattened user csv information.
    df_user.to_csv(csv_output_path, encoding='utf-8', header=True, index=False, mode="w")

    print(f"Created flattened csv {csv_output_path} for user {user_id}.")


def main():
    DATASET_TOLOKA_CSV_PATH = "../data/toloka_telemetry_db.csv"

    # Define columns for data
    columns = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'time', 'c9', 'user', 'c11', 'c12']

    # Read the data into a dataframe for further manipulation.

    # 4m 18.8s – Suggest writing this transformed data out to a file to read in that transformed file for further processing.
    df_default = pd.read_csv(DATASET_TOLOKA_CSV_PATH, encoding='utf-8', header=0, names=columns, low_memory=False)
    df_default.drop(columns=["c11", "c12"], inplace=True)

    # unique_users = ["541227437e3c39f534eb94d812a36782"]
    unique_users = ["1d879cab6a4b14427458d7fa73a8e090"]

    # Write out all flatten files per user.
    for user_id in unique_users:
        FLATTENED_USER_CSV_PATH = f"../data/toloka_telemetry_db_{user_id}_flattened.csv"
        # df_temp_user = pd.DataFrame()
        # df_temp_user = df_default[df_default.user == user_id].copy(deep=True)

        # df_temp_user.sort_values(by=['user', 'time'], ascending=[True, True]).to_csv(FLATTENED_USER_CSV_PATH,
        #             encoding='utf-8', header=True, columns=columns, index=False, mode="w")
        
        # Write out user. Perform a copy of the dataset into 'df_user' to prevent altering the original 'df_default'.
        flatten_user_to_csv(
            user_id,
            df_user=df_default[
                (df_default.user == user_id) & 
                (
                    (df_default.c1 == 113431) | 
                    (df_default.c1 == 113424) | 
                    (df_default.c1 == 113423) |
                    (df_default.c1 == 113436) |
                    (df_default.c1 == 113437) |
                    (df_default.c1 == 113438) |
                    (df_default.c1 == 113443) |
                    (df_default.c1 == 113444) |
                    (df_default.c1 == 113441) |
                    (df_default.c1 == 113450) |
                    (df_default.c1 == 113451) |
                    (df_default.c1 == 113452) |
                    (df_default.c1 == 113453) |
                    (df_default.c1 == 113454)
                )
            ], # & ((df_default.c1 == 113431) | (df_default.c1 == 113424) | (df_default.c1 == 113423))
            csv_output_path=FLATTENED_USER_CSV_PATH
            )

if __name__ == "__main__":
    main()