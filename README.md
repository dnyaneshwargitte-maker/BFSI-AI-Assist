# 🏢 CloudifyOps BFSI Insurance & Contact Center Intelligence Platform

An enterprise-grade, Indian BFSI (Banking, Financial Services, and Insurance) Contact Center with **Live AI Analytics (LCA)**, **WebRTC Voice Calling**, **Screen-Pop Intelligence**, **Bedrock Generative AI Summarization (Claude 3.5 Sonnet)**, and a **12-Table PostgreSQL 15 Database Schema**.

Designed specifically for **Hinglish/Hindi/English** multilingual customer service compliant with **RBI** and **IRDAI** standards, with a lean single-instance deployment architecture running on **EC2 (t3.medium)** that completely eliminates the idle AWS NAT Gateway ($32.40/mo savings).

---

## 📸 Platform Highlights & Architecture

- **Branding**: Official CloudifyOps branding ("Cloudify IT, Simplify IT") with high-trust Indian BFSI UI.
- **Dual Portal Modes**:
  1. **Customer Portal**: Policy tracker, sum insured breakdown, FNOL claims tracker, digital locker, and instant WebRTC call button.
  2. **Agent Assist CRM**: Omnichannel softphone with **3 demo agents** selectable at the top corner, real-time screen-pop with authoritative RBI/IRDAI guidelines, live streaming Hinglish transcript, sentiment meter, and Bedrock summary.
- **WebRTC Telephony**: Real-time browser-to-browser voice calling over WebRTC with peer signaling, ring chimes, mute/hangup controls, and fallback audio streams.
- **Database Architecture**: 12 relational PostgreSQL tables covering customers, policies, vehicles, health covers, life covers, PA covers, nominees, claims, documents, hospital network, calls, and transcript segments.

---

## 🗄️ PostgreSQL 15 Database Schema (12 Tables)

| # | Table Name | Key Purpose | Key Columns |
|---|------------|-------------|-------------|
| 1 | `customers` | Master Indian customer profile & bank balances | `customer_id`, `full_name`, `phone_e164`, `aadhaar_last4`, `pan_masked`, `kyc_status`, `account_balance_paise` |
| 1b | `agents` | Demo softphone agents at top corner | `agent_id`, `full_name`, `extension`, `specialization`, `languages`, `status` |
| 2 | `policies` | Active, lapsed, and expired policies | `policy_id`, `customer_id`, `policy_number`, `product_type`, `sum_insured_paise`, `premium_annual_paise`, `ncb_percent` |
| 3 | `motor_vehicles` | Vehicle specs for motor & two-wheelers | `vehicle_id`, `policy_id`, `registration_number`, `make`, `model`, `idv_paise`, `year_of_manufacture` |
| 4 | `health_covers` | TPA, room rent eligibility, sub-limits | `cover_id`, `policy_id`, `tpa_name`, `room_rent_type`, `proportionate_deduction`, `procedure_sublimits` |
| 5 | `life_covers` | Term life, riders, loan accounts | `cover_id`, `policy_id`, `sum_assured_paise`, `accidental_death_rider_paise`, `policy_term_years` |
| 6 | `pa_covers` | Personal accident schedule (PPD & TTD) | `cover_id`, `policy_id`, `occupation_class`, `ppd_schedule` (JSONB), `ttd_weekly_percent`, `ttd_max_weeks` |
| 7 | `nominees` | Legal beneficiary and nominee details | `nominee_id`, `policy_id`, `customer_id`, `full_name`, `relationship`, `nominee_share_percent` |
| 8 | `claims` | FNOL registrations & claim lifecycle | `claim_id`, `claim_ref`, `policy_id`, `customer_id`, `claim_type`, `status`, `claim_amount_paise`, `notes` |
| 9 | `documents` | Mandatory checklist & verification per claim | `doc_id`, `claim_id`, `doc_type`, `is_mandatory`, `submitted`, `verified` |
| 10 | `hospital_network` | Cashless empanelled hospital directory | `hospital_id`, `hospital_name`, `tpa_name`, `city`, `cashless_active`, `specialities` |
| 11 | `calls` | LCA call session master & audio URIs | `call_id`, `call_uuid`, `customer_id`, `agent_id`, `caller_phone_e164`, `bedrock_summary`, `sentiment_customer` |
| 12 | `call_transcript_segments` | Utterance fragments with speaker diarization | `segment_id`, `call_id`, `speaker` (customer/agent), `transcript_text`, `language_detected`, `sentiment` |

