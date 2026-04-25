# backend/rag/knowledge_base.py
"""
Seed documents for ChromaDB embedding store.
These documents are embedded using sentence-transformers (all-MiniLM-L6-v2)
and stored as vector chunks in ChromaDB at startup.

Collections:
  - donor_emails     : Real-world donor email scenarios
  - best_practices   : NonProfit communications guidelines
  - quiz_bank        : Reference Q&A pairs with explanations
"""

# ── Donor Email Scenarios ─────────────────────────────────────────────────────
# Each document is a realistic NonProfit email scenario.
# The embedding model converts each into a 384-dim vector.
# At query time, the topic string is embedded and cosine similarity
# is used to find the most relevant chunks.

DONOR_EMAILS = [
    {
        "id": "email_001",
        "topic": "tax_receipt",
        "content": (
            "Dear Team, I made a donation of $1,000 on January 5th and have not "
            "received my tax receipt. I need it urgently for my tax filing deadline "
            "next week. My donor ID is DON-20240105. Please help as soon as possible. "
            "- Robert Chen"
        ),
        "category": "donation_inquiry",
        "urgency": "high",
        "scenario": "missing_tax_receipt",
    },
    {
        "id": "email_002",
        "topic": "donor_retention",
        "content": (
            "Hi, I have been donating monthly for 3 years but I am considering "
            "cancelling my recurring donation. I feel like I never hear about "
            "the impact my contributions are making. Can you share some updates? "
            "I donated $50 every month for 36 months totaling $1,800. - Maria Santos"
        ),
        "category": "donor_retention",
        "urgency": "high",
        "scenario": "donor_disengagement",
    },
    {
        "id": "email_003",
        "topic": "volunteer_cancellation",
        "content": (
            "Hello, I signed up to volunteer at the food drive on March 20th "
            "but unfortunately I have a family emergency and need to cancel. "
            "My volunteer ID is VOL-7734. I am sorry for the short notice "
            "and I hope you can find a replacement quickly. - James Williams"
        ),
        "category": "volunteer_request",
        "urgency": "medium",
        "scenario": "volunteer_cancellation",
    },
    {
        "id": "email_004",
        "topic": "grant_application",
        "content": (
            "Dear Grants Team, I am writing on behalf of the Smith Foundation "
            "regarding grant proposal GRN-2024-089. We submitted our application "
            "6 weeks ago and have not heard back. Could you provide a status update? "
            "The funding decision affects our Q2 program planning. - Dr. Amanda Cole"
        ),
        "category": "grant_application",
        "urgency": "medium",
        "scenario": "grant_status_followup",
    },
    {
        "id": "email_005",
        "topic": "complaint",
        "content": (
            "I am extremely disappointed. I attended your fundraising gala last "
            "Saturday and the event was poorly organized. The auction items were "
            "misrepresented and I paid $500 for something that was not as described. "
            "I want a refund immediately or I will dispute the charge. - Thomas Baker"
        ),
        "category": "complaint",
        "urgency": "critical",
        "scenario": "refund_demand",
    },
    {
        "id": "email_006",
        "topic": "major_donor",
        "content": (
            "Good morning, I represent the Johnson Family Foundation and we are "
            "interested in making a significant contribution of $50,000 to your "
            "children's education program. Could we schedule a call with your "
            "Executive Director to discuss the impact and recognition opportunities? "
            "- Patricia Johnson"
        ),
        "category": "donation_inquiry",
        "urgency": "critical",
        "scenario": "major_gift_inquiry",
    },
    {
        "id": "email_007",
        "topic": "media_inquiry",
        "content": (
            "Hi, I am a reporter at the City Gazette working on a story about "
            "local Non-Profits making a difference in the community. I would love "
            "to interview your director and feature your organization in our Sunday "
            "edition. My deadline is this Thursday. - Mike Torres, City Gazette"
        ),
        "category": "media_inquiry",
        "urgency": "high",
        "scenario": "press_interview_request",
    },
    {
        "id": "email_008",
        "topic": "recurring_donation",
        "content": (
            "Hello, I set up a monthly recurring donation of $50 six months ago "
            "but I noticed my credit card was charged twice this month. "
            "My donor reference is DON-REC-4421. Please investigate and refund "
            "the duplicate charge as soon as possible. - Susan Park"
        ),
        "category": "complaint",
        "urgency": "high",
        "scenario": "duplicate_charge",
    },
    {
        "id": "email_009",
        "topic": "volunteer_inquiry",
        "content": (
            "Hi there! I am a retired teacher and I would love to volunteer with "
            "your literacy program. I have 20 years of teaching experience and can "
            "commit to 10 hours per week on weekdays. How do I get started and "
            "what is the application process? - Carol Davis"
        ),
        "category": "volunteer_request",
        "urgency": "low",
        "scenario": "new_volunteer_signup",
    },
    {
        "id": "email_010",
        "topic": "donor_recognition",
        "content": (
            "Dear Team, I attended your annual gala last night and was surprised "
            "that my name was missing from the donor recognition wall despite "
            "my $5,000 contribution made in October with reference DON-OCT-5000. "
            "This was embarrassing in front of my colleagues. Please correct this. "
            "- David Lee"
        ),
        "category": "complaint",
        "urgency": "high",
        "scenario": "recognition_error",
    },
    {
        "id": "email_011",
        "topic": "pledge_fulfillment",
        "content": (
            "Hi, I made a pledge of $2,000 at your gala in November and I would "
            "like to fulfill it now. Can you send me payment instructions? "
            "I prefer to pay by check. My pledge reference is PLG-NOV-2000. "
            "Thank you for the amazing work you do. - Jennifer Martinez"
        ),
        "category": "donation_inquiry",
        "urgency": "medium",
        "scenario": "pledge_payment",
    },
    {
        "id": "email_012",
        "topic": "program_inquiry",
        "content": (
            "Hello, I am a social worker and I have several clients who could "
            "benefit from your food assistance program. How do they apply? "
            "What are the eligibility requirements and how quickly can they "
            "receive assistance? - Michael Thompson, City Social Services"
        ),
        "category": "general_info",
        "urgency": "medium",
        "scenario": "program_referral",
    },
    {
        "id": "email_013",
        "topic": "event_sponsorship",
        "content": (
            "Dear Sponsorship Team, our company, TechCorp Inc, is interested in "
            "sponsoring your annual charity run next month. We would like to "
            "discuss sponsorship tiers and what visibility options are available "
            "for a $10,000 contribution. - Lisa Wong, TechCorp Inc"
        ),
        "category": "donation_inquiry",
        "urgency": "medium",
        "scenario": "corporate_sponsorship",
    },
    {
        "id": "email_014",
        "topic": "bequest_inquiry",
        "content": (
            "I am 78 years old and I would like to include your organization in "
            "my will. I want to leave a bequest of $100,000 to support your "
            "senior care program. Who should I contact to discuss this and ensure "
            "the gift is properly documented? - Eleanor Hughes"
        ),
        "category": "donation_inquiry",
        "urgency": "high",
        "scenario": "planned_giving",
    },
    {
        "id": "email_015",
        "topic": "feedback",
        "content": (
            "I just wanted to say thank you for the wonderful work your team did "
            "at the community dinner last week. My family and I were truly moved "
            "by the dedication of your volunteers. We will be making an additional "
            "donation of $200 this month. Keep up the amazing work! - The Garcia Family"
        ),
        "category": "general_info",
        "urgency": "low",
        "scenario": "positive_feedback",
    },
]

