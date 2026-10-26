import html
import json
import math

import streamlit as st
import streamlit.components.v1 as components
from influencer_posts import get_influencer_roles, get_influencers
from few_shot import FewShotPosts
from post_generator import generate_post

st.set_page_config(
    page_title="Post Generator",
    page_icon="📝",
    layout="centered",
)

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

DONATE_URL = "https://buymeacoffee.com/vikyraj696x"

LIGHT_THEME_CSS = """
html[data-user-theme="light"] { color-scheme: light; }
html[data-user-theme="light"] [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
html[data-user-theme="light"] .main { color: #1f2328; }
html[data-user-theme="light"] h1,
html[data-user-theme="light"] h2,
html[data-user-theme="light"] h3,
html[data-user-theme="light"] h4,
html[data-user-theme="light"] h5,
html[data-user-theme="light"] h6 { color: #1f2328 !important; }
html[data-user-theme="light"] [data-testid="stCaptionContainer"] p,
html[data-user-theme="light"] [data-testid="stWidgetLabel"] p { color: #57606a !important; }
html[data-user-theme="light"] [data-testid="stSelectbox"] [data-baseweb="select"] > div { background-color: #ffffff; border-color: #d0d7de; }
html[data-user-theme="light"] [data-testid="stSelectbox"] [data-baseweb="select"] > div div { color: #1f2328; }
html[data-user-theme="light"] [data-baseweb="popover"] [data-baseweb="menu-list"] { background-color: #ffffff; }
html[data-user-theme="light"] [data-baseweb="popover"] [role="option"] { color: #1f2328; }
html[data-user-theme="light"] [data-baseweb="popover"] [role="option"]:hover { background-color: #f6f8fa; }
html[data-user-theme="light"] [data-testid="baseButton-secondary"] { background: transparent; border-color: #8b949e; color: #1f2328; }
html[data-user-theme="light"] [data-testid="baseButton-secondary"]:hover { background: #f6f8fa; border-color: #ef5b5b; color: #ef5b5b; }
"""

