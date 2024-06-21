import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

alt.themes.enable("dark")

working_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = f"{working_dir}/data"
files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Dropdown to select a file
selected_file = st.selectbox('Select a file', files, index=None)

st.write(selected_file)


if selected_file:
    file_path = os.path.join(folder_path, selected_file)

    columns_to_read = ["Frequency in Hz", "Dissipation factor", "Power factor", "C'", "C''"]
    df = pd.read_excel(file_path, usecols=columns_to_read)

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    log_scale = st.checkbox('Log-Log Scale')

    if st.button('Generate Plot'):
        sns.set_style('whitegrid')
        fig, ax = plt.subplots(figsize=(20, 12))

        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax, marker='o')
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax, palette='viridis')
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax, hue=df[y_axis], palette='viridis', s=100)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[y_axis], kde=True, ax=ax, color='skyblue')
            ax.set_ylabel('Density')
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax, palette='viridis')
            ax.set_ylabel('Count')

        if log_scale:
            ax.set_xscale('log')
            ax.set_yscale('log')

        ax.set_title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=20, fontweight='bold')
        ax.set_xlabel(x_axis, fontsize=14)
        ax.set_ylabel(y_axis, fontsize=14)
        ax.grid(True, which="both", ls="--")

        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)

        st.pyplot(fig)
