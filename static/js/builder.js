var grid_width = 600;

class CrosswordBuilder extends React.Component {
    constructor() {
        super();
        this.state = {
            title: '',
            notes: '',
            exclude_words: '',
            template_info: {
                size: 15,
                word_lengths: '',
                max_length: 20
            },
            template: '',
            currentSelectedCells: '',
            currentSelectedWord: '',
            clues: {},
            completing: false,
            selected_cell: '',
            mouseIsDownOnGrid: false,
            grid_hover: false,
            word_list: [],
            num_completed_clues: 1,
        };
        this.randomTemplate();
    }
    render() {
        return (
            <div
                tabIndex="1"
                onKeyDown={(e) => this.keyDown(e.key)}
                onClick={() => this.clickOutside()}
            >
                <Title onChange={(val) => this.setState({title:val})} title_val={this.state.title}/>
                <table>
                    <tr>
                        <td>
                            <TemplateSpecs
                                onChange={(event) => this.eventChangeHandler(event)}
                                temp_specs={this.state.template_info}
                                rand_temp_action={() => this.randomTemplate()}
                            />
                        </td>
                        <td>

                        </td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td>
                            <Grid
                                currentSelectedCells={this.state.currentSelectedCells} template={this.state.template}
                                toggleBlackCells={(e, cells) => this.toggleBlackCells(e, cells)}
                                selected_cell={this.state.selected_cell}
                                onCellClick={(x,y) => this.setSelected(x,y)}
                            />
                        </td>
                        <td>
                            <p><progress max={this.state.word_list.length} value={this.state.num_completed_clues}></progress></p>
                            <CurrentWords
                                onChange={(word, cells) => this.highlightWord(word, cells)}
                                words={this.state.word_list}
                                clues={this.state.clues}
                            />
                        </td>
                        <td>
                            <WordInfo word={this.state.currentSelectedWord}/>
                        </td>
                        <td>
                            <Clues
                                selWord={this.state.currentSelectedWord+this.state.currentSelectedCells}
                                defValue={this.getCurrentClue()}
                                onChange={(key, newClue) => this.setClue(key, newClue)}
                                nextClue={() => this.nextClue()}
                            />
                        </td>
                        <td>
                            <Notes onChange={(val) => this.setState({notes:val})} notes_val={this.state.notes}/>
                        </td>
                        <td>
                            <ExcludeWords
                                onChange={(val) => this.setState({exclude_words:val})}
                                exclude_words={this.state.exclude_words}
                            />
                        </td>
                    </tr>
                </table>
                <ActionButton text='Fill out grid' onClick={() => this.getGridSolution(this)} />
                <ActionButton text='Publish' onClick={() => this.publish()} />
                <ActionButton text='Kill process' onClick={() => this.setState({completing: false})} />
                <ActionButton text='Clear grid' onClick={() => this.clearTemplate()} />
                <ActionButton text='Exclude word' onClick={() => this.excludeWord()} />
            </div>
        )
    }
    setNumCompletedClues(word_list) {
        var completed = 0;
        for(var i=0;i<word_list.length;i++) {
            var key = word_list[i].word+word_list[i].cells;
            if(key in this.state.clues) {
                if(this.state.clues[key].length > 0) completed += 1;
            }
        }
        this.setState({num_completed_clues: completed})
    }
    excludeWord() {
        var exclude_words = this.state.exclude_words;
        if (exclude_words.length > 0) exclude_words = exclude_words + '\n'
        exclude_words = exclude_words + this.state.currentSelectedWord;
        this.setState({exclude_words: exclude_words})
        $('#exclude_word_list').val(exclude_words);
    }
    keyDown(key) {
        if (this.state.selected_cell=='') return;
        var x=parseInt(this.state.selected_cell.split(',')[0]);
        var y=parseInt(this.state.selected_cell.split(',')[1]);
        var index = x*this.state.template_info.size+y;
        if ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(key.toUpperCase())>-1 || key=='Backspace') {
            if(key=='Backspace'){var newVal = '*'}
            else {var newVal = key.toUpperCase()}
            var newTemp = this.state.template;
            this.fillInGrid(
                newTemp.substr(0,index) + newVal + newTemp.substr(index+1)
            )
            return;
        }
        if (key=='ArrowUp') {
            var newX = x;
            do {
                newX = newX-1;
                if(newX==-1) {
                    newX = x;
                    break;
                }
            } while (this.state.template[newX*this.state.template_info.size+y]==' ')
            this.setState({selected_cell: ''+newX+','+y})
            return;
        }
        if (key=='ArrowDown') {
            var newX = x;
            do {
                newX = newX+1;
                if(newX==this.state.template_info.size) {
                    newX = x;
                    break;
                }
            } while (this.state.template[newX*this.state.template_info.size+y]==' ')
            this.setState({selected_cell: ''+newX+','+y})
            return;
        }
        if (key=='ArrowLeft') {
            var newY = y;
            do {
                newY = newY-1;
                if(newY==-1) {
                    newY = y;
                    break;
                }
            } while (this.state.template[x*this.state.template_info.size+newY]==' ')
            this.setState({selected_cell: ''+x+','+newY})
            return;
        }
        if (key=='ArrowRight') {
            var newY = y;
            do {
                newY = newY+1;
                if(newY==this.state.template_info.size) {
                    newY = y;
                    break;
                }
            } while (this.state.template[x*this.state.template_info.size+newY]==' ')
            this.setState({selected_cell: ''+x+','+newY})
            return;
        }
    }
    setSelected(x,y) {
        if(x!=='') {
            this.setState({selected_cell: ''+x+','+y})
        } else {
            this.setState({selected_cell: ''})
        }
    }
    clickOutside() {
        if(this.state.grid_hover) this.setState({selected_cell: ''})
    }
    getGridSolution(self) {
        self.clearTemplate()
        self.setState({completing: true})
        var client = new XMLHttpRequest();
        var len = self.state.template_info.size*self.state.template_info.size;
        client.onprogress = function(){
            self.fillInGrid(this.responseText.substring(this.responseText.length-len, this.responseText.length));
            if (!self.state.completing) client.abort()
        }
        client.open('get', 'fill_out_grid?template='+self.state.template+'&exclude_words='+self.state.exclude_words);
        client.send();
    }
    nextClue() {
        var words = this.state.word_list;
        if(this.state.currentSelectedWord.length==0) {i = -1}
        else {
            for(var i=0;i<words.length;i++) {
                if (words[i].word == this.state.currentSelectedWord && words[i].cells == this.state.currentSelectedCells) {break;}
            }
        }
        var nextWord = words[(i+1)%words.length]
        $('#word_list').val(nextWord.cells).change();
        this.setState({currentSelectedWord: nextWord.word, currentSelectedCells: nextWord.cells})
    }
    toggleBlackCells(e, cells) {
        e.preventDefault();
        var cellArr = cells.split('-');
        var newTemp = this.state.template;
        for (var i=0;i<cellArr.length;i++) {
            var x=cellArr[i].split(',')[0];
            var y=cellArr[i].split(',')[1];
            var index = parseInt(x)*this.state.template_info.size+parseInt(y)
            var val = newTemp[index];
            newTemp = newTemp.substr(0, index) + (val==' ' ? '*' : ' ') + newTemp.substr(index + 1);
        }
        this.fillInGrid(newTemp)
    }
    publish() {
        if(this.state.template.indexOf('*')>-1) {
            console.log("Empty spaces in grid")
            return;
        }
        if(this.state.num_completed_clues != this.state.word_list.length) {
            console.log("Haven't finished clues")
            return;
        }
        if(this.state.title.length==0){
            console.log("Give it a title")
            return;
        }
        $.ajax({
            url: 'publish',
            data: {
                title: this.state.title,
                template: this.state.template,
                clues: JSON.stringify(this.state.clues)
            },
            success(result) {
                window.location.href = window.location.href.replace('builder/',result)
            }
        })
    }
    getCurrentClue() {
        if(this.state.currentSelectedWord == '') return '';
        var key = this.state.currentSelectedWord+this.state.currentSelectedCells;
        if (!key in this.state.clues) return '';
        return this.state.clues[key];
    }
    setClue(key, newClue) {
        var stateClue = this.state.clues;
        stateClue[key] = newClue;
        this.setState({clues: stateClue});
        this.setNumCompletedClues(this.state.word_list)
    }
    highlightWord(word, cells) {
        this.setState({currentSelectedCells: cells, currentSelectedWord: word});
    }
    getCurrentWords(template) {
        var allWords = [];
        var remHighlight = true;
        //across
        for (var i=0;i<this.state.template_info.size;i++) {
            var line = template.substring(i*this.state.template_info.size, (i+1)*this.state.template_info.size);
            var words = line.split(' ');
            for (var w=0;w<words.length;w++) {
                if (words[w].indexOf('*')==-1 && words[w].length > 0) {
                    var cells = [];
                    for (var j=0;j<words[w].length;j++) {cells.push(''+i+','+(line.indexOf(words[w])+j))}
                    allWords.push({word: words[w], cells: cells.join('-')})
                    if (this.state.currentSelectedWord == words[w] && this.state.currentSelectedCells == cells.join('-')) {
                        remHighlight=false;
                    }
                }
            }
        }
        //down
        for (var i=0;i<this.state.template_info.size;i++) {
            var line = '';
            for (var j=0;j<this.state.template_info.size;j++) {
                line += template[i+j*this.state.template_info.size];
            }
            var words = line.split(' ');
            for (var w=0;w<words.length;w++) {
                if (words[w].indexOf('*')==-1 && words[w].length > 0) {
                    var cells = [];
                    for (var j=0;j<words[w].length;j++) {cells.push(''+(line.indexOf(words[w])+j)+','+i)}
                    allWords.push({word: words[w], cells: cells.join('-')})
                    if (this.state.currentSelectedWord == words[w] && this.state.currentSelectedCells == cells.join('-')) {
                        remHighlight=false;
                    }
                }
            }
        }
        if (remHighlight && this.state.currentSelectedWord!='' && this.state.currentSelectedCells!='') {this.highlightWord('','')}
        allWords.sort(function(a,b){return (a.word.toLowerCase()>b.word.toLowerCase() ? 1 : -1)});
        this.setNumCompletedClues(allWords)
        return allWords;
    }
    clearTemplate() {
        var newTemp = '';
        for (var i=0;i<this.state.template.length;i++) {
            if (!this.state.template[i].match(/[a-z]/)) {newTemp = newTemp + this.state.template[i]}
            else {newTemp = newTemp + '*'}
        }
        this.fillInGrid(newTemp)
    }
    fillInGrid(template) {
        this.setState({template: template});
        this.setState({word_list: this.getCurrentWords(template)})
    }
    eventChangeHandler(event) {
        var temp_info = this.state.template_info;
        temp_info[event.target.id] = event.target.value;
        this.fillInGrid(temp_info);
    }
    randomTemplate() {
        var self = this;
        $.ajax({
            url: 'random_template',
            data: this.state.template_info,
            type: 'GET',
            success: function(result) {
                if(result!='None') {
                    self.fillInGrid(result)
                } else {
                    console.log('Couldn\'t find matching template')
                }
            }
        })
    }
}

