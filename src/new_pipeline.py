import streamlit as st
from pymdownx.blocks.details import Details

from opps_opportunity_source import preprocess_opp_source


from opps_opportunity_source import show_opportunity_source_table
from filter_opps import define_filters
from opps_new_pipeline import preprocess_data, show_opportunity_table





def show_summary_by_stage(data, key):
    col1, col2,col3 = st.columns([3,7,4])
    column = col1.radio('Metric', options=['Stage Name', 'Product Family', 'Full Name', 'Territory Bucket', 'Market Segment',
     'Industry', 'Opportunity Type'], horizontal=False, key=key)

    opps = data.copy()
    opps['Amount'] = (opps['Amount']/1000)
    opps['Amount'] = opps['Amount'].round(2)
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


def show_new_pipeline():
    st.markdown("""
    <style>
    /* Reduce padding superior de toda la app */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }
    </style>
""", unsafe_allow_html=True)
    st.session_state['opps_filtered'],st.session_state['period'] = define_filters(st.session_state['opps'], key_prefix="tab1")
    data = st.session_state.opps_filtered.copy()
    filtered_data = preprocess_data(data)
    st.subheader("Summary by Selected Metric", divider="red")
    show_summary_by_stage(filtered_data, key='summary_stage1')
    st.subheader("Details", divider="red")
    show_opportunity_table(filtered_data)


show_new_pipeline()