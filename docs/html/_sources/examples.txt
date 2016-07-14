********
Examples 
********
.. _examples:
 
Here you will find a list of the included examples. Each example have a short 
description and a screenshot (if applicable).


Jupyter Notebooks
=================

There are a couple examples that are provided as Jupyter Notebooks (.ipynb). 
They are possible to either view online in a browser directly on github, or 
opened as a Notebook. 


matplotlib_util_demo.ipynb
--------------------------
Displays the same space as the pygame and pyglet draw demos, but using
matplotlib and the notebook.

`Matplotlib Util Demo 
<https://github.com/viblo/pymunk/blob/master/examples/matplotlib_util_demo.ipynb>`_

.. image:: _static/examples/matplotlib_util_demo.png


newtons_cradle.ipynb
--------------------
Similar simulation as newtons_cradle.py, but this time as a Notebook. 
Compared to the draw demo this demo will output a animation of the simulated
space.

`Newtons Cradle 
<https://github.com/viblo/pymunk/blob/master/examples/newtons_cradle.ipynb>`_

.. raw:: html

    <video width="400" height="300" controls>
        <source src="_static/examples/newtons_cradle.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video> 

Standalone Python 
=================

To run the examples yourself either install pymunk or run it using the 
convenience run.py script.

Given that pymunk is installed where your python will find it::

    >cd examples
    >python breakout.py

To run directly without installing anything. From the pymunk source folder::

    >cd examples
    >python run.py breakout.py 
    
Each example contains something unique. Not all of the examples use the same 
style. For example, some use the pymunk.pygame_util module to draw stuff, 
others contain the actual drawing code themselfs. However, each example is 
self contained. Except for external libraries (such as pygame) and pymunk each
example can be run directly to make it easy to read the code and understand 
what happens even if it means that some code is repeated for each example.

If you have made something that uses pymunk and would like it displayed here 
or in a showcase section of the site, feel free to contact me!


.. contents:: Example files
    :local:
        
.. autoexample:: ../../examples
    :image_folder: _static/examples
