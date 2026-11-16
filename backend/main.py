"""
CloudifyOps BFSI Insurance & Contact Center Intelligence Platform
FastAPI Application Backend (Port 8000)
Enterprise Multi-Persona BFSI with Real-time WebRTC & PostgreSQL
"""
import os
import sys

# Ensure project root is in Python sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load .env file (EC2 deployment or local dev)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=False)
except ImportError:
    pass  # python-dotenv not installed – rely on environment vars from Docker Compose

import json
import uuid
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.database import db
from backend.webrtc_signaling import signaling_manager
from backend.lca_simulator import LCA_SCENARIOS, get_scenario_for_caller

app = FastAPI(
    title="CloudifyOps BFSI Intelligence Platform API",
    description="Multilingual BFSI Contact Center with Live AI Analytics, WebRTC & PostgreSQL",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# DATA MODELS
# ----------------------------------------------------------------------------
class CustomerSignupRequest(BaseModel):
    full_name: str
    phone_e164: str
    email: str
    dob: Optional[str] = "1990-01-01"
    gender: Optional[str] = "Male"
    city: Optional[str] = "Mumbai"
    address_state: Optional[str] = "Maharashtra"
    pincode: Optional[str] = "400001"
    aadhaar_last4: Optional[str] = "1234"
    pan_masked: Optional[str] = "ABCDE1234F"

class CustomerLoginRequest(BaseModel):
    phone_e164: str
    password_or_otp: Optional[str] = "123456"

class AgentSignupRequest(BaseModel):
    agent_id: str
    full_name: str
    email: str
    extension: str
    specialization: str
    languages: Optional[str] = "English, Hindi, Hinglish"

class AgentLoginRequest(BaseModel):
    agent_id: str
    password: Optional[str] = "password"

class AgentStatusUpdateRequest(BaseModel):
    status: str # available, on_call, busy, break, offline

class ClaimCreateRequest(BaseModel):
    policy_id: int
    customer_id: int
    claim_type: str
    incident_date: Optional[str] = None
    claim_amount_paise: int
    notes: Optional[str] = None
    call_id: Optional[int] = None

class CardFreezeRequest(BaseModel):
    customer_id: int
    card_last4: str
    reason: str

# ----------------------------------------------------------------------------
# HEALTH
# ----------------------------------------------------------------------------
@app.get("/api/health")
def health_check():
    """EC2 / GitLab CI verify-stage health probe."""
    try:
        db_backend = db.health_check()
    except Exception as e:
        db_backend = f"error: {e}"
    return {
        "status": "ok",
        "version": "2.0.0",
        "service": "CloudifyOps BFSI Enterprise Backend",
        "database": db_backend,
        "webrtc": "active"
    }

# ----------------------------------------------------------------------------
# AUTHENTICATION: CUSTOMER LOGIN & SIGNUP
# ----------------------------------------------------------------------------
@app.post("/api/auth/customer-signup")
def customer_signup(req: CustomerSignupRequest):
    # Check if phone already registered
    existing = db.fetch_one("SELECT * FROM customers WHERE phone_e164 = %s", (req.phone_e164,))
    if existing:
        return {"success": True, "customer": existing, "message": "Account already exists. Logged in successfully."}

    query = """
    INSERT INTO customers (full_name, phone_e164, email, dob, gender, city, address_state, pincode, aadhaar_last4, pan_masked, kyc_status, account_balance_paise)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'verified', 5000000)
    """
    db.execute(query, (
        req.full_name, req.phone_e164, req.email, req.dob, req.gender,
        req.city, req.address_state, req.pincode, req.aadhaar_last4, req.pan_masked
    ))
    new_cust = db.fetch_one("SELECT * FROM customers WHERE phone_e164 = %s", (req.phone_e164,))

    # Auto-assign a starter health or motor policy
    pol_query = """
    INSERT INTO policies (customer_id, policy_number, insurer_name, product_type, product_name, sum_insured_paise, premium_annual_paise, start_date, end_date, status, ncb_percent)
    VALUES (%s, %s, 'CloudifyOps BFSI Shield', 'health', 'CloudifyOps Comprehensive Health Protection', 50000000, 1850000, CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', 'active', 10)
    """
    db.execute(pol_query, (new_cust["customer_id"], f"POL-HLTH-{uuid.uuid4().hex[:6].upper()}"))

    return {"success": True, "customer": new_cust, "message": "Customer registered successfully."}

@app.post("/api/auth/customer-login")
def customer_login(req: CustomerLoginRequest):
    clean_phone = req.phone_e164.strip()
    cust = db.fetch_one("SELECT * FROM customers WHERE phone_e164 LIKE %s", (f"%{clean_phone}%",))
    if not cust:
        # Check by id if numeric
        if clean_phone.isdigit() and len(clean_phone) <= 3:
            cust = db.fetch_one("SELECT * FROM customers WHERE customer_id = %s", (int(clean_phone),))

    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found with this mobile number.")

    policies = db.fetch_all("SELECT * FROM policies WHERE customer_id = %s", (cust["customer_id"],))
    claims = db.fetch_all("SELECT * FROM claims WHERE customer_id = %s", (cust["customer_id"],))

    return {
        "success": True,
        "customer": cust,
        "policies": policies,
        "claims": claims,
        "token": f"jwt_mock_cust_{cust['customer_id']}"
    }

# ----------------------------------------------------------------------------
# AUTHENTICATION: AGENT LOGIN & SIGNUP
# ----------------------------------------------------------------------------
@app.post("/api/auth/agent-signup")
def agent_signup(req: AgentSignupRequest):
    existing = db.fetch_one("SELECT * FROM agents WHERE agent_id = %s", (req.agent_id,))
    if existing:
        return {"success": True, "agent": existing, "message": "Agent ID already exists. Logged in."}

    query = """
    INSERT INTO agents (agent_id, full_name, email, extension, specialization, languages, status)
    VALUES (%s, %s, %s, %s, %s, %s, 'available')
    """
    db.execute(query, (req.agent_id, req.full_name, req.email, req.extension, req.specialization, req.languages))
    new_agent = db.fetch_one("SELECT * FROM agents WHERE agent_id = %s", (req.agent_id,))
    return {"success": True, "agent": new_agent, "message": "Agent registered successfully."}

@app.post("/api/auth/agent-login")
def agent_login(req: AgentLoginRequest):
    agent = db.fetch_one("SELECT * FROM agents WHERE agent_id = %s", (req.agent_id,))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent ID not recognized. Choose AGT-101, AGT-102, or AGT-103.")
    return {
        "success": True,
        "agent": agent,
        "token": f"jwt_mock_agt_{agent['agent_id']}"
    }

# ----------------------------------------------------------------------------
# AGENTS STATUS & REAL-TIME PRESENCE
# ----------------------------------------------------------------------------
@app.get("/api/agents")
def get_agents():
    agents = db.fetch_all("SELECT * FROM agents ORDER BY agent_id ASC")
    return {"agents": agents}

@app.post("/api/agents/{agent_id}/status")
async def update_agent_status(agent_id: str, req: AgentStatusUpdateRequest):
    db.execute("UPDATE agents SET status = %s WHERE agent_id = %s", (req.status, agent_id))
    agent = db.fetch_one("SELECT * FROM agents WHERE agent_id = %s", (agent_id,))
    
    # Update presence in signaling manager and broadcast
    if agent_id in signaling_manager.client_meta:
        signaling_manager.client_meta[agent_id]["status"] = req.status
    await signaling_manager.broadcast_agent_status()
    
    return {"success": True, "agent_id": agent_id, "new_status": req.status}

# ----------------------------------------------------------------------------
# CUSTOMERS API
# ----------------------------------------------------------------------------
@app.get("/api/customers")
def get_customers():
    customers = db.fetch_all("SELECT * FROM customers ORDER BY customer_id ASC")
    return {"customers": customers}

@app.get("/api/customers/{customer_id_or_phone}")
def get_customer(customer_id_or_phone: str):
    clean = customer_id_or_phone.strip()
    if clean.isdigit() and len(clean) < 6:
        cust = db.fetch_one("SELECT * FROM customers WHERE customer_id = %s", (int(clean),))
    else:
        cust = db.fetch_one("SELECT * FROM customers WHERE phone_e164 LIKE %s", (f"%{clean}%",))
    
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")

    policies = db.fetch_all("SELECT * FROM policies WHERE customer_id = %s", (cust["customer_id"],))
    claims = db.fetch_all("SELECT * FROM claims WHERE customer_id = %s", (cust["customer_id"],))

    return {
        "customer": cust,
        "policies": policies,
        "claims": claims
    }

# ----------------------------------------------------------------------------
# POLICIES & CLAIMS API
# ----------------------------------------------------------------------------
@app.get("/api/policies")
def get_policies(customer_id: Optional[int] = None):
    if customer_id:
        policies = db.fetch_all("SELECT * FROM policies WHERE customer_id = %s", (customer_id,))
    else:
        policies = db.fetch_all("SELECT * FROM policies ORDER BY policy_id ASC")
    return {"policies": policies}

@app.get("/api/claims")
def get_claims(customer_id: Optional[int] = None):
    if customer_id:
        claims = db.fetch_all("SELECT * FROM claims WHERE customer_id = %s ORDER BY claim_id DESC", (customer_id,))
    else:
        claims = db.fetch_all("SELECT * FROM claims ORDER BY claim_id DESC")
    return {"claims": claims}

@app.post("/api/claims/fnol")
def create_fnol_claim(claim: ClaimCreateRequest):
    claim_ref = f"CLM-2025-{uuid.uuid4().hex[:6].upper()}"
    incident_date = claim.incident_date or "2026-05-13"
    
    query = """
    INSERT INTO claims (claim_ref, policy_id, customer_id, call_id, claim_type, incident_date, status, claim_amount_paise, notes)
    VALUES (%s, %s, %s, %s, %s, %s, 'registered', %s, %s)
    """
    db.execute(query, (
        claim_ref, claim.policy_id, claim.customer_id, claim.call_id,
        claim.claim_type, incident_date, claim.claim_amount_paise, claim.notes
    ))
    return {
        "success": True,
        "claim_ref": claim_ref,
        "message": f"First Notice of Loss (FNOL) successfully registered under reference {claim_ref}"
    }

@app.post("/api/banking/freeze-card")
def freeze_card(req: CardFreezeRequest):
    return {
        "success": True,
        "status": "frozen",
        "card_last4": req.card_last4,
        "message": f"Debit card ending in {req.card_last4} temporarily locked per RBI Zero-Liability guideline."
    }

@app.post("/api/motor/send-inspection-link")
def send_inspection_link(phone: str = Query(...)):
    return {
        "success": True,
        "phone": phone,
        "inspection_link": f"https://self-inspect.cloudifyops.com/video-kyc/{uuid.uuid4().hex[:8]}",
        "message": "5-Minute AI Self-Inspection video link dispatched via SMS and WhatsApp."
    }

@app.get("/api/hospitals")
def get_hospitals(city: Optional[str] = None):
    if city:
        hospitals = db.fetch_all("SELECT * FROM hospital_network WHERE city = %s", (city,))
    else:
        hospitals = db.fetch_all("SELECT * FROM hospital_network")
    return {"hospitals": hospitals}

@app.get("/api/lca/lookup/{phone}")
def get_lca_screenpop(phone: str):
    scenario = get_scenario_for_caller(phone)
    return scenario

# ----------------------------------------------------------------------------
# WEBRTC WEBSOCKET SIGNALING
# ----------------------------------------------------------------------------
@app.websocket("/ws/signaling/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await signaling_manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await signaling_manager.handle_message(client_id, data)
    except WebSocketDisconnect:
        signaling_manager.disconnect(client_id)
        await signaling_manager.broadcast_agent_status()
    except Exception as e:
        print(f"[WebSocket] Exception with client {client_id}: {e}")
        signaling_manager.disconnect(client_id)

# ----------------------------------------------------------------------------
# STATIC & FRONTEND SERVING (SEPARATED CUSTOMER & AGENT PORTALS)
# ----------------------------------------------------------------------------
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(FRONTEND_DIST):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIST), name="static")

@app.get("/")
def serve_root():
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "CloudifyOps BFSI Intelligence Platform Backend Running. Visit /docs for API schema."}

@app.get("/customer")
def serve_customer_portal():
    cust_path = os.path.join(FRONTEND_DIST, "customer.html")
    if os.path.exists(cust_path):
        return FileResponse(cust_path)
    raise HTTPException(status_code=404, detail="Customer portal page not found")

@app.get("/agent")
def serve_agent_portal():
    agent_path = os.path.join(FRONTEND_DIST, "agent.html")
    if os.path.exists(agent_path):
        return FileResponse(agent_path)
    raise HTTPException(status_code=404, detail="Agent portal page not found")

@app.get("/cloudifyops_logo.png")
def serve_logo():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cloudifyops_logo.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