class ActionButton extends React.Component {
    render() {
        return (
            <button onClick={() => this.props.onClick()}>
                {this.props.text}
            </button>
        )
    }
}

class Clues extends React.Component {
    render() {
        return (
            <textarea
                placeholder="Enter clue here"
                style={{
                    height: grid_width,
                }}
                onChange={(event) => this.props.onChange(this.props.selWord, event.target.value)}
                value = {this.props.defValue==null ? '' : this.props.defValue}
                onKeyPress={(event) => this.onKeyPress(event)}
            />
        )
    }
    onKeyPress(event) {
        if (event.key == 'Enter') {
            event.preventDefault();
            this.props.nextClue();
        }
    }
}

class WordInfo extends React.Component {
    render() {
        return (
             <iframe style={{
                height: grid_width,
             }} src={'/puzzle/builder/word_info?word='+this.props.word}></iframe>
        )
    }
}

class CurrentWords extends React.Component {
    render() {
        return (
            <select id='word_list'
                size='100'
                style={{height:grid_width-25}}
                onChange={(event) => this.props.onChange(event.target.options[event.target.selectedIndex].text, event.target.value)}
            >
                {this.props.words.map((wordInfo) =>
                    <option key={wordInfo.cells} word={wordInfo.word}
                    style={{color:
                        wordInfo.word+wordInfo.cells in this.props.clues ?
                            (this.props.clues[wordInfo.word+wordInfo.cells].length > 0 ? "black" : "red") : "red"
                    }}
                    value={wordInfo.cells}>{wordInfo.word}</option>
                )}
            </select>
        )
    }
}

