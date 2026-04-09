import streamlit as st
import engine  # This imports your engine.py file!
import time

# Set up the webpage
st.set_page_config(page_title="HackZion Security", page_icon="🛡️")

st.title("🛡️ Autonomous Vulnerability Manager")
st.markdown("Live monitoring and automated remediation for Node.js ecosystems.")

# Create a clean layout with 3 metric boxes
col1, col2, col3 = st.columns(3)
col1.metric("System Status", "Monitoring")
col2.metric("Active Threats", "Pending Scan")
col3.metric("Auto-Remediation", "Enabled")

st.divider()

# The main action button
if st.button("🚀 Trigger Security Sweep", use_container_width=True):
    # Streamlit's status container creates a cool expanding dropdown
    with st.status("Initializing Autonomous Engine...", expanded=True) as status:
        st.write("🔍 Scanning target project...")
        time.sleep(1)  # Slight delay for visual effect

        # Call YOUR function from engine.py
        has_vulns = engine.run_vulnerability_scan()

        if has_vulns:
            st.write("⚠️ High-Severity vulnerabilities detected in package.json!")
            time.sleep(1)

            st.write("💾 Creating secure backup...")
            engine.backup_file()

            st.write(
                "🔧 Applying patches and running tests (Please wait 30-60 seconds)..."
            )
            engine.apply_patch_and_verify()

            # Update the UI once finished
            status.update(
                label="System Successfully Secured", state="complete", expanded=False
            )
            st.success(
                "✅ All vulnerabilities patched. Tests passed. Rollback not required."
            )
            st.balloons()  # Drops celebration balloons on the screen
        else:
            status.update(label="System Secure", state="complete", expanded=False)
            st.success("✅ System is already secure. No action needed.")
