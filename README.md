# SIFY – Cloud Setup Simplified (AI-Powered Assistant)

SIFY is a generative AI-powered chatbot designed to simplify cloud infrastructure setup on Google Cloud Platform (GCP). It allows users to describe what they want in natural language and provides tailored configuration assistance based on their cloud experience level.



## Overview

Cloud configuration can be challenging, especially for beginners. SIFY bridges this gap by offering a conversational interface that understands what the user wants and guides them through setting up the required cloud services.

Key Highlights:
- Supports multiple user experience levels: Beginner, Intermediate, and Expert
- Dynamic question generation based on user expertise
- Generates CLI commands, GCP Console steps, or automates provisioning
- Built with FastAPI backend and Google Vertex AI (Gemini) for natural language understanding



## User Flow

1. **User Logs In**
   - The user enters their name and selects their experience level (Beginner, Intermediate, or Expert).
   - This information is stored in a session and used throughout the chat to tailor the experience.

2. **User Describes Their Requirement**
   - Example: "I need a scalable web app."
   - SIFY processes the request and identifies the necessary GCP services (e.g., Compute Engine, Load Balancer, Cloud SQL).

3. **Service Configuration**
   - For each required service, SIFY identifies key configuration parameters (e.g., machine type, region).
   - Based on the user’s experience level:
     - Beginners receive simple and intuitive questions.
     - Intermediate users receive slightly more detailed prompts.
     - Experts get direct, technical queries (e.g., "Choose a machine type (e2-medium, n2-standard-4)").

4. **Session Storage**
   - All answers provided by the user are stored in the session for later use.

5. **Final Configuration Summary**
   - Once all necessary questions are answered, SIFY generates a configuration summary based on the user’s responses.

6. **Deployment Options**
   - CLI: Provides ready-to-use terminal commands.
   - Console: Provides step-by-step manual instructions for the GCP Console.
   - Automated Setup (future scope): Automatically provisions the resources.



## Future Improvements

1. **Enhance Experience-Based Questioning**  
   - Improve how SIFY adapts its responses for beginners, intermediate users, and experts by adjusting the tone, complexity, and technical depth of each question.

2. **Smooth Follow-up Logic**  
   - Refine the flow of follow-up questions to ensure that SIFY collects all required configuration inputs across services in a logical, user-friendly manner.

3. **One-Click Automated Setup via Extension Interface**  
   - Develop a complete automation feature that mimics an extension-like interface.  
   - With one click, users will be able to provision and configure all requested services, making the entire setup process fully hands-off.



## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** FastAPI
- **AI Integration:** Google Vertex AI (Gemini API)
- **Database:** Firestore
- **Session Handling:** Python Sessions
- **Cloud Provisioning (Optional):** Terraform, GCloud CLI

