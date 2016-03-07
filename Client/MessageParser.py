import json

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass
            # Response not valid

    def parse_error(self, payload):
        self.payload = payload[0].get('error', '')

    def parse_info(self, payload):
        self.payload = payload[1].get('info', '')

    def parse_history(self, payload):
        self.payload = payload[2].get('msg', '')
    # Include more methods for handling the different responses...
