
# run.py

import os
from agent.sip_client import SIPClient
from agent.audio_stream import AudioStream
from agent.stt_whisper import transcribe_stream
from agent.tts_coqui import speak_text
from agent.llm_engine import generate_response
from vicidial.call_flow import CallFlowManager
from dotenv import load_dotenv

load_dotenv("config/credentials.env")

def main():
    # Load config
    sip_user = os.getenv("SIP_USERNAME")
    sip_pass = os.getenv("SIP_PASSWORD")
    sip_server = os.getenv("SIP_SERVER")
    vicidial_api_url = os.getenv("VICIDIAL_API_URL")
    vicidial_user = os.getenv("VICIDIAL_USERNAME")
    vicidial_pass = os.getenv("VICIDIAL_PASSWORD")

    # Start Vicidial agent manager
    call_manager = CallFlowManager(api_url=vicidial_api_url, user=vicidial_user, password=vicidial_pass)

    # Register SIP and setup audio
    sip_client = SIPClient(sip_user, sip_pass, sip_server)
    audio_stream = AudioStream()
    sip_client.set_audio_callback(audio_stream.feed_audio)

    print("[*] Starting SIP registration...")
    sip_client.connect()

    print("[*] Waiting for calls...")
    while True:
        if sip_client.call_active:
            call_manager.set_status("TALKING")

            pcm_audio = audio_stream.get_audio()

            print("[>] Transcribing...")
            user_text = transcribe_stream(pcm_audio)

            if not user_text:
                continue

            print(f"[USER]: {user_text}")

            print("[<] Generating AI response...")
            ai_reply = generate_response(user_text)

            print(f"[AI]: {ai_reply}")
            speak_text(ai_reply)

            if "transfer" in user_text.lower():
                print("[*] Initiating transfer...")
                call_manager.transfer_call()

        else:
            call_manager.set_status("PAUSED")

if __name__ == "__main__":
    main()
