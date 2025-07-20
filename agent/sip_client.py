# Handles SIP registration and RTP
# agent/sip_client.py

import pjsua as pj
import threading

class SIPClient:
    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.server = server
        self.call_active = False
        self.audio_callback = None
        self.lib = pj.Lib()

    def set_audio_callback(self, callback):
        self.audio_callback = callback

    def connect(self):
        self.lib.init(log_cfg=pj.LogConfig(level=3))
        transport = self.lib.create_transport(pj.TransportType.UDP)
        self.lib.start()

        acc_cfg = pj.AccountConfig(domain=self.server, username=self.username, password=self.password)
        acc_cfg.id = f"sip:{self.username}@{self.server}"
        acc_cfg.reg_uri = f"sip:{self.server}"
        self.account = self.lib.create_account(acc_cfg)

        print(f"[*] SIP account created: {acc_cfg.id}")

        self.lib.set_null_snd_dev()

        self.acc_cb = SIPAccountCallback(self)
        self.account.set_callback(self.acc_cb)

        # Keep app running
        self.thread = threading.Thread(target=self.lib_handle_events)
        self.thread.start()

    def lib_handle_events(self):
        while True:
            self.lib.handle_events(timeout=0.5)

    def hangup(self):
        if hasattr(self, 'current_call'):
            self.current_call.hangup()

class SIPAccountCallback(pj.AccountCallback):
    def __init__(self, client):
        pj.AccountCallback.__init__(self, client.account)
        self.client = client

    def on_incoming_call(self, call):
        print("[*] Incoming call...")
        self.client.call_active = True
        self.client.current_call = call
        call.set_callback(CallCallback(self.client))
        call.answer(200)

class CallCallback(pj.CallCallback):
    def __init__(self, client):
        pj.CallCallback.__init__(self, client.current_call)
        self.client = client

    def on_media_state(self):
        call = self.call
        if call.info().media_state == pj.MediaState.ACTIVE:
            call_slot = call.info().conf_slot
            self.client.lib.conf_connect(call_slot, 0)
            self.client.lib.conf_connect(0, call_slot)
            print("[*] Audio connected.")
        else:
            print("[*] Media inactive.")

    def on_state(self):
        print(f"[!] Call state: {self.call.info().state_text}")
        if self.call.info().state == pj.CallState.DISCONNECTED:
            self.client.call_active = False
            self.client.hangup()

