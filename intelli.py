#!/usr/bin/env python3
# File name: intelli.py
# Description: Automatic Analysis of IntelliCage data
# Author: Nicolas Ruffini
# Github: https://github.com/NiRuff/IntelliPy/
# Date: 12-03-2020

from os.path import dirname
import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
from pathlib import Path

import datetime

def np_calc_learning_rate_non_sucrose(df, path, phase, group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod=""):
    # create out path
    out_path = path + "/" + phase + "_nosepoke_learning_Data" + nameMod + ".xlsx"

    df["hourIntervall"] = df["StartTimecode"] // 3600

    # create df_licked with only those entries that were incorrect or correct and followed by a lick --> lickduration > 0
    df_temp = df[(df["SideCondition"] == "Incorrect") | (df["LickDuration"] > 0)]
    df_licked = df_temp.copy()

    df["CorrectNoLick"] = np.where((df["SideCondition"] == "Correct") & (df["LickDuration"] == 0), 1, 0)
    df["CorrectAndLick"] = np.where((df["SideCondition"] == "Correct") & (df["LickDuration"] > 0), 1, 0)

    df["NosepokePerAnimal"] = df.groupby("Animal")["VisitID"].expanding().count().reset_index(0)["VisitID"]
    df_licked["NosepokePerAnimal"] = df_licked.groupby("Animal")["VisitID"].expanding().count().reset_index(0)[
        "VisitID"]

    # code 1/0 for Correct, Sucrose and NotIncorrect
    df["Correct"] = np.where(df["SideCondition"] == "Correct", 1, 0)
    df_licked["Correct"] = np.where(df_licked["SideCondition"] == "Correct", 1, 0)

    # now sum it up
    df["cumCorrectNoLick"] = df.groupby("Animal")["CorrectNoLick"].expanding().sum().reset_index(0)["CorrectNoLick"]
    df["cumCorrectAndLick"] = df.groupby("Animal")["CorrectAndLick"].expanding().sum().reset_index(0)["CorrectAndLick"]
    df["cumCorrectNosepokes"] = df.groupby("Animal")["Correct"].expanding().sum().reset_index(0)["Correct"]
    df["cumNosepokes"] = df.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)["NosepokePerAnimal"]
    df_licked["cumCorrectNosepokes"] = df_licked.groupby("Animal")["Correct"].expanding().sum().reset_index(0)["Correct"]
    df_licked["cumNosepokes"] = df_licked.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)["NosepokePerAnimal"]

    df["cumCorrectNosepokesRate"] = df["cumCorrectNosepokes"] / df["cumNosepokes"]
    df["cumCorrectNoLickRate"] = df["cumCorrectNoLick"] / df["cumNosepokes"]
    df["cumCorrectAndLickRate"] = df["cumCorrectAndLick"] / df["cumNosepokes"]
    df_licked["cumCorrectNosepokesRate"] = df_licked["cumCorrectNosepokes"] / df_licked["cumNosepokes"]

    # fill with previous value
    df_filled = df.copy()
    df_filled.fillna(method="ffill", inplace=True)
    df_hour = df_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")

    df_licked_filled = df_licked.copy()
    df_licked_filled.fillna(method="ffill", inplace=True)
    df_licked_hour = df_licked_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")

    df_pivotHourCorrect = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectNosepokesRate")
    df_pivotHourCorrect.fillna(method="ffill", inplace=True)

    df_licked_pivotHourCorrect = df_licked_hour.pivot(index="hourIntervall", columns="Animal",
                                                      values="cumCorrectNosepokesRate")
    df_licked_pivotHourCorrect.fillna(method="ffill", inplace=True)

    df_pivotNosepokeCorrect = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectNosepokesRate")
    df_pivotNosepokeCorrect.fillna(method="ffill", inplace=True)

    df_licked_pivotNosepokeCorrect = df_licked.pivot(index="NosepokePerAnimal", columns="Animal",
                                                     values="cumCorrectNosepokesRate")
    df_licked_pivotNosepokeCorrect.fillna(method="ffill", inplace=True)

    df_pivotNPCorrectNoLick = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectNoLickRate")
    df_pivotNPCorrectNoLick.fillna(method="ffill", inplace=True)

    df_pivotHourCorrectNoLick = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectNoLickRate")
    df_pivotHourCorrectNoLick.fillna(method="ffill", inplace=True)

    df_pivotNPCorrectAndLick = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectAndLickRate")
    df_pivotNPCorrectAndLick.fillna(method="ffill", inplace=True)

    df_pivotHourCorrectAndLick = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectAndLickRate")
    df_pivotHourCorrectAndLick.fillna(method="ffill", inplace=True)

    df_licked_pivotNosepokeCorrect_transposed = df_licked_pivotNosepokeCorrect.transpose()
    df_licked_pivotHourCorrect_transposed = df_licked_pivotHourCorrect.transpose()
    df_pivotNosepokeCorrect_transposed = df_pivotNosepokeCorrect.transpose()
    df_pivotHourCorrect_transposed = df_pivotHourCorrect.transpose()
    df_pivotNPCorrectNoLick_transposed = df_pivotNPCorrectNoLick.transpose()
    df_pivotHourCorrectNoLick_transposed = df_pivotHourCorrectNoLick.transpose()
    df_pivotNPCorrectAndLick_transposed = df_pivotNPCorrectAndLick.transpose()
    df_pivotHourCorrectAndLick_transposed = df_pivotHourCorrectAndLick.transpose()

    all_dfs = [df_licked_pivotNosepokeCorrect_transposed, df_licked_pivotHourCorrect_transposed,
               df_pivotNosepokeCorrect_transposed, df_pivotHourCorrect_transposed, df_pivotNPCorrectNoLick_transposed,
               df_pivotHourCorrectNoLick_transposed, df_pivotNPCorrectAndLick_transposed, df_pivotHourCorrectAndLick_transposed]

    for curr_df in all_dfs:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.reindex(animals).mean()

    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df_pivotNosepokeCorrect_transposed.to_excel(writer, sheet_name="CorrectNosepokeRate", startrow=0, startcol=0)
    df_pivotHourCorrect_transposed.to_excel(writer, sheet_name="CorrectNosepokeRateHour", startrow=0, startcol=0)
    if no_lick_ex:
        df_licked_pivotNosepokeCorrect_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickEx", startrow=0,
                                                       startcol=0)
        df_licked_pivotHourCorrect_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickEx_hour", startrow=0,
                                                   startcol=0)
    if no_lick_rem:
        df_pivotNPCorrectAndLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickIncorr", startrow=0,
                                                       startcol=0)
        df_pivotHourCorrectAndLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickIncorrHour", startrow=0,
                                                       startcol=0)
    if no_lick_only:
        df_pivotNPCorrectNoLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickOnly", startrow=0,
                                                      startcol=0)
        df_pivotHourCorrectNoLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickOnlyHour", startrow=0,
                                                      startcol=0)

    sheets = ["CorrectNosepokeRate", "CorrectNosepokeRateHour"]
    if no_lick_ex:
        sheets.extend(["CorrNPRate_NoLickEx", "CorrNPRate_NoLickEx_hour"])
    if no_lick_rem:
        sheets.extend(["CorrNPRate_NoLickIncorr", "CorrNPRate_NoLickIncorrHour"])
    if no_lick_only:
        sheets.extend(["CorrNPRate_NoLickOnly", "CorrNPRate_NoLickOnlyHour"])


    tables = [df_pivotNosepokeCorrect_transposed, df_pivotHourCorrect_transposed]
    if no_lick_ex:
        tables.extend([df_licked_pivotNosepokeCorrect_transposed, df_licked_pivotHourCorrect_transposed])
    if no_lick_rem:
        tables.extend([df_pivotNPCorrectAndLick_transposed, df_pivotHourCorrectAndLick_transposed])
    if no_lick_only:
        tables.extend([df_pivotNPCorrectNoLick_transposed, df_pivotHourCorrectNoLick_transposed])


    for i in range(len(sheets)):
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]

        # Create a chart object
        chart = workbook.add_chart({'type': 'line'})

        # Configure the series of the chart from the dataframe data
        for j in range(len(tables[i].index) - len(group_dict)):
            row = j + 1
            chart.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, 1, 0, len(tables[i].index) - len(group_dict)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })

        worksheet.insert_chart('A35', chart)
        chart2 = workbook.add_chart({'type': 'line'})

        for j in range(len(tables[i].index) - len(group_dict), len(tables[i].index)):
            row = j + 1
            chart2.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, len(tables[i].index) - len(group_dict), 0, len(tables[i].index)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })
        worksheet.insert_chart('M35', chart2)
    writer.save()
    print(out_path + " written")

