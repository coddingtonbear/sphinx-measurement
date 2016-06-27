import locale
import math
import re

from docutils import nodes
from measurement.utils import guess
import six


@six.python_2_unicode_compatible
class MeasurementNode(nodes.Node):
    tagname = '#measurement'
    children = ()

    def __init__(self, data, rawsource=None):
        super(MeasurementNode, self).__init__()
        self.rawsource = rawsource
        self.data = data

    def __str__(self):
        return '{tag_name} {data}'.format(
            tag_name=self.tagname,
            data=self.data,
        )

    def __repr__(self):
        return '<{string_representation}>'.format(
            string_representation=six.text_type(self)
        )

    def as_string(self, writer):
        identities = get_identities(writer.document.traverse(MeasurementNode))

        if self.data.get('reference'):
            try:
                measurement = identities[self.data['reference']]['measurement']
                digit_count = identities[self.data['reference']]['digit_count']
            except KeyError:
                raise Exception(
                    "Referenced measurement '{name}' not found.".format(
                        name=self.data['reference']
                    )
                )
        else:
            measurement = self.data['measurement']
            digit_count = self.data['digit_count']

        unit_attribute_name = measurement.unit_attname(
            self.data.get(
                'conversion_unit',
                measurement.unit
            )
        )
        value = float(
            ('%%.%sg' % digit_count) %
            getattr(measurement, unit_attribute_name),
        )
        # If the number of significant digits is equal or fewer than the
        # number of magnitudes of this number, format the number as
        # an integer rather than a float.
        if digit_count <= int(math.log10(value) + 1):
            value = int(value)
        locale.setlocale(
            locale.LC_ALL,
            writer.document.settings.env.config.measurement_locale
        )
        formatted = locale.format(
            '%s',
            value,
            grouping=(
                writer.document.settings.env.config.measurement_grouping,
            )
        )

        return formatted


def get_identities(nodes):
    identities = {}

    for node in nodes:
        if 'identity' in node.data:
            identities[node.data['identity']] = node.data

    return identities


def visit_measurement_node(self, node):
    self.body.append(node.as_string(self))


def depart_measurement_node(self, node):
    pass


def measurement_node(
    typ, rawtext, text, lineno, inliner, options={}, content=[]
):
    return [
        MeasurementNode(
            process_measurement_string(text),
            rawsource=rawtext,
        )
    ], []


def process_measurement_string(incoming_string):
    """Process an incoming measurement string into its constituent parts.

    Returns a dictionary having a subset of the following keys:

    * `measurement`: An instance of a subclass of
      `measurement.base.MeasureBase`.
    * `reference`: The name used for referencing an existing stored
      measurement.
    * `identity`: The name to _store_ this value as for later use.
    * `conversion_unit`: The unit to convert an incoming unit into.

    :type incoming_kstring: unicode
    :rtype: dict
    """
    processed = {}

    if ' in ' in incoming_string:
        incoming_string, raw_conversion_unit = incoming_string.split(' in ')
        processed['conversion_unit'] = raw_conversion_unit.strip()
    if ' as ' in incoming_string:
        incoming_string, raw_identity = incoming_string.split(' as ')
        processed['identity'] = raw_identity.strip()

    is_measurement = False

    extractor = re.compile(r'(?P<numeric>[0-9e,.-]+)(?P<unit>.*)')
    extractor_match = extractor.match(incoming_string)

    if extractor_match:
        extractor_result = extractor_match.groupdict()
        # Get the float value of the measurement
        try:
            value = float(
                re.compile(r'[^\de.-]+').sub('', extractor_result['numeric'])
            )
            is_measurement = True
        except ValueError:
            pass

    if is_measurement:
        # `value` and `extractor_match` remain available from the above block
        # Get the number of significant digits
        digit_count_string = extractor_result['numeric']
        if 'e' in digit_count_string:
            digit_count_string = (
                digit_count_string[0:digit_count_string.find('e')]
            )
        processed['digit_count'] = len(
            re.compile(r'\d').findall(digit_count_string)
        )

        unit = extractor_result['unit'].strip()

        # Create a measurement object using the unit and value
        processed['measurement'] = guess(value, unit)
    else:
        processed['reference'] = incoming_string.strip()

    return processed


def setup(app):
    app.add_node(
        MeasurementNode,
        html=(visit_measurement_node, depart_measurement_node)
    )
    app.add_role('measurement', measurement_node)
    app.add_config_value(
        'measurement_locale',
        locale.getdefaultlocale()[0],
        'html',
    )
    app.add_config_value(
        'measurement_grouping',
        True,
        'html',
    )
