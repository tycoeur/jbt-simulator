# -*- coding: utf-8 -*-
import math

from models.coordinate_time_tuple import CoordinateTimeTuple
from models.note import Note
import re
from utils import processing_measure


@processing_measure.measure
def fumen_load(path: str):
    position_dict = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿口'
    arrow_dict = '∧Ｖ＜＞'
    time_dict = '|－'
    dicts = position_dict + arrow_dict + time_dict

    coordinate_time_tuples: list[CoordinateTimeTuple] = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            line = re.sub(rf'[^{dicts}]', '', line)
            if line:
                coordinate: str = line[:4]
                time: str = re.sub(r'\|', '', line[4:])
                coordinate_time_tuples.append(CoordinateTimeTuple(coordinate, time))

    times: list[str] = []
    coordinates: list[str] = []
    measures: list[tuple[str, list[str]]] = []
    for coordinate_time_tuple in coordinate_time_tuples:
        coordinates.append(coordinate_time_tuple.coordinate)

        if coordinate_time_tuple.time:
            times.append(coordinate_time_tuple.time)

        if len(times) >= 4 and len(''.join(coordinates)) % 16 == 0:
            coordinate = ''.join(times).replace('－', '')
            time_dict = ''.join(coordinates).replace('口', '')
            diff = coordinate.translate(str.maketrans('', '', time_dict))
            if not diff:
                measures.append((''.join(coordinates), times))
                times = []
                coordinates = []

    offset = 80  # ms
    total_time = offset
    bpm = 200
    notes: list[Note] = []
    for measure in measures:
        _coordinates = measure[0]
        times = measure[1]
        for time in times:
            for c in time:
                split_size = len(time)
                total_time += 60000.0 / bpm / split_size  # TODO 口⑤口口 |④－| の表記の対処法
                if c == '－':
                    continue
                notes.append(Note(c, total_time, [(i % 16) + 1 for i, x in enumerate(_coordinates) if x == c], bpm))
    return notes, offset


def get_marker_frames(notes: list[Note], music_pos) -> list[tuple[list[int], int]]:
    """
    概要: music_pos を基準に，パネル座標とマーカーフレームとのセットの配列を返す．
    @param notes: ノーツデータの配列
    @param music_pos: 現在再生中の楽曲再生位置
    @return パネル座標とマーカーフレームとのセットの配列
            [([13], 24), ([6], 20), ([3, 12], 16), ([16], 8), ([15], 6), ([14], 3)]
    """
    MARKER_TIME_PER_FRAME = 36
    MARKER_FRAME = 25
    MARKER_TOTAL_TIME = MARKER_TIME_PER_FRAME * MARKER_FRAME

    within_notes = [(note.positions, int(math.floor((music_pos - note.t) / MARKER_TIME_PER_FRAME)))
                    for note in [note for note in notes if music_pos - MARKER_TOTAL_TIME < note.t <= music_pos]]

    return within_notes