class Grid extends React.Component {
    constructor() {
        super();
        this.state = {
            hover: ''
        }
    }
    render() {
        var highlightedCells = this.props.currentSelectedCells.split('-');
        var rowJSX = [];
        var size = Math.sqrt(this.props.template.length);
        for (var i=0;i<size;i++) {
            var cellJSX = [];
            for (var j=0;j<size;j++) {
                cellJSX.push(
                    <Cell
                        grid_size={size}
                        key={''+i+','+j}
                        x={i} y={j}
                        val={this.props.template[i*size+j]}
                        highlighted = {highlightedCells.indexOf(''+i+','+j)>-1}
                        selected = {this.props.selected_cell}
                        onhover = {(x,y) => this.setHover(x,y)}
                        onMouseOut = {() => this.setState({hover: ''})}
                        toHover = {this.state.hover.split('-')}
                        onrightclick = {(e, x, y) => this.props.toggleBlackCells(e, this.state.hover)}
                        onCellClick = {(x,y) => this.props.onCellClick(x,y)}
                    />
                )
            };
            rowJSX.push(
                <div key={i}>
                    {cellJSX}<br/>
                </div>
            )
        }
        return (
            <div
                style={{
                    width:''+grid_width+'px',
                    height:''+grid_width+'px'
                }}
            >
                {rowJSX}
            </div>
        )
    }
    componentDidMount() {
        window.addEventListener('mousedown', () => this.pageClick(this), false);
    }
    pageClick(self) {
        if(self.state.hover==''){self.props.onCellClick('','')}
    }
    setHover(x,y) {
        var size = Math.sqrt(this.props.template.length);
        var hover = ''+x+','+y;
        var opposite = ''+(size-x-1)+','+(size-y-1);
        if(hover!=opposite) {hover += '-'+opposite;}
        this.setState({hover: hover})
    }
}

