"""
Samsung Wash Assistant — RAG-powered Streamlit Chatbot
Premium UI for querying the Samsung washing machine manual.
"""

import streamlit as st
import os

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="Samsung Wash Assistant",
    page_icon="🫧",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
*, *::before, *::after {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: linear-gradient(165deg, #0b1121 0%, #0f172a 45%, #101b30 100%) !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(59,130,246,.25);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(59,130,246,.45); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1526, #111827) !important;
    border-right: 1px solid rgba(59,130,246,.08) !important;
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #64748b !important;
    font-size: .68rem !important;
    font-weight: 600 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    margin-bottom: .6rem !important;
}

section[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(59,130,246,.05) !important;
    border: 1px solid rgba(59,130,246,.1) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: .8rem !important;
    font-weight: 400 !important;
    padding: .5rem .8rem !important;
    text-align: left !important;
    transition: all .25s cubic-bezier(.4,0,.2,1) !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(59,130,246,.12) !important;
    border-color: rgba(59,130,246,.3) !important;
    color: #e2e8f0 !important;
    transform: translateX(4px) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(59,130,246,.08) !important;
    margin: 1rem 0 !important;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 1.2rem 0 .6rem;
}

.app-header-icon {
    font-size: 2.4rem;
    display: block;
    margin-bottom: .35rem;
    animation: headerFloat 3.5s ease-in-out infinite;
}

@keyframes headerFloat {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.app-header-title {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #3b82f6 0%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.3;
}

.app-header-sub {
    font-size: .85rem;
    color: #475569;
    font-weight: 300;
    margin-top: .2rem;
}

/* ── Welcome Screen ── */
.welcome-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    max-width: 580px;
    margin: 0 auto;
}

.welcome-badge {
    display: inline-block;
    background: rgba(59,130,246,.08);
    border: 1px solid rgba(59,130,246,.18);
    border-radius: 20px;
    padding: .3rem .8rem;
    font-size: .72rem;
    color: #60a5fa;
    font-weight: 500;
    margin-bottom: 1.2rem;
    letter-spacing: .02em;
}

.welcome-heading {
    font-size: 1.35rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: .4rem;
}

.welcome-text {
    font-size: .88rem;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 1.8rem;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: rgba(15,23,42,.45) !important;
    border: 1px solid rgba(59,130,246,.06) !important;
    border-radius: 14px !important;
    padding: .9rem 1.1rem !important;
    margin-bottom: .6rem !important;
    backdrop-filter: blur(10px) !important;
    animation: msgSlide .3s ease-out !important;
}

@keyframes msgSlide {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stChatMessage"] p {
    color: #e2e8f0 !important;
    font-size: .88rem !important;
    line-height: 1.7 !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    border: 1px solid rgba(59,130,246,.12) !important;
    border-radius: 14px !important;
    transition: all .3s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(59,130,246,.35) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.06) !important;
}

[data-testid="stChatInput"] textarea {
    color: #e2e8f0 !important;
    font-size: .88rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #374151 !important;
}

/* ── Sidebar Brand ── */
.sb-brand {
    text-align: center;
    padding: .4rem 0 .8rem;
}

.sb-brand-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: .15rem;
}

.sb-brand-name {
    font-size: 1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #3b82f6, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sb-brand-sub {
    font-size: .65rem;
    color: #374151;
    margin-top: .1rem;
}

/* ── Sidebar Footer ── */
.sb-footer {
    text-align: center;
    padding: .8rem 0;
    font-size: .65rem;
    color: #334155;
    line-height: 1.7;
}

.sb-footer b { color: #475569; }

/* ── Status Dot ── */
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 6px;
    vertical-align: middle;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(16,185,129,.35); }
    50%     { opacity:.65; box-shadow:0 0 0 4px rgba(16,185,129,0); }
}

/* ── Welcome Cards (Streamlit buttons in columns) ── */
.stColumn button[kind="secondary"] {
    background: rgba(15,23,42,.55) !important;
    border: 1px solid rgba(59,130,246,.1) !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
    font-size: .82rem !important;
    padding: .75rem .6rem !important;
    transition: all .3s cubic-bezier(.4,0,.2,1) !important;
}

