// lib/trainingData.ts

export type Difficulty = "Easy" | "Medium" | "Hard";

export type ScamType =
  | "Website"
  | "Email"
  | "SMS"
  | "WhatsApp"
  | "Phone"
  | "UPI"
  | "QR Code"
  | "Shopping"
  | "Investment"
  | "Banking"
  | "Job Scam";

export interface TrainingQuestion {
  id: number;
  difficulty: Difficulty;
  type: ScamType;
  question: string;
  options: ["Safe", "Scam"];
  answer: "Safe" | "Scam";
  explanation: string;
  threatIndicators: string[];
}

export const trainingQuestions: TrainingQuestion[] = [
  {
    id: 1,
    difficulty: "Easy",
    type: "SMS",
    question:
      "Dear Customer, your SBI account has been blocked. Click http://sbi-verify-now.tk to reactivate immediately.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Banks never ask customers to verify accounts through random shortened or suspicious links sent via SMS.",
    threatIndicators: ["Urgency", "Fake Link", "Credential Theft"],
  },
  {
    id: 2,
    difficulty: "Easy",
    type: "Email",
    question:
      "Email from 'amazon-support@amaz0n-deals.com' stating you won a free iPhone 15 Pro. Click to claim within 2 hours.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "The sender domain uses a zero instead of 'o' and creates false urgency, both classic phishing signs.",
    threatIndicators: ["Spoofed Domain", "Too Good To Be True", "Time Pressure"],
  },
  {
    id: 3,
    difficulty: "Easy",
    type: "WhatsApp",
    question:
      "Message from unknown number: 'Hi Dad, I lost my phone, this is my new number. Please send Rs 15,000 urgently.'",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "This is the classic 'family emergency' impersonation scam relying on emotional urgency and unverified identity.",
    threatIndicators: ["Impersonation", "Emotional Manipulation", "Urgency"],
  },
  {
    id: 4,
    difficulty: "Easy",
    type: "UPI",
    question:
      "A stranger sends a UPI collect request saying 'Please accept to receive Rs 5000 cashback'.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "UPI collect requests are used to authorize payments FROM your account. Accepting one meant for 'receiving money' actually deducts money.",
    threatIndicators: ["Fake Cashback", "UPI Collect Trick", "Unknown Sender"],
  },
  {
    id: 5,
    difficulty: "Easy",
    type: "Phone",
    question:
      "Caller claims to be from your bank's fraud department and asks you to share the OTP to 'cancel a suspicious transaction'.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "No legitimate bank employee will ever ask for your OTP over a phone call under any circumstance.",
    threatIndicators: ["OTP Request", "Authority Impersonation", "Urgency"],
  },
  {
    id: 6,
    difficulty: "Easy",
    type: "QR Code",
    question:
      "A seller on a resale app asks you to scan a QR code and enter your UPI PIN to 'receive' payment for your item.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Scanning a QR code and entering a PIN is only required to SEND money, never to receive it.",
    threatIndicators: ["QR Payment Trick", "PIN Request", "Marketplace Fraud"],
  },
  {
    id: 7,
    difficulty: "Easy",
    type: "Shopping",
    question:
      "You browse an official brand website, add items to cart, and pay via the brand's verified payment gateway.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "Shopping on a verified official domain using a recognized payment gateway is a normal, safe transaction.",
    threatIndicators: [],
  },
  {
    id: 8,
    difficulty: "Easy",
    type: "Banking",
    question:
      "You log in to your bank's official app using your fingerprint to check your account balance.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "Using the official banking app with biometric authentication is a secure, standard practice.",
    threatIndicators: [],
  },
  {
    id: 9,
    difficulty: "Easy",
    type: "Email",
    question:
      "Newsletter email from a company you subscribed to, with an unsubscribe link at the bottom.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "A newsletter from a service you knowingly subscribed to, with a standard unsubscribe option, is legitimate.",
    threatIndicators: [],
  },
  {
    id: 10,
    difficulty: "Easy",
    type: "Job Scam",
    question:
      "A recruiter messages offering a work-from-home job paying Rs 5,000/day for 'liking YouTube videos', requiring a refundable registration fee first.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Legitimate employers never ask candidates to pay money upfront to secure a job or task-based income.",
    threatIndicators: ["Upfront Fee", "Unrealistic Pay", "Too Good To Be True"],
  },
  {
    id: 11,
    difficulty: "Medium",
    type: "Website",
    question:
      "A site named 'flipkart-mega-sale-offers.com' shows 90% off on iPhones with a countdown timer and demands payment via UPI only.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "The domain is not the official Flipkart domain, and extreme discounts with forced UPI-only payment and countdown pressure are classic fake e-commerce tactics.",
    threatIndicators: ["Fake Domain", "Unrealistic Discount", "Payment Pressure"],
  },
  {
    id: 12,
    difficulty: "Medium",
    type: "Investment",
    question:
      "A Telegram group promises guaranteed 300% returns in 7 days through a 'stock trading algorithm', requiring an initial deposit to join.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Guaranteed high returns in a short time frame are a hallmark of Ponzi and pump-and-dump investment scams.",
    threatIndicators: ["Guaranteed Returns", "Unregulated Platform", "Upfront Deposit"],
  },
  {
    id: 13,
    difficulty: "Medium",
    type: "Banking",
    question:
      "SMS says: 'Your KYC is expiring today. Update immediately at http://bit.ly/kyc-update-sbi or account will be frozen.'",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Shortened links, artificial deadlines, and 'account freeze' threats are typical of KYC phishing scams.",
    threatIndicators: ["Shortened URL", "Fake Deadline", "Threat of Account Freeze"],
  },
  {
    id: 14,
    difficulty: "Medium",
    type: "WhatsApp",
    question:
      "A message with an official-looking logo says you're selected for a 'government subsidy scheme' and asks you to fill your Aadhaar and bank details on an external form.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Government schemes are never announced or processed through unsolicited WhatsApp messages requesting sensitive ID and bank data.",
    threatIndicators: ["Sensitive Data Request", "Fake Authority", "External Form"],
  },
  {
    id: 15,
    difficulty: "Medium",
    type: "Email",
    question:
      "An email from your actual HR, sent from the company domain, confirming your approved leave dates.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "An email from a verified internal company domain about routine HR matters is legitimate business communication.",
    threatIndicators: [],
  },
  {
    id: 16,
    difficulty: "Medium",
    type: "Phone",
    question:
      "A call from an unknown number claims to be 'TRAI' saying your SIM will be disconnected in 2 hours due to illegal activity, and transfers you to 'cybercrime officer' demanding money via UPI to avoid arrest.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "This is the 'digital arrest' scam. No government agency disconnects SIMs via phone call or demands money to avoid arrest.",
    threatIndicators: ["Fear Tactics", "Fake Authority", "Digital Arrest Scam"],
  },
  {
    id: 17,
    difficulty: "Medium",
    type: "Shopping",
    question:
      "You receive a message with a tracking link for a package you actually ordered, matching the courier's real domain.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "A tracking notification matching a real order and a verified courier domain is a normal delivery update.",
    threatIndicators: [],
  },
  {
    id: 18,
    difficulty: "Medium",
    type: "UPI",
    question:
      "Someone claiming to be an army officer selling furniture online asks you to pay a small 'verification amount' via a payment link before shipping.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Fake military personnel scams on marketplaces pressure buyers into upfront payments using fabricated verification steps.",
    threatIndicators: ["Fake Identity", "Upfront Payment", "Marketplace Fraud"],
  },
  {
    id: 19,
    difficulty: "Medium",
    type: "QR Code",
    question:
      "A flyer pasted over a legitimate parking meter QR code redirects to a payment page with a slightly misspelled municipal domain.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "QR code tampering (quishing) in public places redirects victims to fraudulent payment pages using lookalike domains.",
    threatIndicators: ["QR Tampering", "Lookalike Domain", "Public Location Fraud"],
  },
  {
    id: 20,
    difficulty: "Medium",
    type: "Job Scam",
    question:
      "LinkedIn message from a 'recruiter' with no company page, asking you to pay Rs 2,000 for a 'background verification' before an interview is scheduled.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Legitimate companies conduct and pay for their own background verification; candidates are never charged for it.",
    threatIndicators: ["Upfront Fee", "No Verifiable Company", "Unusual Process"],
  },
  {
    id: 21,
    difficulty: "Hard",
    type: "Email",
    question:
      "An email appears to come from your CEO's exact email address, urgently requesting an immediate wire transfer for a 'confidential acquisition', asking you not to call to confirm.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "This is Business Email Compromise (BEC). Spoofed executive emails combined with confidentiality and urgency requests are designed to bypass verification.",
    threatIndicators: ["Executive Impersonation", "Urgency", "Request to Avoid Verification"],
  },
  {
    id: 22,
    difficulty: "Hard",
    type: "Website",
    question:
      "A banking login page has the correct logo and layout, valid HTTPS padlock, but the URL is 'hdfcbank.secure-login-portal.com'.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "HTTPS only confirms an encrypted connection, not legitimacy. The actual domain is a subdomain trick designed to impersonate the real bank.",
    threatIndicators: ["Subdomain Spoofing", "Fake HTTPS Trust", "Visual Impersonation"],
  },
  {
    id: 23,
    difficulty: "Hard",
    type: "Investment",
    question:
      "A polished trading app, downloaded outside the Play Store, shows your portfolio growing daily, but withdrawal always requires paying a 'tax' or 'unlock fee' first.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Fake trading apps display fabricated growth to build trust, then demand endless upfront fees to block real withdrawals.",
    threatIndicators: ["Sideloaded App", "Fake Portfolio Growth", "Withdrawal Fee Trap"],
  },
  {
    id: 24,
    difficulty: "Hard",
    type: "Phone",
    question:
      "A voice call using an AI-cloned voice of your relative, sounding distressed, asks for urgent money transfer to a new account due to a 'car accident'.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "AI voice cloning scams replicate a loved one's voice to exploit panic and urgency; always verify through a separate channel before acting.",
    threatIndicators: ["AI Voice Cloning", "Emotional Urgency", "Unverified Channel"],
  },
  {
    id: 25,
    difficulty: "Hard",
    type: "UPI",
    question:
      "A fraudulent tech support pop-up convinces you to install a remote screen-sharing app, then guides you to 'test' a refund by entering your UPI PIN.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Remote access combined with a live PIN entry lets scammers directly observe and steal credentials or authorize transactions.",
    threatIndicators: ["Remote Access Trojan", "Fake Refund", "Live Credential Theft"],
  },
  {
    id: 26,
    difficulty: "Hard",
    type: "SMS",
    question:
      "SMS appears in the same thread as your bank's real messages (same sender ID), saying a large debit was made and to call a number to dispute it.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "SMS sender ID spoofing can insert fake messages into a legitimate thread; always verify through the bank's official app or number, not one provided in the message.",
    threatIndicators: ["Sender ID Spoofing", "Fake Alert", "Provided Contact Number"],
  },
  {
    id: 27,
    difficulty: "Hard",
    type: "Banking",
    question:
      "You initiate a transfer yourself through your bank's official app to a payee you manually verified and saved previously.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "A self-initiated transfer through an official app to a previously verified payee is a standard, secure transaction.",
    threatIndicators: [],
  },
  {
    id: 28,
    difficulty: "Hard",
    type: "Shopping",
    question:
      "A 'clearance sale' Instagram ad links to a store with no return policy, no physical address, only advance payment via personal UPI ID, and reviews are all posted the same week.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Lack of business verification, personal UPI collection, and suspiciously uniform reviews indicate a fraudulent pop-up shopping scam.",
    threatIndicators: ["No Business Verification", "Personal UPI Collection", "Fake Reviews"],
  },
  {
    id: 29,
    difficulty: "Hard",
    type: "Job Scam",
    question:
      "You're hired after a real interview, receive an official offer letter on company letterhead from the verified corporate domain, and onboarding starts via the company's HR portal.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "A verified interview process, corporate domain communication, and formal HR onboarding indicate a legitimate job offer.",
    threatIndicators: [],
  },
  {
    id: 30,
    difficulty: "Hard",
    type: "QR Code",
    question:
      "A restaurant table QR code, matching the printed menu branding and consistent with the restaurant's known ordering system, opens the official ordering site.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "A QR code consistent with the venue's known, verified ordering system opening the legitimate site is a normal safe use case.",
    threatIndicators: [],
  },
  {
    id: 31,
    difficulty: "Medium",
    type: "WhatsApp",
    question:
      "A message says you've been added to a 'stock tips' group by a mutual contact, with screenshots of other members' profits, urging you to invest via a linked app.",
    options: ["Safe", "Scam"],
    answer: "Scam",
    explanation:
      "Fake investment groups use fabricated profit screenshots and social proof from added 'members' to lure victims into fraudulent trading apps.",
    threatIndicators: ["Fake Social Proof", "Unregulated App", "Group Pressure"],
  },
  {
    id: 32,
    difficulty: "Easy",
    type: "Investment",
    question:
      "You invest through your bank's official mutual fund portal after completing standard KYC verification.",
    options: ["Safe", "Scam"],
    answer: "Safe",
    explanation:
      "Investing through a regulated, official bank portal with standard KYC is a legitimate and safe financial activity.",
    threatIndicators: [],
  },
];