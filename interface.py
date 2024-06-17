import streamlit as st
import time
import re

import pandas as pd
import plotly.figure_factory as ff

from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from agent import CsvAgent
from eda import QueryEda

st.title("Querying With a CSV file")

csv_file = st.file_uploader("Upload your CSV file", type=("csv"))

if csv_file:
    df = pd.read_csv(csv_file)
    st.info("The total row & column count is: ")
    st.write(df.shape)
    st.dataframe(df)

    csv_agent = CsvAgent()
    agent_executor = csv_agent.GetAgentExecutor(df=df)


def plot(user_eda_column):
    with st.container(border=True):
        st.scatter_chart(df, y=[user_eda_column])
        st.info("Scatter Plot")
    with st.container(border=True):
        st.plotly_chart(
            figure_or_data=ff.create_distplot(
                [df[user_eda_column].dropna()], group_labels=[user_eda_column]
            )
        )
        st.info("Hist Plot")
    return


tab1, tab2, tab3 = st.tabs(["QnA", "Summary Stats", "EDA-Plot"])

with tab1:
    st.header("Question and Answer")
    question1 = st.text_input(
        "Ask something about the file",
        placeholder="Ask question like What is the average value of your numeric column?",
        disabled=not csv_file,
    )
    if csv_file and question1:
        if agent_executor:
            try:
                with st.spinner("Wait, response is generating... !"):
                    st.success("Here is the response:")
                    query_eda = QueryEda(agent_executor)
                    retval = query_eda.qna(question1)
                    st.success(retval)
            except Exception as e:
                st.error(f"Error: {e}")  # Detailed error message
        else:
            st.error("Agent executor is not initialized.")
    else:
        st.warning("Please upload a file to continue.")


with tab2:
    st.header("Summary Stats")
    question2 = st.text_input(
        "Insert data column name for eda",
        placeholder="Insert column name?",
        disabled=not csv_file,
    )
    if csv_file and question2:
        if agent_executor:
            try:
                with st.spinner("Wait, response is generating... !"):
                    st.success("Here is the response:")
                    query_eda: QueryEda = QueryEda(agent_executor)
                    retval = query_eda.summary(question2)
                    message_placeholder = st.empty()

                    # Simulate stream of response with milliseconds delay
                    full_response = ""
                    for chunk in re.split(r"(\s+)", retval):
                        full_response += chunk + " "
                        time.sleep(0.01)

                        # Update the message placeholder
                        message_placeholder.markdown(full_response)

                    # Ensure the entire output is displayed
                    message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Agent executor is not initialized.")
    else:
        st.warning("Please upload a file to continue.")


with tab3:
    st.header("EDA-Plot")
    question3 = st.text_input(
        "Insert data column name for eda plot",
        placeholder="Insert column name?",
        disabled=not csv_file,
    )
    if csv_file and question3:
        try:

            with st.spinner("Wait, response is generating... !"):

                plot(question3)

        except Exception as e:
            st.error("No data to show !!.")

    else:
        st.warning("Please upload a file to continue.")

st.write("Thanks for visiting!")
