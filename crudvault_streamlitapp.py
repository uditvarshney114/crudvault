import streamlit as st
from pathlib import Path
import os
import time

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CRUDvault",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0d0d12;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #131318 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color: #c4c3d4 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Logo ── */
.logo-wrap {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 0 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 24px;
}
.logo-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: #7c6af5;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.logo-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #f0eff8 !important;
    letter-spacing: -0.5px;
    margin: 0 !important; padding: 0 !important;
}
.logo-sub {
    font-size: 11px; color: #4a4960;
    text-transform: uppercase; letter-spacing: 1px;
}

/* ── Nav Labels ── */
.nav-section-label {
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 1.4px; color: #4a4960;
    font-weight: 600; margin: 16px 0 8px;
}

/* ── Stat Cards ── */
.stat-row {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 28px;
}
.stat-card {
    background: #131318;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 18px;
    display: flex; align-items: center; gap: 14px;
}
.stat-icon { font-size: 24px; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 700;
    color: #f0eff8; line-height: 1;
}
.stat-lbl { font-size: 12px; color: #7b7a8e; margin-top: 2px; }

/* ── Page Title ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px; font-weight: 800;
    color: #f0eff8; letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.page-sub { font-size: 13px; color: #7b7a8e; margin-bottom: 28px; }

/* ── Panel / Card ── */
.crud-panel {
    background: #131318;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
}
.panel-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px; padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px; font-weight: 700; color: #f0eff8;
}
.badge {
    margin-left: auto; padding: 3px 10px; border-radius: 20px;
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.8px; font-weight: 700;
}
.badge-green  { background: rgba(52,211,153,0.12); color: #34d399; }
.badge-purple { background: rgba(124,106,245,0.15); color: #a78bfa; }
.badge-amber  { background: rgba(251,191,36,0.12);  color: #fbbf24; }
.badge-red    { background: rgba(248,113,113,0.12); color: #f87171; }

/* ── Output boxes ── */
.output-box {
    border-radius: 10px; padding: 14px 16px;
    font-family: 'DM Mono', monospace; font-size: 13px;
    line-height: 1.7; margin-top: 12px; white-space: pre-wrap;
}
.output-success { background: rgba(52,211,153,0.07); border: 1px solid rgba(52,211,153,0.25); color: #34d399; }
.output-error   { background: rgba(248,113,113,0.07); border: 1px solid rgba(248,113,113,0.25); color: #f87171; }
.output-info    { background: rgba(124,106,245,0.08); border: 1px solid rgba(124,106,245,0.25); color: #a78bfa; }
.output-amber   { background: rgba(251,191,36,0.07);  border: 1px solid rgba(251,191,36,0.25);  color: #fbbf24; }

/* ── File list item ── */
.file-item {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 14px;
    background: #1a1a22;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; margin-bottom: 8px;
    transition: border-color 0.15s;
}
.file-item:hover { border-color: rgba(255,255,255,0.12); }
.file-emoji { font-size: 20px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 8px; }
.file-name  { font-family: 'DM Mono', monospace; font-size: 13px; font-weight: 500; color: #f0eff8; }
.file-meta  { font-size: 11px; color: #4a4960; margin-top: 2px; }

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
    background: #1a1a22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #f0eff8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(124,106,245,0.5) !important;
    box-shadow: 0 0 0 2px rgba(124,106,245,0.15) !important;
}
.stButton > button {
    background: #7c6af5 !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 8px 22px !important; font-size: 14px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { background: #6b5ae0 !important; transform: translateY(-1px) !important; }

div[data-testid="stRadio"] > label { color: #c4c3d4 !important; }
div[data-testid="stRadio"] > div { gap: 8px !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 20px 0 !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1a1a22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important; color: #f0eff8 !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
.stTextInput label, .stTextArea label,
.stSelectbox label, .stRadio label {
    font-size: 12px !important; text-transform: uppercase !important;
    letter-spacing: 0.8px !important; color: #7b7a8e !important;
    font-weight: 500 !important;
}

/* ── Success / Error msgs ── */
[data-testid="stAlert"] { border-radius: 10px !important; font-family: 'DM Mono', monospace !important; }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 40px 20px;
    color: #4a4960; font-size: 14px;
}
.empty-icon { font-size: 40px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "files" not in st.session_state:
    st.session_state.files = {}          # { name: { content, size, created, modified } }
if "ops" not in st.session_state:
    st.session_state.ops = 0
if "messages" not in st.session_state:
    st.session_state.messages = {}       # { section: (text, type) }

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_size(b):
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    return f"{b/1024**2:.2f} MB"

def file_emoji(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else "txt"
    return {"txt":"📄","py":"🐍","js":"📜","json":"📋","csv":"📊","md":"📝","html":"🌐","css":"🎨"}.get(ext, "📄")

def file_bg(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else "txt"
    return {"txt":"rgba(124,106,245,0.15)","py":"rgba(52,211,153,0.15)","js":"rgba(251,191,36,0.15)",
            "json":"rgba(96,165,250,0.15)","csv":"rgba(244,114,182,0.15)","md":"rgba(167,139,250,0.15)",
            "html":"rgba(251,146,60,0.15)","css":"rgba(56,189,248,0.15)"}.get(ext, "rgba(124,106,245,0.12)")

def set_msg(section, text, mtype="success"):
    st.session_state.messages[section] = (text, mtype)

def get_msg(section):
    return st.session_state.messages.get(section, None)

def inc_ops():
    st.session_state.ops += 1

def total_size():
    return sum(f["size"] for f in st.session_state.files.values())

def output_html(text, mtype="success"):
    cls = {"success":"output-success","error":"output-error","info":"output-info","amber":"output-amber"}.get(mtype,"output-info")
    return f'<div class="output-box {cls}">{text}</div>'

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-icon">🗂️</div>
      <div>
        <div class="logo-title">CRUDvault</div>
        <div class="logo-sub">Python File Manager</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">Operations</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["✦  Create File", "◎  Read File", "⟳  Update File", "⌫  Delete File", "▦  All Files"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="nav-section-label">Workspace</div>', unsafe_allow_html=True)
    fc = len(st.session_state.files)
    st.markdown(f"""
    <div style='font-size:12px; color:#7b7a8e; margin-bottom:8px;'>
        Storage used: <span style='color:#f0eff8; font-family:DM Mono,monospace'>{fmt_size(total_size())}</span>
    </div>
    <div style='background:#1a1a22; border-radius:99px; height:4px; margin-bottom:4px; overflow:hidden;'>
      <div style='height:4px; width:{min(total_size()/(1024*100)*100, 100):.1f}%;
           background:linear-gradient(90deg,#7c6af5,#a78bfa); border-radius:99px;'></div>
    </div>
    <div style='font-size:11px; color:#4a4960;'>{fc} file{"s" if fc!=1 else ""} in vault</div>
    """, unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-icon">📄</div>
    <div><div class="stat-num">{len(st.session_state.files)}</div><div class="stat-lbl">Total Files</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">📦</div>
    <div><div class="stat-num">{fmt_size(total_size())}</div><div class="stat-lbl">Total Size</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🕐</div>
    <div><div class="stat-num">{st.session_state.ops}</div><div class="stat-lbl">Operations</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CREATE
# ═══════════════════════════════════════════════════════════════════════════════
if page == "✦  Create File":
    st.markdown('<div class="page-title">Create File</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Create a new file and write content into it</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="crud-panel">
      <div class="panel-header">
        <span class="panel-dot" style="background:#34d399"></span>
        <span class="panel-title">New File</span>
        <span class="badge badge-green">CREATE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        fname = st.text_input("File Name", placeholder="e.g. notes.txt, data.csv, script.py", key="c_name")
        fcontent = st.text_area("File Content", placeholder="Write your file content here...", height=160, key="c_content")

        col1, col2 = st.columns([1, 4])
        with col1:
            create_btn = st.button("✦  Create File", use_container_width=True)
        with col2:
            if st.button("Clear", key="clear_create"):
                st.session_state.c_name = ""
                st.session_state.c_content = ""
                st.rerun()

        if create_btn:
            name = fname.strip()
            if not name:
                set_msg("create", "⚠ Please enter a file name.", "error")
            elif name in st.session_state.files:
                set_msg("create", f'⚠ Error: "{name}" already exists.', "error")
            else:
                ts = time.strftime("%H:%M:%S")
                size = len(fcontent.encode())
                st.session_state.files[name] = {"content": fcontent, "size": size, "created": ts, "modified": ts}
                inc_ops()
                set_msg("create", f'✓ File "{name}" created successfully.\n\nSize: {fmt_size(size)}\nCreated: {ts}', "success")
                st.rerun()

        msg = get_msg("create")
        if msg:
            st.markdown(output_html(msg[0], msg[1]), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: READ
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "◎  Read File":
    st.markdown('<div class="page-title">Read File</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">View the content of any file in your vault</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="crud-panel">
      <div class="panel-header">
        <span class="panel-dot" style="background:#a78bfa"></span>
        <span class="panel-title">File Content</span>
        <span class="badge badge-purple">READ</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    files = list(st.session_state.files.keys())
    if not files:
        st.markdown('<div class="empty-state"><div class="empty-icon">🗂️</div>No files yet. Create one first!</div>', unsafe_allow_html=True)
    else:
        selected = st.selectbox("Select File", ["— Choose a file —"] + files, key="r_select")
        if st.button("◎  Read File", key="read_btn"):
            if selected == "— Choose a file —":
                set_msg("read", "⚠ Please select a file.", "error")
            else:
                f = st.session_state.files[selected]
                content = f["content"] if f["content"] else "(Empty file)"
                set_msg("read", content, "info")
                inc_ops()
                st.rerun()

        msg = get_msg("read")
        if msg:
            st.markdown(f"""
            <div style='margin-top:12px;'>
              <div style='font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:#4a4960;margin-bottom:8px;'>File Content</div>
              {output_html(msg[0], msg[1])}
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: UPDATE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⟳  Update File":
    st.markdown('<div class="page-title">Update File</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Rename, append to, or overwrite an existing file</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="crud-panel">
      <div class="panel-header">
        <span class="panel-dot" style="background:#fbbf24"></span>
        <span class="panel-title">Modify File</span>
        <span class="badge badge-amber">UPDATE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    files = list(st.session_state.files.keys())
    if not files:
        st.markdown('<div class="empty-state"><div class="empty-icon">🗂️</div>No files yet. Create one first!</div>', unsafe_allow_html=True)
    else:
        selected = st.selectbox("Select File", ["— Choose a file —"] + files, key="u_select")
        operation = st.radio("Operation", ["Rename", "Append Content", "Overwrite Content"],
                             horizontal=True, key="u_op")

        if operation == "Rename":
            new_name = st.text_input("New File Name", placeholder="e.g. renamed_file.txt", key="u_newname")
        else:
            default_val = st.session_state.files[selected]["content"] if selected != "— Choose a file —" and selected in st.session_state.files else ""
            label = "Content to Append" if operation == "Append Content" else "New Content (Overwrites Existing)"
            new_content = st.text_area(label, value=default_val if operation == "Overwrite Content" else "", height=140, key="u_content")

        if st.button("⟳  Apply Update", key="update_btn"):
            if selected == "— Choose a file —":
                set_msg("update", "⚠ Please select a file.", "error")
            elif operation == "Rename":
                nn = new_name.strip()
                if not nn:
                    set_msg("update", "⚠ Please enter a new file name.", "error")
                elif nn in st.session_state.files:
                    set_msg("update", f'⚠ "{nn}" already exists.', "error")
                else:
                    st.session_state.files[nn] = dict(st.session_state.files[selected])
                    st.session_state.files[nn]["modified"] = time.strftime("%H:%M:%S")
                    del st.session_state.files[selected]
                    inc_ops()
                    set_msg("update", f'✓ Renamed "{selected}" → "{nn}"\nModified: {st.session_state.files[nn]["modified"]}', "success")
            elif operation == "Append Content":
                st.session_state.files[selected]["content"] += "\n" + new_content
                st.session_state.files[selected]["size"] = len(st.session_state.files[selected]["content"].encode())
                st.session_state.files[selected]["modified"] = time.strftime("%H:%M:%S")
                inc_ops()
                set_msg("update", f'✓ Content appended to "{selected}".\nNew size: {fmt_size(st.session_state.files[selected]["size"])}', "success")
            else:
                st.session_state.files[selected]["content"] = new_content
                st.session_state.files[selected]["size"] = len(new_content.encode())
                st.session_state.files[selected]["modified"] = time.strftime("%H:%M:%S")
                inc_ops()
                set_msg("update", f'✓ "{selected}" overwritten successfully.\nNew size: {fmt_size(st.session_state.files[selected]["size"])}', "success")
            st.rerun()

        msg = get_msg("update")
        if msg:
            st.markdown(output_html(msg[0], msg[1]), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DELETE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⌫  Delete File":
    st.markdown('<div class="page-title">Delete File</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Permanently remove a file from your vault</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="crud-panel">
      <div class="panel-header">
        <span class="panel-dot" style="background:#f87171"></span>
        <span class="panel-title">Remove File</span>
        <span class="badge badge-red">DELETE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    files = list(st.session_state.files.keys())
    if not files:
        st.markdown('<div class="empty-state"><div class="empty-icon">🗂️</div>No files to delete.</div>', unsafe_allow_html=True)
    else:
        selected = st.selectbox("Select File to Delete", ["— Choose a file —"] + files, key="d_select")

        if selected != "— Choose a file —" and selected in st.session_state.files:
            f = st.session_state.files[selected]
            st.markdown(f"""
            <div style='background:#1a1a22; border:1px solid rgba(248,113,113,0.2);
                 border-radius:10px; padding:14px 16px; margin:12px 0;'>
              <div style='font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:#f87171;margin-bottom:10px;'>File Preview</div>
              <div style='font-family:DM Mono,monospace;font-size:13px;color:#c4c3d4;white-space:pre-wrap;'>{f["content"] or "(Empty file)"}</div>
              <div style='margin-top:10px;font-size:11px;color:#4a4960;'>Size: {fmt_size(f["size"])} · Modified: {f["modified"]}</div>
            </div>
            """, unsafe_allow_html=True)

        confirm = st.checkbox(f'I confirm I want to permanently delete this file', key="d_confirm")
        if st.button("⌫  Delete File", key="delete_btn"):
            if selected == "— Choose a file —":
                set_msg("delete", "⚠ Please select a file.", "error")
            elif not confirm:
                set_msg("delete", "⚠ Please check the confirmation box first.", "error")
            else:
                del st.session_state.files[selected]
                inc_ops()
                set_msg("delete", f'✓ "{selected}" deleted successfully.', "success")
                st.rerun()

        msg = get_msg("delete")
        if msg:
            st.markdown(output_html(msg[0], msg[1]), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL FILES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "▦  All Files":
    st.markdown('<div class="page-title">All Files</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Browse and manage everything in your vault</div>', unsafe_allow_html=True)

    search = st.text_input("Search files", placeholder="Filter by filename...", key="search")

    files = st.session_state.files
    filtered = {k: v for k, v in files.items() if search.lower() in k.lower()} if search else files

    if not filtered:
        st.markdown('<div class="empty-state"><div class="empty-icon">🗂️</div>No files found.</div>', unsafe_allow_html=True)
    else:
        for name, f in filtered.items():
            bg = file_bg(name)
            emoji = file_emoji(name)
            st.markdown(f"""
            <div class="file-item">
              <div class="file-emoji" style="background:{bg}">{emoji}</div>
              <div style="flex:1">
                <div class="file-name">{name}</div>
                <div class="file-meta">{fmt_size(f["size"])} · Created {f["created"]} · Modified {f["modified"]}</div>
              </div>
              <div>
                <span class="badge badge-{'green' if name.endswith('.py') else 'purple' if name.endswith('.md') else 'amber' if name.endswith('.json') else 'purple'}">{name.rsplit(".",1)[-1].upper() if "." in name else "FILE"}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 40px 0 16px; color: #4a4960; font-size: 12px;'>
  Built with Python + Streamlit &nbsp;·&nbsp; CRUDvault
</div>
""", unsafe_allow_html=True)