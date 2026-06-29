import cv2

def apply_blur(frame, kernel_size=(99, 99), sigma_x=30):
    """Mengaplikasikan Gaussian Blur ke seluruh frame."""
    return cv2.GaussianBlur(frame, kernel_size, sigma_x)

def add_status_text(frame, text="✌️ Peace Detected!"):
    """Menambahkan teks indikator ke frame."""
    # OpenCV tidak mendukung karakter emoji secara bawaan pada cv2.putText, 
    # jadi kita gunakan teks standar "Peace Detected!"
    clean_text = text.replace("✌️ ", "")
    cv2.putText(
        frame, 
        clean_text, 
        (20, 50), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (0, 255, 0), 
        2, 
        cv2.LINE_AA
    )
    return frame

