from io import StringIO
from unittest.mock import patch
import os
import unittest

import log_filter_util.log_filter_util


class OutputTest(unittest.TestCase):

    # Argument parsing tests because args are defined in specification
    def test_argument_parse_method_should_set_value_for_first_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['-f', '10']).first, 10
        )

    def test_argument_parse_method_should_set_value_for_first_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--first', '10']).first, 10
        )

    def test_argument_parse_method_should_set_value_for_last_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['-l', '10']).last, 10
        )

    def test_argument_parse_method_should_set_value_for_last_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--last', '10']).last, 10
        )

    def test_argument_parse_method_should_set_true_for_ipv4_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['-i']).ipv4, True
        )

    def test_argument_parse_method_should_set_true_for_ipv4_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--ipv4']).ipv4, True
        )

    def test_argument_parse_method_should_set_true_for_ipv6_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['-I']).ipv6, True
        )

    def test_argument_parse_method_should_set_true_for_ipv6_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--ipv6']).ipv6, True
        )

    # TODO: This option parsing is not correct, only this one. Need more detailed analyse
    #       There is no difference in --time, --timestamp and --timestamps for some reason
    def test_argument_parse_method_should_set_true_for_timestamp_if_provided(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--timestamps']).timestamps, True
        )

    # TODO: Consider some refactoring of this method later, maybe possible with mock
    def test_argument_parse_method_should_set_file_object_reference_for_file_if_provided(self):
        filename = 'testfile'
        with open(filename, 'w') as f:
            f.write('')
        file = log_filter_util.log_filter_util.argument_parse([filename]).FILE
        self.assertEqual(
            str(file), "<_io.TextIOWrapper name='testfile' mode='r' encoding='UTF-8'>"
        )
        file.close()
        os.remove(filename)

    # Arguments first and last ale mutually exclusive
    def test_argument_parse_method_should_not_take_first_and_last_in_the_same_time(self):
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit):
                log_filter_util.log_filter_util.argument_parse(['--first', '10', '--last', '10'])

    def test_argument_parse_method_should_set_multiple_values_if_provided(self):
        self.assertEqual(
            log_filter_util.log_filter_util.argument_parse(['--timestamps']).timestamps, True
        )


if __name__ == '__main__':
    unittest.main()
