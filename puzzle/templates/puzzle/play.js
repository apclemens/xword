{
  "_": "Congratulations, you found the solution to the puzzle.  Aren't you a genius.  Go win a Nobel prize, genius.",
  "title": "{{ puzzle.title }}",
  "by": "By Line",
  "clues": [
    {% autoescape on %}
    {% for clue in clues %}
    { "d":"{{ clue.direction }}",
      "n":{{ clue.start_num }},
      "x":{{ clue.start_x }},
      "y":{{ clue.start_y }},
      "a":"{{ clue.answer|upper }}",
      "c":"{{ clue.clue_text|escapejs }}"
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
    {% endautoescape %}
  ]
}
