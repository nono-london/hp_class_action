import streamlit as st
import sys
from pathlib import Path

# add project to PYTHONPATH
sys.path.insert(1, str(Path(__file__).resolve().parent.parent))


from hp_class_action.hinge_issue.data_analyses.histo_claims import (chart_claim_hidden_claims,
                                                                    chart_claim_hidden_claims_as_percent)

st.header("HP Class Action")

st.markdown("Number of claims split between private-messaged and forum-ed")
fig_all_claims, _ = chart_claim_hidden_claims(show_chart=False)
st.pyplot(fig_all_claims,)

st.markdown("Number of claims in percentage split between private-messaged and forum-ed")
fig_all_claims_percent, _ = chart_claim_hidden_claims_as_percent(show_chart=False)
st.pyplot(fig_all_claims_percent)
