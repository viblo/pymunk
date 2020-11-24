****
News 
****


Conda install pymunk
--------------------
*Victor - 2019-03-09*

Pymunk is now available on conda-forge, making it possible to use conda install 
to install Pymunk::

    > conda install -c conda-forge pymunk


Introductory video tutorials
----------------------------
*Victor - 2018-02-25*

Youtube user Attila has created a series of videos covering the basics of 
Pymunk. Take a look here for a gentle introduction into Pymunk:
 
.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PL1P11yPQAo7pH9SWZtWdmmLumbp_r19Hs" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


New page theme
------------------
*Victor - 2017-06-07*

**An mobile friendlier experience!**

A couple of days ago I noticed that the Pymunk web page get a significant 
amount of traffic from mobile, and at the same time the Sphinx theme it uses 
is not built for mobile browsing. So as a result I decided to change theme to 
something that can scale down to mobile size better. I hope the new page gives 
a better experience for everyone!


Pymunk on Android
-----------------
*Victor - 2017-06-04*

**Pymunk runs on Android!**

With the latest version (5.2.0) Pymunk can now be compiled and run on Android 
phones. Available as an example: `examples/kivy_pymunk_demo 
<https://github.com/viblo/pymunk/tree/master/examples/kivy_pymunk_demo>`_
is a Kivy example that can be built and run on Android. 

Below is a screen cap from my phone (an Xperia X Compact) running the Kivy 
example. The example itself is an interactive variant of the logo animation 
used on the front page of Pymunk.org

.. raw:: html

    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/AUfK7IJITEk" frameborder="0" 
    allowfullscreen></iframe>


Move from ctypes to CFFI?
-------------------------
*Victor - 2016-05-19*

**Should pymunk move to CFFI?**

To make development of pymunk easier Im planning to move from using ctypes
to CFFI for the low level Chipmunk wrapping. The idea is that CFFI is a 
active project which should mean it will be easier to get help, for example
around the 64bit python problems on windows.

Please take a look at Issue 99 on github which tracks this switch.
https://github.com/viblo/pymunk/issues/99


Travis-ci & tox
---------------
*Victor - 2014-11-13*

**pymunk is now using travis-ci for continuous integration**

In an effort to make testing and building of pymunk easier travis has been 
configured to build pymunk. At the same time support for tox was added to 
streamline local testing.


Move to Github
--------------
*Victor - 2013-10-04*

**pymunk has moved its source and issue list to Github!**

From the start pymunk has been hosted at Google Code, in the beginning using 
it for everything, source control, issue tracker, documentation and so on. 
During that time Github has become more and more popular and overall a better 
hosting platform. 

At the same time distributed version control systems have risen in popularity 
over traditional ones like Subversion.

Adding to this Google Code will stop hosting binaries in January 2014.

Because of this I have been thinking a while about moving pymunk away from 
svn and google code. I had an issue open on google code in which all feedback 
proposed git and github, and that has been my own thought as well. And so, 
today the move has been completed!

To get the latest source you will need a git client and then do::
    
    > git clone https://github.com/viblo/pymunk.git

If you prefer a graphical client (I do) I find SourceTree very good. 

Issues have been migrated to https://github.com/viblo/pymunk/issues

Binaries will be available from Pypi just like before, but the binary 
hosting at Google Code will not get any updates.

The google code page will from now on only have a redirect to pymunk.org and 
github.


Older news
----------

Older news items have been archived.
