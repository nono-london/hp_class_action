import sys
from pathlib import Path

import streamlit as st

# add project to PYTHONPATH
sys.path.insert(1, str(Path(__file__).resolve().parent.parent))

from hp_class_action.hinge_issue.data_analyses.histo_claims import (chart_claim_hidden_claims,
                                                                    chart_claim_hidden_claims_as_percent)

FROM_YEAR: int = 2017

st.title("HP Class Action")

st.header("HP Forum")

st.subheader("Broken Hinge Reported Problem")

st.markdown("Number of claims reported through private-messages and via the forum")
fig_all_claims, _ = chart_claim_hidden_claims(show_chart=False, from_year=FROM_YEAR)
st.pyplot(fig_all_claims, )

st.markdown("Number of claims in percentage split between private-messaged and forum-ed")
fig_all_claims_percent, _ = chart_claim_hidden_claims_as_percent(show_chart=False, from_year=FROM_YEAR)
st.pyplot(fig_all_claims_percent)
