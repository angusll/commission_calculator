import streamlit as st
import pandas as pd
import numpy as np
from models import AgentLevelAdditions
from core import YIC, calculate_rolling_commission, cal_annual_sales

agent_level = AgentLevelAdditions()
st.title("Comission Scheme")
### Sidebar inputs ###
st.sidebar.title("Inputs")
agent_level = st.sidebar.selectbox(
    "Agent Level", options=agent_level.model_dump().keys()
)
template = {i: 10000 for i in range(1, 13)}
df_template = pd.DataFrame(template.items(), columns=["month", "sales"])
edited_df = st.sidebar.data_editor(df_template)

if st.sidebar.button(key="calculate", label="Calculate"):
    st.write(f"Agent level: {agent_level}")
    sales_df = calculate_rolling_commission(edited_df, agent_level=agent_level)
    slim_sales_df = sales_df[["month", "sales", "rolling_commission"]]
    yic = YIC(annual_sales=cal_annual_sales(sales_df)).get_annual_bonus()
    st.dataframe(slim_sales_df, hide_index=True, use_container_width=True)
    st.write(f"YIC: {yic}")
