# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Puzzle, Clue, Word

# Register your models here.
admin.site.register(Puzzle)
admin.site.register(Clue)
admin.site.register(Word)
