try:
    from django.http import StreamingHttpResponse, HttpResponse
    from .models import Word
except:
    pass
import wikipedia
from PyDictionary import PyDictionary


def get_wikipedia(word, show_dis=True):
    print 'Getting wikipedia definition of '+word
    try:
        yield wikipedia.summary(word)
    except wikipedia.DisambiguationError as e:
        if show_dis:
            for opt in e.options[:min(3, len(e.options))]:
                yield '<h3>'+opt+'</h3>'
                for x in get_wikipedia(opt, False):
                    yield x
    except wikipedia.PageError:
        yield 'Not found'


def get_definition(word):
    print 'Getting definition of '+word
    dictionary = PyDictionary()
    definition = dictionary.meaning(word)
    if definition == None:
        return '<i>No definition found</i>'
    html = ''
    for part in definition.keys():
        html += '<i>'+part+'</i>'
        html += '<ul>'
        for defin in definition[part]:
            html += '<li>'+defin+'</li>'
        html += '</ul>'
    return html


def get_html(word):
    if word == '':
        yield word
    else:
        word_objects = Word.objects.filter(word=word)
        yield '<div style="background-color:white;width:100%">'
        if len(word_objects) > 0:
            yield word_objects[0].help_text
        else:
            yield '<h1>'+word+'</h1>'
            html = '<h1>'+word+'</h1>'
            defin = get_definition(word)
            yield defin
            html += defin
            #yield '<h2>Wikipedia</h2>'
            #html += '<h2>Wikipedia</h2>'
            #for x in get_wikipedia(word):
            #    yield x
            #    html += x
            word_object = Word(word=word, help_text=html)
            word_object.save()
        yield '</div>'


def get_word_info(request):
    word = request.GET['word']
    return StreamingHttpResponse(get_html(word))


def get_word_info_no_stream(request):
    word = request.GET['word']
    info = ''
    for i in get_html(word):
        info += i
    return HttpResponse(info)


def get_word_info_from_word(word):
    html = get_html(word)
    return html


def main():
    gen = get_html('bohr')
    while True:
        print next(gen)


if __name__ == '__main__':
    main()

