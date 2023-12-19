import streamlit as st
import pandas as pd
import numpy as np
from models import AgentLevelAdditions
from core import YIC, calculate_rolling_commission, cal_annual_sales, Renewal
from loguru import logger

agent_level = AgentLevelAdditions()
st.title("Comission Scheme")
### Sidebar inputs ###
st.sidebar.title("Inputs")
agent_level = st.sidebar.selectbox(
    "Agent Level", options=agent_level.model_dump().keys()
)
template = {i: 10000 for i in range(1, 13)}
df_template = pd.DataFrame(template.items(), columns=["month", "sales"])

edited_df_dict = {}
for i in range(1, 6):
    st.sidebar.subheader(f"Year {i} Sales Data")
    edited_df_dict[f"edited_df{i}"] = st.sidebar.data_editor(
        df_template, key=i
    )


# st.sidebar.subheader("Year 2 Sales Data")
# edited_df2 = st.sidebar.data_editor(df_template, key=1)

# st.sidebar.subheader("Year 3 Sales Data")
# edited_df3 = st.sidebar.data_editor(df_template, key=2)

# st.sidebar.subheader("Year 4 Sales Data")
# edited_df4 = st.sidebar.data_editor(df_template, key=3)

# st.sidebar.subheader("Year 5 Sales Data")
# edited_df5 = st.sidebar.data_editor(df_template, key=4)

if st.sidebar.button(key="calculate", label="Calculate"):
    st.write(f"Agent level: {agent_level}")
    yearly_sales = {}
    for i, (name, edited_df) in enumerate(edited_df_dict.items()):
        st.write(f"Year {i+1} Commission scheme")
        sales_df = calculate_rolling_commission(
            edited_df, agent_level=agent_level
        )
        annual_sales = cal_annual_sales(sales_df)
        yearly_sales[i] = annual_sales
        slim_sales_df = sales_df[["month", "sales", "rolling_commission"]]
        yic = YIC(annual_sales=annual_sales)
        yic.get_annual_bonus()
        yic_df = pd.DataFrame(
            {"YIC": [yic.annual_bonus]}, columns=["YIC"], index=["Total"]
        )

        logger.info(yic_df)
        r = Renewal(yearly_sales)
        yearly_renewal_bonus_dict = r.get_renewal_commission()
        yearly_renewal_df = pd.DataFrame.from_dict(
            yearly_renewal_bonus_dict,
            columns=["Renewal Bonud"],
            orient="index",
        )

        st.dataframe(slim_sales_df, hide_index=True, use_container_width=True)
        st.dataframe(yic_df, hide_index=False, use_container_width=True)
        st.dataframe(
            yearly_renewal_df, hide_index=False, use_container_width=True
        )
