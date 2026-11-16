-- ============================================================================
-- CLOUDIFYOPS BFSI INSURANCE & CONTACT CENTER INTELLIGENCE PLATFORM
-- Seed Data: 5 Indian BFSI Personas, 3 Demo Agents & Regulatory Datasets
-- All values in INR (paise represented as BIGINT: 1 INR = 100 paise)
-- ============================================================================

-- Clean existing data
TRUNCATE TABLE call_transcript_segments, calls, documents, claims, nominees,
               pa_covers, life_covers, health_covers, motor_vehicles,
               policies, hospital_network, agents, customers RESTART IDENTITY CASCADE;

-- ----------------------------------------------------------------------------
-- 1. SEED AGENTS: 3 Demo Contact Center Specialists (Shown at Top Corner)
-- ----------------------------------------------------------------------------
INSERT INTO agents (agent_id, full_name, email, extension, specialization, languages, status, avatar_url) VALUES
('AGT-101', 'Priya Nair', 'priya.nair@cloudifyops.com', '101', 'Health & PA Claims Specialist', 'English, Hindi, Malayalam', 'available', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'),
('AGT-102', 'Amit Verma', 'amit.verma@cloudifyops.com', '102', 'Motor Insurance & Asset Lending', 'English, Hindi, Hinglish', 'available', 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80'),
('AGT-103', 'Sneha Kulkarni', 'sneha.kulkarni@cloudifyops.com', '103', 'Disputed Banking & KYC Lead', 'English, Hindi, Marathi', 'available', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80');

-- ----------------------------------------------------------------------------
-- 2. SEED CUSTOMERS: 5 Indian Insurance & Banking Personas
-- ----------------------------------------------------------------------------
INSERT INTO customers (
    customer_id, full_name, phone_e164, email, dob, gender,
    aadhaar_last4, pan_masked, address_state, city, pincode,
    kyc_status, bank_account_number_masked, bank_ifsc, account_balance_paise
) VALUES
-- Use Case 1: Retail Banking Disputed Charge
(1, 'Rajesh Sharma', '+919820155412', 'rajesh.sharma@example.com', '1986-04-12', 'Male',
 '8821', 'ABCPS****K', 'Maharashtra', 'Mumbai', '400050',
 'verified', 'XXXX-XXXX-4419', 'HDFC0000128', 12400000), -- Balance: Rs 1,24,000.00

-- Use Case 2: Health Insurance Lilavati Knee Replacement
(2, 'Dr. Sunita Deshpande', '+919890233120', 'sunita.deshpande@example.com', '1974-09-22', 'Female',
 '3910', 'AEPPD****R', 'Maharashtra', 'Pune', '411004',
 'verified', 'XXXX-XXXX-8821', 'ICIC0000042', 35000000),

-- Use Case 3: Mortgage Lending Whitefield Home Loan Payoff
(3, 'Ananya & Sundaram Iyer', '+919740122910', 'sundaram.iyer@example.com', '1981-11-05', 'Male',
 '6614', 'AYUPI****M', 'Karnataka', 'Bengaluru', '560066',
 'verified', 'XXXX-XXXX-9931', 'SBIN0004120', 48200000),

-- Use Case 4: Two-Wheeler Lapsed Policy Renewal & Break-In
(4, 'Arjun Patil', '+919665011284', 'arjun.patil@example.com', '1995-02-18', 'Male',
 '2291', 'BRPPP****G', 'Maharashtra', 'Nashik', '422005',
 'verified', 'XXXX-XXXX-3104', 'BARB0VJNASH', 8500000),

-- Use Case 5: Personal Accident Industrial Finger Amputation
(5, 'Dinesh Rao', '+919870055618', 'dinesh.rao@example.com', '1988-07-30', 'Male',
 '5519', 'AQWPR****T', 'Maharashtra', 'Thane', '400601',
 'verified', 'XXXX-XXXX-7123', 'CNRB0001824', 9200000);

-- Reset sequence for customers
SELECT setval('customers_customer_id_seq', 5, true);

-- ----------------------------------------------------------------------------
-- 3. SEED POLICIES & LOAN ACCOUNTS
-- ----------------------------------------------------------------------------
INSERT INTO policies (
    policy_id, customer_id, policy_number, insurer_name, product_type,
    product_name, sum_insured_paise, premium_annual_paise, start_date, end_date,
    status, ncb_percent, addon_flags
) VALUES
-- 1. Rajesh Sharma: Preferred Salary Account Debit Card & Cyber Shield
(1, 1, 'POL-BNK-4419', 'CloudifyOps Banking Shield', 'banking_loan',
 'HDFC Preferred Salary & Platinum Debit Card Cover', 50000000, 150000, '2025-01-01', '2026-01-01',
 'active', 0, '{"zero_liability_enabled": true, "pos_fraud_cover": true, "card_last4": "4419", "card_brand": "Visa Platinum", "channel_flagged": "POS Chip Swipe"}'::jsonb),

-- 2. Dr. Sunita Deshpande: Family Health Optima
(2, 2, 'POL-HLTH-6012', 'CloudifyOps Health Care', 'health',
 'Family Health Optima Comprehensive', 100000000, 3250000, '2023-03-15', '2027-03-14',
 'active', 20, '{"room_rent_clause": "No Proportionate Deduction", "knee_sublimit_paise": 25000000, "cumulative_bonus_paise": 20000000, "tenure_continuous_years": 4}'::jsonb),

-- 3. Ananya & Sundaram Iyer: Home Loan Account
(3, 3, 'HL-40291-BLR', 'CloudifyOps Home Finance', 'banking_loan',
 'Prime Home Loan Floating Rate (Whitefield Villa)', 500000000, 48000000, '2020-04-10', '2040-04-09',
 'active', 0, '{"vault_box": "B-104", "vault_location": "Bengaluru Central Vault", "property": "Whitefield, Bengaluru", "floating_rate": true, "rbi_prepayment_penalty": 0}'::jsonb),

-- 4. Arjun Patil: Hero Splendor Two-Wheeler (Lapsed 45 Days Ago)
(4, 4, 'POL-TW-7721', 'CloudifyOps Motor Shield', 'two_wheeler',
 'Two-Wheeler Comprehensive Package (Hero Splendor+)', 3850000, 249200, '2024-09-25', '2025-09-24',
 'lapsed', 20, '{"lapsed_days": 45, "irdai_gr27_retained": true, "break_in_required": true, "inspection_type": "Video Self-Inspection 5-Min", "cpa_paise": 34200, "tp_paise": 71400, "od_gross_paise": 132000, "ncb_discount_paise": 26400, "tax_gst_paise": 38016}'::jsonb),

-- 5. Dinesh Rao: Standalone Personal Accident
(5, 5, 'POL-PA-3391', 'CloudifyOps Guardian Shield', 'pa',
 'Standalone Individual Personal Accident (Class II)', 200000000, 450000, '2024-06-01', '2026-05-31',
 'active', 0, '{"occupation": "Factory & Industrial Machinery Supervisor", "risk_class": "Class II", "pre_registered_claim": "CLM-2025-PA-11823"}'::jsonb);

SELECT setval('policies_policy_id_seq', 5, true);

-- ----------------------------------------------------------------------------
-- 4. SEED MOTOR VEHICLES
-- ----------------------------------------------------------------------------
INSERT INTO motor_vehicles (
    vehicle_id, policy_id, registration_number, make, model, variant,
    year_of_manufacture, fuel_type, engine_cc, idv_paise, rto_state, is_commercial,
    chassis_number, engine_number
) VALUES
(1, 4, 'MH-15-DX-4412', 'Hero MotoCorp', 'Splendor Plus', 'i3S BS6 Drum Self Cast',
 2021, 'Petrol', 97, 3850000, 'Maharashtra', false,
 'MBLHAW085M9K02914', 'HA08EMM9K11482');

SELECT setval('motor_vehicles_vehicle_id_seq', 1, true);

-- ----------------------------------------------------------------------------
-- 5. SEED HEALTH COVERS
-- ----------------------------------------------------------------------------
INSERT INTO health_covers (
    cover_id, policy_id, tpa_name, tpa_contact, room_rent_type,
    room_rent_limit_paise, proportionate_deduction, maternity_covered,
    pre_existing_waiting_days, specific_illness_waiting_days,
    ncb_accumulated_paise, cumulative_bonus_paise, copay_percent, procedure_sublimits
) VALUES
(1, 2, 'MediAssist TPA Pvt Ltd', '+91-1800-425-9444', 'no_cap',
 0, false, true, 0, 0,
 20000000, 20000000, 0,
 '{"joint_replacement_per_knee_paise": 25000000, "cataract_per_eye_paise": 5000000, "angioplasty_paise": 35000000}'::jsonb);

SELECT setval('health_covers_cover_id_seq', 1, true);

-- ----------------------------------------------------------------------------
-- 6. SEED LIFE & HOME LOAN COVERS
-- ----------------------------------------------------------------------------
INSERT INTO life_covers (
    cover_id, policy_id, policy_term_years, premium_payment_term,
    sum_assured_paise, accidental_death_rider_paise, critical_illness_rider_paise,
    waiver_premium_rider, premium_frequency, policy_bond_issued
) VALUES
(1, 3, 20, 20, 500000000, 0, 0, false, 'monthly', true);

SELECT setval('life_covers_cover_id_seq', 1, true);

-- ----------------------------------------------------------------------------
-- 7. SEED PERSONAL ACCIDENT COVERS
-- ----------------------------------------------------------------------------
INSERT INTO pa_covers (
    cover_id, policy_id, occupation_class, accidental_death_percent,
    ppd_schedule, ttd_weekly_percent, ttd_max_weeks, ttd_weekly_cap_paise
) VALUES
(1, 5, 'class2', 100,
 '{"loss_of_index_finger_dominant": 14, "loss_of_middle_finger_dominant": 12, "loss_of_hand": 60, "loss_of_thumb": 25, "loss_of_sight_one_eye": 50}'::jsonb,
 1.0, 104, 200000);

SELECT setval('pa_covers_cover_id_seq', 1, true);

-- ----------------------------------------------------------------------------
-- 8. SEED NOMINEES
-- ----------------------------------------------------------------------------
INSERT INTO nominees (
    nominee_id, policy_id, customer_id, full_name, relationship,
    dob, aadhaar_last4, phone, bank_account_number_masked, bank_ifsc,
    nominee_share_percent, is_minor, guardian_name
) VALUES
(1, 2, 2, 'Kedar Deshpande', 'Spouse', '1972-05-14', '7721', '+919890233121', 'XXXX-XXXX-9142', 'ICIC0000042', 100, false, NULL),
(2, 5, 5, 'Shweta Dinesh Rao', 'Spouse', '1990-10-11', '4120', '+919870055619', 'XXXX-XXXX-8812', 'CNRB0001824', 100, false, NULL);

SELECT setval('nominees_nominee_id_seq', 2, true);

-- ----------------------------------------------------------------------------
-- 9. SEED CASHLESS HOSPITAL NETWORK
-- ----------------------------------------------------------------------------
INSERT INTO hospital_network (
    hospital_id, hospital_name, tpa_name, city, state, pincode,
    address, phone, cashless_active, specialities, latitude, longitude
) VALUES
(1, 'Lilavati Hospital & Research Centre', 'MediAssist TPA', 'Mumbai', 'Maharashtra', '400050',
 'A-791, Bandra Reclamation, Bandra West, Mumbai', '+91-22-2675-1000', true,
 ARRAY['Orthopedics', 'Robotic Knee Replacement', 'Cardiology', 'Neurology', 'Oncology'], 19.0522, 72.8315),
(2, 'Ruby Hall Clinic', 'MediAssist TPA', 'Pune', 'Maharashtra', '411001',
 '40, Sassoon Road, Sangamvadi, Pune', '+91-20-6645-5100', true,
 ARRAY['Joint Replacement', 'Cardiology', 'Organ Transplant'], 18.5314, 73.8762),
(3, 'Manipal Hospital Whitefield', 'MediAssist TPA', 'Bengaluru', 'Karnataka', '560066',
 '#143, 212-215, EPIP Zone, Whitefield, Bengaluru', '+91-80-2502-4444', true,
 ARRAY['Emergency', 'Orthopedics', 'Critical Care'], 12.9815, 77.7289);

SELECT setval('hospital_network_hospital_id_seq', 3, true);

-- ----------------------------------------------------------------------------
-- 10. SEED CALLS: Pre-loaded Demo Inbound Sessions (LCA Engine)
-- ----------------------------------------------------------------------------
INSERT INTO calls (
    call_id, call_uuid, customer_id, agent_id, start_time, end_time,
    duration_seconds, caller_phone_e164, call_status, bedrock_summary,
    fnol_intent_detected, sentiment_customer, sentiment_agent
) VALUES
-- Call 1: Rajesh Sharma (Disputed Transaction)
(1, 'CALL-UUID-2025-001', 1, 'AGT-103', NOW() - INTERVAL '1 hour', NOW() - INTERVAL '58 minutes',
 120, '+919820155412', 'completed',
 'Customer reported unauthorized POS charge of Rs 18,500 at Croma Mumbai. Agent verified card ending in 4419, invoked RBI 3-Day Zero Liability Guideline DBR.No.Leg.BC.78, initiated immediate temporary card block, and registered Dispute Ref #DISP-2025-POS-4419.',
 true, 'negative', 'positive'),

-- Call 2: Dr. Sunita Deshpande (Lilavati Hospital Knee Replacement)
(2, 'CALL-UUID-2025-002', 2, 'AGT-101', NOW() - INTERVAL '40 minutes', NOW() - INTERVAL '37 minutes',
 180, '+919890233120', 'completed',
 'Insured enquired about room rent eligibility and robotic knee surgery coverage at Lilavati Hospital under Policy POL-HLTH-6012. Confirmed Single Private AC room is 100% covered with zero proportionate deduction. Joint replacement covered up to Rs 2,50,000 per knee. Total available cover Rs 12,00,000. Pre-authorization desk notified.',
 false, 'positive', 'positive'),

-- Call 3: Dinesh Rao (Personal Accident Industrial Amputation)
(3, 'CALL-UUID-2025-003', 5, 'AGT-101', NOW() - INTERVAL '15 minutes', NOW() - INTERVAL '10 minutes',
 300, '+919870055618', 'completed',
 'Insured intimated traumatic industrial amputation of index and middle fingers on right hand under PA Policy POL-PA-3391 (SI Rs 20,00,000). Agent calculated 26% PPD benefit (Rs 5,20,000) + 6 weeks TTD (Rs 12,000) = Rs 5,32,000. Auto-triggered FNOL Ref #CLM-2025-PA-11823. Mandatory checklist sent via SMS.',
 true, 'neutral', 'positive');

SELECT setval('calls_call_id_seq', 3, true);

-- ----------------------------------------------------------------------------
-- 11. SEED CLAIMS: Pre-registered Claims across Lines of Business
-- ----------------------------------------------------------------------------
INSERT INTO claims (
    claim_id, claim_ref, policy_id, customer_id, call_id, claim_type,
    incident_date, intimation_date, status, claim_amount_paise, settled_amount_paise,
    surveyor_name, surveyor_contact, repudiation_reason, notes
) VALUES
-- Dinesh Rao PA Claim
(1, 'CLM-2025-PA-11823', 5, 5, 3, 'ppd',
 CURRENT_DATE - 42, CURRENT_DATE, 'registered', 53200000, 0,
 'Sanjay Deshmukh (IRDAI #SUR-9941)', '+91-98220-44910', NULL,
 'Traumatic amputation of dominant index & middle finger. PPD 26% (Rs 5,20,000) + 6 weeks TTD (Rs 12,000). Awaiting Civil Surgeon certificate.'),

-- Rajesh Sharma Banking Dispute
(2, 'DISP-2025-POS-4419', 1, 1, 1, 'disputed_transaction',
 CURRENT_DATE, CURRENT_DATE, 'under_survey', 1850000, 0,
 'Fraud Risk Analyst - Bank Ops', '+91-1800-120-4419', NULL,
 'Unauthorized POS swipe at Croma Electronics Mumbai. RBI Zero-Liability 3-day mandate applicable.');

SELECT setval('claims_claim_id_seq', 2, true);

-- ----------------------------------------------------------------------------
-- 12. SEED DOCUMENTS: Checklists for Claims
-- ----------------------------------------------------------------------------
INSERT INTO documents (
    doc_id, claim_id, doc_type, is_mandatory, submitted,
    submitted_at, verified, verified_at, rejection_reason
) VALUES
(1, 1, 'disability_cert', true, false, NULL, false, NULL, NULL),
(2, 1, 'employer_report', true, true, NOW() - INTERVAL '1 day', true, NOW(), NULL),
(3, 1, 'discharge_summary', true, true, NOW() - INTERVAL '2 days', true, NOW(), NULL),
(4, 1, 'kyc', true, true, NOW() - INTERVAL '5 days', true, NOW(), NULL);

SELECT setval('documents_doc_id_seq', 4, true);

-- ----------------------------------------------------------------------------
-- 13. SEED CALL TRANSCRIPT SEGMENTS (Realistic Multilingual Hinglish Utterances)
-- ----------------------------------------------------------------------------
INSERT INTO call_transcript_segments (
    segment_id, call_id, speaker, start_time_ms, end_time_ms,
    transcript_text, language_detected, sentiment, pii_redacted
) VALUES
-- Call 1: Rajesh Sharma POS dispute
(1, 1, 'customer', 0, 5200, 'Sir, mere account se abhi-abhi ₹18,500 ka POS debit transaction hua hai, par main toh office mein hoon! Maine koi shopping nahi ki.', 'hinglish', 'negative', false),
(2, 1, 'agent', 5500, 11000, 'Namaste Mr. Sharma, bilkul pareshan mat hoiye. Main dekh pa rahi hoon Croma Electronics Mumbai par 14:18 baje ₹18,500 ka transaction hua hai card ending in 4419 par.', 'hinglish', 'positive', true),
(3, 1, 'agent', 11500, 16800, 'Per RBI 3-Day Zero-Liability guideline, aap safe hain. Main abhi turant aapka card 4419 freeze kar rahi hoon aur dispute lodge kar rahi hoon.', 'hinglish', 'positive', false),

-- Call 2: Dr. Sunita Deshpande Health query
(4, 2, 'customer', 0, 6800, 'Mera agle hafte Lilavati Hospital mein knee replacement operation scheduled hai. Kya meri policy POL-HLTH-6012 mein single private AC room lene par proportionate deduction lagega ya full claim milega?', 'hinglish', 'neutral', false),
(5, 2, 'agent', 7100, 14200, 'Dr. Deshpande, aapki policy Family Health Optima mein Single Private AC room par ZERO proportionate deduction clause hai. Joint replacement per knee ₹2,50,000 tak 100% cashless cover hai.', 'hinglish', 'positive', false);

SELECT setval('call_transcript_segments_segment_id_seq', 5, true);

