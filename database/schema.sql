-- ============================================================================
-- CLOUDIFYOPS BFSI INSURANCE & CONTACT CENTER INTELLIGENCE PLATFORM
-- PostgreSQL 15 Database Schema (12 Tables)
-- Compliant with RBI, IRDAI, and AWS Live Call Analytics (LCA) Specifications
-- ============================================================================

-- Drop existing tables if re-initializing (in reverse dependency order)
DROP TABLE IF EXISTS call_transcript_segments CASCADE;
DROP TABLE IF EXISTS calls CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS nominees CASCADE;
DROP TABLE IF EXISTS pa_covers CASCADE;
DROP TABLE IF EXISTS life_covers CASCADE;
DROP TABLE IF EXISTS health_covers CASCADE;
DROP TABLE IF EXISTS motor_vehicles CASCADE;
DROP TABLE IF EXISTS policies CASCADE;
DROP TABLE IF EXISTS hospital_network CASCADE;
DROP TABLE IF EXISTS agents CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ----------------------------------------------------------------------------
-- 1. CUSTOMERS: Master insured/customer profile
-- ----------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_e164 VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    dob DATE,
    gender VARCHAR(10),
    aadhaar_last4 VARCHAR(4),
    pan_masked VARCHAR(20),
    address_state VARCHAR(50),
    city VARCHAR(50),
    pincode VARCHAR(10),
    kyc_status VARCHAR(20) DEFAULT 'verified',
    bank_account_number_masked VARCHAR(30),
    bank_ifsc VARCHAR(20),
    account_balance_paise BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_phone ON customers(phone_e164);

