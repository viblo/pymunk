(function () {
    var createList = function (selector) {
        var selected = document.querySelectorAll(selector);

        if (selected.length === 0) {
            return;
        }

        var ul = document.createElement('ul');

        selected.forEach((el, i) => {
            let p = el.querySelector('.descclassname');
            let n = el.querySelector('.descname');
            let l = el.querySelector('.headerlink');

            var a = document.createElement("a");
            a.setAttribute('href', l.getAttribute('href'));
            a.setAttribute('title', 'Link to this definition');
            a.append(p.cloneNode(true));
            a.append(n.cloneNode(true));

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
    let el = document.querySelector('.submodule-index');
    if (el) {
        ul0.append(el);
    }

    customIndex = document.querySelector('.custom-index');
    customIndex.replaceChildren();
    customIndex.append(ul0);

    var x = [];
    x.push(['Classes', 'dl.class > dt']);
    x.push(['Functions', 'dl.function > dt']);
    x.push(['Variables', 'dl.data > dt']);

    x.forEach(function (e) {
        var l = createList(e[1]);
        if (l) {
            var x = c.cloneNode(true);
            var p = document.createElement('p');
            p.classList.add('rubric');
            p.textContent = e[0];
            x.append(p);
            x.append(l);
            customIndex.append(x);
        }

    });

})();