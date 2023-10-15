class CustomHTTPError(Exception):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"HTTP Error {status_code}: {response_text}")
