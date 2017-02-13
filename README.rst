==============
comanage_nacha
==============
A simple Wells Fargo flavor NACHA file builder, parser, and validation toolkit
------------------------------------------------------------------------------

.. image:: https://travis-ci.org/DisruptiveLabs/comanage_nacha.svg?branch=master
    :target: https://travis-ci.org/DisruptiveLabs/comanage_nacha
.. image:: https://coveralls.io/repos/github/DisruptiveLabs/comanage_nacha/badge.svg?branch=master
    :target: https://coveralls.io/github/DisruptiveLabs/comanage_nacha?branch=master
.. image:: https://badge.fury.io/py/comanage_nacha.svg
    :target: https://badge.fury.io/py/comanage_nacha

.. code-block:: bash

    pip install comanage_nacha

.. code-block:: python

    from comanage_nacha import NachaFile

    nacha = NachaFile()
    batch = nacha.add_batch()
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=23, amount=10000)
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=23, amount=10000)

    nacha_string = nacha.render_to_string()

:Authors:
    Franklyn Tackitt @kageurufu
