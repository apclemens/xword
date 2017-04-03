from .models import Puzzle, Clue
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit


TAB_LENGTH = 10

def split_clue_lines(clues, width):
    lines = []
    across_clues = [c for c in clues if c.direction == 'A']
    lines.append('ACROSS')
    for c in across_clues:
        clue_text = str(c.start_num) + '. ' + c.clue_text
        first_line = simpleSplit(clue_text, 'Helvetica', 12, width)[0]
        next_lines = simpleSplit(clue_text[len(first_line):], 'Helvetica', 12, width-TAB_LENGTH)
        lines += [first_line] + ['_'+l for l in next_lines]
    down_clues = [c for c in clues if c.direction == 'D']
    lines.append(' ')
    lines.append('DOWN')
    for c in down_clues:
        clue_text = str(c.start_num) + '. ' + c.clue_text
        first_line = simpleSplit(clue_text, 'Helvetica', 12, width)[0]
        next_lines = simpleSplit(clue_text[len(first_line):], 'Helvetica', 12, width-TAB_LENGTH)
        lines += [first_line] + next_lines
    return lines


def make_pdf(response, puzzle_id):
    puzzle = Puzzle.objects.get(UUID=puzzle_id)
    clues = Clue.objects.filter(puzzle=puzzle)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    #  Draw title
    title = puzzle.title
    p.setFont("Helvetica", 30)
    p.drawString(inch, height - inch, title) # Notice the UK

    # Draw grid
    puzzle_template = [puzzle.puzzle_text[i*puzzle.size:(i+1)*puzzle.size] for i in range(puzzle.size)]
    grid_size = width/2 - inch
    sq_size = grid_size / puzzle.size
    start_x = height-inch-30-15
    start_y = width/2
    for i in range(len(puzzle_template)):
        for j in range(len(puzzle_template[0])):
            if puzzle_template[i][j] == ' ':
                f = 1
            else:
                f = 0
            p.rect(start_y+j*sq_size, start_x-i*sq_size, sq_size, sq_size, fill=f)
    # Draw cell numbers
    p.setFont("Helvetica", sq_size/4)
    for c in clues:
        p.drawString(start_y+c.start_y*sq_size+1, start_x-c.start_x*sq_size+sq_size-sq_size/4-1, str(c.start_num))

    # Draw clues
    p.setFont('Helvetica', 12)
    clue_lines = split_clue_lines(clues, width/2-inch-inch/2)
    for i in range(len(clue_lines)):
        line = clue_lines[i]
        x = inch
        if line[0] == '_':
            line = line[1:]
            x += TAB_LENGTH
        p.drawString(x, height - inch - 30 - 15 - 13*i, line)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return p


if __name__ == '__main__':
    p = make_pdf('puzzle.pdf', 5)
