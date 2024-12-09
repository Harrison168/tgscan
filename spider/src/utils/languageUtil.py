#!/usr/bin/env python
# -*- encoding: utf-8 -*-



import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import text


language_detector_model_path = "spider/resources/language_detector.tflite"


class LanguageUtil:

    language_detector = None

    def __init__(self):
        language_detector_base_options = python.BaseOptions(model_asset_path=language_detector_model_path)
        language_detector_options = text.LanguageDetectorOptions(base_options=language_detector_base_options)
        self.language_detector = text.LanguageDetector.create_from_options(language_detector_options)


    def detect_language(self, text):
        language_code = "en"
        detection_result = self.language_detector.detect(text)
        if len(detection_result.detections)>0:
            # print(f'{detection_result.detections[0].language_code}: '
            #       f'({detection_result.detections[0].probability:.2f})')
            language_code = detection_result.detections[0].language_code

        return language_code