---

## 👥 5 Pre-Seeded Indian BFSI Personas & Use Cases

1. **Rajesh Sharma (`+919820155412`)** — *Retail Banking Disputed Charge*
   - Utterance: *"Sir, mere account se abhi-abhi ₹18,500 ka POS debit transaction hua hai, par main toh office mein hoon!"*
   - Screen-Pop: Visa Platinum #4419, ₹1,24,000 balance, **RBI 3-Day Zero-Liability Guideline (DBR.No.Leg.BC.78)**, 1-Click Card Freeze.
2. **Dr. Sunita Deshpande (`+919890233120`)** — *Health Insurance Knee Surgery*
   - Utterance: *"Mera agle hafte Lilavati Hospital mein knee replacement operation scheduled hai. Kya room rent par proportionate deduction lagega?"*
   - Screen-Pop: **No Proportionate Deduction Clause** (Single Private AC Room 100% covered), ₹2.5 Lakh knee sub-limit, ₹12 Lakh total cover (₹10L SI + ₹2L NCB).
3. **Ananya & Sundaram Iyer (`+919740122910`)** — *Mortgage Foreclosure*
   - Utterance: *"Hum agle hafte apna home loan account HL-40291 close karna chahte hain. Exact balance aur prepayment penalty batayein?"*
   - Screen-Pop: Principal ₹34,18,450, Payoff ₹34,29,690, **₹0 RBI Prepayment Penalty on Floating Rate Loans**, Collateral Vault Box #B-104.
4. **Arjun Patil (`+919665011284`)** — *Two-Wheeler Lapsed Policy Renewal*
   - Utterance: *"Hero Splendor ki insurance 45 din pehle expire ho gayi thi. Kya purana NCB discount milega aur inspection zaroori hai?"*
   - Screen-Pop: **20% NCB retained under IRDAI GR 27 (<90 days)**, 5-Min Video Self-Inspection link dispatched, Total renewal ₹2,492 (with mandatory CPA cover).
5. **Dinesh Rao (`+919870055618`)** — *Personal Accident Finger Amputation*
   - Utterance: *"Factory accident mein mere right hand ki index aur middle fingers amputate ho gayi hain. 20 Lakh PA policy mein kitna payout milega?"*
   - Screen-Pop: **IRDAI PPD Schedule 26% (₹5,20,000) + 6 weeks TTD (₹12,000) = ₹5,32,000 Total Benefit**. Pre-registered Claim #CLM-2025-PA-11823.

---

## 🎧 3 Demo Top-Corner Agents

- **Agent Priya Nair (`AGT-101`)**: Senior Health & Personal Accident Claims Specialist (Ext 101)
- **Agent Amit Verma (`AGT-102`)**: Motor Insurance & Asset Lending Advisor (Ext 102)
- **Agent Sneha Kulkarni (`AGT-103`)**: Disputed Banking Transactions & KYC Lead (Ext 103)

---

## 🚀 Part 1: Local Setup Guide (Windows / Mac / Linux)

### Step 1: Initialize Database in Local PostgreSQL

Open your terminal or PowerShell and run:

```bash
# Option A: Automatic Python Initializer (Checks PostgreSQL on port 5432 & 5433)
python database/setup_db.py --user postgres --password your_postgres_password --dbname bfsi_db

# Option B: Direct psql CLI
psql -U postgres -c "CREATE DATABASE bfsi_db;"
psql -U postgres -d bfsi_db -f database/schema.sql
psql -U postgres -d bfsi_db -f database/seed.sql
```

