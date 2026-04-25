export const URGENCY_CONFIG = {
  critical: { bg: "bg-red-500",    text: "text-white",  ring: "#EF4444", label: "CRITICAL" },
  high:     { bg: "bg-orange-500", text: "text-white",  ring: "#F97316", label: "HIGH"     },
  medium:   { bg: "bg-yellow-400", text: "text-black",  ring: "#FBBF24", label: "MEDIUM"   },
  low:      { bg: "bg-emerald-500",text: "text-white",  ring: "#10B981", label: "LOW"      },
};

export const INTENT_ICON = {
  donation_inquiry:  "💰",
  volunteer_request: "🤝",
  complaint:         "⚠️",
  general_info:      "ℹ️",
  grant_application: "📋",
  media_inquiry:     "📰",
};

export const SAMPLE_EMAILS = [
  {
    label: "Urgent Receipt",
    preview: "Missing tax receipt — gala next week…",
    text: "Hi, my name is Sarah Johnson. I made a donation of $500 on March 15th with reference ID DON-20240315. I haven't received my tax receipt yet and the gala is next week. This is very urgent. Please help!",
  },
  {
    label: "Volunteer Drop",
    preview: "Volunteer John withdrawing from food drive…",
    text: "Dear team, volunteer John Martinez (VOL-8821) would like to withdraw from the April 12 food drive. He says something came up. Can someone reach out to find a replacement?",
  },
  {
    label: "Grant Inquiry",
    preview: "Gates Foundation requesting updated financials…",
    text: "I'm reaching out on behalf of the Gates Foundation regarding your 2024 community grant proposal GRN-4492. Could you send updated financials before Friday?",
  },
];

export const QUIZ_TOPICS = [
  "Responding to major donor emails",
  "Handling volunteer cancellations",
  "Donor retention best practices",
  "Writing grant acknowledgment letters",
  "Managing media inquiries",
  "Escalating urgent donor complaints",
];

export const DIFFICULTIES = ["easy", "medium", "hard"];

export const TRIAGE_STEPS = [
  "Classifying intent…",
  "Extracting entities…",
  "Generating draft…",
];