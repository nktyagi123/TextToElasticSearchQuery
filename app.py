import streamlit as st
import json
import os
from elasticsearch import Elasticsearch

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    print("@@@@@@@@@@@@@@@@@",type(response.text))
    return response.text

def read_elasticsearch_query(query, index):
    
    es =  Elasticsearch(hosts=['https://ops-analytics-preprod.appl.kp.org:9200'],verify_certs=False,timeout=600, http_auth=('G073080', "Rakesh@nktyagi423") )

    try:
        print(query)
        query1 = json.loads(query)
        print("********************",type(query1))
        # Execute the Elasticsearch query
        result = es.search(index=index, body=query1)
        # Accessing the hits (search results)
        hits = result['hits']['hits']
        return hits
    except Exception as e:
        print(f"Error executing Elasticsearch query: {e}")
        return None
     

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to Elasticsearch queries!
    SECTION \n\nFor example,\nExample 1 - How many documents are there in the index?,
    The Elasticsearch query will be something like this: `{"query": {"match_all": {}}}`.
    \nExample 2 - Show me all documents where EntityType is 'Type1'?,
    The Elasticsearch query will be something like this: `{"query": {"match": {"EntityType": "Type1"}}}`.

    also the elasticsearch query should not have anything like ``` in beginning or end and elasticsearch word in output

    """


]

# Apply background color and styling
st.markdown(
    """
    <style>
        body {
            background-color: #f8f8f8;  /* Light gray background */
            font-family: 'Arial', sans-serif;
            color: #333;  /* Dark gray text */
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        .stApp {
            width: 90%;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            background-color: #fff;  /* White container background */
        }
        .stButton {
            background-color: #4CAF50;  /* Green button color */
            color: black;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton:hover {
            background-color: #45a049;  /* Darker green on hover */
        }
        .response-box {
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 20px;
            background-color: #fff;  /* White box background */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        @media only screen and (max-width: 600px) {
            .stApp {
                width: 90%;
                padding: 10px;
            }
            .stButton {
                padding: 10px 20px;
                font-size: 16px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title and header
st.title("Gemini App To Retrieve ELK Data")
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question", key="ask_button")

# if submit is clicked
if submit:
    response1 = get_gemini_response(question, prompt)
    st.info("Query Is : " + response1)
    index_name = "hs-fullstack_test-influencers"
    response = read_elasticsearch_query(response1, index_name)

    # # Display the response in a box
    # st.subheader("The Response is")
    # with st.container():
    #     for row in response:
    #         st.json(row['_source'])

    
    # Create vertical and horizontal bar charts in a single row
    col1, col2 = st.columns(2)

    # Vertical bar chart
    with col1:
        st.subheader("Vertical Bar Chart")
        chart_data = [row['_source']['EntityType'] for row in response]
        st.bar_chart(chart_data)

    # Horizontal bar chart
    with col2:
        st.subheader("Horizontal Bar Chart")
        st.bar_chart(chart_data, use_container_width=True)

    # Create a table
    st.subheader("Table")
    table_data = [row['_source'] for row in response]
    st.table(table_data)

# # Apply background color and styling
# st.markdown(
#     """
#     <style>
#         body {
#             background-color: #f8f8f8;  /* Light gray background */
#             font-family: 'Arial', sans-serif;
#             color: #333;  /* Dark gray text */
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }
#         .stApp {
#             width: 90%;
#             max-width: 800px;
#             margin: 0 auto;
#             padding: 20px;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             border-radius: 10px;
#             background-color: #fff;  /* White container background */
#         }
#         .stButton {
#             background-color: #4CAF50;  /* Green button color */
#             color: black;
#             padding: 12px 24px;
#             text-align: center;
#             text-decoration: none;
#             display: inline-block;
#             font-size: 18px;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#             transition: background-color 0.3s;
#         }
#         .stButton:hover {
#             background-color: #45a049;  /* Darker green on hover */
#         }
#         .response-box {
#             padding: 15px;
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             margin-top: 20px;
#             background-color: #fff;  /* White box background */
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#         }
#         @media only screen and (max-width: 600px) {
#             .stApp {
#                 width: 90%;
#                 padding: 10px;
#             }
#             .stButton {
#                 padding: 10px 20px;
#                 font-size: 16px;
#             }
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Streamlit app title and header
# st.title("Gemini App To Retrieve ELK Data")
# question = st.text_input("Input: ", key="input")
# submit = st.button("Ask the question", key="ask_button")

# # if submit is clicked
# if submit:
#     response1 = get_gemini_response(question, prompt)
#     st.info("Query Is : " + response1)
#     index_name = "hs-fullstack_test-influencers"
#     response = read_elasticsearch_query(response1, index_name)

#     # Display the response in a box
#     st.subheader("The Response is")
#     with st.container():
#         for row in response:
#             st.json(row['_source'])







# ## Streamlit App

# st.set_page_config(page_title="I can Retrieve Any ELK query")
# st.header("Gemini App To Retrieve ELK Data")

# question=st.text_input("Input: ",key="input")

# submit=st.button("Ask the question")

# # if submit is clicked
# if submit:
#     response1=get_gemini_response(question,prompt)
#     print("Query Is : ",response1)
#     index_name = "hs-fullstack_test-influencers"
#     response=read_elasticsearch_query(response1,index_name)
#     st.subheader("The Response is")
#     st.header(response1)
#     for row in response:
#         st.json(row['_source'])