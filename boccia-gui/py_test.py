import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from control_settings_window import ControlSettingsWindow
from main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Create a QApplication instance

    def setUp(self):
        self.main_window = MainWindow()
        self.main_window.serial_connection = MagicMock()
        self.main_window.statusLabel = MagicMock()

    def test_send_calibration_code_success(self):
        self.main_window.serial_connection.is_open = True
        self.main_window.sendCalibrationCode()
        self.main_window.serial_connection.write.assert_called_once_with(b'8700\n')
        self.main_window.statusLabel.setText.assert_not_called()

    def test_send_calibration_code_exception(self):
        self.main_window.serial_connection.is_open = True
        self.main_window.serial_connection.write.side_effect = Exception('Test exception')
        self.main_window.sendCalibrationCode()
        self.main_window.statusLabel.setText.assert_called_once_with('Status: Error sending calibration code')

    def test_send_calibration_code_no_connection(self):
        self.main_window.serial_connection.is_open = False
        self.main_window.sendCalibrationCode()
        self.main_window.statusLabel.setText.assert_called_once_with('Status: No serial connection')

if __name__ == '__main__':
    unittest.main()
