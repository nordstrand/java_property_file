#  java_property_file [![Build Status](https://travis-ci.org/nordstrand/java_property_file.svg?branch=master)]

Ansible module for updating property files formatted with java.util.Properties syntax

## Usage
    
    $ ansible --module-path=../library/ -m java_property_file \
      -a "dest=test.properties option=key value=newvalue" \
      localhost


## Tests

Run:

    $ pip install ansible
    $ python -m test.test

