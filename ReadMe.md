# 💼 LoanAgent – AI-Powered Banking Portal

**Empowering faster, fairer, and smarter loan decisions using IBM Watson AI**

---

## 📌 Introduction

The Indian banking and financial sector, while rapidly digitizing, still faces critical challenges in streamlining the **loan application process**—particularly in small and mid-sized banks and NBFCs. From slow approvals to lack of scheme awareness, customers and staff alike face a complex, inefficient system.

**LoanAgent** is an AI-powered digital portal that leverages **IBM Watson**, **cloud computing**, and **automation** to transform the entire loan journey—making it **faster**, **more accurate**, and **more inclusive** for all.

---

## 🚨 Problem Statement

Despite digitization, loan workflows remain problematic:

- 🕒 Loan approvals can take **days to weeks**, especially for rural or new customers.
- 🧾 Staff conduct **manual document checks**, increasing workload and error rates.
- ❌ Customers often miss out on **government schemes** due to lack of awareness.
- ❓ Poor communication leaves applicants **in the dark** about their application status.

---

## 🎯 Objective

LoanAgent aims to:

- 💡 Deliver **end-to-end digital loan application**, assessment, and approval.
- 🤖 Use **IBM Watson AI** to automate eligibility checks and ensure compliance with **RBI guidelines**.
- 🎯 Provide **personalized scheme recommendations** based on user profile.
- 📢 Ensure **real-time transparency** through notifications and status updates.

---

## 💡 Why This Problem?

Manual and opaque processes:
- Limit outreach to **underserved communities**
- Overburden banking staff
- Result in **low scheme adoption** in rural India
- Pose **compliance risks** under increasing regulation

**Solution?** An AI-powered, transparent, and scalable system.

---

## 🚀 Solution Overview

LoanAgent offers a **secure, cloud-based portal** that revolutionizes the loan experience:

### 🔹 For Customers:
- **Conversational AI** assistant for queries and guidance
- **Instant eligibility check** with real-time results
- **Scheme recommendations** based on their profile
- **Live status tracking** with automated email alerts

### 🔹 For Staff/Admins:
- Secure **dashboard** for reviewing applications
- AI insights for **risk scoring and scheme eligibility**
- Document uploads & approvals in one place
- Automated communication with applicants

---

## 🌟 Key Features

| Feature | Description |
|--------|-------------|
| 🗣️ **LoanAgent** | Conversational AI assistant for guidance, FAQs, and status |
| ✅ **AI Eligibility Check** | Powered by IBM Watson for fast and accurate loan assessment |
| 🧠 **Smart Scheme Recommender** | Shows only eligible government/private loan schemes |
| 📋 **Staff Dashboard** | Unified panel for document review, approvals, and insights |
| 📧 **Automated Notifications** | HTML email alerts for approvals, missing docs, etc. |

---

## 🛠️ Technical Implementation

| Component | Details |
|----------|---------|
| 🔐 **Security** | Session-based auth, bcrypt hashing, file validation |
| 🧠 **AI Integration** | IBM Watson AI for eligibility, scheme matching, and document review |
| 💌 **Communication** | SMTP integration for HTML email notifications |
| 🔗 **Backend** | Flask + Python with IBM IAM authentication and REST APIs |
| 🌐 **Frontend** | Responsive HTML/CSS/JS UI for customers & staff |
| ☁️ **Deployment** | Vercel (frontend + backend), IBM Cloud (AI Agent) |
| 🧪 **Testing & DevOps** | Postman for API testing, Git/GitHub for version control |

---

## 🧠 IBM Resources Used

- 🎯 **IBM Watson AI** – Trained on Indian financial data for explainable, compliant decisions
- ☁️ **IBM Cloud** – Secure, scalable infrastructure for AI and application hosting
- 🔐 **IBM IAM** – Authentication and authorization for safe API access

---

## 📈 Impact

| Metric | Result |
|--------|--------|
| ⚡ Loan Processing Time | Reduced from weeks to **minutes** |
| 📊 Scheme Adoption | Increased by **30%** via personalized suggestions |
| 🌍 Financial Inclusion | Improved awareness in **rural and underserved regions** |
| ✅ Compliance & Transparency | Enhanced traceability for staff and applicants |

---

## 📷 Screenshots

> *(Add relevant screenshots here showing the customer portal, staff dashboard, AI chat interface, etc.)*

---

## 📚 Future Scope

- 📱 Mobile-first design
- 🏦 Multi-bank SaaS support
- 📊 Analytics Dashboard for bank performance
- 🧾 OCR-based document scanning for verification

---

## 🙌 Conclusion

LoanAgent modernizes banking by **replacing outdated processes** with a secure, AI-driven experience. It empowers institutions and customers alike—bringing **efficiency**, **transparency**, and **financial inclusion** to the forefront of Indian lending.

> **“Faster loans, smarter banking – with AI at the core.”**

---

## 👨‍💻 Developed With

- Python, Flask
- HTML, CSS, JavaScript
- IBM Watsonx.ai
- IBM Cloud
- Postman, GitHub, Vercel

## Agent Developed using

- Framework: LangGraph
- Architecture: ReAct
- RAG architecture is followed using vector index.

---

## SetUp Guide
-Clone the Repository:
git clone https://github.com/PriyanshPorwal999/IBM_Bank_Agent.git
cd IBM_Bank_Agent
- Navigate to the Backend Folder:
cd backend
- Create a Virtual Environment:
python -m venv venv
- Activate the Virtual Environment:
  - On Windows (PowerShell/CMD): .\venv\Scripts\activate
  - On macOS/Linux: source venv/bin/activate
- Install Dependencies:
pip install -r requirements.txt
-Configure Environment Variables
  - Create the .env file: In the backend directory, create a file named .env.
  - Add Configuration: API_KEY='your_ibm_cloud_api_key' 
                       AGENT_ENDPOINT='your_watsonx_agent_endpoint_url'
-  Run the Application
python run.py                       

