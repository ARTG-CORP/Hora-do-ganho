import requests
import streamlit as st

st.set_page_config(page_title="Top 5 Criptos - Última Hora")
st.title("Top 5 Criptomoedas com Maior Alta na Última Hora")

def calcular_variacao_1h(symbol):
    try:
        url = 'https://api.binance.com/api/v3/klines'
        params = {'symbol': symbol, 'interval': '1h', 'limit': 1}
        response = requests.get(url, params=params)
        data = response.json()

        if not data or isinstance(data, dict):
            return None

        open_price = float(data[0][1])
        close_price = float(data[0][4])
        return ((close_price - open_price) / open_price) * 100
    except:
        return None

def top_5_1h():
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    try:
        data = response.json()
    except:
        return []

    usdt_pairs = []
    for coin in data:
        if isinstance(coin, dict) and 'symbol' in coin:
            if coin['symbol'].endswith('USDT'):
                usdt_pairs.append(coin['symbol'])

    variacoes = []
    with st.spinner("Calculando variações..."):
        for symbol in usdt_pairs:
            variacao = calcular_variacao_1h(symbol)
            if variacao is not None:
                variacoes.append((symbol, variacao))

    top_5 = sorted(variacoes, key=lambda x: x[1], reverse=True)[:5]
    return top_5

if st.button("Atualizar Top 5"):
    top_5 = top_5_1h()
    if top_5:
        st.subheader("Top 5 Criptomoedas da Última Hora:")
        for symbol, variacao in top_5:
            st.write(f"**{symbol}**: {variacao:.2f}%")
    else:
        st.error("Não foi possível obter os dados. Tente novamente mais tarde.")
