Manylinux wheels
================

This is for building linux binary wheels. So "pip install pymunk" works on linux.

tldr
----

cd tools/manylinux-build/
make pull wheels

# linux binary wheel files are in 'tools/manylinux-build/wheelhouse'

Longer instructions
-------------------

The *manylinux1* tag (see `PEP 513 <https://www.python.org/dev/peps/pep-0513/>`__)
refers to a specific set of core library minimum versions, which most recent
desktop Linux distros have.
To ensure that our libraries are ABI-compatible with these core libraries, we
build on an old Linux distribution in a docker container.

manylinux is an older linux with a fairly compatable ABI, so you can make linux binary
wheels that run on many different linux distros.

* https://github.com/pygame/pygame (README based on this one)
* https://github.com/pypa/auditwheel
* https://github.com/pypa/manylinux


This is easiest on a Linux machine with the Docker daemon running. To get the
prebuilt base images with pymunk dependencies::

    make pull-x64    # 64 bit, or
    make pull-x86    # 32 bit, or
    make pull        # Both

Then build the wheels::

    make wheels-x64  # 64 bit, or
    make wheels-x86  # 32 bit, or
    make wheels      # both

The wheels will be created in a directory called ``wheelhouse``.


Virtual Machine
---------------

NOTE: you can run docker on Mac and Windows ok now, so a virtual machine may not be needed.


Below are instructions on using a vagrant virtual machine, so we can build the wheels from
mac, windows or linux boxes.


These aren't meant to be copypasta'd in. Perhaps these can be worked into a script later::

    # You should be in the base of the pymunk repo when you run all this.
    $ pwd
    /home/jblogs/pymunk

    # Download many megabytes of ubuntu.
    mkdir vagrant.xenial64
    cd vagrant.xenial64
    vagrant init ubuntu/xenial64

    # edit your Vagrantfile to add /vagrant_pymunk synced folder.
    # You pymunk folder is next to your vagrant
    config.vm.synced_folder "../pymunk", "/vagrant_pymunk"

    # now start vagrant.
    vagrant up
    vagrant ssh

    # now we are on the vagrant ubuntu host
    # We set up docker following these instructions for ubuntu-xenial
    # https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1
    sudo apt-get update
    sudo apt-get remove docker docker-engine docker.io
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

    # Now edit /etc/hosts so it has a first line with the hostname ubuntu-xenial in it.
    # Otherwise docker does not start.
    # 127.0.0.1 localhost ubuntu-xenial
    # makes a /etc/hosts.bak in case something breaks.
    sudo sed -i".bak" '/127.0.0.1 localhost/s/$/ ubuntu-xenial/' /etc/hosts

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo apt-get update

    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    sudo apt-get install docker-ce

    # check that it runs.
    sudo docker run hello-world


    # We should have been in our python package clone root directory before we ran vagrant ssh
    cd /vagrant_pymunk

    # We need to be able to run docker as the ubuntu user.
    sudo usermod -aG docker ubuntu
    sudo usermod -aG docker $USER

    # now log out of vagrant. Need to reload it because docker.
    exit

    vagrant reload
    vagrant ssh

    # now we can start docker. Should be started already.
    sudo service docker start


    cd /vagrant_pymunk/tools/manylinux-build

    # To make the base docker images and push them to docker hub do these commands.
    # Note, these have already been built, so only needed if rebuilding dependencies.
    # https://hub.docker.com/u/pymunk/
    #make base-images
    #make push

    # We use the prebuilt docker images, which should be quicker.
    make wheels

    # List the wheels we've built
    ls -la wheelhouse

    # Testing
    export SDL_AUDIODRIVER=disk
    export SDL_VIDEODRIVER=dummy

    python3.5 -m venv anenv35
    . ./anenv35/bin/activate
    pip install wheelhouse/pymunk-*cp35-cp35m-manylinux1_x86_64.whl
    # TODO: pymunk does not bundle tests.
    # python -m pymunk.tests


    # Now upload all the linux wheels to pypi.
    # Make sure your PYPI vars are set. See .travis_osx_upload_whl.py
    # Note you will need to increment the version in setup.py first.
    cd ..
    mkdir -p dist
    rm -f dist/*.whl
    cp tools/manylinux-build/wheelhouse/*.whl dist/

    pip install twine
    twine upload dist/*.whl