# ── Best Practice Documents ───────────────────────────────────────────────────
# Guidelines embedded as chunks for RAG-based answer evaluation.
# When a user answers a quiz, the topic is used to retrieve the most
# relevant guidelines and inject them into the evaluator prompt.

BEST_PRACTICES = [
    {
        "id": "bp_001",
        "topic": "donor_retention",
        "content": (
            "Donor Retention Best Practice: Respond to all donor inquiries within "
            "24 hours. Personalize every response using the donor's name and "
            "reference their specific donation details including amount, date, and ID. "
            "Thank donors for their loyalty before addressing their concern. "
            "Always provide a concrete next step or resolution timeline. "
            "Research shows donors who receive personalized responses within 24 hours "
            "are 60% more likely to make a repeat donation. For lapsed donors, "
            "always offer an impact update before asking for renewal."
        ),
    },
    {
        "id": "bp_002",
        "topic": "tax_receipt",
        "content": (
            "Tax Receipt Protocol: Tax receipts must be issued within 48 hours of "
            "receiving a donation. For urgent requests, receipts must be resent "
            "within 2 hours. Always verify the donor's email address before resending. "
            "The receipt must include: donation amount, date of donation, organization "
            "name and tax ID number, and a statement confirming no goods or services "
            "were exchanged in return. For year-end tax season requests, prioritize "
            "same-day processing. Never tell a donor to wait more than 48 hours."
        ),
    },
    {
        "id": "bp_003",
        "topic": "complaint_handling",
        "content": (
            "Complaint Handling Protocol — LAST Model: Listen, Apologize, Solve, Thank. "
            "Acknowledge every complaint within 1 hour. Never be defensive or dismissive. "
            "For financial complaints such as duplicate charges or refund demands, "
            "escalate to the finance team within 1 hour and provide the donor with "
            "a specific resolution timeline within 24 hours. "
            "Document all complaints in the CRM system. Follow up after resolution "
            "to confirm the donor is satisfied. A resolved complaint handled well "
            "can convert an unhappy donor into a loyal advocate."
        ),
    },
    {
        "id": "bp_004",
        "topic": "major_donor",
        "content": (
            "Major Donor Engagement Protocol: Any donation inquiry exceeding $10,000 "
            "requires Executive Director involvement within 24 hours. Always offer "
            "a personal phone call or in-person meeting. Before the meeting, prepare "
            "a customized impact report focused on the donor's area of interest. "
            "Discuss naming opportunities, recognition wall listings, and annual "
            "impact reports. Assign a dedicated relationship manager. "
            "Send handwritten thank-you notes within 48 hours of any major gift. "
            "Major donors should receive quarterly personal updates, not just newsletters."
        ),
    },
    {
        "id": "bp_005",
        "topic": "volunteer_management",
        "content": (
            "Volunteer Management Best Practice: Confirm all volunteer registrations "
            "immediately with a welcome email that includes event details, arrival "
            "time, parking instructions, dress code, and a direct contact number. "
            "For last-minute cancellations, respond empathetically without judgment "
            "and immediately activate the volunteer waitlist. Always maintain a "
            "waitlist of at least 20% extra volunteers for critical events. "
            "Send post-event thank-you messages within 24 hours. "
            "Never remove a volunteer from future opportunities due to a single cancellation."
        ),
    },
    {
        "id": "bp_006",
        "topic": "grant_communication",
        "content": (
            "Grant Communication Protocol: Acknowledge all grant applications within "
            "5 business days with a confirmation email including the application ID. "
            "Provide status updates proactively every 30 days during the review period. "
            "When requesting additional documentation, give applicants at least 2 weeks "
            "to respond. Rejection letters must include constructive feedback explaining "
            "the decision and should encourage reapplication in the next cycle. "
            "Approval letters must clearly detail next steps, reporting requirements, "
            "payment schedule, and designated program officer contact."
        ),
    },
    {
        "id": "bp_007",
        "topic": "media_relations",
        "content": (
            "Media Relations Protocol: All media inquiries must be routed to the "
            "Communications Director within 1 hour of receipt. Staff should never "
            "provide statistics, quotes, or program details without prior approval. "
            "Prepare a standard media kit including a fact sheet, recent impact report, "
            "and executive bio for all incoming press requests. "
            "Always attempt to meet journalist deadlines — missed media coverage "
            "significantly impacts donor acquisition and public awareness. "
            "For negative stories, engage proactively with accurate information."
        ),
    },
    {
        "id": "bp_008",
        "topic": "recurring_donation",
        "content": (
            "Recurring Donation Management: Monitor payment processors daily for "
            "duplicate or failed charges. Process all refunds within 3-5 business days "
            "and notify the donor immediately via email with a confirmation number. "
            "For cancellation requests, always offer a donation pause option (1-3 months) "
            "before processing a full cancellation. Send quarterly impact updates "
            "to all recurring donors to reinforce the value of their ongoing support. "
            "Recurring donors have 90% higher lifetime value than one-time donors "
            "and should be treated as the organization's most valuable partners."
        ),
    },
    {
        "id": "bp_009",
        "topic": "donor_recognition",
        "content": (
            "Donor Recognition Best Practice: Verify all donor recognition lists "
            "at least 3 weeks before any public display or event. Allow donors to "
            "review and approve their listing before publication. "
            "For recognition errors, issue a formal written apology within 24 hours, "
            "correct the error immediately, and offer additional personalized "
            "recognition opportunities as compensation. "
            "Recognition errors are among the most damaging trust violations in "
            "donor relations and must be treated with the highest urgency."
        ),
    },
    {
        "id": "bp_010",
        "topic": "general_response",
        "content": (
            "General Email Response Guidelines: Always address the donor by their "
            "preferred name. Open with a genuine expression of gratitude for their "
            "engagement with the organization. Keep responses concise — under 150 words. "
            "Use warm, human language and avoid corporate jargon. "
            "Every response must end with exactly one clear call to action. "
            "Sign off with your full name, title, and direct contact information. "
            "Never leave a donor, volunteer, or partner without knowing their next step. "
            "Response tone should always be empathetic first, informative second."
        ),
    },
    {
        "id": "bp_011",
        "topic": "planned_giving",
        "content": (
            "Planned Giving and Bequest Protocol: Inquiries about bequests or estate "
            "gifts must be escalated to the Executive Director or Development Director "
            "within 24 hours. Always treat planned giving conversations with the highest "
            "level of sensitivity and confidentiality. Provide donors with a dedicated "
            "planned giving brochure and legal language guidance. "
            "Connect donors with your organization's legal counsel for documentation. "
            "Send a handwritten personal letter of appreciation within 48 hours. "
            "Planned gifts represent the highest form of donor commitment."
        ),
    },
    {
        "id": "bp_012",
        "topic": "corporate_sponsorship",
        "content": (
            "Corporate Sponsorship Protocol: Respond to all corporate sponsorship "
            "inquiries within 24 hours with a formal sponsorship prospectus. "
            "Clearly outline all sponsorship tiers, associated benefits, and deadlines. "
            "Offer a call or meeting to customize the sponsorship package. "
            "Provide post-event impact reports showing logo placement, "
            "audience reach, and media coverage. Corporate sponsors require formal "
            "acknowledgment letters for tax purposes within 5 business days. "
            "Nurture corporate relationships year-round, not only around events."
        ),
    },
]

