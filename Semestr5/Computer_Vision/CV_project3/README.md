# Image Inpainting Using Deep Learning

## Project Overview
This project focuses on image inpainting, where missing parts of an image are reconstructed using deep learning techniques. Our goal is to train a neural network model to restore missing regions in human face images by learning patterns from complete images. This project was carried out during Computer Vision course on AI Vth sem on PUT.

## Dataset Description
We used the Human Faces dataset from Kaggle, which contains over 7,000 images representing diverse human faces across different ages, ethnicities, and profiles.

## Preprocessing Steps
Each image was modified by adding a 50x50 pixel black square at a random location to simulate missing data.
To introduce variability, random augmentations (e.g., flipping, rotation, brightness adjustments) were applied to some images.

## Project Goals
Train a deep learning model to restore missing image regions with high accuracy.
Ensure realistic and seamless inpainting by leveraging advanced computer vision techniques.
Experiment with different neural network architectures to improve performance.

## Technologies & Libraries Used
Python (Main programming language)
NumPy, Pandas (Data handling & preprocessing)
OpenCV (cv2), PIL (Image manipulation & processing)
Matplotlib.pyplot (Visualization)
Scikit-learn (sklearn) (Data analysis & utilities)
Albumentations (Data augmentation)
TensorFlow (Deep learning framework)

## Expected Outcomes
A trained deep learning model capable of realistically filling missing regions in images.
Insights into best-performing architectures for inpainting tasks.
Potential future improvements such as higher resolution inpainting or real-time restoration.

## Usage Instructions
Run the preprocessing script to generate masked images.
Train the neural network model using the dataset.
Evaluate the model on test images.
Visualize the inpainting results and analyze performance metrics.

---
**Authors**: Piotr Balewski 156037, Kuba Czech 156035
**Date**: January 2025
