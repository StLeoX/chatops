import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


class RequestMocker:
    DATA_FOLDER = 'user_data'
    user_data = {}  # Dictionary to store loaded user data

    @classmethod
    def load_user_data(cls, user_id):
        file_path = os.path.join(cls.DATA_FOLDER, f'user_{user_id}.json')
        with open(file_path, 'r') as file:
            user_data = json.load(file)
        return user_data

    @classmethod
    def load_all_user_data(cls):
        user_data = {}
        for file_name in os.listdir(cls.DATA_FOLDER):
            if file_name.endswith('.json'):
                user_id = file_name.split('_')[1].split('.')[0]
                user_data[user_id] = cls.load_user_data(user_id)
        return user_data

    @classmethod
    def extract_request(cls, user_id):
        if not cls.user_data:
            cls.user_data = cls.load_all_user_data()

        user_data = cls.user_data.get(user_id, {})
        extracted_data = user_data.get('key_to_extract', None)
        return jsonify({'extracted_data': extracted_data})

    @classmethod
    def simulate_post_request(cls, user_id, payload):
        if not cls.user_data:
            cls.user_data = cls.load_all_user_data()

        cls.user_data[user_id].update(payload)

        return jsonify({'message': 'POST request simulated successfully'})

    @classmethod
    def simulate_delete_request(cls, user_id):
        if not cls.user_data:
            cls.user_data = cls.load_all_user_data()

        deleted_data = cls.user_data.pop(user_id, None)

        return jsonify({'message': 'DELETE request simulated successfully', 'deleted_data': deleted_data})

    @classmethod
    def _echo_request_category(cls, user_id, category):
        if not cls.user_data:
            cls.user_data = cls.load_all_user_data()

        user_data = cls.user_data.get(user_id, {}).get(category, {})
        return jsonify(user_data)

    @classmethod
    def echo_request_workflow(cls, user_id):
        return cls._echo_request_category(user_id, 'workflow')

    @classmethod
    def echo_request_fault_config(cls, user_id):
        return cls._echo_request_category(user_id, 'fault_config')

    @classmethod
    def echo_request_fault_play(cls, user_id):
        return cls._echo_request_category(user_id, 'fault_play')

    @classmethod
    def echo_request_record(cls, user_id):
        return cls._echo_request_category(user_id, 'record')

    @classmethod
    def get_value_by_key(cls, user_id, key, category=None):
        if not cls.user_data:
            cls.user_data = cls.load_all_user_data()

        user_data = cls.user_data.get(user_id, {})

        # Use _echo_request_category if category is provided
        if category:
            user_data = user_data.get(category, {})

        value = user_data.get(key, None)
        return value
