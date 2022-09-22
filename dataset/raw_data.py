import os
from os import path
from xml.etree.ElementInclude import include
import pandas as pd
from typing import Dict, Tuple


def public_train_data(rootdir: str):
    '''
        Return: Dict:   
            input: stations
            output: stations

            data of stations: Dict:   
                station_name: str
                Dict: 
                    data: pandas.DataFrame
                    loc: (float, float)
    '''

    loc_input = _read_locations(path.join(rootdir, 'location_input.csv'))
    loc_output = _read_locations(path.join(rootdir, 'location_output.csv'))

    return {
        'input': _read_stations(path.join(rootdir, 'input'), loc_input),
        'output': _read_stations(path.join(rootdir, 'output'), loc_output),
    }

def public_test_data(testdir: str, traindir: str):
    '''
        Return: List:
            input: stations
                station_name: str
                Dict:
                    data: pandas.DataFrame
                    loc: (float, float)
            loc_output: (float, float)
            folder_name: str
    '''

    loc_input = _read_locations(path.join(traindir, "location_input.csv"))
    loc_output = _read_locations(path.join(testdir, "location.csv"))
    data = {}

    rootdir = path.join(testdir, "input")
    for folder_name in os.listdir(rootdir):
        if path.isdir(folder_name):
            dir_path = path.join(rootdir, folder_name)

            data[folder_name] = {
                'input': _read_stations(dir_path, loc_input),
                'loc_output': loc_output,
            }
    return data


def private_train_data(rootdir: str):
    '''
        Return: Dict:   
            air: stations
            meteo: stations
            data of stations: Dict:   
                station_name: str
                Dict: 
                    data: pandas.DataFrame
                    loc: (float, float)
    '''

    loc_air = _read_locations(path.join(rootdir, "air/location.csv"))
    loc_meteo = _read_locations(path.join(rootdir, "meteo/location.csv"))

    return {
        "air": _read_stations(path.join(rootdir, "air"), loc_air),
        "meteo": _read_stations(path.join(rootdir, "meteo"), loc_meteo)
    }

def private_test_data(rootdir: str):
    '''
        Return: List:
            air: stations
                station_name: str
                Dict:
                    data: pandas.DataFrame
                    loc: (float, float)
            meteo: stations
                station_name: str
                Dict:
                    data: pandas.DataFrame
                    loc: (float, float)
            loc_output: (float, float)
            folder_name: str
    '''

    data = {}
    for folder_name in os.listdir(rootdir):
        if path.isdir(folder_name):
            dir_path = path.join(rootdir, folder_name)

            loc_air = _read_locations(
                path.join(dir_path, "location_input.csv"))
            loc_meteo = _read_locations(
                path.join(dir_path, "meteo/location_meteorology.csv"))
            loc_output = _read_locations(
                path.join(dir_path, "location_output.csv"))

            data[folder_name] = {
                'air': _read_stations(dir_path, loc_air),
                'meteo': _read_stations(path.join(dir_path, "meteo"), loc_meteo),
                'loc_output': loc_output,
            }
    return data


def _read_stations(rootdir: str, loc_map: Dict[str, Tuple[float, float]]):
    stations = {}
    for station_name in loc_map.keys():
        file_path = path.join(rootdir, station_name + ".csv")
        df = pd.read_csv(file_path)
        stations[station_name] = {
            "loc": loc_map[station_name],
            "data": df
        }
    return stations


def _read_locations(file_path: str) -> Dict[str, Tuple[float, float]]:
    df = pd.read_csv(file_path)

    try:
        return dict(zip(
            df['station'],
            zip(df["longitude"], df["latitude"])
        ))
    except:
        try:
            return dict(zip(
                df['location'],
                zip(df["longitude"], df["latitude"])
            ))
        except:
            return dict(zip(
                df["stat_name"],
                zip(df["lon"], df["lat"])
            ))
