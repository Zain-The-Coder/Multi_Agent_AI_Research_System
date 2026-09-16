import time
from google.genai.errors import ServerError

def invoke_with_retry(runnable, payload, retries=4, delay=15):
    for attempt in range(retries):
        try:
            return runnable.invoke(payload)
        except ServerError as e:
            if attempt < retries - 1:
                print(f"⚠️ Model busy hai (503), {delay}s baad retry ({attempt+1}/{retries})...")
                time.sleep(delay)
            else:
                raise