.stColumn button[kind="secondary"]:hover {
    border-color: rgba(59,130,246,.35) !important;
    background: rgba(15,23,42,.8) !important;
    color: #e2e8f0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,.08) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Environment ─────────────────────────────────────────────────────
try:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
except Exception:
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🔑 **Google API Key not found!** Please configure your API key in `.streamlit/secrets.toml` locally, or add it in **Streamlit Secrets** when deploying.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(
    SCRIPT_DIR,
    "How to use the various modes of the washing machine _ Samsung LEVANT.html",
)

# ── RAG Pipeline (cached across sessions) ───────────────────────────
from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


@st.cache_resource(show_spinner=False)
def load_retriever():
    """Build and cache the Chroma retriever (runs once per server life)."""
    loader = BSHTMLLoader(
        HTML_FILE,
        open_encoding="utf-8",
        bs_kwargs={"features": "html.parser"},
    )
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vector_db.as_retriever(search_kwargs={"k": 3})


# ── Initialise retriever with a loading indicator ───────────────────
with st.spinner("🔧 Warming up the AI assistant…"):
    retriever = load_retriever()

# ── Initialize LLM fresh on each run ────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

prompt_template = ChatPromptTemplate.from_template(
    """You are an expert Samsung Washing Machine assistant.
You provide clear, helpful, and well-structured answers.

Answer ONLY using the provided context from the Samsung washing machine manual.
If the answer is not in the context, say:
"I couldn't find that information in the manual. Try asking about washing modes, cycles, or machine features."

Context:
{context}

Question:
{question}

Answer:"""
)

# ── Session state ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sb-brand">'
        '<span class="sb-brand-icon">🫧</span>'
        '<div class="sb-brand-name">Wash Assistant</div>'
        '<div class="sb-brand-sub">Samsung AI Helper</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        '<div style="font-size:.76rem;color:#4b5563;margin-bottom:.8rem">'
        '<span class="status-dot"></span> AI Ready'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Suggested Questions")

    SUGGESTED = [
        ("🌿", "What does Eco Wash mode do?"),
        ("👕", "How should I wash cotton items?"),
        ("🧶", "What is the Wool cycle for?"),
        ("⚡", "How does Quick Wash work?"),
        ("🛏️", "What is Bedding mode used for?"),
        ("🔄", "What do Rinse and Spin cycles do?"),
        ("🧺", "How does Daily Wash work?"),
        ("🌊", "What is Super Eco Wash?"),
    ]

    for icon, q in SUGGESTED:
        if st.button(f"{icon}  {q}", key=f"sq_{q}", use_container_width=True):
            st.session_state["pending_question"] = q
            st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Actions")

    if st.button("🗑️  Clear Chat History", key="clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown(
        '<div class="sb-footer">'
        "Powered by <b>Gemini 2.5 Flash</b><br>"
        "RAG · <b>LangChain</b> + <b>ChromaDB</b><br>"
        "Embeddings · <b>MiniLM-L6-v2</b>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Main header ─────────────────────────────────────────────────────
st.markdown(
    '<div class="app-header">'
    '<span class="app-header-icon">🫧</span>'
    '<div class="app-header-title">Samsung Wash Assistant</div>'
    '<div class="app-header-sub">AI-powered guide to your Samsung washing machine</div>'
    "</div>",
    unsafe_allow_html=True,
)

# ── Chat history ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# ── Welcome screen (empty state) ───────────────────────────────────
if not st.session_state.messages:
    st.markdown(
        '<div class="welcome-wrap">'
        '<div class="welcome-badge">📖 Based on Official Samsung Manual</div>'
        '<div class="welcome-heading">How can I help you today?</div>'
        '<div class="welcome-text">'
        "Ask anything about your Samsung washing machine — modes, cycles, "
        "care tips and more. I'll find the answer in the official manual."
        "</div></div>",
        unsafe_allow_html=True,
    )

    WELCOME_CARDS = [
        ("🌿", "Eco Wash mode", "What does Eco Wash mode do?"),
        ("👕", "Cotton washing", "How should I wash cotton items?"),
        ("🧶", "Wool cycle", "What is the Wool cycle for?"),
        ("⚡", "Quick Wash", "How does Quick Wash work?"),
    ]

    cols = st.columns(2)
    for i, (icon, label, q) in enumerate(WELCOME_CARDS):
        with cols[i % 2]:
            if st.button(f"{icon}  {label}", key=f"wc_{i}", use_container_width=True):
                st.session_state["pending_question"] = q
                st.rerun()

# ── Handle questions ────────────────────────────────────────────────
question = st.chat_input("Ask about your Samsung washing machine…")

# Check for a pending question from sidebar / welcome card click
if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    # ── User message
    st.session_state.messages.append(
        {"role": "user", "content": question, "avatar": "👤"}
    )
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # ── Assistant response (streamed)
    with st.chat_message("assistant", avatar="🫧"):
        try:
            # Retrieve relevant chunks
            with st.spinner("🔍 Searching the manual…"):
                docs = retriever.invoke(question)
                context = "\n\n".join(d.page_content for d in docs)
                messages = prompt_template.format_messages(
                    context=context, question=question
                )

            # Stream the LLM response token-by-token
            def _stream():
                for chunk in llm.stream(messages):
                    if chunk.content:
                        yield chunk.content

            answer = st.write_stream(_stream())

        except Exception as exc:
            answer = (
                f"⚠️ Sorry, I ran into an error:\n\n`{exc}`\n\n"
                "Please check your API key or try again."
            )
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "avatar": "🫧"}
    )
