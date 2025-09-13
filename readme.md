<div align="center">
<p>
  <strong>English</strong> | <a href="readme_ES.md">Español</a>
</p>
</div>

<div align="center">

  <!-- You can replace the emoji with a link to your own logo image if you create one -->
  <h1>⚡ Crypto Insights Terminal ⚡</h1>
  
  <p>
    <strong>A professional-grade, interactive dashboard for historical and daily analysis of the cryptocurrency market, featuring fully automated data updates.</strong>
  </p>
  
  <br>
  
  <p>
    <!-- Dynamic Badges with your actual repo links -->
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/stargazers"><img src="https://img.shields.io/github/stars/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&color=00D1B2&logoColor=white&label=STARS"></a>
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/network/members"><img src="https://img.shields.io/github/forks/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&color=00D1B2&logoColor=white&label=FORKS"></a>
    <a href="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/issues"><img src="https://img.shields.io/github/issues/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool?style=for-the-badge&logo=github&label=ISSUES"></a>
  </p>
  
  <p>
    <!-- Direct link to your deployed Streamlit app -->
    <a href="https://crypto-market-analysis-tool.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
  </p>

</div>

---

### 🖼️ Dashboard Preview

A live, interactive terminal designed for clarity and focus. The dark theme is inspired by professional trading interfaces, ensuring that the data and visualizations are always the center of attention.

<!-- A GIF IS HIGHLY RECOMMENDED HERE FOR MAXIMUM IMPACT! -->
<p align="center">
  <img src="https://github.com/rafael-sosa-ramirez/Crypto-Market-Analysis-Tool/blob/main/assets/Dashboard_1.png" width="850">
</p>

---

## 🚀 What is Crypto Insights Terminal?

**Crypto Insights Terminal** is a web application that provides a comprehensive suite of data analysis tools for the cryptocurrency market. The dashboard automatically updates its data every day, ensuring you always have the latest information to identify trends, analyze historical performance, and discover new investment opportunities.

This project was built with the goal of offering a high-quality user experience, replicating the feel of a professional trading terminal while remaining accessible to everyone.

---

## ⚙️ Architecture & Automated Workflow

The system is engineered with two primary components that work in synergy:

### 1. **Automated Data Collection (Backend)**
*   **Data Source:** Daily API calls are made to the public **[CoinGecko API](https://www.coingecko.com/en/api)** to fetch a complete market snapshot.
*   **Process:** A Python script (`actualizar_datos.py`) is executed automatically every 24 hours by a **[GitHub Actions](https://github.com/features/actions)** workflow.
*   **Storage:** The data collected each day is **appended** to the `historico_criptos.csv` file. This file acts as a simple, evolving database, accumulating a rich historical record over time.

### 2. **Interactive Visualization (Frontend)**
*   **Framework:** The user interface is built with **[Streamlit](https://streamlit.io/)**, enabling rapid development and a rich, interactive user experience.
*   **Data Reading:** The application (`app.py`), deployed on Streamlit Community Cloud, reads the `historico_criptos.csv` file directly from the repository.
*   **Live Updates:** Since the app is linked to the GitHub repo, every time the GitHub Actions workflow pushes an updated CSV, Streamlit automatically reboots the application, loading and displaying the freshest data.

---

## ✨ Core Features

The `app.py` application processes the entire historical dataset to offer the following analysis tools:

*   📈 **Market Summary:** Get a 360° view of the market's current state with global metrics, a unique Market Flow diagnosis, and daily Top 10 movers.
*   🔬 **Segment Analysis:** Visually compare the behavior of different crypto asset groups (Titans, Active Altcoins, Low-Liquidity Gems) to identify trends and risks.
*   🔍 **Asset Explorer:** Dive deep into specific cryptocurrencies. Analyze historical price evolution, compare key metrics against other assets, and apply technical indicators like SMAs.
*   🛠️ **Market Screener:** A powerful tool to filter the entire market based on your custom criteria, including Market Cap, 24h Volume, and Performance.

---

## 🛠️ Tech Stack

*   **Language:** [Python 3](https://www.python.org/)
*   **Automation:** [GitHub Actions](https://github.com/features/actions)
*   **Data Collection:** [CoinGecko API](https://www.coingecko.com/en/api)
*   **Data Analysis:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
*   **Frontend & Visualization:** [Streamlit](https://streamlit.io/) & [Plotly](https://plotly.com/python/)

---

## ⚠️ Important Disclaimer

> **This project was created for educational and demonstration purposes only.**
>
> The information presented in this dashboard **does NOT constitute financial, investment, trading, or any other sort of advice**. You should not treat any of the application's content as such.
>
> The author does not recommend that any cryptocurrency should be bought, sold, or held by you. Always conduct your own research (**Do Your Own Research - DYOR**) and consult a professional financial advisor before making any investment decisions.
>
> The author is not responsible for any investment losses you may incur from using or relying on the provided information. Data, sourced from the CoinGecko API, may contain delays or inaccuracies.

---

## 🚀 Get Started

The application is deployed and publicly accessible via Streamlit Community Cloud.


**[➡️ Launch the Crypto Insights Terminal](https://crypto-market-analysis-tool.streamlit.app/)**
