import unittest
import os
from localify import (
    l,
    set_language,
    load_translations,
    set_missing_key_behavior,
    enable_logging,
    config,
    DEBUG,
    INFO,
    WARNING
)


class TestLocalify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the path to the test locales directory
        cls.locales_path = 'locales'
        load_translations(cls.locales_path)
        set_language('en')  # Set default language for tests

    def setUp(self):
        # Reset configurations before each test to ensure test isolation
        set_language('en')
        set_missing_key_behavior('key')

    def test_basic_translation(self):
        message = l("hello").space().l("world").exclamation()
        self.assertEqual(str(message), "Hello World!")

        set_language('it')
        message = l("hello").space().l("world").exclamation()
        self.assertEqual(str(message), "Ciao Mondo!")

    def test_missing_key_default_behavior(self):
        message = l("nonexistent_key")
        self.assertEqual(str(message), "nonexistent_key")

    def test_missing_key_with_default_value(self):
        set_missing_key_behavior('default', default_value='[MISSING]')
        message = l("nonexistent_key")
        self.assertEqual(str(message), "[MISSING]")

    def test_logging_missing_key(self):
        enable_logging(level=DEBUG)
        set_missing_key_behavior('log')
        set_language('it')
        with self.assertLogs('localify', level='WARNING') as cm:
            message = l("nonexistent_key")
            self.assertEqual(str(message), "nonexistent_key")
            # Check if the expected log message is in the output
            self.assertIn("Missing translation key 'nonexistent_key' for language 'it'.", cm.output[0])

    def test_config_function(self):
        config(
            language='en',
            missing_key_behavior='default',
            default_missing_value='[NOT FOUND]',
            logging_level=INFO
        )
        message = l("nonexistent_key")
        self.assertEqual(str(message), "[NOT FOUND]")

    def test_loading_custom_translations(self):
        # Reset missing key behavior
        set_missing_key_behavior('key')

        # Create a custom locales directory for testing
        custom_locales_path = os.path.join(os.path.dirname(__file__), 'custom_locales')
        load_translations(custom_locales_path)
        set_language('en')
        message = l("custom_key")
        self.assertEqual(str(message), "custom_key")


if __name__ == '__main__':
    unittest.main()
