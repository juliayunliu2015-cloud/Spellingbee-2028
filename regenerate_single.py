#!/usr/bin/env python3
import os
from gtts import gTTS
import time

# Create audio directory if it doesn't exist
os.makedirs('audio/group_10', exist_ok=True)

# Regenerate the specific word
word = "pouring"
output_file = f'audio/group_10/{word.lower()}.mp3'

try:
    tts = gTTS(text=word, lang='en', slow=False)
    tts.save(output_file)
    print(f'✓ Generated: {output_file}')
except Exception as e:
    print(f'✗ Error generating {word}: {e}')

time.sleep(0.5)
print('Done!')