NAVBAR_CSS = """
#pg-navbar {
  position: fixed; top: 0; left: 0; right: 0; height: 60px;
  z-index: 999999; box-sizing: border-box;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px;
  background: #0d1117;
  border-bottom: 1px solid #21262d;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
#pg-navbar .pg-logo {
  display: flex; align-items: center; gap: 10px; cursor: pointer;
  user-select: none;
}
#pg-navbar .pg-logo-badge {
  width: 32px; height: 32px; border-radius: 8px;
  background: #161b22; border: 1px solid #30363d;
  color: #ef5b5b; font-weight: 800; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
}
#pg-navbar .pg-title {
  color: #ffffff; font-size: 17px; font-weight: 700;
}
#pg-navbar .pg-links { display: flex; align-items: center; }
#pg-navbar .pg-links a {
  color: #c9d1d9; text-decoration: none; font-size: 14px; font-weight: 600;
  padding: 6px 14px; border-radius: 8px;
}
#pg-navbar .pg-links a:hover { color: #ef5b5b; background: #161b22; }
#pg-navbar .pg-coffee {
  background: #ffdd00; color: #000000; font-weight: 700; font-size: 14px;
  border: none; border-radius: 999px; padding: 8px 16px; cursor: pointer;
  display: flex; align-items: center; gap: 6px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
#pg-navbar .pg-coffee:hover { background: #ffec4d; }

#pg-settings-root {
  position: fixed; top: 68px; right: 20px; width: 240px;
  z-index: 999998;
}
#pg-settings-root[hidden] { display: none; }
.pg-settings-panel {
  background: #161b22; border: 1px solid #30363d; border-radius: 10px;
  padding: 14px; box-sizing: border-box;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.pg-settings-header { color: #ffffff; font-size: 14px; font-weight: 700; margin-bottom: 10px; }
.pg-settings-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.pg-settings-label { color: #8b949e; font-size: 13px; font-weight: 600; }
.pg-seg { display: flex; background: #0d1117; border-radius: 8px; padding: 3px; gap: 2px; }
.pg-seg-btn {
  flex: 1; background: transparent; color: #c9d1d9; border: none; border-radius: 6px;
  padding: 5px 10px; font-size: 12px; font-weight: 600; cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.pg-seg-btn.active { background: #ef5b5b; color: #ffffff; }
.pg-seg-btn:hover:not(.active) { background: #21262d; }
.pg-reload {
  width: 100%; background: transparent; border: 1px solid #30363d; border-radius: 8px;
  color: #e6edf3; font-size: 13px; font-weight: 600; padding: 7px 0; cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.pg-reload:hover { border-color: #ef5b5b; color: #ef5b5b; }
.pg-content-link {
  display: block; color: #ef5b5b; font-size: 12px; font-weight: 600;
  text-decoration: none;
}
.pg-content-link:hover { text-decoration: underline; }

body.pg-nav-ready { padding-top: 76px !important; }

html[data-user-theme="light"] #pg-navbar { background: #ffffff; border-bottom-color: #e5e7eb; }
html[data-user-theme="light"] #pg-navbar .pg-title { color: #0d1117; }
html[data-user-theme="light"] #pg-navbar .pg-logo-badge { background: #f6f8fa; border-color: #d0d7de; color: #ef5b5b; }
html[data-user-theme="light"] #pg-navbar .pg-links a { color: #57606a; }
html[data-user-theme="light"] #pg-navbar .pg-links a:hover { color: #ef5b5b; background: #f6f8fa; }
html[data-user-theme="light"] .pg-settings-panel { background: #ffffff; border-color: #d0d7de; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); }
html[data-user-theme="light"] .pg-settings-header { color: #0d1117; }
html[data-user-theme="light"] .pg-settings-label { color: #57606a; }
html[data-user-theme="light"] .pg-seg { background: #f6f8fa; }
html[data-user-theme="light"] .pg-seg-btn { color: #1f2328; }
html[data-user-theme="light"] .pg-seg-btn:hover:not(.active) { background: #eaeef2; }
html[data-user-theme="light"] .pg-seg-btn.active { background: #ef5b5b; color: #ffffff; }
html[data-user-theme="light"] .pg-reload { border-color: #d0d7de; color: #1f2328; }
html[data-user-theme="light"] .pg-reload:hover { border-color: #ef5b5b; color: #ef5b5b; }
"""

NAVBAR_HTML = """
<div class="pg-logo" id="pg-logo">
  <div class="pg-logo-badge">P</div>
  <span class="pg-title">Post Generator</span>
</div>
<div class="pg-links">
  <a href="#" id="pg-settings">Settings</a>
</div>
<button class="pg-coffee" id="pg-coffee">☕ Buy me a coffee</button>
<div class="pg-settings-root" id="pg-settings-root" hidden>
  <div class="pg-settings-panel">
    <div class="pg-settings-header">Settings</div>
    <div class="pg-settings-row">
      <span class="pg-settings-label">Theme</span>
      <div class="pg-seg">
        <button class="pg-seg-btn" data-theme="dark">Dark</button>
        <button class="pg-seg-btn" data-theme="light">Light</button>
      </div>
    </div>
    <div class="pg-settings-row">
      <button class="pg-reload" id="pg-reload">Reload</button>
    </div>
    <a href="#" class="pg-content-link" id="pg-content-link">Content settings</a>
  </div>
</div>
"""


