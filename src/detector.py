import cv2
import os
import mediapipe as mp
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        # 1. Tentukan path ke model file (relative terhadap file detector.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "..", "assets", "hand_landmarker.task")
        model_path = os.path.abspath(model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file tidak ditemukan di: {model_path}")

        # 2. Buat options
        options = vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.IMAGE,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        # 3. Buat landmarker
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def detect_peace_sign(self, frame):
        # 1. Convert BGR ke RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 2. Buat mp.Image dari array RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 3. Detect
        result = self.landmarker.detect(mp_image)

        # 4. Cek result.hand_landmarks (list of list)
        if not result.hand_landmarks:
            return False

        # 5. Loop tiap tangan, panggil is_peace_sign(landmarks)
        for landmarks in result.hand_landmarks:
            if self.is_peace_sign(landmarks):
                return True

        return False

    def is_peace_sign(self, landmarks):
        # MediaPipe landmark index:
        # Index finger: TIP=8, PIP=6
        # Middle finger: TIP=12, PIP=10
        # Ring finger: TIP=16, PIP=14
        # Pinky finger: TIP=20, PIP=18
        
        index_open = landmarks[8].y < landmarks[6].y
        middle_open = landmarks[12].y < landmarks[10].y
        ring_closed = landmarks[16].y > landmarks[14].y
        pinky_closed = landmarks[20].y > landmarks[18].y

        return index_open and middle_open and ring_closed and pinky_closed

    def close(self):
        self.landmarker.close()
