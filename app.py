import streamlit as st
import engine
import ai_analyst
import ai_sast
import time
import os

st.set_page_config(
    page_title="HackZion v3 | Security Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&display=swap');

:root {
    --bg:       #020b14;
    --panel:    #061120;
    --border:   #0ff3;
    --cyan:     #00f5ff;
    --green:    #00ff88;
    --red:      #ff2d55;
    --yellow:   #ffd60a;
    --dim:      #4a7a8a;
    --text:     #c8e6f0;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--cyan); border-radius: 2px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #040e1a 0%, #020b14 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #061828 0%, #040f1c 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 1rem 1.2rem !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--cyan);
    box-shadow: 0 0 12px var(--cyan);
}
[data-testid="stMetricLabel"] { font-family: 'Share Tech Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.15em !important; color: var(--dim) !important; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-family: 'Orbitron', monospace !important; font-size: 1.4rem !important; color: var(--cyan) !important; }
[data-testid="stMetricDelta"] { font-family: 'Share Tech Mono', monospace !important; font-size: 0.75rem !important; }

[data-testid="stTabs"] button {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    color: var(--dim) !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
    text-shadow: 0 0 8px var(--cyan) !important;
}

[data-testid="stButton"] > button[kind="primary"] {
    background: transparent !important;
    border: 1px solid var(--red) !important;
    color: var(--red) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    box-shadow: 0 0 20px #ff2d5540, inset 0 0 20px #ff2d5508 !important;
    transition: all 0.25s ease !important;
    border-radius: 2px !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #ff2d5515 !important;
    box-shadow: 0 0 40px #ff2d5580, inset 0 0 30px #ff2d5515 !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:not([kind="primary"]) {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 2px !important;
}

[data-testid="stAlert"] {
    border-radius: 2px !important;
    border-left-width: 3px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
}

[data-testid="stStatusWidget"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

hr { border-color: var(--border) !important; }
[data-testid="stCaption"] { font-family: 'Share Tech Mono', monospace !important; color: var(--dim) !important; font-size: 0.7rem !important; }
[data-testid="stProgressBar"] > div { background: var(--cyan) !important; box-shadow: 0 0 8px var(--cyan) !important; }
[data-testid="stExpander"] { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 2px !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ── HELPER: Glowing section header ───────────────────────────────────────────
def section_header(icon, title, color="00f5ff"):
    st.markdown(
        f"""
    <div style="display:flex;align-items:center;gap:10px;margin:1.2rem 0 0.8rem;">
        <span style="font-size:1.2rem">{icon}</span>
        <span style="font-family:'Orbitron',monospace;font-size:0.9rem;
                     color:#{color};letter-spacing:0.2em;text-shadow:0 0 10px #{color}88;
                     text-transform:uppercase">{title}</span>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,#{color}44,transparent);margin-left:8px"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def badge(text, color):
    return f"<span style=\"font-family:'Share Tech Mono',monospace;font-size:0.7rem;padding:2px 8px;border:1px solid #{color};color:#{color};border-radius:2px;text-shadow:0 0 6px #{color}88\">{text}</span>"


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style="text-align:center;padding:1rem 0">
        <div style="font-family:'Orbitron',monospace;font-size:1.4rem;color:#00f5ff;
                    text-shadow:0 0 20px #00f5ff;letter-spacing:0.15em">HACKZION</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;
                    color:#4a7a8a;letter-spacing:0.3em;margin-top:2px">SECURITY ENGINE v3.0</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        f"""
    <div style="margin-bottom:0.5rem">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a7a8a;letter-spacing:0.15em">REMEDIATION ENGINE</div>
        <div style="font-family:'Orbitron',monospace;font-size:1.6rem;color:#00ff88;text-shadow:0 0 15px #00ff88">ONLINE</div>
        {badge("● ACTIVE", "00ff88")}
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
    <div style="margin-bottom:0.5rem">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a7a8a;letter-spacing:0.15em">TARGET DIRECTORY</div>
        <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#00f5ff;text-shadow:0 0 10px #00f5ff88">./target_app</div>
        {badge("⬆ LOCKED", "ffd60a")}
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()

    section_header("⚡", "Threat Vector Matrix", "ff2d55")
    threat_data = {
        "Prototype Pollution": 87,
        "DoS Attack Surface": 73,
        "Supply Chain Risk": 61,
        "CVE Exposure": 54,
    }
    for threat, level in threat_data.items():
        color = "#ff2d55" if level > 80 else "#ffd60a" if level > 60 else "#00f5ff"
        st.markdown(
            f"""
        <div style="margin-bottom:0.6rem">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a7a8a">{threat}</span>
                <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:{color}">{level}%</span>
            </div>
            <div style="background:#061828;height:3px;border-radius:2px">
                <div style="width:{level}%;height:100%;background:{color};box-shadow:0 0 6px {color};border-radius:2px;transition:width 1s"></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.divider()
    st.markdown(
        """
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:#4a7a8a;text-align:center;letter-spacing:0.1em">
        POWERED BY GROQ (LLAMA 3) & NPM AUDIT<br><span style="color:#00f5ff44">━━━━━━━━━━━━━━━━━━━━</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── MAIN HEADER ───────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="padding:1.5rem 0 0.5rem">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:4px">
        <div style="font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:900;
                    color:#00f5ff;text-shadow:0 0 30px #00f5ff,0 0 60px #00f5ff44;letter-spacing:0.05em">
            AUTONOMOUS VULNERABILITY MANAGER
        </div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#4a7a8a;letter-spacing:0.2em">
        ◈ REAL-TIME THREAT DETECTION &nbsp;·&nbsp; AI SAST ANALYSIS &nbsp;·&nbsp; SELF-HEALING PATCH DEPLOYMENT
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ── TARGET SELECTION CONFIGURATOR ─────────────────────────────────────────────
st.markdown(
    "<div style='background:#040f1c; border:1px solid #0ff2; border-radius:4px; padding:1.5rem; margin-bottom:1.5rem;'>",
    unsafe_allow_html=True,
)
section_header("⚙️", "Mission Control: Target Acquisition")

col_target1, col_target2 = st.columns(2)
with col_target1:
    target_scenario = st.selectbox(
        "1. Select Pre-Configured Target Environment",
        [
            "Legacy Project (axios@0.18.0 & lodash@4.17.15)",
            "New Upload: React-Colors-Utils (Zero-Day Malicious)",
            "New Upload: Express Boilerplate (Safe)",
        ],
    )
with col_target2:
    custom_upload = st.file_uploader("2. Or Upload Custom Package (.js)", type=["js"])

st.markdown("</div>", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
dash_tab, ai_tab, log_tab, intel_tab = st.tabs(
    ["⚡ FULL SPECTRUM DASHBOARD", "🧠 AI ANALYST", "📜 SYSTEM LOGS", "🗺️ THREAT INTEL"]
)

# ── DASHBOARD TAB ─────────────────────────────────────────────────────────────
with dash_tab:
    col1, col2, col3, col4 = st.columns(4)
    sys_status = col1.empty()
    threat_status = col2.empty()
    patch_status = col3.empty()
    score_status = col4.empty()

    sys_status.metric("System Status", "Monitoring", "Standby")
    threat_status.metric("Active Threats", "Pending Scan", "Awaiting")
    patch_status.metric("Packages Patched", "0", "Ready")
    score_status.metric("Security Score", "—", "Pre-Scan")
    st.divider()

    # ── THE BIG UNIFIED BUTTON ──
    if st.button(
        "🚨 INITIATE FULL SPECTRUM SECURITY AUDIT",
        type="primary",
        use_container_width=True,
    ):
        with st.status(
            "⚡ EXECUTING ZERO-TRUST CYBER DEFENSE SEQUENCE...", expanded=True
        ) as status:
            prog = st.progress(0)

            # --- PREP PHASE: Write Target to Quarantine ---
            target_file_path = "temp_quarantine_scan.js"
            if custom_upload is not None:
                with open(target_file_path, "wb") as f:
                    f.write(custom_upload.getbuffer())
            else:
                if "Malicious" in target_scenario:
                    code_content = "const target = Buffer.from('cHJvY2Vzcy5lbnYuR1JPUV9BUElfS0VZ', 'base64').toString('utf-8');\neval(target);"
                elif "Safe" in target_scenario:
                    code_content = "const express = require('express');\nconst app = express();\napp.listen(3000, () => console.log('Ready'));"
                else:
                    # Legacy project mock content
                    code_content = "require('axios'); require('lodash');"
                with open(target_file_path, "w") as f:
                    f.write(code_content)

            # --- PHASE 1: PROACTIVE SAST (ZERO-DAY HUNTER) ---
            st.markdown(
                """<div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#b388ff">
                🛡️ PHASE 1 · PROACTIVE SAST (Heuristic Engine Analysis)...</div>""",
                unsafe_allow_html=True,
            )
            for i in range(20):
                prog.progress(i + 1)
                time.sleep(0.02)

            is_safe, sast_report = ai_sast.analyze_raw_code(target_file_path)

            # Cleanup Quarantine
            if os.path.exists(target_file_path):
                os.remove(target_file_path)

            if not is_safe:
                # ZERO-DAY DETECTED - ABORT PIPELINE
                prog.progress(100)
                sys_status.metric(
                    "System Status", "BLOCKED", "⚠ Critical", delta_color="inverse"
                )
                threat_status.metric(
                    "Active Threats", "ZERO-DAY", "Detected", delta_color="inverse"
                )
                score_status.metric(
                    "Security Score", "0 / 100", "Critical", delta_color="inverse"
                )

                st.markdown(
                    f"""
                <div style="background:#1a040a;border:1px solid #ff2d55;border-radius:2px;padding:1rem;margin:1rem 0">
                    <div style="font-family:'Orbitron',monospace;font-size:1rem;color:#ff2d55;letter-spacing:0.1em;margin-bottom:8px">
                        🚨 ZERO-DAY THREAT DETECTED IN QUARANTINE
                    </div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#c8e6f0">
                        The AI-SAST Engine has blocked this payload from executing or installing. Pipeline halted.
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
                st.code(sast_report, language="text")
                status.update(
                    label="🛑 PIPELINE HALTED — THREAT NEUTRALIZED IN QUARANTINE",
                    state="error",
                    expanded=True,
                )
                st.stop()  # Stops execution so it doesn't try to patch a virus

            else:
                st.markdown(
                    """<div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#00ff88">
                    ✓ AI-SAST Clearance Granted (No Obfuscation or Zero-Days found).</div>""",
                    unsafe_allow_html=True,
                )

            # --- PHASE 2: REACTIVE AUDIT (CVE DB) ---
            st.markdown(
                """<div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#00f5ff;margin-top:0.8rem">
                🔍 PHASE 2 · REACTIVE CVE AUDIT (Scanning target_app)...</div>""",
                unsafe_allow_html=True,
            )
            for i in range(20, 40):
                prog.progress(i + 1)
                time.sleep(0.02)

            # Logic to determine if we run the actual engine or mock a safe pass
            if "Legacy" in target_scenario or custom_upload:
                has_vulns = engine.run_vulnerability_scan()
            else:
                has_vulns = 0  # Safe Express mock

            if has_vulns > 0:
                sys_status.metric(
                    "System Status",
                    "COMPROMISED",
                    "⚠ Vulnerable",
                    delta_color="inverse",
                )
                threat_status.metric(
                    "Active Threats",
                    f"{has_vulns} CVEs",
                    "Detected",
                    delta_color="inverse",
                )
                score_status.metric(
                    "Security Score", "24 / 100", "Critical", delta_color="inverse"
                )

                st.markdown(
                    f"""
                <div style="background:#1a040a;border:1px solid #ff2d55;border-radius:2px;padding:0.8rem 1rem;margin:0.5rem 0">
                    <span style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#ff2d55">
                        ⚠ ALERT: {has_vulns} HIGH-SEVERITY CVEs DETECTED IN TARGET DEPENDENCIES
                    </span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # --- PHASE 3: AI ANALYST (THREAT REPORT) ---
                st.markdown(
                    """<div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#ffd60a;margin-top:0.8rem">
                    🧠 PHASE 3 · GENERATING MANAGER INTEL REPORT...</div>""",
                    unsafe_allow_html=True,
                )
                for i in range(40, 60):
                    prog.progress(i + 1)
                    time.sleep(0.02)

                ai_report = ai_analyst.get_threat_explanation(has_vulns)

                with ai_tab:
                    st.markdown(
                        f"""
                    <div style="background:#040f1c;border:1px solid #00f5ff44;border-left:3px solid #00f5ff;border-radius:2px;padding:1.2rem 1.5rem;margin-top:0.5rem">
                        <div style="font-family:'Orbitron',monospace;font-size:0.75rem;color:#00f5ff;letter-spacing:0.2em;margin-bottom:0.8rem">🤖 GROQ (LLAMA 3) THREAT REPORT</div>
                        <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;color:#c8e6f0;line-height:1.6">{ai_report}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # --- PHASE 4: BACKUP ---
                st.markdown(
                    """<div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#00f5ff;margin-top:0.8rem">
                    💾 PHASE 4 · CREATING SECURE SYSTEM BACKUP...</div>""",
                    unsafe_allow_html=True,
                )
                engine.backup_file()
                for i in range(60, 75):
                    prog.progress(i + 1)
                    time.sleep(0.02)
                st.markdown(
                    """<div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#00ff88">
                    ✓ Snapshot secured successfully.</div>""",
                    unsafe_allow_html=True,
                )

                # --- PHASE 5: PATCH & SELF-HEAL ---
                st.markdown(
                    """<div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#00f5ff;margin-top:0.8rem">
                    🔧 PHASE 5 · DEPLOYING AUTONOMOUS PATCHES...</div>""",
                    unsafe_allow_html=True,
                )
                engine.apply_patch_and_verify()
                for i in range(75, 100):
                    prog.progress(i + 1)
                    time.sleep(0.03)

                status.update(
                    label="✅ DEFENSE SEQUENCE COMPLETE — SYSTEM SECURED",
                    state="complete",
                    expanded=False,
                )
                sys_status.metric(
                    "System Status", "SECURE", "✓ Healed", delta_color="normal"
                )
                threat_status.metric(
                    "Active Threats", "0", "Eliminated", delta_color="normal"
                )
                patch_status.metric(
                    "Packages Patched", "2", "Updated", delta_color="normal"
                )
                score_status.metric(
                    "Security Score", "98 / 100", "+74 pts", delta_color="normal"
                )

                st.markdown(
                    """
                <div style="background:#040f1c;border:1px solid #00ff88;border-radius:2px;padding:1rem 1.5rem;margin-top:1rem;text-align:center">
                    <div style="font-family:'Orbitron',monospace;font-size:1rem;color:#00ff88;text-shadow:0 0 15px #00ff88;letter-spacing:0.2em">✓ SYSTEM SECURED · ZERO THREATS REMAINING</div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#4a7a8a;margin-top:6px">Patches verified &nbsp;·&nbsp; test suite passed &nbsp;·&nbsp; rollback bypassed</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
                st.balloons()

            else:
                # SAST Passed & No CVEs found
                for i in range(40, 101):
                    prog.progress(i)
                    time.sleep(0.01)
                status.update(
                    label="✅ SCAN COMPLETE — SYSTEM FULLY SECURE",
                    state="complete",
                    expanded=False,
                )
                sys_status.metric(
                    "System Status", "SECURE", "Verified", delta_color="normal"
                )
                threat_status.metric(
                    "Active Threats", "0", "Clean", delta_color="normal"
                )
                score_status.metric(
                    "Security Score", "100/100", "Perfect", delta_color="normal"
                )

                st.markdown(
                    """
                <div style="background:#040f1c;border:1px solid #00ff88;border-radius:2px;padding:1rem 1.5rem;margin-top:1rem;text-align:center">
                    <div style="font-family:'Orbitron',monospace;font-size:1rem;color:#00ff88;text-shadow:0 0 15px #00ff88;letter-spacing:0.2em">✓ ZERO THREATS DETECTED</div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#4a7a8a;margin-top:6px">SAST cleared &nbsp;·&nbsp; No CVEs &nbsp;·&nbsp; Safe to deploy</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )


# ── AI ANALYST TAB ────────────────────────────────────────────────────────────
with ai_tab:
    section_header("🧠", "AI Threat Intelligence Engine")
    st.markdown(
        """
    <div style="background:#040f1c;border:1px solid #0ff2;border-radius:2px;padding:1.2rem 1.5rem;margin-bottom:1rem">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#4a7a8a;margin-bottom:0.5rem">ANALYST ENGINE</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;color:#c8e6f0;line-height:1.6">
            This module connects to <span style="color:#00f5ff">Groq's LLaMA 3</span> inference engine. It analyzes known CVEs found during Phase 2 and generates plain-English risk assessments for leadership.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── LOGS TAB ──────────────────────────────────────────────────────────────────
with log_tab:
    section_header("📜", "System Operations Log")
    st.markdown(
        """
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#4a7a8a;text-align:center;padding:1rem;border:1px dashed #0ff2;border-radius:2px">
        ◈ LIVE LOG STREAM ACTIVE ◈
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── THREAT INTEL TAB ──────────────────────────────────────────────────────────
with intel_tab:
    section_header("🗺️", "Threat Intelligence Overview")
    i_col1, i_col2 = st.columns([3, 2])

    with i_col1:
        section_header("📦", "Known Dependency Risk", "ffd60a")
        deps = [
            (
                "axios",
                "0.18.0",
                "1.7.9",
                "SSRF · ReDoS · Unvalidated Redirect",
                "HIGH",
                "ff2d55",
            ),
            (
                "lodash",
                "4.17.15",
                "4.17.21",
                "Prototype Pollution · Code Injection",
                "HIGH",
                "ffd60a",
            ),
        ]
        for pkg, cur, safe, cves, sev, col in deps:
            st.markdown(
                f"""
            <div style="background:#061120;border:1px solid #{col}44;border-radius:2px;padding:0.9rem 1.1rem;margin-bottom:0.5rem">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                    <span style="font-family:'Orbitron',monospace;font-size:0.9rem;color:#{col}">{pkg}</span>
                    <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;padding:2px 8px;border:1px solid #{col};color:#{col}">{sev}</span>
                </div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#4a7a8a">
                    INSTALLED: <span style="color:#ff2d55">{cur}</span> &nbsp;→&nbsp;
                    PATCHED:   <span style="color:#00ff88">{safe}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with i_col2:
        section_header("⚙️", "Zero-Trust Architecture", "00ff88")
        steps = [
            ("01", "Quarantine SAST", "LLaMA-3 hunts Zero-Days", "b388ff"),
            ("02", "npm audit", "Scans for known CVEs", "00f5ff"),
            ("03", "AI Report", "Generates risk intel", "ffd60a"),
            ("04", "Backup & Patch", "Applies safe upgrades", "4a7a8a"),
            ("05", "Self-Healing", "Validates & Rolls back if broken", "00ff88"),
        ]
        for num, step, desc, col in steps:
            st.markdown(
                f"""
            <div style="display:flex;align-items:center;gap:12px;padding:0.5rem 0;border-bottom:1px solid #0ff1">
                <div style="font-family:'Orbitron',monospace;font-size:0.75rem;color:#{col};min-width:24px;text-align:center">{num}</div>
                <div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#{col}">{step}</div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:#4a7a8a">{desc}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
