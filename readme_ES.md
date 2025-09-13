<div align="center">
<p>
  <a href="README.md">English</a> | <strong>Español</strong>
</p>
</div>

<div align="center">

  <!-- Puedes reemplazar el emoji con un enlace a tu propio logo si creas uno -->
  <h1>⚡ Terminal de Criptoanálisis ⚡</h1>
  
  <p>
    <strong>Un dashboard interactivo de nivel profesional para el análisis histórico y diario del mercado de criptomonedas, con actualizaciones de datos totalmente automatizadas.</strong>
  </p>
  
  <br>
  
  <p>
    <!-- Insignias dinámicas con los enlaces reales de tu repositorio -->
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/stargazers"><img src="https://img.shields.io/github/stars/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&color=00D1B2&logoColor=white&label=STARS"></a>
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/network/members"><img src="https://img.shields.io/github/forks/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&color=00D1B2&logoColor=white&label=FORKS"></a>
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/issues"><img src="https://img.shields.io/github/issues/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&label=ISSUES"></a>
  </p>
  
  <p>
    <!-- Enlace directo a tu aplicación desplegada en Streamlit -->
    <a href="https://crypto-market-analysis-tool.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
  </p>

</div>

---

### 🖼️ Vista Previa del Dashboard

Un terminal interactivo y en vivo diseñado para la claridad y el enfoque. El tema oscuro está inspirado en las interfaces de trading profesional, asegurando que los datos y las visualizaciones sean siempre el centro de atención.

<!-- ¡UN GIF ES ALTAMENTE RECOMENDADO AQUÍ PARA UN MÁXIMO IMPACTO! -->
<p align="center">
  <img src="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/blob/main/assets/Dashboard_1.png" width="850">
</p>

---

## 🚀 ¿Qué es el Terminal de Criptoanálisis?

**Terminal de Criptoanálisis** es una aplicación web que proporciona un conjunto completo de herramientas de análisis de datos para el mercado de criptomonedas. El dashboard actualiza sus datos automáticamente cada día, garantizando que siempre tengas la información más reciente para identificar tendencias, analizar el rendimiento histórico y descubrir nuevas oportunidades de inversión.

Este proyecto fue construido con el objetivo de ofrecer una experiencia de usuario de alta calidad, replicando la sensación de un terminal de trading profesional sin dejar de ser accesible para todos.

---

## ⚙️ Arquitectura y Flujo de Trabajo Automatizado

El sistema está diseñado con dos componentes principales que trabajan en sinergia:

### 1. **Recopilación Automatizada de Datos (Backend)**
*   **Fuente de Datos:** Se realizan llamadas diarias a la **[API pública de CoinGecko](https://www.coingecko.com/es/api)** para obtener una instantánea completa del mercado.
*   **Proceso:** Un script de Python (`actualizar_datos.py`) se ejecuta automáticamente cada 24 horas mediante un flujo de trabajo de **[GitHub Actions](https://github.com/features/actions)**.
*   **Almacenamiento:** Los datos recopilados cada día se **añaden** al archivo `historico_criptos.csv`. Este archivo actúa como una base de datos simple y evolutiva, acumulando un rico registro histórico a lo largo del tiempo.

### 2. **Visualización Interactiva (Frontend)**
*   **Framework:** La interfaz de usuario está construida con **[Streamlit](https://streamlit.io/)**, lo que permite un desarrollo rápido y una experiencia de usuario rica e interactiva.
*   **Lectura de Datos:** La aplicación (`app.py`), desplegada en Streamlit Community Cloud, lee el archivo `historico_criptos.csv` directamente desde el repositorio.
*   **Actualizaciones en Vivo:** Dado que la aplicación está vinculada al repositorio de GitHub, cada vez que el flujo de trabajo de GitHub Actions sube un CSV actualizado, Streamlit reinicia automáticamente la aplicación, cargando y mostrando los datos más recientes.

---

## ✨ Características Principales

La aplicación `app.py` procesa todo el conjunto de datos históricos para ofrecer las siguientes herramientas de análisis:

*   📈 **Resumen del Mercado:** Obtén una visión de 360° del estado actual del mercado con métricas globales, un diagnóstico único de Flujo de Mercado y los Top 10 movimientos diarios.
*   🔬 **Análisis de Segmentos:** Compara visualmente el comportamiento de diferentes grupos de criptoactivos (Titanes, Altcoins Activas, Joyas de Baja Liquidez) para identificar tendencias y riesgos.
*   🔍 **Explorador de Activos:** Profundiza en criptomonedas específicas. Analiza la evolución histórica de precios, compara métricas clave con otros activos y aplica indicadores técnicos como las SMAs.
*   🛠️ **Filtro de Mercado (Screener):** Una potente herramienta para filtrar todo el mercado según tus criterios personalizados, incluyendo capitalización de mercado, volumen en 24h y rendimiento.

---

## 🛠️ Tecnologías Utilizadas (Tech Stack)

*   **Lenguaje:** [Python 3](https://www.python.org/)
*   **Automatización:** [GitHub Actions](https://github.com/features/actions)
*   **Recopilación de Datos:** [API de CoinGecko](https://www.coingecko.com/es/api)
*   **Análisis de Datos:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
*   **Frontend y Visualización:** [Streamlit](https://streamlit.io/) & [Plotly](https://plotly.com/python/)

---

## ⚠️ Descargo de Responsabilidad Importante

> **Este proyecto fue creado únicamente con fines educativos y de demostración.**
>
> La información presentada en este dashboard **NO constituye asesoramiento financiero, de inversión, de trading o de cualquier otro tipo**. No debes tratar ningún contenido de la aplicación como tal.
>
> El autor no recomienda la compra, venta o tenencia de ninguna criptomoneda. Realiza siempre tu propia investigación (**Do Your Own Research - DYOR**) y consulta a un asesor financiero profesional antes de tomar cualquier decisión de inversión.
>
> El autor no se hace responsable de las pérdidas de inversión en las que puedas incurrir por usar o basarte en la información proporcionada. Los datos, obtenidos de la API de CoinGecko, pueden contener retrasos o inexactitudes.

---

## 🚀 Cómo Empezar

La aplicación está desplegada y es de acceso público a través de Streamlit Community Cloud.

**[➡️ Iniciar el Terminal de Criptoanálisis](https://crypto-market-analysis-tool.streamlit.app/)**