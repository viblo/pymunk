.. raw:: html

    <div id='bd-2021'>
        <span>Click to dismiss. Animation by Er Robin at <a href="https://codepen.io/ErRobin/pen/ZEWYNEQ">codepen.io</a></span>
        <canvas id=c></canvas>
    
    </div>
    <style>

    #bd-2021 {
        position: fixed; /* Sit on top of the page content */
        display: none; /* Hidden by default */
        width: 100%; /* Full width (cover the whole page) */
        height: 100%; /* Full height (cover the whole page) */
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0,0,0,0.5); /* Black background with opacity */
        z-index: 2; /* Specify a stack order in case you're using a different order for other elements */
        cursor: pointer; /* Add a pointer on hover */
        
    }
    #bd-2021 > span {
        color: gray;
        position: absolute;
        bottom: 0;
        z-index: 3;
        font-size: x-small;
    }
    #bd-2021 > canvas {
        position: absolute;
        top: 0;
        left: 0;
        opacity: 90%;
    }

    </style>

    <script type="text/javascript" src='_static/bd-2021/bd-2021.js'></script>

    <script>
        let now = new Date();
        if (now.getDate() == 11 && now.getMonth() == 3){
            $("#bd-2021").show();
            anim(function(){
                $("#bd-2021").fadeOut(1000);    
            });
        }
        $("#bd-2021").click(function(){ $(this).hide() })
    </script>

.. include:: ../../README.rst
        
Contents
--------
 
.. toctree::
    :maxdepth: 4
    
    installation
    overview
    pymunk
    examples
    showcase
    tutorials
    benchmarks
    advanced
    changelog
    Downloads <https://pypi.python.org/pypi/pymunk/>
    Issue Tracker <https://github.com/viblo/pymunk/issues>
    Source Repository <https://github.com/viblo/pymunk>
    license

Indices and tables
------------------
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`