def np_calc_learning_rate_sucrose(df, path, group_dict, no_lick_ex, no_lick_rem, no_lick_only, water_y_suc_n, water_y_suc_y, water_n_suc_y, sucrose_label):

    if water_y_suc_n:
        df_yn = df.copy()
        df_yn["SideCondition"] = df_yn["SideCondition"].replace([sucrose_label], "Incorrect")
        np_calc_learning_rate_non_sucrose(df_yn, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_OnlyWaterCorrect")
    if water_y_suc_y:
        df_yy = df.copy()
        df_yy["SideCondition"] = df_yy["SideCondition"].replace([sucrose_label], "Correct")
        np_calc_learning_rate_non_sucrose(df_yy, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_WaterSucroseCorrect")
    if water_n_suc_y:
        df_ny = df.copy()
        df_ny["SideCondition"] = df_ny["SideCondition"].replace(["Correct"], "Incorrect")
        df_ny["SideCondition"] = df_ny["SideCondition"].replace([sucrose_label], "Correct")
        np_calc_learning_rate_non_sucrose(df_ny, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_OnlySucroseCorrect")

    # create out path
    out_path = path + "/Sucrose_Preference_nosepoke_learning_Data.xlsx"

    df["hourIntervall"] = df["StartTimecode"] // 3600
    df["NosepokePerAnimal"] = df.groupby("Animal")["VisitID"].expanding().count().reset_index(0)["VisitID"]

    # now sum it up
    df["cumulativeLickDuration"] = df.groupby("Animal")["LickDuration"].expanding().sum().reset_index(0)["LickDuration"]
    df["cumNosepokes"] = df.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)[
        "NosepokePerAnimal"]

    df["cumulativeLickDurationSucrose"] = \
    df[df["SideCondition"] == sucrose_label].groupby("Animal")["LickDuration"].expanding().sum().reset_index(0)[
        "LickDuration"]

    # set all first ratios per Animal to 0
    df.loc[df.groupby('Animal', as_index=False).head(1).index, 'sucrosePerTotalLickduration'] = 0
    df.loc[df.groupby('Animal', as_index=False).head(1).index, 'cumulativeLickDurationSucrose'] = 0
    df["cumulativeLickDurationSucrose"].fillna(method="ffill", inplace=True)

    df["sucrosePerTotalLickduration"] = df["cumulativeLickDurationSucrose"] / df["cumulativeLickDuration"]

    df_l = df[df["LickDuration"] > 0].copy()
    df_l["LickDurIndex"] = df_l.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)[
        "NosepokePerAnimal"]
    df_pivot = df_l.pivot(index="LickDurIndex", columns="Animal", values="sucrosePerTotalLickduration")

    # fill with previous value
    df_pivot.fillna(method="ffill", inplace=True)
    df_filled = df.copy()
    df_filled.fillna(method="ffill", inplace=True)
    df_hour = df_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")
    df_pivotHour = df_hour.pivot(index="hourIntervall", columns="Animal", values="sucrosePerTotalLickduration")
    df_pivotHour.fillna(method="ffill", inplace=True)


    # LickDuration
    df_pivot_transposed = df_pivot.transpose()
    df_pivotHour_transposed = df_pivotHour.transpose()

    all_dfs = [df_pivot_transposed, df_pivotHour_transposed]

    for curr_df in all_dfs:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.loc[animals].mean()


    out_path = path + "/Sucrose_Preference_sucroseRate.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')

    df_pivot_transposed.to_excel(writer, sheet_name="SucroseLickDurationRatioPerNP")
    df_pivotHour_transposed.to_excel(writer, sheet_name="SucroseLickDurationRatioPerHour")

    sheets = ["SucroseLickDurationRatioPerNP", "SucroseLickDurationRatioPerHour"]
    tables = [df_pivot_transposed, df_pivotHour_transposed]

    for i in range(len(sheets)):
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]

        # Create a chart object
        chart = workbook.add_chart({'type': 'line'})

        # 1 Configure the series of the chart from the dataframe data
        for j in range(len(tables[i].index) - len(group_dict)):
            row = j + 1
            chart.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, 1, 0, len(tables[i].index) - len(group_dict)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })

        worksheet.insert_chart('A35', chart)
        chart2 = workbook.add_chart({'type': 'line'})

        for j in range(len(tables[i].index) - len(group_dict), len(tables[i].index)):
            row = j + 1
            chart2.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, len(tables[i].index) - len(group_dict), 0, len(tables[i].index)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })
        worksheet.insert_chart('M35', chart2)

    writer.save()
    print(out_path + " written")

