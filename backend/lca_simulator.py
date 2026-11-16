"""
CloudifyOps BFSI Intelligence Platform - Live Call Analytics (LCA) Engine
Simulates Amazon Transcribe Streaming, Comprehend Sentiment & Bedrock Claude 3.5 Sonnet
for 5 Indian BFSI Use Cases (Hinglish/Hindi/English code-switching).
"""
import time
import asyncio
from typing import Dict, Any, List

LCA_SCENARIOS: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # Use Case 1: Retail Banking - Disputed Transaction & Live Ledger Lookup
    # -------------------------------------------------------------------------
    "+919820155412": {
        "customer_name": "Rajesh Sharma",
        "phone": "+919820155412",
        "policy_id": 1,
        "policy_ref": "POL-BNK-4419",
        "scenario_title": "Retail Banking - Disputed POS Transaction & Live Ledger Lookup",
        "intent": "Fraudulent POS Transaction Intimation",
        "screen_pop": {
            "live_balance": "₹1,24,000.00",
            "flagged_tx": "₹18,500.00 | Merchant: Croma Electronics - Mumbai | Channel: POS Chip Swipe | Time: 14:18 IST",
            "card_status": "Visa Platinum Debit ending in 4419 (Active)",
            "regulatory_rule": "RBI 3-Day Zero-Liability Guideline - Rule Circular DBR.No.Leg.BC.78",
            "recommended_script": "Mr. Sharma, I see the ₹18,500 POS transaction at Croma Electronics at 14:18 PM. Would you like me to immediately freeze card 4419 while you stay on the line?",
            "action_button": "Freeze Card 4419 & Log Dispute",
            "auto_claim_type": "disputed_transaction"
        },
        "transcript_flow": [
            {
                "speaker": "customer",
                "text": "Sir, mere account se abhi-abhi ₹18,500 ka POS debit transaction hua hai, par main toh office mein hoon! Maine koi shopping nahi ki. Yeh charge kahan hua hai aur mera balance kitna bacha hai?",
                "language": "Hinglish",
                "sentiment": "negative",
                "delay_ms": 1000
            },
            {
                "speaker": "agent",
                "text": "Namaste Mr. Sharma, bilkul pareshan mat hoiye. Main dekh pa rahi hoon Croma Electronics Mumbai par 14:18 baje ₹18,500 ka transaction hua hai card ending in 4419 par. Aapka bacha balance ₹1,24,000 hai.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 3000
            },
            {
                "speaker": "customer",
                "text": "Yeh charge maine nahi kiya hai madam! Mera physical card toh mere paas wallet mein hai.",
                "language": "Hinglish",
                "sentiment": "negative",
                "delay_ms": 5000
            },
            {
                "speaker": "agent",
                "text": "Mr. Sharma, RBI Circular DBR.No.Leg.BC.78 ke tehat 3 din ke andar report karne par Zero-Liability guideline lagu hoti hai. Main abhi aapka card 4419 freeze kar rahi hoon aur dispute reference lodge kar rahi hoon.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 7000
            }
        ],
        "bedrock_summary": {
            "call_intent": "Disputed Card Transaction / Zero-Liability Intimation",
            "customer_sentiment": "Initially Agitated -> Reassured",
            "policy_verification": "Verified HDFC Salary Account & Debit Card ending in 4419",
            "rbi_compliance": "RBI Circular DBR.No.Leg.BC.78 applied. Customer informed of 100% zero liability window within 3 working days.",
            "actions_taken": "Visa Platinum card ending in 4419 temporarily locked. Dispute Ref #DISP-2025-POS-4419 generated.",
            "next_best_action": "Issue replacement contactless chip debit card with zero re-issuance fee. Dispatch SMS verification to registered mobile."
        }
    },

    # -------------------------------------------------------------------------
    # Use Case 2: Health Insurance - Cashless Room-Rent & Procedure Sub-Limit
    # -------------------------------------------------------------------------
    "+919890233120": {
        "customer_name": "Dr. Sunita Deshpande",
        "phone": "+919890233120",
        "policy_id": 2,
        "policy_ref": "POL-HLTH-6012",
        "scenario_title": "Health Insurance - Cashless Room-Rent & Procedure Sub-Limit Retrieval",
        "intent": "Pre-Authorization & Room Rent Verification",
        "screen_pop": {
            "policy_status": "Active (4th Continuous Year - Pre-existing covered)",
            "room_rent_clause": "No Proportionate Deduction Clause - Single Private AC Room 100% Covered",
            "sublimit": "Joint Replacement capped at ₹2,50,000 per knee",
            "available_cover": "₹10,00,000 Sum Insured + ₹2,00,000 Cumulative No-Claim Bonus = ₹12,00,000 Total",
            "regulatory_rule": "IRDAI Health Master Circular on Proportionate Deduction Transparency",
            "recommended_script": "Dr. Deshpande, under your policy #POL-HLTH-6012, single private AC room has zero deduction. For joint replacement, your policy covers up to ₹2,50,000 per joint, and you have ₹12,00,000 total cover available.",
            "action_button": "Issue Cashless Pre-Auth Letter to Lilavati",
            "auto_claim_type": "health_cashless"
        },
        "transcript_flow": [
            {
                "speaker": "customer",
                "text": "Mera agle hafte Lilavati Hospital mein knee replacement operation scheduled hai. Kya meri policy POL-HLTH-6012 mein single private AC room lene par proportionate deduction lagega ya full claim milega?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 1000
            },
            {
                "speaker": "agent",
                "text": "Dr. Deshpande, aapki policy Family Health Optima mein Single Private AC room par ZERO proportionate deduction clause hai. Joint replacement per knee ₹2,50,000 tak 100% cashless cover hai.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 3000
            },
            {
                "speaker": "customer",
                "text": "Bahut accha! Aur total available limit kitni hai mere paas?",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 5000
            },
            {
                "speaker": "agent",
                "text": "Aapke paas ₹10,00,000 basic Sum Insured plus ₹2,00,000 cumulative bonus, yani kul ₹12,00,000 ka cover uplabdh hai. Main Lilavati TPA desk par cashless intimation bhej rahi hoon.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 7000
            }
        ],
        "bedrock_summary": {
            "call_intent": "Cashless Hospitalization Sub-limit & Room Category Enquiry",
            "customer_sentiment": "Positive / Satisfied",
            "policy_verification": "Verified Family Health Optima #POL-HLTH-6012 (Continuous 4 Years)",
            "rbi_compliance": "IRDAI Sub-limit Disclosure Standards honored; exact contract clauses quoted upfront.",
            "actions_taken": "Confirmed Lilavati empanelment (TPA MediAssist). Cashless intimation note added to policy record.",
            "next_best_action": "Send cashless admission e-kit to Dr. Deshpande via WhatsApp and SMS."
        }
    },

    # -------------------------------------------------------------------------
    # Use Case 3: Mortgage Lending - Outstanding Principal & Foreclosure Fee
    # -------------------------------------------------------------------------
    "+919740122910": {
        "customer_name": "Ananya & Sundaram Iyer",
        "phone": "+919740122910",
        "policy_id": 3,
        "policy_ref": "HL-40291-BLR",
        "scenario_title": "Mortgage Lending - Outstanding Principal & Foreclosure Fee Retrieval",
        "intent": "Home Loan Closure & Foreclosure Calculation",
        "screen_pop": {
            "principal_outstanding": "₹34,18,450.00",
            "accrued_interest": "₹11,240.00",
            "payoff_total": "₹34,29,690.00 (Valid for next 5 calendar days)",
            "foreclosure_penalty": "₹0.00 (RBI Floating Rate Mandate - Individual Borrowers Exempted)",
            "collateral_location": "Original Title Deed & Sale Agreement in Bengaluru Central Vault (Box #B-104)",
            "recommended_script": "Mr. & Mrs. Iyer, your exact closure amount as of today is ₹34,29,690. Per RBI guidelines, there is ZERO foreclosure penalty. Once paid, original title deeds will be released within 15 working days.",
            "action_button": "Generate Official Foreclosure Quote PDF",
            "auto_claim_type": "disputed_transaction"
        },
        "transcript_flow": [
            {
                "speaker": "customer",
                "text": "Hello team, hum agle hafte apna home loan account HL-40291 full close karna chahte hain. Humein exact outstanding balance batayein aur kya koi prepayment penalty lagegi?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 1000
            },
            {
                "speaker": "agent",
                "text": "Namaste Mr. Iyer. Aapka exact closure amount aaj ki date mein ₹34,29,690 hai. RBI guidelines ke mutabiq floating rate individual loan par ZERO prepayment penalty hai.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 3000
            },
            {
                "speaker": "customer",
                "text": "Aur hamare Whitefield property ke original title deeds kab release honge?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 5000
            },
            {
                "speaker": "agent",
                "text": "Aapke documents Bengaluru Central Vault Box #B-104 mein hain. Payment receive hone ke 15 working days ke andar handover ho jayenge.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 7000
            }
        ],
        "bedrock_summary": {
            "call_intent": "Home Loan Pre-closure & Collateral Document Retrieval",
            "customer_sentiment": "Calm / Content",
            "policy_verification": "Prime Home Loan #HL-40291-BLR (Property: Whitefield, Bengaluru)",
            "rbi_compliance": "RBI Notification on Zero Foreclosure Penalty on Floating Rate Loans fully compliant.",
            "actions_taken": "5-day valid closure figure of ₹34,29,690 generated. Vault Box #B-104 flagged for retrieval prep.",
            "next_best_action": "Email formal loan closure computation sheet and RTGS bank details to customer."
        }
    },

    # -------------------------------------------------------------------------
    # Use Case 4: Two-Wheeler Insurance - Lapsed Policy Renewal & Break-In
    # -------------------------------------------------------------------------
    "+919665011284": {
        "customer_name": "Arjun Patil",
        "phone": "+919665011284",
        "policy_id": 4,
        "policy_ref": "POL-TW-7721",
        "scenario_title": "Two-Wheeler Insurance - Lapsed Policy Renewal & NCB Retention",
        "intent": "Lapsed Vehicle Insurance Renewal Quote",
        "screen_pop": {
            "lapse_period": "45 Calendar Days",
            "ncb_status": "20% NCB Preserved & Valid (IRDAI GR 27 rule: safe up to 90 days)",
            "break_in_rule": "Mandatory Self-Inspection Video Link (>30 days lapse)",
            "vehicle_valuation": "Hero Splendor+ 2021 | IDV: ₹38,500.00",
            "premium_breakdown": "Net OD: ₹1,056 | TP: ₹714 | CPA: ₹342 | 18% GST: ₹380.16 | Total: ₹2,492.00",
            "recommended_script": "Mr. Patil, your 20% NCB is completely safe as you are well within the 90-day window, saving you ₹264. You just need to complete a 5-minute self-inspection video on your phone. Your net renewal amount is ₹2,492 including taxes and the mandatory ₹15 Lakh accident cover. Can I send the payment link to your WhatsApp?",
            "action_button": "Trigger 5-Min Video Inspection SMS",
            "auto_claim_type": "motor_own_damage"
        },
        "transcript_flow": [
            {
                "speaker": "customer",
                "text": "Bhai, meri Hero Splendor ki insurance 45 din pehle expire ho gayi thi. Kya mera purana NCB discount abhi bhi milega? Renew karane ke liye inspection zaroori hai kya, aur total kitna premium banega with mandatory PA cover?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 1000
            },
            {
                "speaker": "agent",
                "text": "Haan Arjun ji, bilkul! IRDAI GR 27 rule ke mutabiq 90 din tak aapka 20% NCB discount safe rehta hai. 45 din lapse hone ke karan bas ek 5 minute ka video self-inspection karna hoga phone se.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 3000
            },
            {
                "speaker": "customer",
                "text": "Theek hai, total kharcha kitna aayega GST aur accident cover ke saath?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 5000
            },
            {
                "speaker": "agent",
                "text": "Aapka 20% NCB discount minus karke aur ₹15 Lakh mandatory accident cover ke saath kul premium ₹2,492 banega. Main abhi aapke WhatsApp par inspection aur payment link send kar raha hoon.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 7000
            }
        ],
        "bedrock_summary": {
            "call_intent": "Lapsed Two-Wheeler Renewal & Break-in Video Inspection Guidance",
            "customer_sentiment": "Positive / Ready to Renew",
            "policy_verification": "Hero Splendor Plus MH-15-DX-4412 (IDV ₹38,500)",
            "rbi_compliance": "IRDAI General Regulation 27 (NCB retention within 90 days) confirmed and applied.",
            "actions_taken": "Automated renewal quote of ₹2,492 formulated with mandatory CPA cover. Video upload link queued.",
            "next_best_action": "Send WhatsApp self-inspection web-link. Policy auto-issuance on AI inspection approval."
        }
    },

    # -------------------------------------------------------------------------
    # Use Case 5: Personal Accident - Permanent Partial Disability & TTD
    # -------------------------------------------------------------------------
    "+919870055618": {
        "customer_name": "Dinesh Rao",
        "phone": "+919870055618",
        "policy_id": 5,
        "policy_ref": "POL-PA-3391",
        "scenario_title": "Personal Accident Insurance - Permanent Partial Disability (PPD) & TTD Calculation",
        "intent": "Industrial Accident PPD & TTD Claim Intimation (FNOL)",
        "screen_pop": {
            "policy_risk": "Active | Risk Category: Class II (Factory & Industrial Operations — 100% Eligible)",
            "sum_insured": "₹20,00,000.00",
            "ppd_calculation": "Loss of Index Finger (14%) = ₹2,80,000 | Middle Finger (12%) = ₹2,40,000 -> Total PPD = ₹5,20,000",
            "ttd_calculation": "6 Weeks Elapsed × 1% SI/week (Capped at ₹2,000/week) = ₹12,000.00",
            "total_estimated_payout": "₹5,32,000.00 (PPD ₹5,20,000 + TTD ₹12,000)",
            "fnol_status": "Auto-Triggered Claim Ref #CLM-2025-PA-11823",
            "recommended_script": "Mr. Rao, under your policy's Schedule of Benefits, the loss of your index and middle fingers qualifies for a verified payout of ₹5,20,000. Additionally, you are entitled to ₹12,000 for your 6 weeks of temporary recovery, bringing your total benefit to ₹5,32,000. I have pre-registered Claim #CLM-2025-PA-11823. You only need a disability certificate from a government civil hospital and your factory incident report.",
            "action_button": "Dispatch Claim Document Checklist via WhatsApp",
            "auto_claim_type": "ppd"
        },
        "transcript_flow": [
            {
                "speaker": "customer",
                "text": "Sir, 6 hafte pehle factory accident mein mere right hand ki index aur middle fingers amputate ho gayi hain. Meri 20 Lakh ki PA policy mein kitna claim amount milega? Kya temporary chhutti ka weekly paisa bhi milega, aur mujhe kaun se medical certificates jama karne honge?",
                "language": "Hinglish",
                "sentiment": "negative",
                "delay_ms": 1000
            },
            {
                "speaker": "agent",
                "text": "Dinesh ji, humein is hadse ka behad dukh hai. IRDAI schedule ke mutabiq right dominant index finger ke liye 14% aur middle finger ke liye 12% total 26% yani ₹5,20,000 Permanent Partial Disability banegi.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 3000
            },
            {
                "speaker": "customer",
                "text": "Aur woh 6 hafte ki temporary recovery ka kya milega?",
                "language": "Hinglish",
                "sentiment": "neutral",
                "delay_ms": 5000
            },
            {
                "speaker": "agent",
                "text": "6 hafte ke recovery allowance ke ₹12,000 judenge, kul milakar ₹5,32,000 ka claim banta hai. Maine Claim Ref #CLM-2025-PA-11823 auto-trigger kar diya hai. Bas Civil Surgeon ka certificate aur factory Form 16 upload karna hoga.",
                "language": "Hinglish",
                "sentiment": "positive",
                "delay_ms": 7000
            }
        ],
        "bedrock_summary": {
            "call_intent": "First Notice of Loss (FNOL) - Traumatic Industrial Amputation",
            "customer_sentiment": "Distressed -> Relieved and Well-Guided",
            "policy_verification": "Standalone Personal Accident #POL-PA-3391 (Risk Class II, Sum Insured ₹20L)",
            "rbi_compliance": "IRDAI Schedule of Standard PPD Benefits strictly applied (14% + 12% = 26%).",
            "actions_taken": "Automated FNOL Registered: Claim #CLM-2025-PA-11823. Total estimated payout booked: ₹5,32,000.",
            "next_best_action": "Assign Senior Surveyor Sanjay Deshmukh (IRDAI #SUR-9941) for expedited doorstep verification."
        }
    }
}

def get_scenario_for_caller(phone_number: str) -> Dict[str, Any]:
    clean_phone = phone_number.replace(" ", "").replace("-", "")
    if clean_phone in LCA_SCENARIOS:
        return LCA_SCENARIOS[clean_phone]
    # Default fallback to Rajesh Sharma if unrecognized
    return LCA_SCENARIOS["+919820155412"]

