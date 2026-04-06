import streamlit as st
import pandas as pd
import uuid
import time
from datetime import datetime

# -------------------------------
# CONFIG & CONSTANTS
# -------------------------------
st.set_page_config(page_title="Secure Enterprise Portal", layout="wide")

MAX_LOGIN_ATTEMPTS = 3
BUDGET_THRESHOLD = 10000

# Mock DB
USERS_DB = {
    "user@test.com": {"password": "123", "role": "User", "name": "Employee A"},
    "manager@test.com": {"password": "123", "role": "Manager", "name": "Manager B"},
    "admin@test.com": {"password": "123", "role": "Admin", "name": "Admin C"},
}

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
def init_state():
    if "initialized" not in st.session_state:
        st.session_state.update({
            "initialized": True,
            "logged_in": False,
            "user_email": None,
            "role": None,
            "user_name": None,
            "login_attempts": 0,
            "requests": [],
            "logs": []
        })

init_state()

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def log_event(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append({
        "Timestamp": timestamp,
        "User": st.session_state.user_email or "System",
        "Event": msg
    })

def logout():
    # Keep logs and attempts, but clear auth session
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.role = None
    st.rerun()

def authorize(allowed_roles):
    if st.session_state.role not in allowed_roles:
        st.error(f"🚫 Unauthorized. This area is for {allowed_roles} only.")
        log_event(f"Unauthorized access attempt to {allowed_roles} area")
        return False
    return True

# -------------------------------
# AUTHENTICATION
# -------------------------------
def login_page():
    st.title("🔐 Secure Login")
    
    with st.container(border=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
                st.error("❌ Account locked. Too many failed attempts.")
                return

            if email in USERS_DB and USERS_DB[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.role = USERS_DB[email]["role"]
                st.session_state.user_name = USERS_DB[email]["name"]
                st.session_state.login_attempts = 0
                log_event("User logged in")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.error(f"❌ Invalid credentials. ({MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts} attempts remaining)")

# -------------------------------
# DASHBOARDS
# -------------------------------

def user_dashboard():
    st.header(f"👋 Welcome, {st.session_state.user_name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("New Request")
        with st.form("request_form", clear_on_submit=True):
            title = st.text_input("Project/Item Name")
            amount = st.number_input("Budget Amount (₹)", min_value=0, step=100)
            submit = st.form_submit_button("Submit Request")

            if submit:
                if not title:
                    st.warning("Please provide a title.")
                else:
                    new_req = {
                        "id": str(uuid.uuid4())[:8],
                        "user": st.session_state.user_email,
                        "title": title,
                        "amount": amount,
                        "status": "Pending",
                        "timestamp": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.requests.append(new_req)
                    log_event(f"Submitted request: {title}")
                    st.toast("Request Submitted!")
                    st.rerun()

    with col2:
        st.subheader("Your History")
        if not st.session_state.requests:
            st.info("No requests found.")
        else:
            df = pd.DataFrame(st.session_state.requests)
            user_df = df[df["user"] == st.session_state.user_email]
            st.dataframe(user_df, use_container_width=True, hide_index=True)

def manager_dashboard():
    if not authorize(["Manager"]): return
    
    st.header("🧑‍💼 Manager Approval Queue")
    
    pending = [r for r in st.session_state.requests if r["status"] == "Pending"]
    
    if not pending:
        st.success("All caught up! No pending requests.")
        return

    for req in pending:
        with st.expander(f"Request {req['id']}: {req['title']} - ₹{req['amount']}", expanded=True):
            col1, col2 = st.columns(2)
            
            # Using unique keys based on ID to prevent Streamlit Duplicate ID errors
            if col1.button(f"Approve", key=f"app_{req['id']}"):
                if req["amount"] > BUDGET_THRESHOLD:
                    req["status"] = "Escalated"
                    log_event(f"Escalated {req['id']} (Over budget)")
                else:
                    req["status"] = "Approved"
                    log_event(f"Approved {req['id']}")
                st.rerun()

            if col2.button(f"Reject", key=f"rej_{req['id']}", type="primary"):
                req["status"] = "Rejected"
                log_event(f"Rejected {req['id']}")
                st.rerun()

def admin_dashboard():
    if not authorize(["Admin"]): return
    
    st.header("🛠 System Administration")
    
    tab1, tab2 = st.tabs(["Manage Requests", "System Logs"])
    
    with tab1:
        if st.session_state.requests:
            df = pd.DataFrame(st.session_state.requests)
            st.dataframe(df, use_container_width=True)
            
            if st.button("Clear All Data"):
                st.session_state.requests = []
                log_event("Admin cleared all request data")
                st.rerun()
        else:
            st.info("No system data to display.")

    with tab2:
        if st.session_state.logs:
            st.table(pd.DataFrame(st.session_state.logs).iloc[::-1]) # Show latest first
        else:
            st.write("No logs recorded.")

# -------------------------------
# FEDERATED LEARNING
# -------------------------------
def federated_learning_page():
    st.header("🧠 Federated Learning Simulator")
    st.info("Secure model training across distributed nodes without moving raw data.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        1. **Local Training**: Clients train model on local data.
        2. **Weight Updates**: Only model gradients are sent to server.
        3. **Aggregation**: Server updates global model using FedAvg.
        """)
        
        if st.button("Start Global Aggregation Round"):
            with st.status("Aggregating local updates...", expanded=True) as status:
                time.sleep(1)
                st.write("Collecting weights from 3 nodes...")
                time.sleep(1)
                updates = [0.82, 0.85, 0.79]
                global_acc = sum(updates) / len(updates)
                status.update(label="Aggregation Complete!", state="complete")
            
            st.metric("New Global Model Accuracy", f"{round(global_acc * 100, 2)}%", "+1.2%")
            log_event("FL Aggregation Cycle completed")

# -------------------------------
# MAIN ENTRY POINT
# -------------------------------
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar Navigation
        with st.sidebar:
            st.title("Settings")
            st.write(f"Logged in as: **{st.session_state.user_name}**")
            st.write(f"Role: `{st.session_state.role}`")
            st.divider()
            
            nav = st.radio("Navigation", ["Dashboard", "Federated Learning"])
            
            if st.button("Logout", use_container_width=True):
                logout()

        # Page Routing
        if nav == "Dashboard":
            role = st.session_state.role
            if role == "User":
                user_dashboard()
            elif role == "Manager":
                manager_dashboard()
            elif role == "Admin":
                admin_dashboard()
        
        elif nav == "Federated Learning":
            federated_learning_page()

if __name__ == "__main__":
    main()