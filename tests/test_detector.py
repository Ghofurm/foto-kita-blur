import unittest
from unittest.mock import MagicMock
import sys
import os

# Menambahkan direktori src ke sys.path agar modul bisa di-import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from detector import HandDetector

class TestHandDetector(unittest.TestCase):
    def setUp(self):
        # Inisialisasi detector
        self.detector = HandDetector()

    def test_is_peace_sign_true(self):
        # Mock 21 landmarks tangan
        landmarks = [MagicMock() for _ in range(21)]
        
        # Atur koordinat Y untuk mensimulasikan jari telunjuk & tengah terbuka, manis & kelingking tertutup
        landmarks[6].y = 0.5   # Index PIP
        landmarks[8].y = 0.3   # Index TIP (di atas PIP -> terbuka)
        landmarks[10].y = 0.5  # Middle PIP
        landmarks[12].y = 0.3  # Middle TIP (di atas PIP -> terbuka)
        landmarks[14].y = 0.5  # Ring PIP
        landmarks[16].y = 0.7  # Ring TIP (di bawah PIP -> tertutup)
        landmarks[18].y = 0.5  # Pinky PIP
        landmarks[20].y = 0.7  # Pinky TIP (di bawah PIP -> tertutup)

        self.assertTrue(self.detector.is_peace_sign(landmarks))

    def test_is_peace_sign_false(self):
        # Mock 21 landmarks tangan (semua jari terbuka / kepalan tangan)
        landmarks = [MagicMock() for _ in range(21)]
        for lm in landmarks:
            lm.y = 0.5

        self.assertFalse(self.detector.is_peace_sign(landmarks))

    def tearDown(self):
        self.detector.close()

if __name__ == '__main__':
    unittest.main()

