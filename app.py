import streamlit as st
from arxiv_api_exploration import fetch_arxiv_papers
from pipeline import run_research_pipeline


# Page configuration
st.set_page_config(
    page_title="Agentic Research Assistant",
    layout="wide"
)

st.title("📚 Agentic Research Assistant")
st.caption("Browse top arXiv papers first, then run agentic research analysis")



# Session state
if "papers" not in st.session_state:
    st.session_state["papers"] = None

if "result" not in st.session_state:
    st.session_state["result"] = None



# Input section
st.subheader("🔎 Research Question")

research_question = st.text_input(
    "Enter your research question",
    placeholder="Compare CNN and transformer based deepfake detection methods"
)


# Fetch papers
fetch_button = st.button("🔍 Fetch Top Papers")

if fetch_button and research_question.strip():

    with st.spinner("Fetching top arXiv papers..."):
        st.session_state["papers"] = fetch_arxiv_papers(
            research_question,
            max_results=5
        )

    st.session_state["result"] = None

    if not st.session_state["papers"]:
        st.warning("No papers found.")
    else:
        st.success(f"Fetched {len(st.session_state['papers'])} papers")


# Display fetched papers
if st.session_state["papers"]:

    st.subheader("📄 Top arXiv Papers")
    st.caption("Read the papers below before running the analysis")

    for idx, paper in enumerate(st.session_state["papers"], 1):
        with st.expander(f"{idx}. {paper['title']}"):
            st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
            st.markdown(f"**Published:** {paper['published']}")

            st.markdown("**Abstract:**")
            st.write(paper["abstract"])

            col1, col2 = st.columns(2)
            with col1:
                st.link_button(
                    "Open arXiv Page",
                    f"https://arxiv.org/abs/{paper['id']}"
                )
            with col2:
                if paper.get("pdf_url"):
                    st.link_button(
                        "Download PDF",
                        paper["pdf_url"]
                    )


# Run research pipeline
if st.session_state["papers"]:

    st.divider()

    run_button = st.button("🧠 Run Agentic Research Analysis")

    if run_button:

        with st.spinner("Running agentic research pipeline..."):
            st.session_state["result"] = run_research_pipeline(
                research_question
            )

        st.success("Research analysis completed")



# Display analysis results
if st.session_state["result"]:

    result = st.session_state["result"]

    st.divider()

    st.subheader("🎯 Classified Intent")
    st.write(result["intent"])

    st.subheader("🧩 Generated Sub-Questions")
    for i, sq in enumerate(result["sub_questions"], 1):
        st.write(f"{i}. {sq}")

    st.subheader("📑 Synthesized Findings")
    for sq, synthesis in result["synthesis"].items():
        with st.expander(sq):
            st.write(synthesis)

    st.subheader("📄 Final Research Report")
    st.json(result["report"].model_dump())
