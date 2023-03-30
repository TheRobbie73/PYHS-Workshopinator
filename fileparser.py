import pygame as pg
import numpy as np
import pathlib as pl
import os

def main() -> list[dict]:
    file_path = pl.Path(__file__).absolute().parent/"read.rad"
    if not file_path.exists(): raise Exception("RAD file cannot be found! Make sure the file is labelled 'read.rad'")
    with open(file_path, "r") as file:
        data_list = []

        for i, line in enumerate(file):
            line.rstrip()
            if i == 0:
                # Station lat and long
                pass
            elif i % 2 == 0:
                # data line
                data_list.append(parse_data_line(line))

    return data_list

#todo: 
# instead of return data_list, return data_meta: dict
# {
#   "data_list"     : data_list,
#   "data_mean"     : mean,
#   "data_median"   : median
# }

def parse_data_line(data: str) -> dict:
    data_list = data.split()
    data_dict = {
        "time"          : data_list[0],
        "rot"           : tuple([float(i) for i in data_list[1:3]]),
        "rot_offset"    : tuple([float(i) for i in data_list[3:5]]),
        "freq"          : float(data_list[5]),
        "freq_width"    : float(data_list[6]),
        "mode"          : int(data_list[7]),
        "freq_num"      : int(data_list[8]),
        "data_points"   : [float(i) for i in data_list[9:]]
    }

    return data_dict

def render_all(data_list: list[dict], freq: int, surf: pg.surface.Surface) -> pg.surface.Surface:
    """
    Get intensity of certain freq from data and plot
    onto surface via azimuth/elevation coordinates.
    Min value -> blue, max value -> red.
    freq [0, freq_num - 1]
    """
    surf_size = surf.get_size()

    # literally just to get the min and max values
    intensities = [data_dict["data_points"][freq] for data_dict in data_list]
    data_range = (min(intensities), max(intensities))

    for data_dict in data_list:
        # azimuth range - (-180, 180)
        # elevation range - (0, 90)
        pos = (
            int((data_dict["rot"][0] + 180.0)*surf_size[0]/360.0),
            int(surf_size[1] - data_dict["rot"][1]*surf_size[1]/90.0)
        )
        red = int((data_dict["data_points"][freq] - data_range[0])*255/(data_range[1] - data_range[0]))
        blue = 255 - int((data_dict["data_points"][freq] - data_range[0])*255/(data_range[1] - data_range[0]))
        colour = "#{:02X}00{:02X}".format(red, blue)

        pg.draw.circle(
            surf,
            colour,
            pos,
            3
        )
    
    return surf

def graph_all(data_list: list[dict], freq: int, surf: pg.surface.Surface) -> pg.surface.Surface:
    surf_size = surf.get_size()
    intensities = [data_dict["data_points"][freq] for data_dict in data_list]
    data_range = (min(intensities), max(intensities))

    pos_list = []
    for i, data_dict in enumerate(data_list):
        pos = (
            int(i*surf_size[0]/(len(data_list) - 1)),
            surf_size[1] - int((data_dict["data_points"][freq] - data_range[0])*surf_size[1]/(data_range[1] - data_range[0]))
        )
        pos_list.append(pos)
        pg.draw.circle(
            surf,
            "#FFFFFF",
            pos,
            3
        )
    pg.draw.lines(
        surf,
        "#FFFFFF",
        False,
        pos_list,
        2
    )
    
    return surf

def graph_point(data_dict: dict, surf: pg.surface.Surface) -> pg.surface.Surface:
    """
    Graph of freq intensities of a certain point
    """
    data_range = (min(data_dict["data_points"]), max(data_dict["data_points"]))

    mean = sum(data_dict["data_points"])/data_dict["freq_num"]

    #data_range = (min(data_dict["data_points"]), mean)
    surf_size = surf.get_size()

    pos_list = []
    for i, intensity in enumerate(data_dict["data_points"]):
        pos = (
            int(i*surf_size[0]/data_dict["freq_num"]),
            surf_size[1] - int((intensity - data_range[0])*surf_size[1]/(data_range[1] - data_range[0]))
        )
        pos_list.append(pos)
        pg.draw.circle(
            surf,
            "#FFFFFF",
            pos,
            3
        )
    pg.draw.lines(
        surf,
        "#FFFFFF",
        False,
        pos_list,
        2
    )

    return surf

if __name__ == "__main__":
    test_data = "2023:080:02:44:17   39.8  50.6  -2.0   0.0  1419.39 0.00781250   4 156 -52.6 -53.5 -57.4 -56.3 -52.2 -46.2 -33.1 -29.0 -22.9 -20.0 -17.5 -15.6  -2.1  84.1  -4.5  -7.7  -5.1   0.4   8.0  18.9  15.6  10.4   7.8  10.0  12.7  14.2  17.5  18.2  20.2  21.6  24.2  26.7  29.0  30.9  33.5  35.1  37.8  40.0  42.5  45.3  48.0  49.5  51.5  54.1  55.7  58.3  60.4  63.8  66.6  69.2  70.3  74.0  75.2  77.6  79.9  82.9  55.6  58.9  66.1  74.0  77.7  87.6  99.8 105.3 111.5 125.5 130.5 141.5 150.0 159.6 163.6 169.7 165.6 169.8 167.7 170.7 171.9 170.8 166.0 158.1 154.8 146.6 144.4 143.9 147.0 144.3 146.2 149.9 154.8 162.1 167.6 177.6 179.5 184.5 188.6 187.1 190.6 189.5 183.9 181.2 178.3 169.6 215.5 249.6 279.5 323.3 370.7 422.8 490.0 555.2 705.4 923.1 1323.8 2307.8 4794.3 12023.1 27873.2 51055.9 31934.9 54980.7 32561.3 17770.5 11519.3 15365.5 25860.0 41359.6 46567.5 37963.2 21648.5 9850.6 4092.5 2019.3 1162.7 813.0 621.2 494.9 433.9 383.8 349.5 321.9 295.5 279.3 262.6 248.3 234.3 221.8 220.2 209.9 216.6 174.0 158.1 146.2 136.2 132.3 131.4 132.5"
    surf = pg.surface.Surface((500, 400))
    surf.fill("#000000")
    test_surf = graph_point(
        parse_data_line(test_data), 
        surf
    )