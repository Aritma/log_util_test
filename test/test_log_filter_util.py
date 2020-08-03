from io import StringIO
import unittest
from unittest.mock import patch

import log_filter_util.log_filter_util


class OutputTest(unittest.TestCase):

    def test_main_method_should_print_string_to_stdout(self):
        with patch('sys.stdout', new=StringIO()) as output_value:
            log_filter_util.log_filter_util.main()
            self.assertEqual(output_value.getvalue(), 'test\n')


if __name__ == '__main__':
    unittest.main()