def vis_calc_learning_rate(df, path, phase, group_dict):


    # define intervalls
    df["hourIntervall"] = df["StartTimecode"] // 3600

    # group and sum per animal
    df["totalNosepokes"] = df.groupby("Animal")["NosepokeNumber"].expanding().sum().reset_index(0)["NosepokeNumber"]
    df["totalSideErrors"] = df.groupby("Animal")["SideErrors"].expanding().sum().reset_index(0)["SideErrors"]
    df["totalPlaceErrors"] = df.groupby("Animal")["PlaceError"].expanding().sum().reset_index(0)["PlaceError"]
    df["totalVisits"] = df.groupby("Animal")["VisitOrder"].expanding().count().reset_index(0)["VisitOrder"]

    # calculate SideErrorRate and learningRate
    df["cumSideErrorRate"] = df["totalSideErrors"] / df["totalNosepokes"]
    df["cumPlaceErrorRate"] = df["totalPlaceErrors"] / df["totalVisits"]
    df["correctSidePerNosepoke"] = 1 - df["cumSideErrorRate"]
    df["correctPlacePerVisit"] = 1 - df["cumPlaceErrorRate"]

    # pivot tables per visit
    df_pi_visit_SE = df.pivot(index="VisitOrder", columns="Animal", values="correctSidePerNosepoke")
    df_pi_visit_PE = df.pivot(index="VisitOrder", columns="Animal", values="correctPlacePerVisit")
    df_hour = df.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")

    # pivot tables per hour
    df_pi_hour_SE = df_hour.pivot(index="hourIntervall", columns="Animal", values="correctSidePerNosepoke")
    df_pi_hour_PE = df_hour.pivot(index="hourIntervall", columns="Animal", values="correctPlacePerVisit")

    # impute missing values
    df_pi_visit_SE.fillna(method="ffill", inplace=True)
    df_pi_hour_SE.fillna(method="ffill", inplace=True)
    df_pi_visit_PE.fillna(method="ffill", inplace=True)
    df_pi_hour_PE.fillna(method="ffill", inplace=True)

    # create transposed datasets
    df_pi_visit_SE_transposed = df_pi_visit_SE.transpose()
    df_pi_hour_SE_transposed = df_pi_hour_SE.transpose()
    df_pi_visit_PE_transposed = df_pi_visit_PE.transpose()
    df_pi_hour_PE_transposed = df_pi_hour_PE.transpose()

    all_dfs = [df_pi_visit_SE_transposed, df_pi_hour_SE_transposed, df_pi_visit_PE_transposed,
               df_pi_hour_PE_transposed]



    for curr_df in all_dfs:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.loc[animals].mean()

    # create out path
    out_path = path + "/" + phase + "_visit_learning_Data.xlsx"

    # write files
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df_pi_visit_SE_transposed.to_excel(writer, sheet_name="correctSidePerNosepoke", startrow=0, startcol=0)
    df_pi_hour_SE_transposed.to_excel(writer, sheet_name="correctSidePerNosepokeHour", startrow=0, startcol=0)
    df_pi_visit_PE_transposed.to_excel(writer, sheet_name="correctPlacePerVisit", startrow=0, startcol=0)
    df_pi_hour_PE_transposed.to_excel(writer, sheet_name="correctPlacePerVisitHour", startrow=0, startcol=0)

    sheets = ["correctSidePerNosepoke", "correctSidePerNosepokeHour", "correctPlacePerVisit",
              "correctPlacePerVisitHour"]
    tables = [df_pi_visit_SE_transposed, df_pi_hour_SE_transposed, df_pi_visit_PE_transposed,
              df_pi_hour_PE_transposed]

    for i in range(len(sheets)):
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]

        # Create a chart object
        chart = workbook.add_chart({'type': 'line'})

        # Configure the series of the chart from the dataframe data
        for j in range(len(tables[i].index) - len(group_dict)):
            row = j + 1
            chart.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, 1, 0, len(tables[i].index) - len(group_dict)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })

        worksheet.insert_chart('A35', chart)
        chart2 = workbook.add_chart({'type': 'line'})

        for j in range(len(tables[i].index) - len(group_dict), len(tables[i].index)):
            row = j + 1
            chart2.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, len(tables[i].index) - len(group_dict), 0, len(tables[i].index)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })
        worksheet.insert_chart('M35', chart2)
    writer.save()
    print(out_path + " written")

