import streamlit as st
import pandas as pd

##############
# Dataframes #
##############
# Reference and description
df_reference_and_descripiton_s1 = pd.read_csv("./data/ditch1/reference_and_description_section_1.csv")
df_reference_and_descripiton_s2 = pd.read_csv("./data/ditch1/reference_and_description_section_2.csv")

# Mineralogical composition
df_mineralogical_composition_s1 = pd.read_csv("./data/ditch1/semi-quantitative_mineralogical_composition_section_1.csv")
df_mineralogical_composition_s2 = pd.read_csv("./data/ditch1/semi-quantitative_mineralogical_composition_section_2.csv")

# Chemical contents
df_chemical_contents = pd.read_csv("./data/ditch1/chemical_contents.csv")


st.logo("ist_logo.webp", size="large")

st.title("Analysis of the Data")

st.subheader("Reference and Description of Ceramic Artifact Samples")
st.text("Section 1")
st.dataframe(df_reference_and_descripiton_s1)
st.text("Section 2")
st.dataframe(df_reference_and_descripiton_s2)

st.subheader("Semi-Quantitative Mineralogical Composition of Ceramic Artifact Samples")
st.text("Section 1")
st.bar_chart(df_mineralogical_composition_s1.set_index("Sample"))
st.text("Section 2")
st.bar_chart(df_mineralogical_composition_s2.set_index("Sample"))

st.subheader("Chemical Contents in Ceramic Artifact Samples")
st.dataframe(df_chemical_contents) # falta Ce/Ce* nos dados !!!!!!