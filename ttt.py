import cv2
import tkinter as tk
from tkinter import messagebox
import threading
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import webbrowser


class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")

        # Initialize the camera
        self.cap = cv2.VideoCapture(0)
        self.video_source = 0
        self.scanning = False

        # Create a label to display the video feed
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Create a label to display QR code data
        self.qr_info_label = tk.Label(root, text="Scan a QR code", font=("Arial", 14))
        self.qr_info_label.pack(pady=20)

        # Create a button to start/stop scanning
        self.scan_button = tk.Button(root, text="Start Scanning", command=self.toggle_scanning)
        self.scan_button.pack(pady=10)

    def toggle_scanning(self):
        """Start or stop the camera scanning based on current state."""
        if self.scanning:
            self.scanning = False
            self.scan_button.config(text="Start Scanning")
        else:
            self.scanning = True
            self.scan_button.config(text="Stop Scanning")
            self.start_scanning()

    def start_scanning(self):
        """Start the video feed and continuously scan for QR codes."""
        while self.scanning:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Decode the QR codes in the current frame
            decoded_objects = decode(frame)

            # Check if we found any QR codes
            for obj in decoded_objects:
                # Extract the data from the QR code
                qr_data = obj.data.decode("utf-8")

                # Display the QR data on the label
                self.qr_info_label.config(text=f"Scanned Data: {qr_data}")

                # If the QR code is a URL, open it in the web browser
                if qr_data.startswith("http://") or qr_data.startswith("https://"):
                    self.open_url(qr_data)

            # Convert the frame to an image format compatible with Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)

            # Update the video feed label
            self.video_label.config(image=img)
            self.video_label.image = img

            self.root.update_idletasks()
            self.root.update()

        self.cap.release()

    def open_url(self, url):
        """Open the scanned URL in the default web browser."""
        webbrowser.open(url)

    def on_close(self):
        """Release the camera and close the application."""
        self.scanning = False
        self.cap.release()
        self.root.quit()


if __name__ == "__main__":
    # Set up the Tkinter window
    root = tk.Tk()
    app = QRCodeScannerApp(root)

    # Make sure to handle window close events properly
    root.protocol("WM_DELETE_WINDOW", app.on_close)

    # Run the app
    root.mainloop()