def vis_calc_pivot(df, path, phase, group_dict, hour_intervals = []):

    times = ["StartDate"]
    for entry in hour_intervals:
        col_name = str(int(entry)) + "_hourIntervall"
        df[col_name] = df["StartTimecode"]//(3600*int(entry))
        times.append(col_name)

    #df["6_hourIntervall"] = df["StartTimecode"]//(3600*6)
    #df["12_hourIntervall"] = df["StartTimecode"]//(3600*12)

    values = ["LickDuration", "LickNumber", "NosepokeDuration", "NosepokeNumber"]
    #times = ["StartDate", "12_hourIntervall", "6_hourIntervall"]

    df_pivot_list = list()
    sheets = list()
    ori_col_names = []

    for value in values:
        for time in times:
            df_pivot_list.append(df.pivot_table(columns=time, index="Animal", values=value, aggfunc=np.sum))
            if time == "StartDate":
                sheets.append(value + "_" + "24h")
                ori_col_names.append(time)
            else:
                sheets.append(value + time.replace("_hourIntervall", "h"))
                ori_col_names.append(time)

    for curr_df in df_pivot_list:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.loc[animals].mean()

    # create out path
    out_path = path + "/" + phase + "_pivot_Data.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')

    # write df as csv to directory
    df.to_csv( path + "/" + phase + "data.csv")

    for i in range(len(sheets)):

        df_pivot_list[i].to_excel(writer, sheet_name=sheets[i], startrow=0 , startcol=0)
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]


        # if only one value per interval, insert bins instead of line chart
        # work with ori_col_names

        if (df[ori_col_names[i]].nunique() == 1):
            # Create a chart object
            chart = workbook.add_chart({'type': 'column'})

            # Configure the series of the chart from the dataframe data
            for j in range(len(df_pivot_list[i].index) - len(group_dict)):
                row = j + 1
                chart.add_series({
                    'name': [sheets[i], row, 0],
                    'categories': [sheets[i], 0, 1, 0, len(df_pivot_list[i].index) - len(group_dict)],
                    'values': [sheets[i], row, 1, row, len(df_pivot_list[i].columns) + 1],
                })
        else:
            # Create a chart object
            chart = workbook.add_chart({'type': 'line'})

            # Configure the series of the chart from the dataframe data
            for j in range(len(df_pivot_list[i].index)-len(group_dict)):
                row = j + 1
                chart.add_series({
                    'name':       [sheets[i], row, 0],
                    'categories': [sheets[i], 0, 1, 0, len(df_pivot_list[i].index)-len(group_dict)],
                    'values':     [sheets[i], row, 1, row, len(df_pivot_list[i].columns)+1],
                })

        worksheet.insert_chart('A35', chart)

        if (df[ori_col_names[i]].nunique() == 1):
            chart2 = workbook.add_chart({'type': 'column'})
            for j in range(len(df_pivot_list[i].index)-len(group_dict), len(df_pivot_list[i].index)):
                row = j + 1
                chart2.add_series({
                    'name':       [sheets[i], row, 0],
                    'categories': [sheets[i], 0, 1, 0, len(df_pivot_list[i].index)],
                    'values':     [sheets[i], row, 1, row, len(df_pivot_list[i].columns)+1],
                })
            worksheet.insert_chart('M35', chart2)

        else:
            chart2 = workbook.add_chart({'type': 'line'})
            for j in range(len(df_pivot_list[i].index)-len(group_dict), len(df_pivot_list[i].index)):
                row = j + 1
                chart2.add_series({
                    'name':       [sheets[i], row, 0],
                    'categories': [sheets[i], 0, 1, 0, len(df_pivot_list[i].index)],
                    'values':     [sheets[i], row, 1, row, len(df_pivot_list[i].columns)+1],
                })
            worksheet.insert_chart('M35', chart2)

    writer.save()
    print(out_path + " written")

