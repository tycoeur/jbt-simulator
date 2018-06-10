# -*- coding: utf-8 -*-
from models.coordinate_time_tuple import CoordinateTimeTuple
from models.note import Note
import re
from utils import processing_measure


@processing_measure.measure
def load(path):
    file = open(path, 'r')

    position_dict = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿口'
    arrow_dict = '∧Ｖ＜＞'
    time_dict = '|－'
    dicts = position_dict + arrow_dict + time_dict

    lines = [line for line in [re.sub('[^%s]' % dicts, '', line) for line in file.readlines()] if len(line) > 0]
    coordinate_time_tuples = [CoordinateTimeTuple(line[:4], re.sub('[%s]' % '|', '', line[4:])) for line in lines]

    times = []
    coordinates = []
    measures = []

    for coordinate_time_tuple in coordinate_time_tuples:
        coordinates.append(coordinate_time_tuple.coordinate)
        if len(coordinate_time_tuple.time) > 0:
            times.append(coordinate_time_tuple.time)
        if len(times) >= 4 and len(''.join(coordinates)) % 16 == 0:
            coordinate = ''.join(times).replace('－', '')
            time_dict = ''.join(coordinates).replace('口', '')
            diff = coordinate.translate(str.maketrans('', '', time_dict))
            if len(diff) <= 0:
                measures.append([''.join(list(coordinates)), list(times)])
                del times[:]
                del coordinates[:]

    total_time = 0
    bpm = 200
    notes = []
    for i, measure in enumerate(measures):
        coordinates = measure[0]
        times = measure[1]
        for time in times:
            for c in time:
                split_size = len(time)
                total_time += 60000.0 / bpm / split_size  # TODO 口⑤口口 |④－| の表記の対処法
                if c == '－':
                    continue
                notes.append(Note(c, total_time, [(i % 16) + 1 for i, x in enumerate(coordinates) if x == c], bpm))

    return notes
