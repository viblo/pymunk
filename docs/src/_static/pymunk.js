(function () {
    var createList = function(selector){

        var ul = document.createElement('ul');
        var selected = document.querySelectorAll(selector);
        
        if (selected.length === 0){
            return;
        }
        
        selected.forEach((el, i)=>{
            let p = el.children.querySelectorAll('.descclassname');
            let n = el.children.querySelectorAll('.descname');
            let l = el.children.querySelectorAll('.headerlink');

            var a = document.createElement("a");
            a.setAttribute('href', l.getAttribute('href'));
            a.setAttribute('title', 'Link to this definition');
            a.append(p);
            a.append(b);

            var li = document.createElement('li');
            li.append(a);

            ul.append(li);
        });
        return ul;
    }

    var c = document.createElement('div');
    c.style.float = 'left';
    c.style.minWidth = '300px';
    
    var ul0 = c.cloneNode(true);
    ul0.append(document.querySelectorAll('.submodule-index'));

    customIndex = document.querySelectorAll('.custom-index');
    customIndex.replaceChildren();
    customIndex.append(ul0);
    
    var x = [];
    x.push(['Classes','dl.class > dt']);
    x.push(['Functions','dl.function > dt']);
    x.push(['Variables','dl.data > dt']);
    
    x.forEach(function (e){
        var l = createList(e[1]);
        if (l) {
            var x = c.cloneNode(true);
            var p = document.createElement('p');
            p.classList.add('rubric');
            p.textContent = e[0];
            x.append();
            x.append(l);
        }
        customIndex.append(ul);
    });
    
})();