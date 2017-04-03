import random, math, os


def template_match(template, lengths, max_length):
    size = int(math.sqrt(len(template)))
    lines_across = [template[i*size:(i+1)*size] for i in range(size)]
    lines_down = [''.join([lines_across[i][j] for i in range(size)]) for j in range(size)]
    temp_lengths = []
    for line in lines_across + lines_down:
        temp_lengths += [len(word) for word in line.split(' ')]
    while 0 in temp_lengths:
        temp_lengths.remove(0)
    for l in lengths:
        if int(l) not in temp_lengths:
            return False
        temp_lengths.remove(int(l))
    if max(temp_lengths) > int(max_length):
        return False
    return True


def get_template(size, lengths, max_length):
    while '' in lengths:
        lengths.remove('')
    module_dir = os.path.dirname(__file__)  # get current directory
    f = open(os.path.join(module_dir,'templates/'+str(size)+'x'+str(size)), 'r')
    templates = f.read().split('\n')
    f.close()
    while '' in templates:
        templates.remove('')
    random.shuffle(templates)
    for template in templates:
        if template_match(template, lengths, max_length):
            return template
    return None


def main():
    template = get_template(15, [15, 15], 8)
    size = 15
    lines_across = [template[i*size:(i+1)*size] for i in range(size)]
    for l in lines_across:
        print l


if __name__ == '__main__':
    main()