*(Note: If your local PostgreSQL service is currently stopped, the backend automatically provides a zero-configuration SQLite fallback `bfsi_local.db` with identical schema and seed records so you are never blocked from UI development!)*

### Step 2: Start Backend & UI

```bash
# Run the FastAPI server (serves REST API, WebRTC WebSocket & UI)
python backend/main.py
```

### Step 3: Open in Browser

Open your browser to:
👉 **`http://localhost:8000`**

- Toggle between **Customer Portal** and **Agent Assist CRM**.
- Click **"Call Insurance Agent"** as a Customer to initiate a real WebRTC call.
- The top corner of the Agent CRM will ring with an incoming call alert. Click **Accept & Assist** to start live multilingual speech transcription and screen-pop analytics!

---

## ☁️ Part 2: Amazon EC2 Migration Guide (t3.medium)

### Why an AWS NAT Gateway is NOT Needed ($0 vs $32.40/Month)
- **Public Subnet + Elastic IP**: The EC2 instance resides in a Public Subnet attached to an Amazon VPC Internet Gateway (IGW) with an Elastic IP (EIP).
- **Security Groups**: Port 443 (HTTPS), Port 80 (HTTP to HTTPS redirect), Port 22 (SSH restricted to your IP).
- **Running Cost**: Only **~$56.85 – $63.67 / month** total for 300 calls/month with Bedrock Claude 3.5 Sonnet v2.

### Step 1: Launch EC2 Instance
- **Instance Type**: `t3.medium` (2 vCPU, 4 GB RAM, 30 GB gp3 SSD)
- **AMI**: Ubuntu 22.04 LTS
- **Security Group**: Open Inbound `22` (SSH), `80` (HTTP), `443` (HTTPS)
- **Elastic IP**: Allocate an Elastic IP and associate it with the instance.

### Step 2: Deploy Stack on EC2
SSH into your EC2 instance and run:

```bash
# Clone or copy project files to EC2
git clone <your-repo-url> bfsi-ai-assist
cd bfsi-ai-assist

# Make deployment script executable and run
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

### Step 3: Free HTTPS Setup (Mandatory for WebRTC Microphone)
Modern browsers block microphone capture and WebRTC over plain HTTP.

```bash
# Option A: Zero IT Approvals (Instant sslip.io wildcard domain)
# Example: If your Elastic IP is 54.210.45.89:
sudo certbot certonly --standalone -d 54-210-45-89.sslip.io

# Option B: Company Subdomain (Point A-record in DNS)
sudo certbot certonly --standalone -d insurance-demo.yourcompany.com
```

### Step 4: Amazon Connect Approved Origins
In Amazon Connect Console:
`Amazon Connect -> Your Instance -> Application Integration -> Approved Origins`
Add your domain: `https://<your-domain>` to enable softphone embedded calling without CORS blocks.

---

## 📁 Repository Directory Layout

```
BFSI AI assist/
├── cloudifyops_logo.png           # CloudifyOps logo image
├── docker-compose.yml             # PostgreSQL 15 + FastAPI + Nginx Docker stack
├── Dockerfile.backend             # Lean Python 3.12 container
├── nginx.conf                     # Nginx TLS 1.3 & WebSocket proxy
├── deploy_ec2.sh                  # 1-Click EC2 deployment automation
├── requirements.txt               # Backend dependencies
├── .env.example                   # Environment configuration template
├── database/
│   ├── schema.sql                 # 12 PostgreSQL DDL tables with constraints
│   ├── seed.sql                   # 5 Personas, 3 Agents, Covers & Hospitals
│   └── setup_db.py                # Automated migration & verification runner
├── backend/
│   ├── main.py                    # FastAPI server (REST + Static + WS)
│   ├── database.py                # Database pool with SQLite fallback
│   ├── webrtc_signaling.py        # WebRTC PeerConnection coordinator
│   └── lca_simulator.py           # Amazon Transcribe & Bedrock Sonnet engine
└── frontend/
    ├── index.html                 # Responsive BFSI Portal (Customer & Agent)
    └── cloudifyops_logo.png       # Embedded branding asset
```

