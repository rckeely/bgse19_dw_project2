import pandas as pd
import os
import datetime


def makeDirIfNotExists(my_dir):
    try:
        os.listdir(my_dir)
    except FileNotFoundError as e:
        print('Making data/archive directory.')
        os.makedirs(my_dir)

    return 1


def getLatestELOData():
    #Elo file paths
    nfl_elo_add = 'https://projects.fivethirtyeight.com/nfl-api/nfl_elo.csv'
    nfl_elo_latest_add = 'https://projects.fivethirtyeight.com/nfl-api/nfl_elo_latest.csv'

    #file names
    nfl_elo_file = 'nfl_elo.csv'
    nfl_elo_latest_file = 'nfl_elo_latest.csv'

    #Data file path
    data_dir = 'data/elo'

    #Archive Directory
    archive_dir = 'data/elo/archive'

    try:
        nfl_elo = pd.read_csv(nfl_elo_add)
        nfl_elo_latest = pd.read_csv(nfl_elo_latest_add)
    except Exception as e:
        print('Could not get latest data')
        return -1

    try:
        makeDirIfNotExists(data_dir)
        makeDirIfNotExists(archive_dir)

        files_in_dir = os.listdir(data_dir)
    except Exception as e:
        print("Could not make new directory on disk; check permissions?")
        return -1

    try:
        #For each file, if not present in listdir, then download; if present move to archive
        old_path = data_dir + '/' + nfl_elo_file
        if nfl_elo_file in files_in_dir:
            #Move to archive
            new_path = archive_dir + '/nfl_elo_' + datetime.date.today().strftime('%Y%m%d') + 'csv'
            os.rename(old_path,new_path)

        #Then download new file
        print('Got latest total file.')
        nfl_elo.to_csv(old_path, index=False)

        ##

        old_path = data_dir + '/' + nfl_elo_latest_file
        if nfl_elo_latest_file in files_in_dir:
            #Move to archive
            new_path = archive_dir + '/nfl_elo_latest_' + datetime.date.today().strftime('%Y%m%d') + 'csv'
            os.rename(old_path,new_path)

        print('Got latest small file.')
        nfl_elo_latest.to_csv(old_path, index=False)

        return 1
    except Exception as e:
        print('Error saving latest files to disk.')
        return -1