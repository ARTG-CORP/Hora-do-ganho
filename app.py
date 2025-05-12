
import requests
import streamlit as st

st.set_page_config(page_title="Top 5 Criptos - Última Hora")
st.title("Top 5 Criptomoedas com Maior Alta na Última Hora")

def calcular_variacao_1h(symbol):
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': '1h', 'limit': 1}
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or not data:
        return None

    open_price = float(data[0][1])
    close_price = float(data[0][4])
    return ((close_price - open_price) / open_price) * 100

def top_5_1h():
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    data = response.json()

    usdt_pairs = [coin['symbol'] for coin in data if coin['symbol'].endswith('USDT')]
    variacoes = []

    with st.spinner("Calculando variações..."):
        for symbol in usdt_pairs:
            try:
                variacao = calcular_variacao_1h(symbol)
                if variacao is not None:
                    variacoes.append((symbol, variacao))
            except:
                continue

    top_5 = sorted(variacoes, key=lambda x: x[1], reverse=True)[:5]
    return top_5

if st.button("Atualizar Top 5"):
    top_5 = top_5_1h()
    st.subheader("Top 5 Criptomoedas da Última Hora:")
    for symbol, variacao in top_5:
        st.write(f"**{symbol}**: {variacao:.2f}%")