def main():
    render_navbar()
    inject_global_css()

    st.markdown("# Post Generator")
    st.caption("Generate engaging LinkedIn posts powered by AI")

    st.markdown('<div id="pg-settings-section"></div>', unsafe_allow_html=True)
    st.markdown("### Content Settings")

    fs = FewShotPosts()
    tags = fs.get_tags()
    influencer_roles = get_influencer_roles()

    col1, col2 = st.columns(2)
    with col1:
        selected_influencer = st.selectbox(
            "Influencer",
            options=get_influencers(),
            format_func=lambda name: f"{name} — {influencer_roles.get(name, '')}",
        )
    with col2:
        selected_tag = st.selectbox("Topic", options=tags)

    col3, col4 = st.columns(2)
    with col3:
        selected_length = st.selectbox("Length", options=length_options)

    with col4:
        selected_language = st.selectbox("Language", options=language_options)

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        generate_clicked = st.button("Generate", type="primary", use_container_width=True)
    with btn_col2:
        regenerate_clicked = st.button("Regenerate", type="secondary", use_container_width=True)

    theme = "light" if st.query_params.get("theme") == "light" else "dark"
    apply_theme_script(theme)

    if generate_clicked or regenerate_clicked:
        with st.spinner("Generating your post..."):
            post = generate_post(selected_length, selected_language, selected_tag, selected_influencer)
        if post:
            st.session_state["pg_last_post"] = post
            render_post_card(post, theme)
        else:
            st.error("Failed to generate post. Please try again.")
    elif "pg_last_post" in st.session_state:
        render_post_card(st.session_state["pg_last_post"], theme)


