# 🫁 Anatomy Trains AI Portal: Automated MPT Learning Stack

[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-blue?logo=google-gemini&logoColor=white&style=for-the-badge)](https://aistudio.google.com/)
[![Brevo](https://img.shields.io/badge/SMTP-Brevo-green?logo=brevo&logoColor=white&style=for-the-badge)](https://www.brevo.com/)
[![GitHub Actions](https://img.shields.io/badge/Workflow-GitHub%20Actions-black?logo=github-actions&logoColor=white&style=for-the-badge)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An automated, serverless, **$0-cost educational engine** engineered for postgraduate Master of Physiotherapy (MPT) specializations. The system natively streams Thomas Myers' complete _"Anatomy Trains: Myofascial Meridians for Manual and Movement Therapists"_ textbook directly into a 1-million token native context window. By tracking historical states, it dynamically scales clinical lecture complexity, injects a progress dashboard tracker, compiles a structured interactive quiz, and isolates the answer keys at the absolute footer baseline of a beautifully rendered daily responsive HTML email layout.

---

## 🚀 Key Features

- **Native Long-Context Analysis (Zero Fragmentation):** Replaces traditional vector-based RAG architectures. By reading the textbook completely un-chunked, the model retains pristine comprehension of global, continuous myofascial meridians without losing structural contexts across chapters[cite: 1].
- **Telemetry-Driven Adaptive Pacing:** Tracks milestones within a state-managed `progress.json` ledger, automatically adjusting target study sessions from 15 minutes up to an exhaustive 60-minute masterclass lecture.
- **Anti-Spoiler Assessment Logic:** Formulates rigorous clinical multiple-choice questions in the mid-section of the syllabus layout while appending detailed physiological rationales strictly at the absolute baseline footer.
- **Automated Sync Dashboard:** Dynamically compiles a chronological overview of your completed modules, rendering your active learning progression metrics into every fresh email dispatch.
- **Serverless $0 Operational Budget:** Operates entirely within the free executing compute frames of GitHub Actions pipelines, Google AI Studio tokens, and Brevo SMTP daily transactional allowances (300 free emails/day).

---

## 🛠️ System Architecture

```text
  [GitHub Actions Cron]
           │
           ▼
┌──────────────────────┐      Reads Current State
│  generate_lesson.py  │◄─────────────────────────────┐
└──────────┬───────────┘                              │
           │                                          │
           ├─► Temp Uploads ──► [Anatomy Trains PDF]  │
           │                                          │
           ├─► Dispatches ────► [Gemini Flash Engine] │
           │                                          │
           ├─► Compiles HTML ─► [Brevo SMTP Server] ──┼─► (Delivers Email Inbox)
           │                                          │
           ▼                                          │
   Appends History Log ───────────────────────────────┘
           │
           ▼
[Auto-Commit: progress.json & lessons/*.md] ──► (Saves History to Git)
```

## Setup a clean local python isolated execution virtual sandbox

python -m venv .venv

## Activate your newly configured isolated sandbox environment

## On macOS/Linux:

source .venv/bin/activate

## On Windows (PowerShell):

.venv\Scripts\Activate.ps1

## On Windows (Command Prompt):

.venv\Scripts\activate.bat

## Install core parsing and translation dependencies packages

pip install -r requirements.txt

## 🚀 Let's Connect

<p align="center">
  <img src="https://media.licdn.com/dms/image/v2/D4D03AQExq8xiys4Maw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1712999308042?e=1782345600&v=beta&t=8iYi3LQrNgnBsRyWtM2_YvsoR1MdtdbXOjl-FXMsEQM" alt="Kush Hingol" width="100" style="border-radius:50%;" />
</p>

<p align="center">
  <b>Kush Hingol</b><br>
  AI • Cloud • Software Engineering • Automation
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/kush-hingol/">
    <img src="https://img.shields.io/badge/Follow%20on-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
</p>

<p align="center">
  If you enjoy this project, let's connect and discuss AI, AWS, Cloud Engineering, Automation, and Software Development.
</p>

⭐ If this repository helped you, consider giving it a star!
