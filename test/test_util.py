from io import StringIO
from unittest.mock import patch
import os
import unittest

import log_filter_util.util


class OutputTest(unittest.TestCase):

    # Argument parsing tests because args are defined in specification
    def test_argument_parse_method_should_set_value_for_first_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['-f', '10']).first, 10
        )

    def test_argument_parse_method_should_set_value_for_first_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--first', '10']).first, 10
        )

    def test_argument_parse_method_should_set_value_for_last_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['-l', '10']).last, 10
        )

    def test_argument_parse_method_should_set_value_for_last_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--last', '10']).last, 10
        )

    def test_argument_parse_method_should_set_true_for_ipv4_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['-i']).ipv4, True
        )

    def test_argument_parse_method_should_set_true_for_ipv4_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--ipv4']).ipv4, True
        )

    def test_argument_parse_method_should_set_true_for_ipv6_if_provided_in_short_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['-I']).ipv6, True
        )

    def test_argument_parse_method_should_set_true_for_ipv6_if_provided_in_long_variant(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--ipv6']).ipv6, True
        )

    # TODO: This option parsing is not correct, only this one. Need more detailed analyse
    #       There is no difference in --time, --timestamp and --timestamps for some reason
    def test_argument_parse_method_should_set_true_for_timestamp_if_provided(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--timestamps']).timestamps, True
        )

    # TODO: Consider some refactoring of this method later, maybe possible with mock
    def test_argument_parse_method_should_set_file_object_reference_for_file_if_provided(self):
        filename = 'testfile'
        with open(filename, 'w') as f:
            f.write('')
        file = log_filter_util.util.argument_parse([filename]).FILE
        self.assertEqual(
            str(file), "<_io.TextIOWrapper name='testfile' mode='r' encoding='UTF-8'>"
        )
        file.close()
        os.remove(filename)

    # Arguments first and last ale mutually exclusive
    def test_argument_parse_method_should_not_take_first_and_last_in_the_same_time(self):
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit):
                log_filter_util.util.argument_parse(['--first', '10', '--last', '10'])

    def test_argument_parse_method_should_set_multiple_values_if_provided(self):
        self.assertEqual(
            log_filter_util.util.argument_parse(['--timestamps']).timestamps, True
        )

    # get_data_content function tests
    def test_data_content_should_equal_to_lines_of_stdin_if_provided(self):
        with patch('sys.stdin', new=StringIO('1\n2\n3\n')):
            self.assertEqual(
                log_filter_util.util.get_data_content(
                    log_filter_util.util.argument_parse([])
                ), ['1\n', '2\n', '3\n']
            )

    def test_data_content_should_equal_to_lines_of_file_if_provided(self):
        filename = 'testfile'
        with open(filename, 'w') as f:
            f.write('1\n2\n3\n')
        args = log_filter_util.util.argument_parse([filename])
        file = args.FILE
        self.assertEqual(
            log_filter_util.util.get_data_content(args), ['1\n', '2\n', '3\n']
        )
        file.close()
        os.remove(filename)

    # contains_timestamp function tests
    def test_contains_timestamp_should_return_true_if_timestamp_00_00_00_exists_in_line(self):
        self.assertTrue(log_filter_util.util.contains_timestamp('00:00:00-TEST'))

    def test_contains_timestamp_should_return_true_if_timestamp_23_59_59_exists_in_line(self):
        self.assertTrue(log_filter_util.util.contains_timestamp('TEST23:59:59TEST'))

    def test_contains_timestamp_should_return_false_if_invalid_timestamp_exists_in_line(self):
        self.assertFalse(log_filter_util.util.contains_timestamp('24:30:61-TEST'))

    def test_contains_timestamp_should_return_false_if_timestamp_do_not_exists_in_line(self):
        self.assertFalse(log_filter_util.util.contains_timestamp('TEST-TEST'))

    # get_ipv4_part tests
    def test_get_ipv4_part_should_return_ipv4_string_if_valid_address_exists_in_mid_of_line(self):
        self.assertEqual(log_filter_util.util.get_ipv4_part('TEST10.20.30.40TEST'), '10.20.30.40')

    def test_get_ipv4_part_should_return_ipv4_string_if_valid_address_exists_at_start_of_line(self):
        self.assertEqual(log_filter_util.util.get_ipv4_part('10.20.30.40TEST'), '10.20.30.40')

    def test_get_ipv4_part_should_return_ipv4_string_if_valid_address_exists_in_end_of_line(self):
        self.assertEqual(log_filter_util.util.get_ipv4_part('TEST10.20.30.40'), '10.20.30.40')

    def test_get_ipv4_part_should_return_none_if_invalid_address_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv4_part('TEST10.20.30.400'), None)

    def test_get_ipv4_part_should_return_none_if_no_address_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv4_part('TEST-TEST'), None)

    # get_ipv6_part tests
    def test_get_ipv6_part_should_return_ipv6_string_if_valid_address_with_noncapitals_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv6_part(
            'TEST-2001:0db8:85a3:0000:0000:8a2e:0370:7334-TEST'), '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        )

    def test_get_ipv6_part_should_return_ipv6_string_if_valid_address_with_capitals_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv6_part(
            'TEST-2001:0DB8:85A3:0000:0000:8A2E:0370:7334-TEST'), '2001:0DB8:85A3:0000:0000:8A2E:0370:7334'
        )

    def test_get_ipv6_part_should_return_none_if_invalid_address_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv6_part(
            'TEST-2001:0DB8:WXYZ:0000:0000:8A2E:0370:7334-TEST'), None
        )

    def test_get_ipv6_part_should_return_none_if_no_address_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv6_part(
            'TEST-TEST'), None
        )

    def test_get_ipv6_part_should_return_none_if_non_standard_address_exists_in_line(self):
        self.assertEqual(log_filter_util.util.get_ipv6_part(
            'TEST-2001:DB8:WXYZ::8A2E:370:7334-TEST'), None
        )


if __name__ == '__main__':
    unittest.main()
