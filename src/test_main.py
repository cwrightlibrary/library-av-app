import unittest
from unittest.mock import patch
from main import AVApp

class TestAVApp(unittest.TestCase):
    def setUp(self):
        self.app = AVApp()

    def tearDown(self):
        self.app.destroy()

    def test_setup_menubar(self):
        self.app.setup_menubar()
        self.assertIsNotNone(self.app.MENUBAR)
        self.assertIsNotNone(self.app.FILE_MENU)
        self.assertIsNotNone(self.app.EDIT_MENU)
        self.assertIsNotNone(self.app.HELP_MENU)

    @patch('main.filedialog.askopenfile')
    def test_open_csv(self, mock_askopenfile):
        mock_file = open('test.csv', 'w')
        mock_askopenfile.return_value = mock_file
        self.app.open_csv()
        self.assertIsNotNone(self.app.df)
        self.assertEqual(self.app.current_file_path, mock_file)

    # Add more test cases for other methods...

if __name__ == '__main__':
    unittest.main()