import cv2
import sys
import time
from camera import Camera
from detector import HandDetector
from effects import apply_blur

def main():
    print("Memulai Foto Kita Blur...")
    print("Tekan 'Q' atau 'ESC' di jendela kamera untuk keluar.")

    camera = Camera(device_id=0, width=640, height=480)
    detector = HandDetector()

    try:
        camera.start()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    window_name = "Foto Kita Blur"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    waktu_terakhir_deteksi = 0
    blur_delay = 1.0  # Durasi blur bertahan dalam detik (cooldown)

    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            print("Gagal membaca frame dari kamera.")
            break

        # Horizontal flip agar terasa seperti cermin
        frame = cv2.flip(frame, 1)

        # Deteksi gestur peace sign
        is_peace = detector.detect_peace_sign(frame)
        waktu_sekarang = time.time()

        if is_peace:
            waktu_terakhir_deteksi = waktu_sekarang

        # Apply efek jika peace sign terdeteksi atau masih dalam batas delay
        if is_peace or (waktu_sekarang - waktu_terakhir_deteksi < blur_delay):
            frame = apply_blur(frame)

        cv2.imshow(window_name, frame)

        # Tunggu input tombol (Q atau ESC untuk keluar)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 27:
            break

    # Cleanup
    print("Menutup aplikasi...")
    camera.release()
    detector.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
