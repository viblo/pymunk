********
Examples 
********
.. _examples:
 
Here you will find a list of the included examples. Each example has a short 
description and a screenshot (if applicable).

To look at the source code of an example open it on Github by following 
the link. The examples are also included in the source distribution of Pymunk 
(but not if you install using the wheel file). You can find the source 
distribution at PyPI, https://pypi.org/project/pymunk/#files (file named pymunk-x.y.z.zip).

Jupyter Notebooks
=================

There are a couple examples that are provided as Jupyter Notebooks (.ipynb). 
They are possible to either view online in a browser directly on github, or 
opened as a Notebook. 


matplotlib_util_demo.ipynb
--------------------------
Displays the same space as the pygame and pyglet draw demos, but using
matplotlib and the notebook.

Source: `examples/matplotlib_util_demo.ipynb
<https://github.com/viblo/pymunk/blob/master/examples/matplotlib_util_demo.ipynb>`_

.. image:: _static/examples/matplotlib_util_demo.png


newtons_cradle.ipynb
--------------------
Similar simulation as newtons_cradle.py, but this time as a Notebook. 
Compared to the draw demo this demo will output an animation of the simulated
space.

Source: `examples/newtons_cradle.ipynb
<https://github.com/viblo/pymunk/blob/master/examples/newtons_cradle.ipynb>`_

.. raw:: html

    <video width="400" height="300" controls>
        <source src="_static/examples/newtons_cradle.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video> 

Standalone Python 
=================

To run the examples yourself either install Pymunk and run the module. 
Alternatively you can run each file separately.

Given that Pymunk is installed::
  
    $> python -m pymunk.examples.breakout
    
To list all the examples, use the -l option::

    $> python -m pymunk.examples -l

Each example contains something unique. Not all the examples use the same 
style. For example, some use the pymunk.pygame_util module to draw stuff, 
others contain the actual drawing code themselves. However, each example is 
self-contained. Except for external libraries (such as Pygame) and Pymunk each
example can be run directly to make it easy to read the code and understand 
what happens even if it means that some code is repeated for each example.

If you have made something that uses Pymunk and would like it displayed here 
or in a showcase section of the site, feel free to contact me!

.. contents:: Example files
    :local:
        
.. autoexample:: ../../pymunk/examples
    :image_folder: _static/examples
    :source_url: https://github.com/viblo/pymunk/blob/master/pymunk/examples

Additional Examples
===================

.. autoexample:: ../../additional_examples
    :image_folder: _static/examples
    :source_url: https://github.com/viblo/pymunk/blob/master/additional_examples