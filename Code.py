# -*- coding: utf-8 -*-
"""DataQueryAI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lbBpWsRJz7U5rTAfOkwkaarrF6xoom1Y
"""

pip install transformers torch pandas ipywidgets matplotlib

!pip install streamlit localtunnel sentence-transformers transformers pandas torch

!wget -q -O - ipv4.icanhazip.com

!pip install streamlit
!apt install cloudflared

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app2.py
# 
# import streamlit as st
# import pandas as pd
# import torch
# from transformers import TapasTokenizer, TapasForQuestionAnswering
# from sentence_transformers import SentenceTransformer, util
# import plotly.express as px
# import plotly.graph_objects as go
# import seaborn as sns
# 
# tokenizer = TapasTokenizer.from_pretrained("google/tapas-large-finetuned-wtq")
# model = TapasForQuestionAnswering.from_pretrained("google/tapas-large-finetuned-wtq")
# st_model = SentenceTransformer('all-MiniLM-L6-v2')
# 
# # Streamlit UI
# st.set_page_config(page_title="DataQueryAI", page_icon="📊", layout="wide")
# st.title("📊 DataQueryAI using Google TAPAS")
# st.markdown("### Ask questions about your CSV data and visualize insights effortlessly!")
# 
# df = None
# 
# # File Upload
# uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])
# if uploaded_file:
#     df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
#     df.columns = df.columns.astype(str)
#     st.success("✅ File uploaded successfully!")
#     st.write(df.head())
# 
# def find_best_column(question, dtype_filter=None):
# 
#     global df
#     if dtype_filter == 'categorical':
#         columns_to_consider = [col for col in df.columns if df[col].dtype == 'object']
#     elif dtype_filter == 'numerical':
#         columns_to_consider = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
#     else:
#         columns_to_consider = df.columns
# 
#     column_embeddings = st_model.encode(columns_to_consider, convert_to_tensor=True)
#     question_embedding = st_model.encode(question, convert_to_tensor=True)
#     similarities = util.pytorch_cos_sim(question_embedding, column_embeddings).squeeze()
#     best_match_idx = torch.argmax(similarities).item()
# 
#     if similarities[best_match_idx] > 0.3:
#         return columns_to_consider[best_match_idx]
#     return None
# 
# def handle_categorical_query(question):
#     global df
#     best_col = find_best_column(question)
#     if best_col and df[best_col].dtype in [object, "category", "string"]:
#         unique_values = df[best_col].dropna().unique().tolist()
#         return f"✅ Best matching column: {best_col}. Unique values: {', '.join(unique_values[:10])}..." if unique_values else "❌ No values found."
#     return "❌ No relevant categorical query found."
# 
# def handle_numerical_query(question):
#     global df
#     target_column = find_best_column(question)
#     if not target_column:
#         return "❌ No relevant column found."
#     if df[target_column].dtype in ["int64", "float64"]:
#         df[target_column] = pd.to_numeric(df[target_column], errors="coerce")
#     elif df[target_column].dtype == "object":
#         if "count" in question.lower() or "how many" in question.lower():
#             return f"✅ The total count of unique values in {target_column} is: {df[target_column].nunique()}"
#         return "❌ No numerical query recognized."
# 
#     question_lower = question.lower()
#     if "sum" in question_lower or "total" in question_lower:
#         return f"✅ The sum of {target_column} is: {df[target_column].sum():,.2f}"
#     if "average" in question_lower or "mean" in question_lower:
#         return f"✅ The average of {target_column} is: {df[target_column].mean():,.2f}"
#     if "count" in question_lower or "number of" in question_lower or "how many" in question_lower:
#         return f"✅ The total count of {target_column} entries is: {df[target_column].count()}"
#     if "highest" in question_lower or "maximum" in question_lower:
#         return f"✅ The highest value in {target_column} is: {df[target_column].max():,.2f}"
#     if "lowest" in question_lower or "minimum" in question_lower:
#         return f"✅ The lowest value in {target_column} is: {df[target_column].min():,.2f}"
#     return "❌ No numerical query recognized."
# 
# def handle_lookup_query(question):
#     global df
#     if df is None:
#         return "❌ No data uploaded."
# 
#     words = question.lower().split()
#     possible_columns = df.columns.tolist()
# 
#     target_column = find_best_column(question)
#     if not target_column:
#         return "❌ No relevant column found."
# 
#     reference_column = None
#     search_value = None
# 
#     for col in possible_columns:
#         if col.lower() != target_column.lower():
#             for value in df[col].astype(str).dropna().unique():
#                 if value.lower() in words:
#                     reference_column = col
#                     search_value = value
#                     break
#             if reference_column:
#                 break
# 
#     if not reference_column:
#         return "❌ Could not determine the reference column."
# 
#     matching_rows = df[df[reference_column].astype(str).str.lower() == search_value.lower()]
#     if not matching_rows.empty:
#         return f"✅ The {target_column} for {search_value} is: {matching_rows.iloc[0][target_column]}"
# 
#     return "❌ No matching data found."
# def handle_comparison_query(question):
# 
#     global df
#     cat_col = find_best_column(question, dtype_filter='categorical')
#     num_col = find_best_column(question, dtype_filter='numerical')
# 
#     if not cat_col or not num_col:
#         return "❌ Could not determine relevant columns for comparison."
# 
#     st.info(f"🔍 Comparing *{num_col}* by *{cat_col}*")
# 
#     bar_data = df.groupby(cat_col)[num_col].sum().reset_index()
#     bar_fig = px.bar(bar_data, x=cat_col, y=num_col, title=f"{num_col} by {cat_col}", color=cat_col)
#     st.plotly_chart(bar_fig)
# 
#     box_fig = px.box(df, x=cat_col, y=num_col, title=f"Distribution of {num_col} by {cat_col}", color=cat_col)
#     st.plotly_chart(box_fig)
# 
#     violin_fig = px.violin(df, x=cat_col, y=num_col, box=True, points="all", title=f"Variation of {num_col} by {cat_col}", color=cat_col)
#     st.plotly_chart(violin_fig)
# 
#     return f"✅ Comparison of {num_col} by {cat_col} displayed."
# 
# def query_table(question):
#     global df
#     question_lower = question.lower()
# 
#     if "vary by" in question_lower or "compare" in question_lower:
#         return handle_comparison_query(question)
#     if any(word in question_lower for word in ["sum", "total", "average", "highest", "lowest", "count", "number of", "how many"]):
#         return handle_numerical_query(question)
#     if "of" in question_lower or "for" in question_lower:
#         return handle_lookup_query(question)
#     return handle_categorical_query(question)
# 
# # Query Input
# query = st.text_input("🔍 Enter your question:", key="query", help="Press Enter to submit.")
# if query:
#     result = query_table(query)
#     st.write(result)
# 
# # Sidebar Visualization Options
# st.sidebar.title("📊 Visualization Options")
# if df is not None:
#     col_to_visualize = st.sidebar.selectbox("🔹 Select Column for Visualization", df.columns)
#     chart_type = st.sidebar.radio("📊 Choose Chart Type", ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Heatmap"])
#     fig = None
# 
#     if col_to_visualize:
#         if chart_type == "Bar Chart":
#             fig = px.bar(df, x=col_to_visualize, title=f"{col_to_visualize} Distribution", color=col_to_visualize)
#         elif chart_type == "Line Chart":
#             fig = px.line(df, y=col_to_visualize, title=f"{col_to_visualize} Trend", markers=True)
#         elif chart_type == "Pie Chart":
#             fig = px.pie(df, names=col_to_visualize, title=f"{col_to_visualize} Composition")
#         elif chart_type == "Histogram":
#             fig = px.histogram(df, x=col_to_visualize, title=f"{col_to_visualize} Histogram", nbins=20)
# 
#         if fig:
#             st.plotly_chart(fig)
#

!streamlit run app2.py & npx localtunnel --port 8501