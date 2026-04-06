# 🚀 RBAC Approval & Federated Learning System (Streamlit)

## 📌 Overview

This project is a **Role-Based Approval & Authorization System** built using **Streamlit**, designed as part of an IT Prototyping assignment using **Design Thinking principles**.

The system simulates a real-world **Leave/Request Approval Workflow** with:

* Role-Based Access Control (RBAC)
* Multi-level approval logic
* Exception handling
* Secure login & authorization
* Federated Learning simulation (privacy-preserving AI concept)

---

## 🎯 Features

### 🔐 Authentication & Authorization

* Secure login system (email + password)
* Session-based authentication
* Role-based access control (RBAC)
* Unauthorized access prevention

---

### 👥 Role-Based Access (RBAC)

| Role        | Permissions                                  |
| ----------- | -------------------------------------------- |
| **User**    | Submit requests, view own requests           |
| **Manager** | Approve / Reject requests                    |
| **Admin**   | Full control (override decisions, view logs) |

---

### 📊 Approval Workflow

* User submits a request
* Manager reviews:

  * Approves if within threshold
  * Escalates if above threshold
  * Rejects if necessary
* Admin has final authority:

  * Override approvals/rejections
  * Handle escalated requests

---

### 🔄 Data Dependency Logic

Approval decisions depend on:

* Budget threshold (`<= 10000`)
* Manager decision
* Request validity

**Flow:**

```
User → Submit → Manager Decision → (Approve / Reject / Escalate) → Admin Override (if needed)
```

---

### ⚠️ Exception Handling

The system handles:

* Invalid login attempts (with limit)
* Unauthorized access
* Missing input data
* High-budget escalation
* System logging for audit

---

### 🧠 Federated Learning Simulation

Simulates decentralized learning:

```
User Device → Local Training → Share Parameters → Aggregation → Global Model
```

* No raw data sharing
* Only model updates are aggregated
* Demonstrates privacy-preserving AI

---

## 🏗️ Project Structure

```
approval-system/
│
├── app.py                # Main Streamlit application
├── pyproject.toml        # Project configuration
├── uv.lock               # Dependency lock file
├── README.md             # Documentation
└── .venv/                # Virtual environment (auto-created)
```

---

## ⚙️ Setup Instructions (Using uv)

### 1️⃣ Install uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

---

### 2️⃣ Initialize Project

```bash
uv init
```

---

### 3️⃣ Add Dependencies

```bash
uv add streamlit pandas
```

---

### 4️⃣ Run the Application

```bash
uv run streamlit run app.py
```

---

### 5️⃣ Reproduce Environment

```bash
uv sync
```

---

## 🔑 Default Credentials

| Role    | Email                                       | Password |
| ------- | ------------------------------------------- | -------- |
| User    | [user@test.com](mailto:user@test.com)       | 123      |
| Manager | [manager@test.com](mailto:manager@test.com) | 123      |
| Admin   | [admin@test.com](mailto:admin@test.com)     | 123      |

---

## 🧠 Design Thinking Implementation

### 1. Empathize

* Identified users: Employees, Managers, Admins

### 2. Define

* Need for secure, scalable approval system

### 3. Ideate

* RBAC + Approval hierarchy + Federated learning

### 4. Prototype

* Streamlit UI + system logic

### 5. Test

* Edge case handling + logical validation

---

## 🎨 Figma Deliverables

The design includes:

* Low-fidelity wireframes
* Login & dashboard flows
* Approval workflow diagrams
* Federated learning architecture
* Annotated explanations

---

## 🔥 Key Highlights

* ✔ Single source of truth (central request state)
* ✔ Strict RBAC enforcement
* ✔ Real approval logic (not just UI)
* ✔ Admin monitoring & logs
* ✔ Privacy-aware system design
* ✔ Clean, modular architecture

---

## 🧪 Example Workflow

1. User logs in and submits a request
2. Manager reviews:

   * Approves (if ≤ ₹10000)
   * Escalates (if > ₹10000)
3. Admin can override decisions
4. Logs track all actions

---

## 📈 Future Improvements

* 🔐 JWT-based authentication
* 🗄 Database integration (PostgreSQL / MongoDB)
* 🌐 Backend API (FastAPI)
* 🤖 Real federated learning with PyTorch
* 🚀 Deployment on Streamlit Cloud

---

## 🏁 Conclusion

This project demonstrates:

* Practical RBAC implementation
* Decision-driven approval workflows
* Secure authentication & authorization
* Conceptual federated learning system

It focuses on **logic, flow, and real-world applicability**, aligning with modern system design principles.

---

## 🙌 Acknowledgment

Developed as part of IT Prototyping Assignment using Design Thinking methodology.

---
