$(function (){
    var createList = function(selector){

        var ul = $('<ul>');
        var selected = $(selector);
        
        if (selected.length === 0){
            return;
        }
        
        selected.clone().each(function (i,e){

            var p = $(e).children('.descclassname');
            var n = $(e).children('.descname');
            var l = $(e).children('.headerlink');

            var a = $('<a>');
            a.attr('href',l.attr('href')).attr('title', 'Link to this definition');

            a.append(p).append(n);

            var entry = $('<li>').append(a);
            ul.append(entry);
        });
        return ul;
    }


    var c = $('<div style="float:left; min-width: 300px;">');

    var ul0 = c.clone().append($('.submodule-index'))

    customIndex = $('.custom-index');
    customIndex.empty();
    customIndex.append(ul0);
    
    var x = [];
    x.push(['Classes','dl.class > dt']);
    x.push(['Functions','dl.function > dt']);
    x.push(['Variables','dl.data > dt']);
    
    x.forEach(function (e){
        var l = createList(e[1]);
        if (l) {        
            var ul = c.clone()
                .append('<p class="rubric">'+e[0]+'</p>')
                .append(l);
        }
        customIndex.append(ul);
    });
    
});