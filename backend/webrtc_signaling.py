"""
CloudifyOps BFSI Intelligence Platform - WebRTC Signaling & Telephony Coordinator
Ensures guaranteed delivery of inbound customer calls to active agent softphones.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
import asyncio
import time
from typing import Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect

class SignalingManager:
    def __init__(self):
        # Map client_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Map client_id -> metadata
        self.client_meta: Dict[str, Dict[str, Any]] = {}
        # Active calls: call_uuid -> details
        self.active_calls: Dict[str, Dict[str, Any]] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"[Signaling] Client connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.client_meta:
            del self.client_meta[client_id]
        print(f"[Signaling] Client disconnected: {client_id}")

    async def send_to(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"[Signaling] Error sending to {client_id}: {e}")

    async def broadcast_agent_status(self):
        agents_status = []
        for cid, meta in self.client_meta.items():
            if meta.get("role") == "agent":
                agents_status.append({
                    "agent_id": cid,
                    "name": meta.get("name"),
                    "status": meta.get("status", "available"),
                    "specialization": meta.get("specialization")
                })
        
        for cid, meta in self.client_meta.items():
            if meta.get("role") == "customer":
                await self.send_to(cid, {
                    "type": "agents_update",
                    "agents": agents_status
                })

    async def handle_message(self, client_id: str, raw_data: str):
        try:
            data = json.loads(raw_data)
        except Exception:
            return

        msg_type = data.get("type")
        payload = data.get("payload", {})

        # 1. Register Client
        if msg_type == "register":
            role = payload.get("role", "customer")
            self.client_meta[client_id] = {
                "role": role,
                "name": payload.get("name", "User"),
                "phone": payload.get("phone", ""),
                "specialization": payload.get("specialization", ""),
                "status": "available"
            }
            print(f"[Signaling] Registered {client_id} as {role} ({payload.get('name')})")
            await self.send_to(client_id, {"type": "registered", "client_id": client_id})
            await self.broadcast_agent_status()

        # 2. Inbound Customer Call -> Agent Softphone
        elif msg_type == "initiate_call":
            target_agent = payload.get("target_agent_id")
            caller_phone = payload.get("caller_phone")
            customer_name = payload.get("customer_name")
            call_uuid = payload.get("call_uuid", f"CALL-{client_id}-{int(time.time())}")

            print(f"[Signaling] Inbound call from '{customer_name}' ({caller_phone}) -> Target: '{target_agent}'")

            # Find recipient agent(s)
            recipient_agents = []
            if target_agent in self.active_connections:
                recipient_agents.append(target_agent)
            else:
                # If the exact target agent isn't connected, route to ANY connected agent!
                for cid, meta in self.client_meta.items():
                    if meta.get("role") == "agent" and cid in self.active_connections:
                        recipient_agents.append(cid)

            if recipient_agents:
                self.active_calls[call_uuid] = {
                    "call_uuid": call_uuid,
                    "caller_id": client_id,
                    "callee_id": recipient_agents[0],
                    "caller_phone": caller_phone,
                    "customer_name": customer_name,
                    "status": "ringing"
                }

                # Ring the agent's softphone console
                for agt in recipient_agents:
                    await self.send_to(agt, {
                        "type": "incoming_call",
                        "payload": {
                            "call_uuid": call_uuid,
                            "caller_id": client_id,
                            "caller_phone": caller_phone,
                            "customer_name": customer_name
                        }
                    })

                # Notify caller that agent softphone is ringing
                await self.send_to(client_id, {
                    "type": "call_ringing",
                    "payload": {"call_uuid": call_uuid, "agent_id": recipient_agents[0]}
                })
            else:
                print(f"[Signaling] No agents online to receive call.")
                await self.send_to(client_id, {
                    "type": "call_failed",
                    "payload": {"reason": "All agents are currently offline. Please ensure the Agent Portal is open."}
                })

        # 3. Agent Accepts Call
        elif msg_type == "accept_call":
            call_uuid = payload.get("call_uuid")
            call_info = self.active_calls.get(call_uuid)
            if call_info:
                call_info["status"] = "connected"
                call_info["callee_id"] = client_id
                caller_id = call_info["caller_id"]
                
                # Notify customer that call is accepted
                await self.send_to(caller_id, {
                    "type": "call_accepted",
                    "payload": {"call_uuid": call_uuid, "agent_id": client_id}
                })
                # Confirm to agent
                await self.send_to(client_id, {
                    "type": "call_started",
                    "payload": {
                        "call_uuid": call_uuid,
                        "caller_id": caller_id,
                        "caller_phone": call_info["caller_phone"],
                        "customer_name": call_info["customer_name"]
                    }
                })

        # 4. Agent Rejects Call
        elif msg_type == "reject_call":
            call_uuid = payload.get("call_uuid")
            call_info = self.active_calls.get(call_uuid)
            if call_info:
                caller_id = call_info["caller_id"]
                await self.send_to(caller_id, {
                    "type": "call_rejected",
                    "payload": {"call_uuid": call_uuid, "reason": "Agent declined call."}
                })
                self.active_calls.pop(call_uuid, None)

        # 5. WebRTC SDP Offer
        elif msg_type == "webrtc_offer":
            call_uuid = payload.get("call_uuid")
            target_id = payload.get("target_id")
            if not target_id and call_uuid and call_uuid in self.active_calls:
                target_id = self.active_calls[call_uuid]["callee_id"]
            if target_id:
                await self.send_to(target_id, {
                    "type": "webrtc_offer",
                    "payload": {
                        "sdp": payload.get("sdp"),
                        "from_id": client_id,
                        "call_uuid": call_uuid
                    }
                })

        # 6. WebRTC SDP Answer
        elif msg_type == "webrtc_answer":
            call_uuid = payload.get("call_uuid")
            target_id = payload.get("target_id")
            if not target_id and call_uuid and call_uuid in self.active_calls:
                target_id = self.active_calls[call_uuid]["caller_id"]
            if target_id:
                await self.send_to(target_id, {
                    "type": "webrtc_answer",
                    "payload": {
                        "sdp": payload.get("sdp"),
                        "from_id": client_id,
                        "call_uuid": call_uuid
                    }
                })

        # 7. ICE Candidate Exchange
        elif msg_type == "ice_candidate":
            call_uuid = payload.get("call_uuid")
            target_id = payload.get("target_id")
            if not target_id and call_uuid and call_uuid in self.active_calls:
                call_info = self.active_calls[call_uuid]
                target_id = call_info["callee_id"] if client_id == call_info["caller_id"] else call_info["caller_id"]
            if target_id:
                await self.send_to(target_id, {
                    "type": "ice_candidate",
                    "payload": {
                        "candidate": payload.get("candidate"),
                        "from_id": client_id,
                        "call_uuid": call_uuid
                    }
                })

        # 8. Hangup / End Call
        elif msg_type == "hangup_call":
            call_uuid = payload.get("call_uuid")
            call_info = self.active_calls.get(call_uuid)
            if call_info:
                other_id = call_info["callee_id"] if client_id == call_info["caller_id"] else call_info["caller_id"]
                await self.send_to(other_id, {
                    "type": "call_ended",
                    "payload": {"call_uuid": call_uuid}
                })
                await self.send_to(client_id, {
                    "type": "call_ended",
                    "payload": {"call_uuid": call_uuid}
                })
                self.active_calls.pop(call_uuid, None)

        # 9. Live Microphone Speech Utterance Relay (Between Customer & Agent)
        elif msg_type == "live_speech_utterance":
            call_uuid = payload.get("call_uuid")
            target_id = None
            if call_uuid and call_uuid in self.active_calls:
                call_info = self.active_calls[call_uuid]
                target_id = call_info["callee_id"] if client_id == call_info["caller_id"] else call_info["caller_id"]
            elif "target_id" in payload:
                target_id = payload.get("target_id")

            if target_id:
                await self.send_to(target_id, {
                    "type": "live_speech_utterance",
                    "payload": payload
                })

signaling_manager = SignalingManager()
