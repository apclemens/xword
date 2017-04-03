# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Puzzle, Clue, publish_puzzle
from django.http import HttpResponse, StreamingHttpResponse
from make_pdf import make_pdf
import json
from generator.generator import quickSolve
from generator.random_template import get_template


def index(request):
    puzzles = Puzzle.objects.all()
    return render(request, 'puzzle/index.html', {'puzzles': puzzles})


def play(request, puzzle_id):
    puzzle = Puzzle.objects.get(UUID=puzzle_id)
    return render(request, 'puzzle/play.html', {'puzzle': puzzle})


def play_js(request, puzzle_id):
    puzzle = Puzzle.objects.get(UUID=puzzle_id)
    clues = Clue.objects.filter(puzzle=puzzle)
    return render(request, 'puzzle/play.js', {'puzzle': puzzle, 'clues': clues})


def pdf(request, puzzle_id):
    puzzle = Puzzle.objects.get(UUID=puzzle_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+puzzle.title.replace(' ', '_')+'.pdf"'
    make_pdf(response, puzzle_id)
    return response


def builder(request):
    return render(request, 'puzzle/builder.html', {'initial_template': get_template(15, [], 8)})


def random_template(request):
    return HttpResponse(get_template(request.GET['size'], request.GET['word_lengths'].split(','), request.GET['max_length']))


def fill_out_grid(request):
    try:
        template = request.GET['template']
        exclude_words = request.GET['exclude_words']
    except:
        template = '**** ****  ******** ***** ******** ***** ************************  *****   ***************   *****    ********** **********    *****   ***************   *****  ************************ ***** ******** ***** ********  **** ****'
        exclude_words = []
    return HttpResponse(json.dumps(quickSolve(template, exclude_words.split('\n'))), content_type="application/json")


def fill_out_grid_stream(request):
    try:
        template = request.GET['template']
        exclude_words = request.GET['exclude_words']
    except:
        template = '**** ****  ******** ***** ******** ***** ************************  *****   ***************   *****    ********** **********    *****   ***************   *****  ************************ ***** ******** ***** ********  **** ****'
        exclude_words = ''
    return StreamingHttpResponse(quickSolve(template, exclude_words.split('\n')))


def publish(request):
    template = request.GET['template']
    clues = json.loads(request.GET['clues'])
    title = request.GET['title']
    id = publish_puzzle(title, template, clues)
    print 'PUZZLE ID: '+str(id)
    return HttpResponse(id)


def bootstrap(request):
    return render(request, 'puzzle/bootstrap.html', {})
