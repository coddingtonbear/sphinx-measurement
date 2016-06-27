# Sphinx-Measurement

**THIS IS A WORK IN PROGRESS; EVERYTHING BELOW IS SUBJECT TO CHANGE**

Easily mark-up and convert between various measures.

## Installation

Install from pip --

```
pip install sphinx-measurement
```

And, add ``sphinx_measurement`` to your ``extensions`` list in your Sphinx
project's configuration.

```
extensions = [
    # other extensions
    'sphinx_measurement',
]
```

## Basic Use

Marking-up a measurement:

```
Mount everest is :measurement:`29029 ft as everest-height` feet tall.
```

And when you later want to talk about that measurement in a different
measurement system:

```
That's :measurement:`everest-height in m` meters tall for those of you living
in countries using a sane measurement system.
```