-- ----------------------------------------------------------------------------
-- 1B. AGENTS: Demo Call Center Agents (Top Corner Softphone Call Routing)
-- ----------------------------------------------------------------------------
CREATE TABLE agents (
    agent_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    extension VARCHAR(10) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    languages VARCHAR(100) DEFAULT 'English, Hindi, Hinglish',
    status VARCHAR(20) DEFAULT 'available', -- available, busy, on_call, offline
    current_call_id VARCHAR(100),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 2. POLICIES: Active, lapsed, and expired insurance policies
-- ----------------------------------------------------------------------------
CREATE TABLE policies (
    policy_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    policy_number VARCHAR(50) NOT NULL UNIQUE,
    insurer_name VARCHAR(100) NOT NULL DEFAULT 'CloudifyOps BFSI Shield',
    product_type VARCHAR(30) NOT NULL, -- motor, health, life_term, pa, two_wheeler, banking_loan
    product_name VARCHAR(100) NOT NULL,
    sum_insured_paise BIGINT NOT NULL DEFAULT 0,
    premium_annual_paise BIGINT NOT NULL DEFAULT 0,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, lapsed, expired, cancelled
    ncb_percent INT DEFAULT 0,
    addon_flags JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_policies_customer ON policies(customer_id);
CREATE INDEX idx_policies_number ON policies(policy_number);

-- ----------------------------------------------------------------------------
-- 3. MOTOR_VEHICLES: Vehicle specs for motor and two-wheeler policies
-- ----------------------------------------------------------------------------
CREATE TABLE motor_vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE CASCADE,
    registration_number VARCHAR(30) NOT NULL UNIQUE,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    variant VARCHAR(50),
    year_of_manufacture INT NOT NULL,
    fuel_type VARCHAR(20) DEFAULT 'Petrol',
    engine_cc INT,
    idv_paise BIGINT NOT NULL, -- Insured Declared Value in paise
    rto_state VARCHAR(20),
    is_commercial BOOLEAN DEFAULT FALSE,
    chassis_number VARCHAR(50),
    engine_number VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_motor_reg ON motor_vehicles(registration_number);

-- ----------------------------------------------------------------------------
-- 4. HEALTH_COVERS: TPA, room-rent eligibility, sub-limits, cashless terms
-- ----------------------------------------------------------------------------
CREATE TABLE health_covers (
    cover_id SERIAL PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE CASCADE,
    tpa_name VARCHAR(100) NOT NULL DEFAULT 'MediAssist TPA Pvt Ltd',
    tpa_contact VARCHAR(50) DEFAULT '+91-1800-425-9444',
    room_rent_type VARCHAR(20) DEFAULT 'no_cap', -- no_cap, percentage, fixed
    room_rent_limit_paise BIGINT DEFAULT 0,
    proportionate_deduction BOOLEAN DEFAULT FALSE,
    maternity_covered BOOLEAN DEFAULT FALSE,
    pre_existing_waiting_days INT DEFAULT 0,
    specific_illness_waiting_days INT DEFAULT 0,
    ncb_accumulated_paise BIGINT DEFAULT 0,
    cumulative_bonus_paise BIGINT DEFAULT 0,
    copay_percent INT DEFAULT 0,
    procedure_sublimits JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 5. LIFE_COVERS: Term life, riders, loan accounts, payoff & collateral
-- ----------------------------------------------------------------------------
CREATE TABLE life_covers (
    cover_id SERIAL PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE CASCADE,
    policy_term_years INT,
    premium_payment_term INT,
    sum_assured_paise BIGINT NOT NULL,
    accidental_death_rider_paise BIGINT DEFAULT 0,
    critical_illness_rider_paise BIGINT DEFAULT 0,
    waiver_premium_rider BOOLEAN DEFAULT FALSE,
    premium_frequency VARCHAR(20) DEFAULT 'annual', -- monthly, quarterly, annual, single
    policy_bond_issued BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 6. PA_COVERS: Personal accident benefit schedule, PPD & TTD
-- ----------------------------------------------------------------------------
CREATE TABLE pa_covers (
    cover_id SERIAL PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE CASCADE,
    occupation_class VARCHAR(20) DEFAULT 'class2', -- class1, class2, class3, class4
    accidental_death_percent INT DEFAULT 100,
    ppd_schedule JSONB DEFAULT '{}'::jsonb, -- body part to payout percentage mapping
    ttd_weekly_percent NUMERIC(5, 2) DEFAULT 1.0,
    ttd_max_weeks INT DEFAULT 104,
    ttd_weekly_cap_paise BIGINT DEFAULT 200000, -- e.g. Rs 2,000/week in paise
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 7. NOMINEES: Nominee and legal beneficiary details
-- ----------------------------------------------------------------------------
CREATE TABLE nominees (
    nominee_id SERIAL PRIMARY KEY,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE CASCADE,
    customer_id INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    dob DATE,
    aadhaar_last4 VARCHAR(4),
    phone VARCHAR(20),
    bank_account_number_masked VARCHAR(30),
    bank_ifsc VARCHAR(20),
    nominee_share_percent INT DEFAULT 100,
    is_minor BOOLEAN DEFAULT FALSE,
    guardian_name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 10. HOSPITAL_NETWORK: Cashless empanelled hospital list for screen-pop
-- ----------------------------------------------------------------------------
CREATE TABLE hospital_network (
    hospital_id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL,
    tpa_name VARCHAR(100) DEFAULT 'MediAssist TPA',
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(10),
    address TEXT,
    phone VARCHAR(30),
    cashless_active BOOLEAN DEFAULT TRUE,
    specialities TEXT[] DEFAULT ARRAY['Cardiology', 'Orthopedics', 'General Surgery', 'Joint Replacement'],
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 11. CALLS: Master LCA call session table
-- ----------------------------------------------------------------------------
CREATE TABLE calls (
    call_id SERIAL PRIMARY KEY,
    call_uuid VARCHAR(100) NOT NULL UNIQUE,
    customer_id INT REFERENCES customers(customer_id) ON DELETE SET NULL,
    agent_id VARCHAR(50) REFERENCES agents(agent_id) ON DELETE SET NULL,
    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMPTZ,
    duration_seconds INT DEFAULT 0,
    caller_phone_e164 VARCHAR(20) NOT NULL,
    call_status VARCHAR(20) DEFAULT 'active', -- active, completed, abandoned
    transcript_s3_uri TEXT,
    audio_s3_uri TEXT,
    bedrock_summary TEXT,
    fnol_intent_detected BOOLEAN DEFAULT FALSE,
    sentiment_customer VARCHAR(20) DEFAULT 'neutral', -- positive, neutral, negative
    sentiment_agent VARCHAR(20) DEFAULT 'positive',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_calls_uuid ON calls(call_uuid);
CREATE INDEX idx_calls_phone ON calls(caller_phone_e164);

-- ----------------------------------------------------------------------------
-- 8. CLAIMS: All FNOL registrations and claim lifecycle tracking
-- ----------------------------------------------------------------------------
CREATE TABLE claims (
    claim_id SERIAL PRIMARY KEY,
    claim_ref VARCHAR(50) NOT NULL UNIQUE,
    policy_id INT NOT NULL REFERENCES policies(policy_id) ON DELETE RESTRICT,
    customer_id INT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    call_id INT REFERENCES calls(call_id) ON DELETE SET NULL,
    claim_type VARCHAR(50) NOT NULL, -- motor_own_damage, motor_tp, health_cashless, health_reimbursement, death, ppd, ttd, pa_accidental_death, disputed_transaction
    incident_date DATE NOT NULL,
    intimation_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(30) DEFAULT 'registered', -- registered, under_survey, documents_pending, approved, settled, repudiated
    claim_amount_paise BIGINT NOT NULL DEFAULT 0,
    settled_amount_paise BIGINT DEFAULT 0,
    surveyor_name VARCHAR(100),
    surveyor_contact VARCHAR(30),
    settlement_date DATE,
    repudiation_reason TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_claims_ref ON claims(claim_ref);
CREATE INDEX idx_claims_customer ON claims(customer_id);

-- ----------------------------------------------------------------------------
-- 9. DOCUMENTS: Document checklist and tracking per claim
-- ----------------------------------------------------------------------------
CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    claim_id INT NOT NULL REFERENCES claims(claim_id) ON DELETE CASCADE,
    doc_type VARCHAR(50) NOT NULL, -- death_cert, policy_bond, kyc, discharge_summary, fir, rc_copy, dl_copy, disability_cert, employer_report, claim_form
    is_mandatory BOOLEAN DEFAULT TRUE,
    submitted BOOLEAN DEFAULT FALSE,
    submitted_at TIMESTAMPTZ,
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    rejection_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 12. CALL_TRANSCRIPT_SEGMENTS: Real-time utterance fragments
-- ----------------------------------------------------------------------------
CREATE TABLE call_transcript_segments (
    segment_id SERIAL PRIMARY KEY,
    call_id INT NOT NULL REFERENCES calls(call_id) ON DELETE CASCADE,
    speaker VARCHAR(20) NOT NULL, -- customer, agent
    start_time_ms BIGINT NOT NULL,
    end_time_ms BIGINT NOT NULL,
    transcript_text TEXT NOT NULL,
    language_detected VARCHAR(10) DEFAULT 'hi-IN', -- hi-IN, en-IN, hinglish
    sentiment VARCHAR(20) DEFAULT 'neutral', -- positive, neutral, negative
    pii_redacted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_segments_call ON call_transcript_segments(call_id);

