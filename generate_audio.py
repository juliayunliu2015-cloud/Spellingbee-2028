import json
import os
from gtts import gTTS
import time

JSON_FILE = "words.json"
AUDIO_DIR = "audio"

def generate_audio():
    """Generate MP3 files for all words"""
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found. Run extract_to_json.py first")
        return
    
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_words = data['total_words']
    processed = 0
    
    for group in data['groups']:
        group_num = group['group']
        group_dir = os.path.join(AUDIO_DIR, f"group_{group_num}")
        os.makedirs(group_dir, exist_ok=True)
        
        for word_data in group['words']:
            word = word_data['word']
            # Sanitize filename
            safe_name = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_').lower()
            filepath = os.path.join(group_dir, f"{safe_name}.mp3")
            
            if os.path.exists(filepath):
                print(f"[{processed+1}/{total_words}] Skipping: {word}")
            else:
                try:
                    tts = gTTS(text=word, lang='en', slow=False)
                    tts.save(filepath)
                    print(f"[{processed+1}/{total_words}] ✓ Generated: {word}")
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    print(f"[{processed+1}/{total_words}] ✗ Error: {word} - {e}")
            
            processed += 1
    
    print(f"\n✓ Audio generation complete!")
    print(f"✓ Files stored in: {AUDIO_DIR}/")

if __name__ == "__main__":
    generate_audio()
