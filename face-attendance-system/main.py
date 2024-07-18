import os
import cv2
import face_recognition
from PIL import Image
import numpy as np
from io import BytesIO
import base64

import sys
sys.path.insert(1, 'Silent-Face-Anti-Spoofing-master')

# import util
import test
from test import test
from db_operations import DBOperations

class App:
    def __init__(self):
        self.db_operations = DBOperations()

    def process_image(self, image_data):
        img = Image.open(BytesIO(base64.b64decode(image_data)))
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return frame

    def find_matching_user(self, frame):
        embeddings_unknown = face_recognition.face_encodings(frame)
        if not embeddings_unknown:
            return None, 'no_persons_found'
        
        embeddings_unknown = embeddings_unknown[0]
        all_users = self.db_operations.get_all_user_embeddings()
        known_embeddings = [user['embeddings'] for user in all_users]
        known_names = [user['name'] for user in all_users]
        
        matches = face_recognition.compare_faces(known_embeddings, embeddings_unknown)
        face_distances = face_recognition.face_distance(known_embeddings, embeddings_unknown)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return known_names[best_match_index], None
        else:
            return None, 'unknown_person'

    def login(self, image_data):
        frame = self.process_image(image_data)
        label = test(
            image=frame,
            model_dir='C:/Users/DELL/Desktop/FACE API/Silent-Face-Anti-Spoofing-master/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:
            name, error = self.find_matching_user(frame)
            if error:
                return error, False
            else:
                self.db_operations.log_login_logout(name, 'in')
                return f'Welcome, {name}.', True
        else:
            return 'You are fake!', False

    def logout(self, image_data):
        frame = self.process_image(image_data)
        label = test(
            image=frame,
            model_dir='C:/Users/DELL/Desktop/FACE API/Silent-Face-Anti-Spoofing-master/resources/anti_spoof_models',
            device_id=0
        )

        if label == 1:
            name, error = self.find_matching_user(frame)
            if error:
                return error, False
            else:
                self.db_operations.log_login_logout(name, 'out')
                return f'Goodbye, {name}.', True
        else:
            return 'You are fake!', False

    def register_new_user(self, image_data, name):
        frame = self.process_image(image_data)
        embeddings = face_recognition.face_encodings(frame)[0].tolist()
        self.db_operations.insert_user(name, embeddings)
        return 'User was registered successfully!'
