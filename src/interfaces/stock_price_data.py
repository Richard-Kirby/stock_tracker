import yfinance as yf


# Manages the ticker data from Yahoo Finance.
class TickerData:
    def __init__(self, symbols):
        self.symbols = symbols

    # Return the ticker data asked for. Returns as a Panda DataFrame, which can then be manipulated as needed.
    def get_ticker(self, period='1d', interval='5m'):
        data = yf.download(self.symbols, period=period, interval=interval)
        print(data)
        return data


if __name__ == '__main__':
    ticker_data = TickerData(['MSFT', 'CSCO',  'GOOG', 'RPI.L'])

    ticker_data_frame = ticker_data.get_ticker()

    rpi_array = ticker_data_frame['Close', 'RPI.L'].to_dict()

    # print(rpi_array)

    for key in rpi_array:
        # print(str(key)[:10], str(key)[11:19], f"{rpi_array[key]:.2f}")
        pass
