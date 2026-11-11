
import streamlit as st

from pathlib import Path

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop


ROOT = Path(__file__).parent

load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎"
)

st.title("Research Agent")
st.caption("AI-powered research assistant")

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("Nhập câu hỏi của bạn...")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    system_prompt = (
        ROOT / "artifacts" / "system_prompt.md"
    ).read_text(encoding="utf-8")

    declarations = load_tool_declarations(
        ROOT / "artifacts" / "tools.yaml"
    )

    tools = to_openai_tools(declarations)

    provider = make_provider("openrouter")

    messages = [
        {"role": "system", "content": system_prompt},
        *st.session_state.history,
        {"role": "user", "content": prompt}
    ]

    with st.chat_message("assistant"):
        with st.spinner("Tớ đang nghĩ, đợi xíu nhé :)) ..."):
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=tools,
                model=None,
                max_tool_rounds=4
            )

        answer = result["assistant_text"]
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.session_state.history.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": answer}
    ])