def inject_global_css():
    st.markdown(
        """
        <style>
          [data-testid="stToolbar"] {
            display: none !important;
          }
          #stHeader {
            display: none !important;
          }
          #pg-settings-section {
            scroll-margin-top: 84px;
          }
          .stButton > button[data-testid="baseButton-primary"] {
            background: #ef5b5b;
            border: 1px solid #ef5b5b;
            color: #ffffff;
            font-weight: 700;
          }
          .stButton > button[data-testid="baseButton-primary"]:hover {
            background: #e04848;
            border-color: #e04848;
            color: #ffffff;
          }
          .stButton > button[data-testid="baseButton-secondary"] {
            background: transparent;
            border: 1px solid #30363d;
            color: #e6edf3;
            font-weight: 600;
          }
          .stButton > button[data-testid="baseButton-secondary"]:hover {
            border-color: #ef5b5b;
            color: #ef5b5b;
            background: rgba(239, 91, 91, 0.08);
          }
          [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background-color: #161b22;
            border-color: #30363d;
          }
          [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {
            border-color: #ef5b5b;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar():
    js = (
        "<script>"
        "(function(){"
        "try{"
        "const doc=window.parent.document;"
        'if(doc.getElementById("pg-navbar"))return;'
        "const style=doc.createElement('style');"
        "style.textContent=`" + NAVBAR_CSS + "`;"
        "doc.head.appendChild(style);"
        "const nav=doc.createElement('div');"
        'nav.id="pg-navbar";'
        "nav.innerHTML=`" + NAVBAR_HTML + "`;"
        "doc.body.insertBefore(nav,doc.body.firstChild);"
        "doc.body.classList.add('pg-nav-ready');"
        "doc.getElementById('pg-logo').addEventListener('click',function(e){e.preventDefault();window.parent.scrollTo({top:0,behavior:'smooth'});});"
        "doc.getElementById('pg-settings').addEventListener('click',function(e){e.preventDefault();var r=doc.getElementById('pg-settings-root');if(r)r.hidden=!r.hidden;});"
        "doc.getElementById('pg-coffee').addEventListener('click',function(){window.parent.open('"
        + DONATE_URL
        + "','_blank');});"
        "function setTheme(t){doc.documentElement.setAttribute('data-user-theme',t);try{localStorage.setItem('pg-theme',t);}catch(err){}var u=new URL(window.parent.location.href);if(t==='light'){u.searchParams.set('theme','light');}else{u.searchParams.delete('theme');}window.parent.location.href=u.toString();}"
        "doc.querySelectorAll('.pg-seg-btn').forEach(function(b){b.addEventListener('click',function(){setTheme(b.getAttribute('data-theme'));});});"
        "doc.getElementById('pg-reload').addEventListener('click',function(){window.parent.location.reload();});"
        "doc.getElementById('pg-content-link').addEventListener('click',function(e){e.preventDefault();var t=doc.getElementById('pg-settings-section');var r=doc.getElementById('pg-settings-root');if(r)r.hidden=true;if(t)t.scrollIntoView({behavior:'smooth',block:'start'});});"
        "doc.addEventListener('click',function(e){var r=doc.getElementById('pg-settings-root');var s=doc.getElementById('pg-settings');if(r&&!r.hidden&&s&&!e.target.closest('#pg-settings')&&!e.target.closest('.pg-settings-root')){r.hidden=true;}});"
        "var cur='dark';if(doc.documentElement.getAttribute('data-user-theme')){cur=doc.documentElement.getAttribute('data-user-theme');}else if(localStorage.getItem('pg-theme')){cur=localStorage.getItem('pg-theme');}"
        "doc.querySelectorAll('.pg-seg-btn').forEach(function(b){if(b.getAttribute('data-theme')===cur)b.classList.add('active');});"
        "}catch(e){}"
        "})();"
        "</script>"
    )
    components.html(js, height=1)


def apply_theme_script(theme):
    js = (
        "<script>"
        "(function(){"
        "try{"
        "const doc=window.parent.document;"
        'doc.documentElement.setAttribute("data-user-theme","' + theme + '");'
        "try{localStorage.setItem('pg-theme','" + theme + "');}catch(err){}"
        'let s=doc.getElementById("pg-theme-css");'
        "if(!s){s=doc.createElement('style');s.id='pg-theme-css';doc.head.appendChild(s);}"
        "s.textContent=`" + LIGHT_THEME_CSS + "`;"
        "}catch(e){}"
        "})();"
        "</script>"
    )
    components.html(js, height=1)


def render_post_card(post, theme="dark"):
    post_escaped = html.escape(post)
    post_json = json.dumps(post)

    is_light = theme == "light"
    light_css = ""
    if is_light:
        light_css = """
          body.light .post-card {
            background: #ffffff;
            border-color: #e0e0e0;
            color: #1f2328;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
          }
          body.light .copy-btn {
            background: #f3f2ef;
            border-color: #e0e0e0;
            color: #57606a;
          }
          body.light .copy-btn:hover {
            background: #e4e1dd;
            color: #ef5b5b;
          }
        """

    est_lines = max(1, math.ceil(len(post) / 50))
    card_height = min(800, 80 + est_lines * 20 + 20)

    components.html(
        f"""
        <style>
          body {{
            margin: 0;
          }}
          .post-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 20px 24px;
            box-sizing: border-box;
            position: relative;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: #e6edf3;
          }}
          .post-body {{
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            min-height: 30px;
            padding-top: 26px;
          }}
          .copy-btn {{
            position: absolute;
            top: 12px;
            right: 12px;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            border: 1px solid #30363d;
            background: #21262d;
            color: #e6edf3;
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
          }}
          .copy-btn:hover {{
            background: #30363d;
            color: #ef5b5b;
          }}
          {light_css}
        </style>
        <div class="post-card">
          <button class="copy-btn" id="copy-btn" title="Copy post">
            <svg id="copy-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="13" height="13" x="9" y="9" rx="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <svg id="check-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none">
              <path d="M20 6 9 17l-5-5"></path>
            </svg>
          </button>
          <div class="post-body">{post_escaped}</div>
        </div>
        <script>
          document.body.classList.add("{"light" if is_light else "dark"}");
          const postText = {post_json};
          const btn = document.getElementById("copy-btn");
          const icon = document.getElementById("copy-icon");
          const check = document.getElementById("check-icon");

          function flashCopied() {{
            icon.style.display = "none";
            check.style.display = "block";
            btn.title = "Copied!";
            setTimeout(function () {{
              icon.style.display = "block";
              check.style.display = "none";
              btn.title = "Copy post";
            }}, 1500);
          }}

          btn.addEventListener("click", function () {{
            navigator.clipboard.writeText(postText).then(flashCopied).catch(flashCopied);
          }});
        </script>
        """,
        height=card_height,
    )


# Run the app
if __name__ == "__main__":
    main()