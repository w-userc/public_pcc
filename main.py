import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64 # Import base64
from pathlib import Path # To read image file

# --- Page Configuration ---
st.set_page_config(
    page_title="Cerâmicas Calcolíticas: Santa Vitória",
    page_icon=":test_tube:",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data # Cache data loading for performance
def load_data():
    try:
        # Adjust paths if your data folder structure is different
        base_path = "./data/ditch1/"
        df_ref_s1 = pd.read_csv(base_path + "reference_and_description_section_1.csv")
        df_ref_s2 = pd.read_csv(base_path + "reference_and_description_section_2.csv")
        df_min_s1 = pd.read_csv(base_path + "semi-quantitative_mineralogical_composition_section_1.csv")
        df_min_s2 = pd.read_csv(base_path + "semi-quantitative_mineralogical_composition_section_2.csv")

        # --- Corrected Loading for Chemical Data ---
        # Read the chemical data, recognizing 'Element' is the key column
        df_chem_raw = pd.read_csv(base_path + "chemical_contents.csv")

        # 1. Set 'Element' as the index
        df_chem_indexed = df_chem_raw.set_index('Element')

        # 2. Transpose the DataFrame: Samples become rows, Elements become columns
        df_chem_transposed = df_chem_indexed.T

        # 3. Reset the index: The Sample numbers (now in the index) become a column
        df_chem_transposed.index.name = 'Sample' # Name the index before resetting
        df_chem = df_chem_transposed.reset_index()

        # 4. Convert 'Sample' column to integer
        df_chem['Sample'] = pd.to_numeric(df_chem['Sample'], errors='coerce')
        df_chem.dropna(subset=['Sample'], inplace=True) # Remove if sample couldn't be converted
        df_chem['Sample'] = df_chem['Sample'].astype(int)

        # 5. Convert element columns to numeric, replacing 'n.d.' (and potentially '%') with NaN
        element_cols = df_chem.columns.drop('Sample') # Get all columns except 'Sample'
        for col in element_cols:
            # Handle potential '%' signs (like in CaO '3.9%') before conversion
            if df_chem[col].dtype == 'object': # Only process object (string) columns
                 df_chem[col] = df_chem[col].astype(str).str.replace('%', '', regex=False)
            # Replace 'n.d.' with NaN and convert to numeric
            df_chem[col] = pd.to_numeric(df_chem[col].replace(['n.d.', 'n.d'], np.nan, regex=False), errors='coerce')

        # --- End of Corrected Loading ---


        # Combine reference data
        df_ref = pd.concat([df_ref_s1, df_ref_s2], ignore_index=True)

        # Ensure key columns in df_ref are numeric for merging
        if 'Sample Reference' in df_ref.columns:
            df_ref['Sample Reference'] = pd.to_numeric(df_ref['Sample Reference'], errors='coerce')
            df_ref.dropna(subset=['Sample Reference'], inplace=True)
            df_ref['Sample Reference'] = df_ref['Sample Reference'].astype(int)
        else:
             st.warning("Reference data is missing 'Sample Reference' column. Merge might fail.")


        return df_ref, df_min_s1, df_min_s2, df_chem # Return the *processed* df_chem

    except FileNotFoundError as e:
        st.error(f"Error loading data file: {e}. Make sure CSV files are in './data/ditch1/' directory or adjust paths.")
        return None, None, None, None
    except Exception as e:
        st.error(f"An error occurred during data loading: {e}")
        # Include traceback for debugging if needed
        # import traceback
        # st.error(traceback.format_exc())
        return None, None, None, None

# --- Load data using the modified function ---
df_reference, df_mineralogical_s1, df_mineralogical_s2, df_chemical = load_data()


# --- App Header ---
def img_to_base64(img_path):
    """Converts an image file to a Base64 string."""
    try:
        path = Path(img_path)
        with path.open("rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.warning(f"Não foi possível codificar o logo '{img_path}': {e}")
        return None

# --- Cabeçalho da App (Método 2: HTML/Markdown) ---
img_path = "ist_logo.webp"
img_base64 = img_to_base64(img_path)

# Adjust image width and margin as needed
image_width_px = 200
right_margin_px = 20

# if img_base64:
#     # Use CSS Flexbox for alignment
#     st.markdown(
#         f"""
#         <div style="display: flex; align-items: center;">
#             <img src="data:image/webp;base64,{img_base64}" width="{image_width_px}" style="margin-right: {right_margin_px}px;">
#             <div>
#                 <h1>Património Cultural e Ciências: Caso de Estudo</h1>
#                 <h3>Fingerprinting Ceramics from the Chalcolithic Santa Vitória Enclosure (SW Iberia)</h3>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
if img_base64:
    # Use CSS Flexbox for alignment
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: {right_margin_px}px;">
            <img src="data:image/webp;base64,{img_base64}" width="{image_width_px}" style="margin: 0;">
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h1 style="margin: 0; font-size: 40px; line-height: 1.2;">
                    Património Cultural e Ciências: Caso de Estudo
                </h1>
                <h3 style="margin: 0 0 0 0; font-size: 22px; line-height: 1.2;">
                    Fingerprinting Ceramics from the Chalcolithic Santa Vitória Enclosure (SW Iberia)
                </h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Fallback if image loading fails
    st.title("Património Cultural e Ciências: Caso de Estudo")
    st.subheader("Fingerprinting Ceramics from the Chalcolithic Santa Vitória Enclosure (SW Iberia)")
st.markdown("---")
st.markdown("""
*Apresenta-se um resumo e análise do artigo científico: "Marques, R. et al. (2024). Fingerprinting Ceramics from the Chalcolithic Santa Vitória Enclosure (SW Iberia). Minerals 14, 399." 
 Este trabalho foi realizado pelos elementos do grupo 5 constituído por Guilherme Prestes (LEMEC), Guilherme Amaro (LEMEC), Liedson Cunha (LEIC).
 [Link para o artigo](https://www.mdpi.com/2075-163X/14/4/399)*

**Objetivo:** Introduzir o artigo científico e identificar os problemas abordados; analisar os resultados obtidos e as metodologias aplicadas; apresentar as conlcusões chegadas e as possíveis contribuições para o avanço do caso de estudo. 
""")

# --- Main Content Sections ---

# 1. Introduction & Context
with st.expander("1. Introdução: Estudo realizado no Recinto Calcolítico de Santa Vitória"):
    st.markdown("""
    <h3 style="color:#388cb0;"><b>Património Estudado:</b></h3> 
    O estudo foca em cerâmicas arqueológicas provenientes do recinto Calcolítico de Santa Vitória, 
    situado em Campo Maior, no Alentejo, sul de Portugal. O recinto, caracterizado por dois fossos 
    concêntricos de traçado sinuoso com lóbulos semicirculares contíguos, datada da segunda metade do 3.º 
    milénio a.C. (Fosso 1: 2556-2040 cal AC; Fosso 2: 2460-2200 cal AC, segundo datações por radiocarbono). 
    Classificado como de interesse público nacional, Santa Vitória é considerado um espaço cerimonial,
    testemunho das práticas sociais, rituais e cosmológicas das comunidades pré-históricas da região.
    
    <ul>
    <li><b style="color:#808b96; font-size:20px;">
        Objetivo principal:</b> 
        Contribuir para a contextualização dos artefactos cerâmicos, o que implica compreender  
        as tecnologias de produção utilizadas e a origem das matérias-primas, entretanto, discutir o papel
        do recinto no panorama regional.
    </li>
    <li><b style="color:#808b96; font-size:20px;">Amostras:</b> 
    Foram estudados 25 fragmentos cerâmicos recolhidos em duas secções distintas do Fosso 1. Estes fragmentos 
    incluem diferentes tipologias, como tigelas, contas (pequenos objetos que poderão ter sido utilizados como 
    decoração) e fragmentos indiferenciados (peças cuja forma original é difícil de identificar).
    </li>
    </ul>
    
    <p style="color:Gray;"><i>(Ver Figuras 1 & 2 no artigo)</i></p>
    
    <h3 style="color:#388cb0;">Questões de Investigação Abordadas</h3>
    
    O artigo aborda as seguintes questões:
    
    <ol>
    <li><b style="color:#808b96;">Procedência das cerâmicas:</b> As cerâmicas foram produzidas localmente ou terão sido importadas de outros locais? </li>
    <li><b style="color:#808b96;">Técnicas de fabrico:</b> Que tecnologias foram usados na produção destas cerâmicas? </li>
    <li><b style="color:#808b96;">Diferenças entre as seções do fosso:</b> Existem variações significativas na composição mineralógica e química das cerâmicas? </li>
    <li><b style="color:#808b96;">Implicações sociais:</b> Que informações as cerâmicas fornecem sobre as dinâmicas sociais da comunidade? </li>
    </ol>
    """, unsafe_allow_html=True)

# 2. Methodology
with st.expander("2. Metodologia: Técnicas usadas para estudar as Cerâmicas"):
    st.markdown("""
    <h3 style="color:#388cb0;">Métodos de Análise</h3>
    
    Para determinar a proveniência das matérias-primas, assim como as tecnologias de produção 
    e a diferença composicional entre os fragmentos, foram usados diferentes técnicas para 
    determinar tanto os componentes químicos como mineralógicos presentes nos fragmentos. 
    
    <ul>
    <li><b style="color:#808b96; font-size:20px;">1. Difração de Raios-X (XRD):</b> 
        <ul>
            <li>Identificar as fases minerais presentes nas cerâmicas, tais como: quartzo, plagioclásios, anfibólios, filossilicatos, feldspatos alcalinos e hematite.</li>
            <li>A presença de filossilicatos e a ausência de minerais característicos de altas temperaturas apontam para uma queima das cerâmicas a temperaturas inferiores a 850°C.</li>
        </ul>
    </li>
    
    <li><b style="color:#808b96; font-size:20px;">2. Análise por Ativação Neutrônica (NAA):</b> 
        <ul>
            <li>Quantificar 24 elementos químicos, incluindo elementos maioritários (ex.: Na, K, Fe) e em traços (ex.: terras raras, Rb, Cs).</li>
            <li>Normalização com escândio (Sc) para minimizar variações naturais e antrópicas.</li>
        </ul>
    </li>
    
    <li><b style="color:#808b96; font-size:20px;">3. Análises Estatísticas:</b> 
        <ul>
            <li><b>Clusterização hierárquica:</b> Agrupar amostras com composições químicas semelhantes.</li>
            <li><b>Correlação de Pearson:</b> Avaliar relações entre elementos químicos.</li>
        </ul>
    </li>
    </ul>
    
    <h3 style="color:#388cb0;">Resultados Principais</h3>
    
    <ul>
    <li><b style="color:#808b96;">Proveniência local:</b> A composição mineralógica das cerâmicas, dominada por plagioclásios, anfibólios e quartzo, reflete o contexto geológico regional, caracterizado por gabros, dioritos e rochas híbridas da região.</li>
    
    <li><b style="color:#808b96;">Tecnologia de produção:</b> 
        <ul>
            <li>Temperatura de queima inferior a 850°C.</li>
            <li>Uso de Temperantes: Adição de grãos não plásticos (temper) em proporções variáveis, com maior evidência na Secção 1, onde os fragmentos <br> apresentam uma textura mais grosseira devido ao tamanho superior dos grãos.</li>
        </ul>
    </li>
    
    <li><b style="color:#808b96;">Diferenças entre seções:</b> 
        <ul>
            <li><b>Seção 1:</b> Maior proporção de grãos grossos e menor teor de ferro.</li>
            <li><b>Seção 2:</b> Maior heterogeneidade química e maior presença de anfibólios/ferro.</li>
        </ul>
    </li>
    
    <li><b style="color:#808b96;">Amostras atípicas:</b> 
        <ul>
            <li><b>Amostra 163:</b> Alto teor de potássio (K), associado a feldspatos alcalinos.</li>
            <li><b>Amostra 183:</b> Alto teor de sódio (Na), ligado a plagioclásios.</li>
        </ul>
    </li>
    </ul>
    
    <p style="color:Gray;"><i>(Ver Figuras 3 & 4 no artigo)</i></p>
    """, unsafe_allow_html=True)

# 3. Results
with st.expander("3. Dados: Apresentação dos Resultados Obtidos"):
    st.markdown("### 3.1 Informação das Amostras")
    if df_reference is not None and 'Sample Reference' in df_reference.columns and 'Section' in df_reference.columns:
        tab1, tab2 = st.tabs(["Amostras Sector 1 (n=10)", "Amostras Sector 2 (n=15)"])
        with tab1:
            st.dataframe(df_reference[df_reference['Section'] == 1][['Sample Reference', 'SU', 'Type', 'Sub-Type']].reset_index(drop=True))
        with tab2:
            st.dataframe(df_reference[df_reference['Section'] == 2][['Sample Reference', 'SU', 'Type', 'Sub-Type']].reset_index(drop=True))
    else:
        st.warning("Não foi possível carregar os dados de referência ou faltam colunas necessárias ('Sample Reference', 'Section').")

    st.markdown("### 3.2 Composição Mineralógica (Resultados DRX / XRD)")
    
    if df_mineralogical_s1 is not None and df_mineralogical_s2 is not None:
        tab1, tab2 = st.tabs(["Mineralogia Sector 1 (%)", "Mineralogia Sector 2 (%)"])
        with tab1:
            st.dataframe(df_mineralogical_s1)
            cols_to_plot_s1 = [col for col in ['Plagioclase', 'Quartz', 'Amphibole', 'Phyllosilicates', 'K-Feldspar', 'Hematite'] if col in df_mineralogical_s1.columns]
            if 'Sample' in df_mineralogical_s1.columns and cols_to_plot_s1:
                 st.bar_chart(df_mineralogical_s1.set_index("Sample")[cols_to_plot_s1])
            else:
                 st.warning("Não foi possível gerar o gráfico de mineralogia do Sector 1 (falta coluna 'Sample' ou colunas de dados).")
        with tab2:
            st.dataframe(df_mineralogical_s2)
            cols_to_plot_s2 = [col for col in ['Plagioclase', 'Quartz', 'Amphibole', 'Phyllosilicates', 'K-Feldspar', 'Hematite'] if col in df_mineralogical_s2.columns]
            if 'Sample' in df_mineralogical_s2.columns and cols_to_plot_s2:
                 st.bar_chart(df_mineralogical_s2.set_index("Sample")[cols_to_plot_s2])
            else:
                 st.warning("Não foi possível gerar o gráfico de mineralogia do Sector 2 (falta coluna 'Sample' ou colunas de dados).")
    else:
        st.warning("Não foi possível carregar os dados mineralógicos.")

    st.markdown("### 3.3 Composição Química (Resultados AAN / NAA)")

    # --- Check df_chemical AFTER loading and processing ---
    if df_chemical is not None and 'Sample' in df_chemical.columns:
        st.markdown("#### Tabela Completa de Dados Químicos (Majoritários em %, Vestigiais em mg/kg)")
        # Display the *processed* chemical data
        st.dataframe(df_chemical) 

        # --- Recreate Figure 5 from the paper ---
        st.markdown("#### Diferenças Químicas (Normalizadas a Sc)")
        st.markdown("*(Baseado na Figura 5 do artigo)*")

        df_plot = df_chemical.copy()

        # Merge section info - df_chemical now has 'Sample', df_reference has 'Sample Reference'
        if df_reference is not None and 'Sample Reference' in df_reference.columns and 'Section' in df_reference.columns:
            df_plot = pd.merge(
                df_plot, df_reference[['Sample Reference', 'Section']],
                left_on='Sample', right_on='Sample Reference', how='left'
            )
            # Optional: Drop the redundant 'Sample Reference' column
            # if 'Sample Reference' in df_plot.columns:
            #    df_plot = df_plot.drop(columns=['Sample Reference'])
        else:
            st.warning("Não foi possível juntar a informação do sector. Verifique as colunas dos dados de referência ('Sample Reference', 'Section').")
            df_plot['Section'] = 'Desconhecido' # Fallback

        # --- Plotting Logic (Mostly unchanged, check column names just in case) ---
        # Check for element columns (use the names from the transposed df)
        # Make sure element names from CSV (like 'Na₂O') are correctly handled if they have special characters
        required_cols_chem = ['Fe₂O₃', 'K₂O', 'Na₂O', 'Sc']
        
        # Check if all required columns exist in df_plot
        missing_cols = [col for col in required_cols_chem if col not in df_plot.columns]

        if not missing_cols and 'Section' in df_plot.columns:
            # Convert required columns to numeric again just in case (might be redundant but safe)
            for col in required_cols_chem:
                 df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')
            
            # Avoid division by zero or NaN/missing Sc values
            df_plot = df_plot.dropna(subset=['Sc'])
            df_plot = df_plot[df_plot['Sc'] > 0]

            # Normalize data
            df_plot['Fe_norm'] = df_plot['Fe₂O₃'] / df_plot['Sc']
            df_plot['K_norm'] = df_plot['K₂O'] / df_plot['Sc']
            df_plot['Na_norm'] = df_plot['Na₂O'] / df_plot['Sc']

            # Handle potential NaN/inf values created during normalization
            df_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
            df_plot.dropna(subset=['Fe_norm', 'K_norm', 'Na_norm'], inplace=True)

            if not df_plot.empty:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                colors = {1: 'blue', 2: 'red', 'Desconhecido': 'grey'}
                markers = {1: 'o', 2: 's', 'Desconhecido': '^'}

                # Plot Fe vs Na (Normalized)
                for section in df_plot['Section'].unique():
                    group = df_plot[df_plot['Section'] == section]
                    label_txt = f'Sector {section}' if section != 'Desconhecido' else 'Sector Desconhecido'
                    ax1.scatter(group['Na_norm'], group['Fe_norm'],
                                label=label_txt,
                                color=colors.get(section, 'black'), marker=markers.get(section, 'x'), alpha=0.7)
                    for i, row in group.iterrows():
                        if row['Sample'] == 163 or row['Sample'] == 183:
                            ax1.text(row['Na_norm'] * 1.01, row['Fe_norm'] * 1.01, str(int(row['Sample'])))
                ax1.set_xlabel('Na₂O / Sc') # Match exact element name
                ax1.set_ylabel('Fe₂O₃ / Sc') # Match exact element name
                ax1.set_title('Fe vs Na (Normalizado)')
                ax1.legend()
                ax1.grid(True, linestyle='--', alpha=0.6)

                # Plot K vs Na (Normalized)
                for section in df_plot['Section'].unique():
                    group = df_plot[df_plot['Section'] == section]
                    label_txt = f'Sector {section}' if section != 'Desconhecido' else 'Sector Desconhecido'
                    ax2.scatter(group['Na_norm'], group['K_norm'],
                                label=label_txt,
                                color=colors.get(section, 'black'), marker=markers.get(section, 'x'), alpha=0.7)
                    for i, row in group.iterrows():
                        if row['Sample'] == 163 or row['Sample'] == 183:
                            ax2.text(row['Na_norm'] * 1.01, row['K_norm'] * 1.01, str(int(row['Sample'])))
                ax2.set_xlabel('Na₂O / Sc') # Match exact element name
                ax2.set_ylabel('K₂O / Sc') # Match exact element name
                ax2.set_title('K vs Na (Normalizado)')
                ax2.legend()
                ax2.grid(True, linestyle='--', alpha=0.6)

                plt.tight_layout()
                st.pyplot(fig)

            else:
                 st.warning("Não há dados válidos disponíveis para gerar os gráficos após normalização e filtragem.")
        else:
            # More informative warning if columns are missing
            st.warning(f"Não foi possível criar os gráficos. Faltam colunas necessárias para normalização ou informação de sector. Necessárias: {required_cols_chem + ['Section']}. Faltando em df_plot: {missing_cols}")
    else:
        # This warning should NOT appear now if loading was successful
        st.warning("Não foi possível carregar ou processar corretamente os dados químicos (falta a coluna 'Sample' após processamento). Verifique a função `load_data` e o ficheiro CSV.")

    

# 4. Discussion & Conclusions
with st.expander("4. Discussão e Conclusões"):
    st.markdown("""
    <h3 style="color:#388cb0;">Conclusões e Implicações</h3>
                
    As cerâmicas calcolíticas de Santa Vitória sugerem uma produção local dominante, compatível com o contexto geológico regional (gabros e dioritos), embora trocas regionais não sejam descartáveis. Variações tecnológicas, como diferenças nos temperantes e heterogeneidade química entre secções, indicam distinções nas práticas de produção ou grupos sociais. 
    
    <li><b style="color:#808b96;">Limitações:</b>
        <ul>
            <li>Falta de análise de matérias-primas locais para comparação direta.</li>
            <li>Número limitado de amostras por tipologia cerâmica.</li>
        </ul>
    </li>
    
    <li><b style="color:#808b96;">Perspectivas futuras:</b>
        <ul>
            <li>Estudos complementares com argilas regionais e mais amostras para confirmar padrões.</li>
            <li>Análises isotópicas ou de luminescência para refinamento cronológico.</li>
        </ul>
    </li>
    </ul>
    """, unsafe_allow_html=True)

# 5. Student Perspective
st.markdown("---")
st.markdown("""
    <h3 style="color:#076aa6;"> Contributo para a Área de Estudo</h3>
    """, unsafe_allow_html=True) 
st.markdown("""
**Enquanto estudantes de licenciatura, é pertinente começarmos a pensar de que modo podemos aplicar os conhecimentos adquiridos em benefício de um propósito maior. 
Portanto, a questão que se pretende abordar nesta secção é a seguinte: de que forma podemos intervir ou contribuir para o avanço da área de estudo apresentada?**
""")

st.subheader("Licenciatura em Engenharia Mecânica (LEMEC)")
st.markdown("""
*   Melhorar a Análise dos Materiais 
*   Usar softwares como SolidWorks para simular:
    *   Como as cerâmicas se comportam sob pressão ou calor (ex.: resistência ao quebrar).
    *   Se a temperatura de queima (inferior a 850°C, como no estudo) afeta sua durabilidade.
""")
st.markdown("---")
st.markdown("""
*   Recriação de Forno Experimental
*   **Objetivo:** Testar o comportamento da argila local em diferentes temperaturas de queima.
*   **Metodologia:**
    *   Construir um forno em escala reduzida, considerando princípios de termodinâmica.
    *   Testar temperaturas entre 700°C e 900°C.
    *   Medir tempo de queima, taxa de resfriamento e resistência do material.

*   **Aplicação:** Validar se a queima abaixo de 850°C produzia cerâmica resistente ou se era uma limitação técnica da época.
""")
st.markdown("---")
st.subheader("Licenciatura em Engenharia Informática e de Computadores (LEIC)")
st.markdown("""
Como futuro profissional, destaco:

*   **Análise rápida:** Usar IA para processar dados químicos e mineralógicos das cerâmicas de Santa Vitória de forma eficiente.  
*   **Ligações:** Relacionar dados de vários sítios a alta velocidade, revelando redes de troca.  
*   **Ferramentas:** Criar plataformas que tornem os resultados acessíveis a todos.  
*   *(Nota:)* A informática potencia a arqueologia sem a substituir.
""")

# 6. Reference 
st.markdown("---")
st.subheader("Referência")
st.markdown("Marques, R.; Rodrigues, A.L.; Russo, D.; Gméling, K.; Valera, A.C.; Dias, M.I.; Prudêncio, M.I.; Basílio, A.C.; Fernandes, P.G.; Ruiz, F. Fingerprinting Ceramics from the Chalcolithic Santa Vitória Enclosure (SW Iberia). *Minerals* **2024**, *14*, 399. [https://doi.org/10.3390/min14040399](https://doi.org/10.3390/min14040399)")

# Footer
st.markdown("---")
st.caption("Aplicação Streamlit desenvolvida para a disciplina de Património Cultural e Ciências, baseada no artigo fornecido e nos critérios de avaliação.")