def main():

    master = tk.Tk()

    curr_datetime = datetime.datetime.now()

    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()

    # show an "Open" dialog box and return the path to the selected file
    nosepoke_file = askopenfilename(title="Select Nosepoke.txt", filetypes=[("Nosepoke file", "*.txt")])
    visit_file = askopenfilename(title="Select Visit.txt", filetypes=[("Visit file", "*.txt")])
    group_assignment_file = askopenfilename(title="Select Group Assignment file", filetypes=[("Group Assignment file", "*.txt")])

    # create dataframe for nosepoke and for visit file
    df_nosepoke = pd.read_csv(nosepoke_file, sep="\t")
    df_visit = pd.read_csv(visit_file, sep="\t")
    print(df_visit.columns)


    # get all phases out of Visit file:
    # if a phase occurs more than one time, it will be catched here and renamed in phase_x_1 and phase_x_2
    phases = df_visit.Module[(df_visit.Module != df_visit.Module.shift()) & (df_visit.Animal == df_visit.Animal.iloc[0])].values

    # add suffix to phases - if element appears > 1 time in whole list,
    # append suffix giving the number of times this phase appeared in slice of list
    p = list(phases)
    phases_temp = list()
    for i in range(len(p)):
        if p.count(p[i]) > 1:
            phases_temp.append(p[i] + "_" + str(p[:i+1].count(p[i])))
        else:
            phases_temp.append(p[i])


    with open(group_assignment_file) as f:
        label = f.readline()
        content = f.readlines()
    group_dict = dict()
    for line in content:
        entries = line.strip().split("\t")
        group_dict.update({entries[0]: entries[1:]})

    # read out sucrose label
    if label.split("\t")[0] != "Label":
        print("Did you enter label in your group assignment file?")
    sucrose_label = label.split("\t")[1].strip()

    print(sucrose_label)

    # create analysis directory and a subdirectory for every phase
    analysis_dir = dirname(nosepoke_file) + "_IntelliPy_Analysis_" + curr_datetime.strftime('%Y_%m_%d')
    Path(analysis_dir).mkdir(parents=True, exist_ok=True)

    for curr_phase in phases_temp:
        Path(analysis_dir + "/" + curr_phase).mkdir(parents=True, exist_ok=True)

    # iterate over all phases, create phase-dataframe and apply functionality
    # ! phases are defined in Visit.txt - slice by ModuleName in Visit.txt and take
    # its min and max VisitId to define for nosepoke file
    # the StartTimecode and EndTimecode have to be adjusted like this:
    # Timecode = Timecode - StartDate
    # So that the Timecode is relative to the phase start

    # get first date overall and subtract from first date per phase later
    # combine first date and time
    first_datetime = df_visit.loc[0, ["StartDate"]].values.item() + " " + df_visit.loc[0, ["StartTime"]].values.item()
    first_datetime_total = datetime.datetime.strptime(first_datetime, '%Y-%m-%d %H:%M:%S.%f')

    # subtract milliseconds of first entry
    millisecond_correction = df_visit.loc[0, ["StartTimecode"]].values.item()
    tdelta = datetime.timedelta(seconds=millisecond_correction)

    experiment_start = first_datetime_total - tdelta

    master.title("Experiment Phases")

    entries = list()
    startdates = list()

    # get startdates of all phases even if a phases occurs multiple times
    # by slicing the dataframe by the old_phase
    for i in range(len(phases)):
        if i > 0:
            old_phase = phases[i-1]
            entries.append(tk.Entry(master, width=60))
            tk.Label(master, text=phases_temp[i]).grid(row=i)
            slice_start = df_visit.loc[df_visit.Module == old_phase, "Module"].index[0]
            slice_df_visit = df_visit.iloc[slice_start:]
            startdates.append(slice_df_visit[slice_df_visit.Module == phases[i]]["StartDate"].iloc[0])
        else:
            entries.append(tk.Entry(master, width=60))
            tk.Label(master, text=phases_temp[i]).grid(row=i)
            startdates.append(df_visit[df_visit.Module == phases[i]]["StartDate"].iloc[0])
    print(startdates)

    i = 0
    for entry in entries:
        if i == 0:
            entry.insert(10, experiment_start)
        else:
            entry.insert(10, startdates[i] + " 00:00:00.000")
        entry.grid(row=i, column=1)
        i += 1

    no_lick_ex = tk.IntVar()
    tk.Checkbutton(master, text="exclude Nosepokes without lick", variable=no_lick_ex).grid(row=0, column=2, sticky=tk.W)
    no_lick_rem = tk.IntVar()
    tk.Checkbutton(master, text="treat Nosepokes without lick as incorrect", variable=no_lick_rem).grid(row=1, column=2, sticky=tk.W)
    no_lick_only = tk.IntVar()
    tk.Checkbutton(master, text="show Nosepokes without lick per animal/group", variable=no_lick_only).grid(row=2, column=2, sticky=tk.W)
    water_y_suc_n = tk.IntVar(value=1)
    tk.Checkbutton(master, text="Water: Correct, Sucrose: Incorrect", variable=water_y_suc_n).grid(row=3, column=2, sticky=tk.W)
    water_y_suc_y = tk.IntVar()
    tk.Checkbutton(master, text="Water: Correct, Sucrose: Correct", variable=water_y_suc_y).grid(row=4, column=2, sticky=tk.W)
    water_n_suc_y = tk.IntVar()
    tk.Checkbutton(master, text="Water: Incorrect, Sucrose: Correct", variable=water_n_suc_y).grid(row=5, column=2, sticky=tk.W)

    tk.Button(master,
              text='Submit',
              command=master.quit).grid(row=6,
                                        column=2,
                                        sticky=tk.W,
                                        pady=4)
    added_hour_intervalls = []

    def addHourInterval():
        e = tk.Entry(master)
        e.grid(sticky=tk.W, column=1, row=len(entries)+3+len(added_hour_intervalls))
        added_hour_intervalls.append(e)

    tk.Button(master,
              text='Add hour intervalls',
              command=addHourInterval).grid(row=len(entries)+1,
                                        column=1,
                                        sticky=tk.W,
                                        pady=4)

    tk.Label(master, text='Hour intervalls').grid(row=len(entries)+2,
                                        column=1,
                                        sticky=tk.W,
                                        pady=4)

    tk.mainloop()

    added_timeframes = pd.DataFrame(["00:00:00.000", "23:59:59.999"], columns=["times"])
    added_timeframes["times"] = pd.to_datetime(added_timeframes["times"], format='%H:%M:%S.%f').dt.time
    tf_start = added_timeframes.iloc[0,0]
    tf_end = added_timeframes.iloc[1,0]



    phase_datetimes = list()
    for entry in entries:
        phase_datetimes.append(datetime.datetime.strptime(entry.get(), '%Y-%m-%d %H:%M:%S.%f'))
    print(phase_datetimes)

    hour_intervals = []
    for e in added_hour_intervalls:
        hour_intervals.append(e.get())

    # create StartTimeEdit column for applying time frame
    df_visit["StartTimeEdit"] = pd.to_datetime(df_visit["StartTime"], format='%H:%M:%S.%f').dt.time
    print(len(df_visit))

    # apply time frame:
    df_visit = df_visit[(df_visit["StartTimeEdit"] >= tf_start) & (df_visit["StartTimeEdit"] <= tf_end)]
    print(len(df_visit))

    # create columns for StartDateTime and EndDateTime
    df_visit.loc[:, "StartDateTime"] = pd.to_datetime(df_visit["StartDate"] + " " + df_visit["StartTime"], format='%Y-%m-%d %H:%M:%S.%f')
    df_visit.loc[:, "EndDateTime"] = pd.to_datetime(df_visit["EndDate"] + " " + df_visit["EndTime"], format='%Y-%m-%d %H:%M:%S.%f')

    df_nosepoke.loc[:, "StartDateTime"] = pd.to_datetime(df_nosepoke["StartDate"] + " " + df_nosepoke["StartTime"], format='%Y-%m-%d %H:%M:%S.%f')
    df_nosepoke.loc[:, "EndDateTime"] = pd.to_datetime(df_nosepoke["EndDate"] + " " + df_nosepoke["EndTime"], format='%Y-%m-%d %H:%M:%S.%f')

    # insert column for "Module" in df_nosepoke
    df_nosepoke["Module"] = pd.np.nan
    for i in range(len(phase_datetimes)):
        if i == len(phase_datetimes)-1:
            df_nosepoke.loc[df_nosepoke["StartDateTime"] >= phase_datetimes[i], "Module"] = phases[i]
        elif i > 0:
            df_nosepoke.loc[(df_nosepoke["StartDateTime"] < phase_datetimes[i+1]) & (df_nosepoke["StartDateTime"] > phase_datetimes[i]), "Module"] = phases[i]
        else:
            df_nosepoke.loc[df_nosepoke["StartDateTime"] < phase_datetimes[i+1], "Module"] = phases[i]

    if df_nosepoke["Module"].isnull().values.any():
        print("Warning, some rows did not get a module assignment")

    # for sanity check
    total_visit_rows = 0
    total_nosepoke_rows = 0

    i = 0
    for j in range(len(phases)):
        # reduce by module
        curr_visit_df_module = df_visit.loc[df_visit["Module"] == phases[j]]

        # further reduce by time - if module appears multiple times, check for start of next module so that
        # > now and < later can assure no duplicate counting of later modules values

        if i+1 < len(phase_datetimes):
            curr_visit_df = curr_visit_df_module.loc[(curr_visit_df_module["StartDateTime"] >= phase_datetimes[i]) & (curr_visit_df_module["StartDateTime"] < phase_datetimes[i+1])]
        else:
            curr_visit_df = curr_visit_df_module.loc[curr_visit_df_module["StartDateTime"] >= phase_datetimes[i]]

        # add visitOrder for curr_visit
        curr_visit_df.loc[:, "VisitOrder"] = curr_visit_df.groupby("Animal")["VisitOrder"].expanding().count().reset_index(0)["VisitOrder"]

        # reset timecode
        curr_visit_df.loc[:, ["StartTimecode"]] = (curr_visit_df["StartDateTime"] - phase_datetimes[i]).dt.total_seconds()
        curr_visit_df.loc[:, ["EndTimecode"]] = (curr_visit_df["EndDateTime"] - phase_datetimes[i]).dt.total_seconds()

        min_visit_id = curr_visit_df["VisitID"].min()
        max_visit_id = curr_visit_df["VisitID"].max()

        # create curr_nosepoke_df from visitIDs
        curr_nosepoke_df = df_nosepoke.loc[(df_nosepoke["VisitID"] >= min_visit_id) & (df_nosepoke["VisitID"] <= max_visit_id)]

        # reset timecode
        curr_nosepoke_df.loc[:, ["StartTimecode"]] = (curr_nosepoke_df["StartDateTime"] - phase_datetimes[i]).dt.total_seconds()
        curr_nosepoke_df.loc[:, ["EndTimecode"]] = (curr_nosepoke_df["EndDateTime"] - phase_datetimes[i]).dt.total_seconds()

        if curr_visit_df.empty:
            print(phases[j], "visit skipped")
        else:
            vis_calc_learning_rate(curr_visit_df.copy(), path=analysis_dir + "/" + phases_temp[j], phase=phases[j], group_dict=group_dict)
            vis_calc_pivot(curr_visit_df.copy(), path=analysis_dir + "/" + phases_temp[j], phase=phases[j], group_dict=group_dict,
                           hour_intervals=hour_intervals)

        if curr_nosepoke_df.empty:
            print(phases[j], "Nosepoke skipped")
        else:
            if phases[i] == "SucrosePreference":
                np_calc_learning_rate_sucrose(curr_nosepoke_df.copy(), path=analysis_dir + "/" + phases_temp[j],
                                              group_dict=group_dict, no_lick_ex=no_lick_ex.get(), no_lick_rem=no_lick_rem.get(),
                                              no_lick_only=no_lick_only.get(), water_y_suc_n=water_y_suc_n.get(),
                                              water_y_suc_y=water_y_suc_y.get(), water_n_suc_y=water_n_suc_y.get(),
                                              sucrose_label=sucrose_label)
            else:
                np_calc_learning_rate_non_sucrose(curr_nosepoke_df.copy(), path=analysis_dir + "/" + phases_temp[j],
                                                  phase=phases[j], group_dict=group_dict, no_lick_ex=no_lick_ex.get(), no_lick_rem=no_lick_rem.get(),
                                                  no_lick_only=no_lick_only.get())

        total_visit_rows += len(curr_visit_df.index)
        total_nosepoke_rows += len(curr_nosepoke_df.index)
        i += 1

    with open(analysis_dir + "/" + "log.txt", "w") as log:
        if total_visit_rows != len(df_visit.index):
            print("!Visit row number not matching!" + str(total_visit_rows) + "\t" + str(len(df_visit.index)) + "\n")
            log.write("!Visit row number not matching!" + str(total_visit_rows) + "\t" + str(len(df_visit.index)) + "\n")
        else:
            log.write("!Visit row number matching! :)" + str(total_visit_rows) + "\t" + str(len(df_visit.index)) + "\n")
        if total_nosepoke_rows != len(df_nosepoke.index):
            print("!Nosepoke row number not matching!" + str(total_nosepoke_rows) + "\t" + str(len(df_nosepoke.index)) + "\n")
            log.write("!Nosepoke row number not matching!" + str(total_nosepoke_rows) + "\t" + str(len(df_nosepoke.index)) + "\n")
        else:
            log.write("!Nosepoke row number matching! :)" + str(total_nosepoke_rows) + "\t" + str(len(df_nosepoke.index)) + "\n")

        log.write("Nosepoke file:\t" + nosepoke_file + "\n")
        log.write("Visit file:\t" + visit_file + "\n")
        log.write("Group_Assignment file:\t" + group_assignment_file + "\n")

        log.write("\nPhase\tTime\n")
        for phase, time in zip(phases_temp, entries):
            log.write(phase + "\t" + str(time.get()) + "\n")

        log.write("\nAdded hour intervals\n")
        for interval in hour_intervals:
            log.write(str(interval) + "\n")

        log.write("\nOptions\n")
        log.write("exclude Nosepokes without lick:\t" + str(no_lick_ex.get()) + "\n")
        log.write("treat Nosepokes without lick as incorrect\t" + str(no_lick_rem.get()) + "\n")
        log.write("show Nosepokes without lick per animal/group:\t" + str(no_lick_only.get()) + "\n")
        log.write("Water: Correct, Sucrose: Incorrect:\t" + str(water_y_suc_n.get()) + "\n")
        log.write("Water: Correct, Sucrose: Correct:\t" + str(water_y_suc_y.get()) + "\n")
        log.write("Water: Incorrect, Sucrose: Correct:\t" + str(water_n_suc_y.get()) + "\n")

    print("Press any key to close")
    input()

    master.destroy()

if __name__ == '__main__':
    try:
        main()
    except:
        print("Press any key to close")
        input()
