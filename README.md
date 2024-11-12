
# 📄 Factura Automation
This project, Factura Automation, is written in Python and serves as a proof of concept for automating the digitization of handwritten invoices (spanish: factura) for Matchpoint Sports Canarias. It enables users to photograph, process, and store invoice data in Google Sheets. Note: This tool is solely intended as a demonstration and is not intended for production use or as a commissioned tool.

## ⚙️ Project Overview
The project encompasses several components:

A mobile phone camera-style UI:
- Home Screen with a camera and a button to capture photos
- Settings Screen for customization
- Gallery Screen displaying all captured photos

A python backend:
- Camera
- Gallery including a watchdog
- Image Processor
- Settings Manager
- Google Sheets Manager

### Technical Workflow
1. UI: The responsive user interface is developed with Tkinter, mirroring the familiar layout of a camera app.
2. Image Capture: Using the OpenCV (cv2) and Pillow library, the app captures images, adds metadata (e.g., “Status”), and stores the images.
3. Image Queue: Captured images are added to an image queue for background processing in a separate thread, allowing the UI to remain responsive. Unprocessed images are automatically reloaded into the image queue upon startup if the app is closed before completion.
4. Preprocessing:
	- The image is processed with SIFT and a FLANN-based matcher to detect and align the invoice based on a blank template.
	- A homography is calculated to warp the detected invoice corners, creating a straightened, 4:3 aspect image regardless of photo perspective.
5. Analysis with OpenAI:
The preprocessed image is analyzed using OpenAI’s GPT-4 API (Vision) with a structured prompt and response schema for consistent output.
6. Data Storage: Extracted information is stored in Google Sheets using the Google Sheets API, formatted as required. Digitalization of the invoices is complete.

## 🚀 How to Run This Project
[Instructions to be added]

## ⚠️ Legal Disclaimer on OpenAI API Usage
This project is intended strictly for testing and demonstration purposes as a proof of concept. It is not designed for production use or for processing real, sensitive data. No actual invoices or personal data are sent to the OpenAI API in this project.