# ── Quiz Q&A Reference Bank ───────────────────────────────────────────────────
# These are embedded as reference style guides for question generation.
# The LLM uses retrieved similar Q&As as style and difficulty references
# but must create NEW questions — not copy these.

QUIZ_QA_BANK = [
    {
        "id": "qa_001",
        "topic": "donor_retention",
        "question": (
            "A major donor who has given annually for 5 years emails saying "
            "they feel disconnected from your organization's impact. "
            "What is the BEST immediate response?"
        ),
        "correct_answer": "B",
        "options": [
            "A. Send them your standard monthly newsletter",
            "B. Call them personally within 24 hours and schedule an impact briefing",
            "C. Email them a copy of your last annual report",
            "D. Add them to the donor recognition wall at the next event",
        ],
        "explanation": (
            "Long-term donors showing disengagement need immediate personal outreach. "
            "A phone call within 24 hours shows they are valued as individuals. "
            "Generic newsletters or reports without personalization will not "
            "address the core issue of feeling disconnected."
        ),
    },
    {
        "id": "qa_002",
        "topic": "complaint_handling",
        "question": (
            "A donor calls furious about a duplicate charge on their credit card "
            "from last month's donation. What should you do FIRST?"
        ),
        "correct_answer": "A",
        "options": [
            "A. Apologize sincerely, confirm the error, and provide a refund timeline",
            "B. Ask them to email their bank statement as proof",
            "C. Transfer them directly to the finance department",
            "D. Explain that billing errors are reviewed at month end",
        ],
        "explanation": (
            "Using the LAST model (Listen, Apologize, Solve, Thank), the first step "
            "is always to acknowledge the error and apologize empathetically. "
            "Making an upset donor wait, seek proof, or navigate departments "
            "will escalate the complaint and risk losing the relationship permanently."
        ),
    },
    {
        "id": "qa_003",
        "topic": "tax_receipt",
        "question": (
            "A donor urgently needs their tax receipt because their filing "
            "deadline is tomorrow. What is the correct protocol?"
        ),
        "correct_answer": "C",
        "options": [
            "A. Tell them receipts are processed in 5 to 7 business days",
            "B. Ask them to check their spam folder first",
            "C. Process and resend the receipt within 2 hours as an urgent request",
            "D. Escalate to a supervisor and follow up the following week",
        ],
        "explanation": (
            "Urgent tax receipt requests must be processed within 2 hours. "
            "Tax filing deadlines are legally non-negotiable for donors. "
            "Standard processing timelines do not apply to urgent requests. "
            "Failing to help promptly can permanently damage the donor relationship."
        ),
    },
    {
        "id": "qa_004",
        "topic": "major_donor",
        "question": (
            "A foundation contacts your organization about a potential $75,000 "
            "donation. Who must be involved in the response and within what timeframe?"
        ),
        "correct_answer": "D",
        "options": [
            "A. The volunteer coordinator within 1 week",
            "B. The social media manager within 48 hours",
            "C. The events team within 3 days",
            "D. The Executive Director within 24 hours",
        ],
        "explanation": (
            "Donations exceeding $10,000 require Executive Director involvement "
            "within 24 hours per major donor protocol. Major donors expect "
            "senior-level engagement. Assigning junior staff or delaying the "
            "response signals the organization does not value the relationship."
        ),
    },
    {
        "id": "qa_005",
        "topic": "volunteer_management",
        "question": (
            "A volunteer cancels 2 hours before a major event citing a personal "
            "emergency. What is the most appropriate organizational response?"
        ),
        "correct_answer": "B",
        "options": [
            "A. Express frustration and remove them from future volunteer lists",
            "B. Respond empathetically, activate the waitlist, and invite them to future events",
            "C. Ask the volunteer to personally find their own replacement",
            "D. Send a formal written notice about the cancellation policy",
        ],
        "explanation": (
            "Volunteers are essential partners, not employees. Responding with "
            "empathy preserves the long-term relationship. Maintaining a 20% "
            "volunteer waitlist buffer is best practice specifically to handle "
            "last-minute cancellations without disrupting operations."
        ),
    },
    {
        "id": "qa_006",
        "topic": "grant_communication",
        "question": (
            "A foundation that submitted a grant application 4 weeks ago has "
            "not received any communication from your organization. "
            "According to best practice, what should have already happened?"
        ),
        "correct_answer": "A",
        "options": [
            "A. An acknowledgment email within 5 days and a status update at 30 days",
            "B. A full decision letter within 2 weeks",
            "C. A phone call requesting additional information",
            "D. Nothing — foundations understand review processes take time",
        ],
        "explanation": (
            "Grant communication protocol requires acknowledging all applications "
            "within 5 business days and providing proactive status updates every "
            "30 days. Silence creates uncertainty that can damage the organization's "
            "reputation in the philanthropic community and discourage future applications."
        ),
    },
    {
        "id": "qa_007",
        "topic": "media_relations",
        "question": (
            "A journalist calls asking for statistics about your program outcomes "
            "for a story being published tomorrow. A staff member answers the call. "
            "What is the correct action?"
        ),
        "correct_answer": "C",
        "options": [
            "A. Share the statistics from last year's annual report immediately",
            "B. Decline the interview and hang up politely",
            "C. Route the inquiry to the Communications Director within 1 hour",
            "D. Ask the journalist to submit a written request first",
        ],
        "explanation": (
            "Media relations protocol requires all inquiries to be routed to the "
            "Communications Director within 1 hour. Staff should never provide "
            "statistics or quotes without approval. Engaging with media without "
            "preparation risks factual errors, misquotes, or unauthorized disclosures."
        ),
    },
    {
        "id": "qa_008",
        "topic": "recurring_donation",
        "question": (
            "A recurring donor of 2 years says they want to cancel their "
            "monthly donation. What should you offer BEFORE processing the cancellation?"
        ),
        "correct_answer": "B",
        "options": [
            "A. Process the cancellation immediately to respect their decision",
            "B. Offer a 1 to 3 month donation pause as an alternative",
            "C. Ask them to reconsider by sending a donation impact video",
            "D. Escalate to the Executive Director to personally call the donor",
        ],
        "explanation": (
            "Best practice requires offering a donation pause option of 1 to 3 months "
            "before processing any recurring donation cancellation. "
            "Recurring donors have 90% higher lifetime value and often cancel due "
            "to temporary financial stress rather than permanent disengagement. "
            "A pause option retains 30-40% of donors who would otherwise cancel."
        ),
    },
]