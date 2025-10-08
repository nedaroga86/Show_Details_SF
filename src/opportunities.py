import streamlit as st

from opps_opportunity_source import preprocess_opp_source

st.markdown("""
    <style>
    /* Reduce padding superior de toda la app */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    </style>
""", unsafe_allow_html=True)
from opps_opportunity_source import show_opportunity_source_table
from filter_opps import define_filters
from opps_new_pipeline import preprocess_data, show_opportunity_table


st.divider()
tab1, tab2 = st.tabs(["📊 New Pipeline", "📈 Opportunity Source"])


def show_summary_by_stage(data, key):
    col1, col2,col3 = st.columns([3,7,4])
    column = col1.radio('Metric', options=['Stage Name', 'Product Family', 'Full Name', 'Territory Bucket', 'Market Segment', 'Industry', 'Opportunity Type'], horizontal=False, key=key)

    opps = data.copy()
    opps['Amount'] = (opps['Amount']/1000)
    opps['Amount'] = opps['Amount'].round(0)
    summary_by_stage = (
        opps.groupby([column])
        .agg(
            Total_Amount=("Amount", "sum"),
            Quantity=("Opportunity ID", "nunique")

        )
        .reset_index()
        .sort_values("Total_Amount", ascending=False)
    )
    col2.dataframe(summary_by_stage,column_config={
                   "Total_Amount": st.column_config.NumberColumn("Total_Amount", format="localized")}
                   ,hide_index=True)
    total_column_a = summary_by_stage['Total_Amount'].sum()
    st.write(f"\nTotal for Total Amount: {total_column_a:,.0f}K")


columns = ['Stage Name', 'Product Family', 'Full Name', 'Territory Bucket', 'Market Segment', 'Industry', 'Opportunity Type']


with tab1:
    filter_cont = st.container(border=True, gap="small")
    with filter_cont:
        st.session_state['opps_filtered'],st.session_state['period'] = define_filters(st.session_state['opps'], key_prefix="tab1")

    data = st.session_state.opps_filtered.copy()

    filtered_data = preprocess_data(data)

    show_summary_by_stage(filtered_data, key='summary_stage1')
    st.divider(width="stretch")
    show_opportunity_table(filtered_data)

with tab2:
    filter_cont2 = st.container(border=True, gap="small")
    with filter_cont2:
        st.session_state['opps_filtered'],st.session_state['period'] = define_filters(st.session_state['opps'], key_prefix="tab2")

    data = st.session_state.opps_filtered.copy()
    filtered_data = preprocess_opp_source(data)
    st.divider()
    show_summary_by_stage(filtered_data, key='summary_stage2')
    st.divider()
    show_opportunity_source_table(filtered_data)

