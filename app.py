# ==============================================================================
# BLOQUE 1: CONFIGURACIÓN Y CARGA DE DATOS
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Crypto Insights Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CÓDIGO DE ESTILO (SIN CAMBIOS) ---
ultimate_contrast_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Roboto+Mono:wght@400;700&display=swap');
html, body, [class*="st-"] { font-family: 'Roboto', sans-serif; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #0E1117; color: #FAFAFA; }
h1, h2, h3, h4, h5, h6 { font-family: 'Roboto', sans-serif; font-weight: 700; color: #FFFFFF !important; }
h1 { color: #00D1B2 !important; text-shadow: 0 0 8px rgba(0, 209, 178, 0.5); }
.stCaption { color: #FFFFFF !important; opacity: 0.8; }
[data-testid="stSidebar"] { background-color: #1A1C23; border-right: 1px solid #2D2D2D; }
[data-testid="stSidebar"] h1 { font-size: 1.8em; color: #FFFFFF !important; text-shadow: none; }
[data-testid="stRadio"] label { display: flex; flex-direction: column; align-items: flex-start; }
[data-testid="stRadio"] label > div:first-of-type { color: #FFFFFF !important; font-size: 1.1em !important; font-weight: 700 !important; margin-bottom: 2px; }
[data-testid="stRadio"] label > div:last-of-type { color: #FFFFFF !important; opacity: 0.7 !important; font-size: 0.9em !important; }
[data-testid="stAlert"] { background-color: #1E1E1E !important; border: 1px solid #00D1B2 !important; border-radius: 10px !important; color: #FFFFFF !important; }
[data-testid="stAlert"] .st-emotion-cache-1wmy9hl { color: #FFFFFF !important; }
[data-testid="stMetric"] { background-color: #1E1E1E; border: 1px solid #2D2D2D; border-radius: 10px; padding: 15px; }
[data-testid="stMetricLabel"] { color: #FFFFFF !important; font-weight: 400 !important; }
[data-testid="stMetricValue"] { font-family: 'Roboto Mono', monospace; font-size: 1.8em; color: #00C853 !important; }
[data-testid="stMetricDelta"] > div[style*="color: rgb(40, 167, 69);"] { color: #00C853 !important; }
[data-testid="stMetricDelta"] > div[style*="color: rgb(220, 53, 69);"] { color: #FF5252 !important; }
[data-testid="stProgressBar"] > div { background-color: #00D1B2; }
.stTabs [data-baseweb="tab-list"] { gap: 24px; }
.stTabs [data-baseweb="tab"] { background-color: #1E1E1E; }
.stTabs [data-baseweb="tab--selected"] { background-color: #00D1B2; color: #0E1117; }
.custom-table-container { background-color: #1E1E1E; border: 1px solid #2D2D2D; border-radius: 10px; padding: 10px; font-family: 'Roboto Mono', monospace; }
.custom-table { width: 100%; border-collapse: collapse; }
.custom-table th { text-align: left; padding: 8px; color: #FFFFFF !important; opacity: 0.7; border-bottom: 1px solid #2D2D2D; font-weight: 400; }
.custom-table td { text-align: left; padding: 8px; vertical-align: middle; }
.positive { color: #00C853; font-weight: 700; }
.negative { color: #FF5252; font-weight: 700; }
.asset-name { font-weight: 700; color: #FAFAFA; }
.progress-bar-container { width: 100%; background-color: #2D2D2D; border-radius: 5px; height: 20px; display: flex; align-items: center; position: relative; }
.progress-bar-fill { background-color: #00D1B2; height: 100%; border-radius: 5px; }
.progress-bar-text { position: absolute; width: 100%; text-align: center; color: #FFFFFF; font-weight: 700; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); }
</style>
"""
st.markdown(ultimate_contrast_css, unsafe_allow_html=True)

# --- PLANTILLA DE DISEÑO PARA GRÁFICOS PLOTLY (CORREGIDA) ---
PLOTLY_DARK_THEME_LAYOUT = {
    'plot_bgcolor': '#1E1E1E',
    'paper_bgcolor': '#0E1117',
    'font': dict(color='#FFFFFF'),
    'title_font_color': '#FFFFFF',
    'xaxis': dict(gridcolor='#2D2D2D', title_font_color='#FFFFFF'),
    'yaxis': dict(gridcolor='#2D2D2D', title_font_color='#FFFFFF'),
    'legend': dict(bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
}

# --- FUNCIONES AUXILIARES ---
def create_movers_table(df, title_emoji, title_text):
    st.markdown(f"<h4>{title_emoji} {title_text}</h4>", unsafe_allow_html=True)
    html = '<div class="custom-table-container"><table class="custom-table"><thead><tr><th>Activo</th><th>Precio</th><th>Cambio 24h</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        change_pct = row['price_change_percentage_24h']
        price = row['current_price']
        color_class = "positive" if change_pct > 0 else "negative"
        html += f"<tr><td class='asset-name'>{row['name']}</td><td>${price:,.4f}</td><td class='{color_class}'>{change_pct:.2f}%</td></tr>"
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

def create_screener_table(df, perf_range):
    st.markdown(f"<h4>Resultados del Screener</h4>", unsafe_allow_html=True)
    html = '<div class="custom-table-container"><table class="custom-table"><thead><tr><th>Activo</th><th>Rank</th><th>Precio</th><th>Rendimiento 24h</th><th>Market Cap</th><th>Volumen 24h</th></tr></thead><tbody>'
    min_val, max_val = perf_range
    range_val = max_val - min_val if (max_val - min_val) != 0 else 1
    for _, row in df.iterrows():
        perf_pct = row['price_change_percentage_24h']
        progress_width = ((perf_pct - min_val) / range_val) * 100
        progress_width = max(0, min(100, progress_width))
        html += f"<tr><td class='asset-name'>{row['name']}</td><td>{row['market_cap_rank']}</td><td>${row['current_price']:,.4f}</td><td><div class='progress-bar-container'><div class='progress-bar-fill' style='width: {progress_width}%;'></div><div class='progress-bar-text'>{perf_pct:.2f}%</div></div></td><td>${int(row['market_cap']):,d}</td><td>${int(row['total_volume']):,d}</td></tr>"
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- FUNCIONES PARA ANÁLISIS HISTÓRICO ---
def plot_normalized_performance(df_filtered):
    df_filtered['normalized_price'] = df_filtered.groupby('name')['current_price'].transform(lambda x: (x / x.iloc[0]) * 100)
    fig = px.line(df_filtered, x='fecha_captura', y='normalized_price', color='name', labels={'normalized_price': 'Crecimiento Normalizado (%)', 'fecha_captura': 'Fecha', 'name': 'Activo'}, hover_data={'current_price': ':.2f'})
    fig.update_layout(**PLOTLY_DARK_THEME_LAYOUT, title_text='Rendimiento Comparativo Normalizado (Base 100)')
    st.plotly_chart(fig, use_container_width=True)

def plot_market_dominance(df_filtered):
    total_market_cap_df = df_filtered.groupby('fecha_captura')['market_cap'].sum().reset_index().rename(columns={'market_cap': 'total_market_cap'})
    df_dominance = pd.merge(df_filtered, total_market_cap_df, on='fecha_captura')
    df_dominance['dominance_%'] = (df_dominance['market_cap'] / df_dominance['total_market_cap']) * 100
    fig = px.area(df_dominance, x='fecha_captura', y='dominance_%', color='name', labels={'dominance_%': 'Dominancia (%)', 'fecha_captura': 'Fecha', 'name': 'Activo'}, hover_data={'market_cap': ':.2f'})
    fig.update_layout(**PLOTLY_DARK_THEME_LAYOUT, title_text='Dominancia de Mercado (%)')
    st.plotly_chart(fig, use_container_width=True)

def plot_technical_analysis(df_coin):
    df_coin['sma_20'] = df_coin['current_price'].rolling(window=20).mean()
    df_coin['sma_50'] = df_coin['current_price'].rolling(window=50).mean()
    std_dev = df_coin['current_price'].rolling(window=20).std()
    df_coin['bb_upper'] = df_coin['sma_20'] + (std_dev * 2)
    df_coin['bb_lower'] = df_coin['sma_20'] - (std_dev * 2)
    delta = df_coin['current_price'].diff(1)
    gain = delta.where(delta > 0, 0); loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean(); avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df_coin['rsi'] = 100 - (100 / (1 + rs))
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.6, 0.2, 0.2])
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['current_price'], name='Precio', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['bb_upper'], name='Banda Sup.', line=dict(width=1, dash='dash', color='gray')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['bb_lower'], name='Banda Inf.', line=dict(width=1, dash='dash', color='gray'), fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['sma_20'], name='SMA 20', line=dict(color='orange', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['sma_50'], name='SMA 50', line=dict(color='purple', width=1.5)), row=1, col=1)
    fig.add_trace(go.Bar(x=df_coin['fecha_captura'], y=df_coin['total_volume'], name='Volumen', marker_color='rgba(0, 209, 178, 0.5)'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_coin['fecha_captura'], y=df_coin['rsi'], name='RSI', line=dict(color='#00D1B2')), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1); fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    fig.update_layout(**PLOTLY_DARK_THEME_LAYOUT, title_text=f'Análisis Técnico para {df_coin["name"].iloc[0]}', xaxis_rangeslider_visible=False)
    fig.update_yaxes(title_text="Precio (USD)", row=1, col=1); fig.update_yaxes(title_text="Volumen", row=2, col=1); fig.update_yaxes(title_text="RSI", row=3, col=1)
    st.plotly_chart(fig, use_container_width=True)

# --- Carga de Datos ---
@st.cache_data(ttl="1h")
def load_and_preprocess_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"🔴 Error Crítico: No se pudo encontrar el archivo de datos '{file_path}'. Asegúrate de que está en la misma carpeta que tu script .py.")
        return None
    df['fecha_captura'] = pd.to_datetime(df['fecha_captura'])
    df = df.sort_values(['id', 'fecha_captura'])
    for p in [1, 7, 30]:
        if len(df['fecha_captura'].unique()) > p:
            df[f'cambio_pct_{p}d'] = df.groupby('id')['current_price'].transform(lambda x: x.pct_change(periods=p) * 100)
    df['rango_pct'] = ((df['high_24h'] - df['low_24h']) / df['low_24h']) * 100
    df['rango_pct'] = df['rango_pct'].fillna(0)
    return df

df_historico = load_and_preprocess_data('historico_criptos.csv')
if df_historico is None: st.stop()
FECHA_ACTUALIZACION = df_historico['fecha_captura'].max()
df_actual = df_historico[df_historico['fecha_captura'] == FECHA_ACTUALIZACION].copy()
top10 = df_actual[df_actual['market_cap_rank'] <= 10]
titanes = top10[top10['market_cap_rank'] <= 2]
grandes_proyectos = top10[(top10['market_cap_rank'] > 2) & (top10['market_cap_rank'] <= 10)]
altcoins_activas = df_actual[(df_actual['market_cap_rank'] > 10) & (df_actual['market_cap_rank'] <= 100)]
baja_liquidez = df_actual[df_actual['market_cap_rank'] > 100]

# ==============================================================================
# BLOQUE 2: LAYOUT PRINCIPAL Y NAVEGACIÓN
# ==============================================================================

st.title("⚡ Crypto Insights Terminal")
st.caption(f"Última sincronización de datos: {FECHA_ACTUALIZACION.strftime('%Y-%m-%d %H:%M:%S')}")

st.sidebar.title("Panel de Navegación")
st.sidebar.markdown("---")
herramienta_seleccionada = st.sidebar.radio(
    "Selecciona una herramienta: 🔍",
    ["Resumen del Mercado", "Análisis de Segmentos", "Explorador de Activos", "Screener de Mercado", "Análisis Histórico Avanzado"],
    captions=["Vista general", "Análisis por grupos", "Investigación profunda", "Búsqueda personalizada", "Tendencias y TA"]
)
st.sidebar.markdown("---")
st.sidebar.info("Este dashboard es una herramienta de análisis. Realiza tu propia investigación antes de invertir.")

# ==============================================================================
# BLOQUE 3: HERRAMIENTAS DEL DASHBOARD
# ==============================================================================

if herramienta_seleccionada == "Resumen del Mercado":
    # ... (CÓDIGO SIN CAMBIOS)
    st.header("📈 Resumen del Mercado Hoy")
    market_cap_total = df_actual['market_cap'].sum()
    volumen_total = df_actual['total_volume'].sum()
    btc_dominance_actual = (df_actual.loc[df_actual['id'] == 'bitcoin', 'market_cap'].iloc[0] / market_cap_total) * 100
    fecha_ayer = FECHA_ACTUALIZACION - pd.Timedelta(days=1)
    mc_delta, btc_dominance_delta = None, None
    if fecha_ayer in df_historico['fecha_captura'].values:
        df_ayer = df_historico[df_historico['fecha_captura'] == fecha_ayer]
        market_cap_ayer = df_ayer['market_cap'].sum()
        if market_cap_ayer > 0:
            mc_delta = ((market_cap_total - market_cap_ayer) / market_cap_ayer) * 100
            btc_market_cap_ayer = df_ayer.loc[df_ayer['id'] == 'bitcoin', 'market_cap'].iloc[0]
            btc_dominance_ayer = (btc_market_cap_ayer / market_cap_ayer) * 100
            btc_dominance_delta = btc_dominance_actual - btc_dominance_ayer
    col1, col2, col3 = st.columns(3)
    col1.metric("Capitalización Total", f"${market_cap_total/1e12:.2f}T", delta=f"{mc_delta:.2f}%" if mc_delta is not None else "N/A")
    col2.metric("Volumen Total (24h)", f"${volumen_total/1e9:.2f}B")
    col3.metric("Dominancia BTC", f"{btc_dominance_actual:.2f}%", delta=f"{btc_dominance_delta:.2f}%" if btc_dominance_delta is not None else None)
    st.markdown("---")
    st.subheader("🌡️ Diagnóstico de Flujo de Mercado")
    monedas_al_alza = df_actual[df_actual['price_change_percentage_24h'] > 0].shape[0]
    total_monedas = len(df_actual)
    porcentaje_alza = (monedas_al_alza / total_monedas)
    diagnostico_texto, diagnostico_emoji = "", ""
    if btc_dominance_delta is not None:
        if porcentaje_alza > 0.55:
            diagnostico_texto, diagnostico_emoji = ("Apetito por el Riesgo (Altcoins)", "🤑") if btc_dominance_delta < -0.1 else ("Rally Generalizado", "📈")
        elif porcentaje_alza < 0.45:
            diagnostico_texto, diagnostico_emoji = ("Aversión al Riesgo (Refugio en BTC)", "😨") if btc_dominance_delta > 0.1 else ("Salida General de Capital", "🚨")
        else:
            diagnostico_texto, diagnostico_emoji = "Mercado Indeciso / Mixto", "🤔"
    else:
        diagnostico_texto, diagnostico_emoji = "Datos insuficientes", "⏳"
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.markdown("**Diagnóstico:**")
        st.markdown(f"## {diagnostico_emoji} {diagnostico_texto}")
    with col2:
        st.markdown("**Amplitud del Mercado (24h):**")
        st.progress(porcentaje_alza)
        st.markdown(f"<span style='color:#00C853'>🟢 Al Alza: {monedas_al_alza} ({porcentaje_alza:.1%})</span>", unsafe_allow_html=True)
    st.caption("Metodología: Este diagnóstico combina la Amplitud del Mercado (activos al alza vs. baja) con la Tendencia de la Dominancia de Bitcoin.")
    st.markdown("---")
    st.subheader("Mayores Movimientos del Día")
    ganadores = df_actual.sort_values('price_change_percentage_24h', ascending=False).head(10)
    perdedores = df_actual.sort_values('price_change_percentage_24h', ascending=True).head(10)
    col1, col2 = st.columns(2)
    with col1:
        create_movers_table(ganadores, "🏆", "Top 10 Ganadores (24h)")
    with col2:
        create_movers_table(perdedores, "💔", "Top 10 Perdedores (24h)")

elif herramienta_seleccionada == "Análisis de Segmentos":
    # ... (CÓDIGO SIN CAMBIOS)
    st.header("🔬 Análisis de Segmentos de Mercado")
    segmento_elegido = st.selectbox("Selecciona un segmento:", ["Titanes y Grandes Proyectos (Top 10)", "Altcoins Activas (11-100)", "Gemas y Activos de Baja Liquidez (>100)"])
    if segmento_elegido == "Titanes y Grandes Proyectos (Top 10)":
        st.subheader("👑 Titanes vs. 🚀 Grandes Proyectos")
        col1, col2 = st.columns(2)
        with col1:
            fig_pie_titanes = px.pie(titanes, values='market_cap', names='name', title='Dominancia de Titanes (BTC & ETH)', hole=.3)
            fig_pie_titanes.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            st.plotly_chart(fig_pie_titanes, use_container_width=True)
        with col2:
            fig_treemap_gp = px.treemap(grandes_proyectos, path=['name'], values='market_cap', title='Market Cap en Grandes Proyectos (3-10)', color='market_cap', color_continuous_scale='Blues')
            fig_treemap_gp.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            st.plotly_chart(fig_treemap_gp, use_container_width=True)
    elif segmento_elegido == "Altcoins Activas (11-100)":
        st.subheader("Altcoins Activas (Rango 11-100)")
        altcoins_activas_plot = altcoins_activas.dropna(subset=['price_change_percentage_24h', 'market_cap', 'total_volume'])
        if not altcoins_activas_plot.empty:
            fig_alt = px.scatter(altcoins_activas_plot, x='price_change_percentage_24h', y='market_cap', size='total_volume', color='market_cap', hover_name='name', log_y=True, size_max=60, labels={"price_change_percentage_24h": "Rendimiento 24h (%)", "market_cap": "Market Cap (USD)"}, title="Rendimiento vs. Market Cap en Altcoins Activas", color_continuous_scale=px.colors.sequential.Viridis)
            fig_alt.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            st.plotly_chart(fig_alt, use_container_width=True)
    elif segmento_elegido == "Gemas y Activos de Baja Liquidez (>100)":
        st.subheader("Gemas y Activos de Baja Liquidez (Rank > 100)")
        st.warning("⚠️ Zona de Alto Riesgo: Estos activos pueden tener volatilidad extrema y baja liquidez.")
        baja_liquidez_plot = baja_liquidez.dropna(subset=['total_volume', 'market_cap', 'rango_pct'])
        if not baja_liquidez_plot.empty:
            fig_bl = px.scatter(baja_liquidez_plot, x='total_volume', y='market_cap', color='rango_pct', hover_name='name', log_x=True, log_y=True, size_max=40, labels={"total_volume": "Volumen 24h (USD)", "market_cap": "Market Cap (USD)", "rango_pct": "Volatilidad 24h (%)"}, title="Análisis de Riesgo: Market Cap vs. Volumen", color_continuous_scale=px.colors.sequential.Inferno)
            fig_bl.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            st.plotly_chart(fig_bl, use_container_width=True)
            
elif herramienta_seleccionada == "Explorador de Activos":
    # ... (CÓDIGO SIN CAMBIOS)
    st.header("🔍 Explorador de Activos")
    monedas = st.multiselect("Selecciona monedas:", sorted(df_actual['name'].unique()), default=["Bitcoin", "Ethereum", "Solana"])
    if monedas:
        df_explor = df_actual[df_actual['name'].isin(monedas)]
        df_explor_hist = df_historico[df_historico['name'].isin(monedas)]
        tab1, tab2, tab3 = st.tabs(["Resumen", "Comparativa", "Histórico"])
        with tab1:
            for moneda in monedas:
                d = df_explor[df_explor['name'] == moneda].iloc[0]
                st.subheader(f"💎 {moneda}")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Precio Actual", f"${d['current_price']:,.4f}", f"{d.get('price_change_percentage_24h', 0):.2f}%")
                col2.metric("Market Cap", f"${d['market_cap']/1e9:.2f}B")
                fdv_ratio = (d['market_cap'] / d['fully_diluted_valuation']) if pd.notna(d['fully_diluted_valuation']) and d['fully_diluted_valuation'] > 0 else "N/A"
                col3.metric("Ratio MC/FDV", f"{fdv_ratio:.2%}" if isinstance(fdv_ratio, float) else "N/A")
                col4.metric("Volatilidad 24h", f"{d.get('rango_pct', 0):.2f}%")
        with tab2:
            metricas_comparables = {"Capitalización de Mercado": "market_cap", "Volumen 24h": "total_volume", "Volatilidad 24h (%)": "rango_pct", "Cambio 24h (%)": "price_change_percentage_24h"}
            metrica_seleccionada = st.selectbox("Selecciona una métrica para comparar:", options=list(metricas_comparables.keys()))
            col_seleccionada = metricas_comparables[metrica_seleccionada]
            df_explor_sorted = df_explor.sort_values(by=col_seleccionada, ascending=False)
            fig_bar_comp = px.bar(df_explor_sorted, x='name', y=col_seleccionada, color='name', title=f"Comparativa de '{metrica_seleccionada}'", text=col_seleccionada)
            fig_bar_comp.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            fig_bar_comp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            st.plotly_chart(fig_bar_comp, use_container_width=True)
        with tab3:
            add_sma = st.checkbox("Añadir Medias Móviles (SMA 7 y 30 días)")
            fig_hist = px.line(df_explor_hist, x='fecha_captura', y='current_price', color='name', title="Evolución de Precio Histórico")
            fig_hist.update_layout(**PLOTLY_DARK_THEME_LAYOUT)
            if add_sma:
                for moneda in monedas:
                    df_m = df_explor_hist[df_explor_hist['name'] == moneda].copy()
                    df_m['SMA7'] = df_m['current_price'].rolling(7).mean()
                    df_m['SMA30'] = df_m['current_price'].rolling(30).mean()
                    fig_hist.add_trace(go.Scatter(x=df_m['fecha_captura'], y=df_m['SMA7'], mode='lines', name=f"{moneda} SMA7", line=dict(dash='dot')))
                    fig_hist.add_trace(go.Scatter(x=df_m['fecha_captura'], y=df_m['SMA30'], mode='lines', name=f"{moneda} SMA30", line=dict(dash='dash')))
            st.plotly_chart(fig_hist, use_container_width=True)
            
elif herramienta_seleccionada == "Screener de Mercado":
    # ... (CÓDIGO SIN CAMBIOS)
    st.header("🛠️ Screener de Mercado")
    df_screener = df_actual.copy()
    col1, col2, col3 = st.columns(3)
    with col1:
        mc_max_log = np.log10(df_screener['market_cap'].max())
        mc_range = st.slider("Rango de Market Cap (USD):", 0.0, mc_max_log, (6.0, 9.0), format="10^%f")
        min_mc, max_mc = 10**mc_range[0], 10**mc_range[1]
        df_screener = df_screener[(df_screener['market_cap'] >= min_mc) & (df_screener['market_cap'] <= max_mc)]
    with col2:
        vol_max_log = np.log10(df_screener['total_volume'].replace(0, 1).max())
        vol_range = st.slider("Rango de Volumen 24h (USD):", 0.0, vol_max_log, (5.0, 8.0), format="10^%f")
        min_vol, max_vol = 10**vol_range[0], 10**vol_range[1]
        df_screener = df_screener[(df_screener['total_volume'] >= min_vol) & (df_screener['total_volume'] <= max_vol)]
    with col3:
        min_perf, max_perf = df_screener['price_change_percentage_24h'].min(), df_screener['price_change_percentage_24h'].max()
        if pd.isna(min_perf) or pd.isna(max_perf): min_perf, max_perf = -10.0, 10.0
        perf_range = st.slider("Rango de Rendimiento 24h (%):", min_perf, max_perf, (-5.0, 5.0), 0.5)
        df_screener = df_screener[(df_screener['price_change_percentage_24h'] >= perf_range[0]) & (df_screener['price_change_percentage_24h'] <= perf_range[1])]
    if not df_screener.empty:
        create_screener_table(df_screener, perf_range)
    else:
        st.warning("Ningún activo coincide con los filtros seleccionados. Intenta ampliarlos.")

# ------------------------ SECCIÓN DE ANÁLISIS HISTÓRICO (REDISEÑADA Y CORREGIDA) ---------------------------
elif herramienta_seleccionada == "Análisis Histórico Avanzado":
    st.header("🔬 Análisis Histórico Avanzado")
    st.sidebar.subheader("Filtros de Análisis Histórico")
    
    # --- FILTROS CENTRALIZADOS EN EL SIDEBAR ---
    all_coins = sorted(df_historico['name'].unique())
    default_coins = ['Bitcoin', 'Ethereum', 'Solana', 'BNB', 'XRP']
    selected_coins = st.sidebar.multiselect(
        "Selecciona activos:", 
        all_coins, 
        default=[c for c in default_coins if c in all_coins]
    )

    min_date, max_date = df_historico['fecha_captura'].min().date(), df_historico['fecha_captura'].max().date()
    if min_date >= max_date:
        st.sidebar.warning("Se necesita más de un día de datos para usar el filtro de fechas.")
        date_range = (min_date, max_date)
    else:
        date_range = st.sidebar.date_input(
            "Selecciona un rango de fechas:", 
            value=(min_date, max_date), 
            min_value=min_date, 
            max_value=max_date
        )

    # --- VALIDACIÓN Y FILTRADO ÚNICO ---
    if not selected_coins or len(date_range) != 2:
        st.warning("Por favor, selecciona al menos un activo y un rango de fechas válido en el panel lateral.")
        st.stop()

    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]).replace(hour=23, minute=59, second=59)
    df_filtered = df_historico[(df_historico['name'].isin(selected_coins)) & (df_historico['fecha_captura'].between(start_date, end_date))]

    if df_filtered.empty:
        st.warning("No se encontraron datos para la selección actual.")
        st.stop()

    # --- PESTAÑAS REACTIVAS A LOS FILTROS DEL SIDEBAR ---
    tab1, tab2, tab3 = st.tabs(["📊 Rendimiento Comparativo", "👑 Dominancia de Mercado", "📈 Análisis Técnico Individual"])

    with tab1:
        st.info("Este gráfico normaliza el precio de todos los activos a una base de 100 en la fecha de inicio para comparar su rendimiento relativo de forma justa.")
        plot_normalized_performance(df_filtered)
    
    with tab2:
        st.info("Este gráfico muestra la cuota de mercado (capitalización) de cada activo como un porcentaje del total de los activos seleccionados.")
        plot_market_dominance(df_filtered)

    with tab3:
        st.info("Selecciona un único activo (de los ya filtrados) para ver un análisis técnico detallado.")
        coin_for_ta = st.selectbox(
            "Selecciona un activo para análisis técnico:", 
            options=selected_coins # El selector solo muestra las monedas ya elegidas
        )
        if coin_for_ta:
            # Para el TA, usamos el historial completo de la moneda para calcular bien los indicadores, y luego filtramos por fecha.
            df_coin_full_history = df_historico[df_historico['name'] == coin_for_ta]
            df_coin_filtered_for_ta = df_coin_full_history[df_coin_full_history['fecha_captura'].between(start_date, end_date)]
            if not df_coin_filtered_for_ta.empty:
                plot_technical_analysis(df_coin_filtered_for_ta)
            else:
                st.warning("No se encontraron datos para este activo en el rango de fechas seleccionado.")