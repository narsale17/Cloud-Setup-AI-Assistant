# Cloud Setup Simplified (AI Assistant) 🚀  

### **An AI-powered chatbot that simplifies cloud setup using natural language.**  

## 📌 **Overview**  
Cloud computing can be complex, requiring CLI commands, Terraform scripts, or extensive GUI navigation. **Cloud Setup Simplified** bridges this gap by providing a **Generative AI-powered chatbot** that helps users configure cloud resources effortlessly.  

With a simple text input like *"Create an EC2 instance with 4GB RAM"*, the AI assistant provides:  
- 📍 **Step-by-step GUI instructions**  
- 🖥 **CLI commands for manual execution**  
- ⚡ **Automated provisioning (Optional feature)**  

---

## 🎯 **Features**  
✅ **Conversational AI-driven cloud setup**  
✅ **Multiple execution options (GUI, CLI, Automated)**  
✅ **No cloud expertise required** – Designed for **non-technical users**  
✅ **Supports Google Cloud (AWS & Azure planned)**  
✅ **FastAPI backend + Google Vertex AI for processing**  
✅ **Browser extension for real-time GCP assistance** *(Future Enhancement)*  

---

## 🛠 **Tech Stack**  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** FastAPI, Google Vertex AI (Gemini API)  
- **Database:** Firestore (for storing user queries)  
- **Cloud Execution:** Terraform, GCloud SDK  
- **Hosting:** Google Cloud Run  

---

## 🚀 **How It Works**  
1️⃣ **User enters a request**: "Create a MySQL database on GCP with backups enabled."  
2️⃣ **AI processes and suggests a cloud setup plan**  
3️⃣ **User selects a deployment method**:  
   - Step-by-step **GUI-based instructions**  
   - **CLI command generation**  
   - **Automated provisioning (if enabled)**  
4️⃣ **Deployment completes, reducing setup time** 🎯  

---

## 📌 **Installation**  

### **1️⃣ Clone the repository**  
```bash
git clone https://github.com/yourusername/cloud-setup-simplified.git
cd cloud-setup-simplified

