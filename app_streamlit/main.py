import sys
from pathlib import Path

import streamlit as st

# add project to PYTHONPATH
sys.path.insert(1, str(Path(__file__).resolve().parent.parent))

from hp_class_action.hinge_issue.data_analyses.histo_claims import (chart_claim_hidden_claims,
                                                                    chart_claim_hidden_claims_as_percent)
from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search
from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo

FROM_YEAR: int = 2017

st.title("HP Class Action")

st.header("HP Forum")

st.subheader("Broken Hinge Reported Problem")
hinge_btn_1, hinge_btn_2 = st.columns([1,1])

with hinge_btn_1:
    st.button(label='Webscrap search data', on_click=webscrap_query_search(max_pages=5))
with hinge_btn_2:
    st.button(label='Webscrap me_too data', on_click=update_summary_metoo(force_update=False))

fig_all_claims, _ = chart_claim_hidden_claims(show_chart=False, from_year=FROM_YEAR)
st.pyplot(fig_all_claims, )
st.caption("Number of claims reported through private-messages and via the forum")

fig_all_claims_percent, _ = chart_claim_hidden_claims_as_percent(show_chart=False, from_year=FROM_YEAR)
st.pyplot(fig_all_claims_percent)
st.caption("Number of claims in percentage split between private-messaged and forum-ed")