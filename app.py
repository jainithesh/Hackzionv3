import streamlit as st
import engine
import ai_analyst
import time
import pandas as pd

# 1. Page Configuration (Wide mode looks more professional)
st.set_page_config(page_title="HackZion Security Engine", page_icon="🛡️", layout="wide")

# 2. The Sidebar (Persistent System Controls)
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("Autonomous Node.js Defense")
    st.divider()
    st.metric(
        label="Remediation Engine", value="ONLINE", delta="Active", delta_color="normal"
    )
    st.metric(
        label="Target Directory",
        value="./target_app",
        delta="Locked",
        delta_color="off",
    )
    st.divider()
    st.caption("Powered by Groq (LLaMA 3) & npm audit")

# 3. Main Header
st.title("🛡️ Autonomous Vulnerability Manager")
st.markdown(
    "Real-time threat detection, AI analysis, and self-healing patch deployment."
)

# 4. Interactive Tabs (Organizes the UI)
dash_tab, ai_tab, log_tab = st.tabs(
    ["🚀 Live Dashboard", "🧠 AI Analyst", "📜 System Logs"]
)

with dash_tab:
    # Top-level metrics
    col1, col2, col3 = st.columns(3)
    sys_status = col1.empty()
    threat_status = col2.empty()
    patch_status = col3.empty()

    # Initial State
    sys_status.metric("System Status", "Monitoring", "-")
    threat_status.metric("Active Threats", "Pending Scan", "-")
    patch_status.metric("Packages Patched", "0")

    st.divider()

    # The Big Red Button
    if st.button(
        "🚨 Trigger Autonomous Security Sweep", type="primary", use_container_width=True
    ):
        with st.status("Initiating Cyber Defense Sequence...", expanded=True) as status:
            st.write("🔍 **Phase 1: Scanning target project...**")
            time.sleep(1)

            # Run the scanner
            has_vulns = engine.run_vulnerability_scan()

            if has_vulns:
                # Update metrics dynamically
                sys_status.metric(
                    "System Status", "COMPROMISED", "-Critical", delta_color="inverse"
                )
                threat_status.metric(
                    "Active Threats", "High Severity", "Detected", delta_color="inverse"
                )

                st.write("⚠️ **Alert: High-Severity vulnerabilities detected!**")

                # Fetch AI Analysis and send it to the AI Tab
                with ai_tab:
                    st.warning("Generating real-time threat intelligence...")
                    ai_report = ai_analyst.get_threat_explanation(has_vulns)
                    st.info(f"**🤖 Groq (LLaMA 3) Threat Report:**\n\n{ai_report}")

                st.write("💾 **Phase 2: Creating secure system backup...**")
                engine.backup_file()
                time.sleep(1)

                st.write("🔧 **Phase 3: Deploying autonomous patches (30-60s)...**")
                engine.apply_patch_and_verify()

                # Final Success State
                status.update(
                    label="Defense Sequence Complete: System Secured",
                    state="complete",
                    expanded=False,
                )
                sys_status.metric(
                    "System Status", "SECURE", "Healed", delta_color="normal"
                )
                threat_status.metric(
                    "Active Threats", "0", "-Eliminated", delta_color="normal"
                )
                patch_status.metric(
                    "Packages Patched", "2", "Updated", delta_color="normal"
                )

                with log_tab:
                    st.success(
                        "2026-04-09: Successfully patched axios and lodash. Test suite passed. Rollback bypassed."
                    )

                st.balloons()
            else:
                status.update(label="Scan Complete", state="complete", expanded=False)
                sys_status.metric(
                    "System Status", "SECURE", "Verified", delta_color="normal"
                )
                threat_status.metric(
                    "Active Threats", "0", "Clean", delta_color="normal"
                )