class Cell extends React.Component {
    shouldComponentUpdate(nextProps) {
        if(this.props.grid_size != nextProps.grid_size) {return true}
        if(''+this.props.x+','+this.props.y == this.props.selected ||
           ''+this.props.x+','+this.props.y == nextProps.selected) {
            return true
        }
        if(this.props.highlighted || nextProps.highlighted) {return true}
        if(this.props.toHover.indexOf(''+this.props.x+','+this.props.y)!=-1 ||
            nextProps.toHover.indexOf(''+this.props.x+','+this.props.y)!=-1) {
                return true
        }
        if(this.props.val != nextProps.val) {return true}
        return false;
    }
    render() {
        var cell_size = grid_width / this.props.grid_size;
        return (
            <div
                style={{
                    width: ''+cell_size+'px',
                    height: ''+cell_size+'px',
                    border: '1px solid',
                    float:'left',
                    background: this.background(),
                    position: 'static',
                    textAlign: 'center',
                    fontSize: ''+(cell_size*.7)+'px',
                    color: (this.props.val==this.props.val.toUpperCase() ? 'black' : 'grey')
                }}
                onMouseOver={() => this.props.onhover(this.props.x, this.props.y)}
                onMouseOut={() => this.props.onMouseOut()}
                onClick={() => this.onClick()}
                onContextMenu={(e) => this.props.onrightclick(e, this.props.x, this.props.y)}
            >
                {this.props.val == '*' ? ' ' : this.props.val.toUpperCase()}
            </div>
        )
    }
    onClick() {
        if(this.props.val != ' ') {
            this.props.onCellClick(this.props.x, this.props.y)
        }
    }
    background() {
        if(''+this.props.x+','+this.props.y == this.props.selected) {return '#ffff00'} // dark yellow
        if(this.props.toHover.indexOf(''+this.props.x+','+this.props.y) != -1) {
            if(this.props.val == ' ') {return '#595959'}
            return '#a6a6a6'
        }
        if(this.props.val == ' ') {return 'black'}
        if(this.props.highlighted) {return '#66ffff'} // light blue
        return 'white'
    }
}

class TemplateSpecs extends React.Component {
    render() {
        return (
            <div>
                <button onClick={() => this.props.rand_temp_action()}>
                    Random template
                </button><br/>
                <input id="size"
                    type="number"
                    defaultValue={this.props.temp_specs.size}
                    onChange={(event)=>this.props.onChange(event)}
                /><br/>
                <input id="word_lengths"
                    type="text"
                    defaultValue={this.props.temp_specs.word_lengths}
                    onChange={(event)=>this.props.onChange(event)}
                /><br/>
                <input id="max_length"
                    type="number"
                    defaultValue={this.props.temp_specs.max_length}
                    onChange={(event)=>this.props.onChange(event)}
                />
            </div>
        )
    }
}

class Title extends React.Component {
    render() {
        return (
            <input
               type="text" placeholder="Title"
               defaultValue={this.props.title_val}
               onChange={(event) => this.props.onChange(event.target.value)}
            />
        )
    }
}

class Notes extends React.Component {
    render() {
        return (
            <textarea
               style={{height:grid_width}}
               type="text" placeholder="Keep notes here"
               defaultValue={this.props.notes_val}
               onChange={(event) => this.props.onChange(event.target.value)}
            />
        )
    }
}

class ExcludeWords extends React.Component {
    render() {
        var to_exclude = this.props.exclude_words;
        return (
            <textarea
               style={{height:grid_width}}
               id='exclude_word_list'
               type="text" placeholder="List words to exclude"
               onChange={(event) => this.props.onChange(event.target.value)}
            ></textarea>
        )
    }
}


ReactDOM.render(<CrosswordBuilder />, document.getElementById('crossword_builder'));
