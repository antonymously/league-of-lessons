'''
Utilities
'''
import time

def fake_stream_text(text, delay = 0.05):
    for char in text:
        yield char
        time.sleep(delay)