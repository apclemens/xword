# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import math, random


class Puzzle(models.Model):
    title = models.CharField(max_length=100)
    size = models.IntegerField()
    puzzle_text = models.CharField(max_length=30*30)
    UUID = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Clue(models.Model):
    clue_text = models.CharField(max_length=100)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    start_num = models.IntegerField()
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    direction = models.CharField(max_length=1)  # "A" for across, "D" for down
    answer = models.CharField(max_length=25)


class Word(models.Model):
    word = models.CharField(max_length=25)
    help_text = models.CharField(max_length=500)

    def __str__(self):
        return self.word


def random_UUID():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    UUID = ''.join([random.choice(chars) for i in range(5)])
    return UUID


def assign_UUID():
    existing_UUIDs = [p.UUID for p in Puzzle.objects.all()]
    UUID = random_UUID()
    while UUID in existing_UUIDs:
        UUID = random_UUID()
    return UUID


def manual_puzzle_add():
    title = raw_input('Name of puzzle: ')
    size = input('Puzzle size: ')
    print 'Input each line of the puzzle'
    puzzle_array = [raw_input() for i in range(size)]
    puzzle = Puzzle(title=title, size=size, puzzle_text=''.join(puzzle_array))
    puzzle.save()
    start_locations = get_start_locations(puzzle_array)
    print 'We will now get the across clues: '
    for iAll in start_locations:
        i = iAll[0]
        if i[-1] == 'D':
            continue
        clue_text = raw_input(i[:-1])
        clue = Clue(clue_text=clue_text,
                    puzzle=puzzle,
                    start_num=int(i[:-1]),
                    direction='A',
                    start_x=iAll[1],
                    start_y=iAll[2],
                    answer=iAll[3])
        clue.save()
    print 'We will now get the down clues: '
    for iAll in start_locations:
        i = iAll[0]
        if i[-1] == 'A':
            continue
        clue_text = raw_input(i[:-1])
        clue = Clue(clue_text=clue_text,
                    puzzle=puzzle,
                    start_num=int(i[:-1]),
                    direction='D',
                    start_x=iAll[1],
                    start_y=iAll[2],
                    answer=iAll[3])
        clue.save()


def id_clue(clues, i_all):
    cell1 = str(i_all[1])+','+str(i_all[2])
    if i_all[0][-1] == 'D':
        cell2 = str(i_all[1]+1)+','+str(i_all[2])
    else:
        cell2 = str(i_all[1])+','+str(i_all[2]+1)
    to_find = cell1+'-'+cell2
    for c in clues.keys():
        if to_find in c:
            return c
    return None


def publish_puzzle(title, template, clues):
    size = int(math.sqrt(len(template)))
    puzzle_array = [template[i*size:(i+1)*size] for i in range(size)]
    puzzle = Puzzle(title=title, size=size, puzzle_text=template, UUID=assign_UUID())
    puzzle.save()
    start_locations = get_start_locations(puzzle_array)
    for iAll in start_locations:
        i = iAll[0]
        clue_text = clues[id_clue(clues, iAll)]
        clue = Clue(clue_text=clue_text,
                    puzzle=puzzle,
                    start_num=int(i[:-1]),
                    direction=iAll[0][-1],
                    start_x=iAll[1],
                    start_y=iAll[2],
                    answer=iAll[3])
        clue.save()
    return puzzle.UUID


def get_start_locations(template):
    start_cells_notation = []
    cell = 1
    c = False
    for i in range(len(template)):
        for j in range(len(template[0])):
            if template[i][j] == ' ':
                continue
            if c:
                cell += 1
            c = False
            if i == 0:
                start_cells_notation.append([str(cell)+'D', i, j, getDownCells(template, (i, j))])
                c = True
            elif template[i-1][j] == ' ':
                start_cells_notation.append([str(cell)+'D', i, j, getDownCells(template, (i, j))])
                c = True
            if j == 0:
                start_cells_notation.append([str(cell)+'A', i, j, getAcrossCells(template, (i, j))])
                c = True
            elif template[i][j-1] == ' ':
                start_cells_notation.append([str(cell)+'A', i, j, getAcrossCells(template, (i, j))])
                c = True
    start_cells_notation.sort(key=lambda x: int(x[0][:-1]))
    return start_cells_notation


def getAcrossCells(template, acrossStart, asStr=False):
    cells = []
    i = (acrossStart[0], acrossStart[1])
    while i[1] != len(template[0]) and template[i[0]][i[1]] != ' ':
        if asStr:
            cells.append([str(j) for j in i])
        else:
            cells.append(template[i[0]][i[1]])
        i = (i[0], i[1]+1)
    return ''.join(cells)


def getDownCells(template, downStart, asStr=False):
    cells = []
    i = (downStart[0], downStart[1])
    while i[0] != len(template) and template[i[0]][i[1]] != ' ':
        if asStr:
            cells.append([str(j) for j in i])
        else:
            cells.append(template[i[0]][i[1]])
        i = (i[0]+1, i[1])
    return ''.join(cells)


def build_puzzle_js(puzzle_id):
    puzzle = Puzzle.objects.get(UUID=puzzle_id)
    clues = Clue.objects.filter(puzzle=puzzle)
    to_write = ['{']
    to_write.append('  "title": "'+puzzle.title+'",')
    to_write.append('  "by": "By Line",')
    to_write.append('  "clues": [')
    for c in clues:
        to_write.append('    { "d":"'+c.direction+'", "n":'+str(c.start_num)+', "x":'+str(c.start_x)+', "y":'+str(c.start_y)+', "a":"'+c.answer.upper()+'", "c":"'+c.clue_text.replace('"','')+'" },')
    to_write.append('  ]')
    to_write.append('}')
    f = open('puzzle.js', 'w')
    f.write('\n'.join(to_write))
    f.close()
