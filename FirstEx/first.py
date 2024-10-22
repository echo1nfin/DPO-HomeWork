import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from datetime import datetime, timedelta

def get_values_from_web(date: str = datetime.now().strftime('%d/%m/%Y')):
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    current_date = date
    params = {'date_req': current_date}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'xml')
    
    currencies = soup.find_all('Valute') 
    return currencies

def dict_values_init(date: str = datetime.now().strftime('%d/%m/%Y')):
    currencies = get_values_from_web(date)
    name_value_dict = dict()

    for currency in currencies:
        name = currency.find('Name').text
        nominal = currency.find('Nominal').text
        value = currency.find('Value').text.replace(',', '.')
        name_value_dict[name] = f"{(float(value)/int(nominal)):.4f}"

    return name_value_dict

def show_valutes_name():
    valutes = dict_values_init()
    list_names = [name for name in valutes]
    return list_names

def valute_interval(first_date: str, second_date: str, name: str = "Доллар США"):
    start_date = datetime.strptime(first_date, '%d/%m/%Y')
    end_date = datetime.strptime(second_date, '%d/%m/%Y')
    exchange_rates = {}

    delta = timedelta(days=1)
    while start_date <= end_date:
        date_str = start_date.strftime('%d/%m/%Y')
        rates = dict_values_init(date_str)
        if name in rates:
            exchange_rates[date_str] = float(rates[name])
        start_date += delta

    return exchange_rates

def plot_exchange_rates(rates: dict, valute_name: str):
    dates = list(rates.keys())
    values = list(rates.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.25)
    
    line, = ax.plot(dates, values, marker='o', linestyle='-', color='b')
    ax.set_title(f'Курс {valute_name} за выбранный интервал')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Курс')
    ax.set_xticklabels(dates, rotation=45)
    ax.grid()

    # Создание слайдера
    ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
    slider = Slider(ax_slider, 'Дата', 0, len(dates) - 1, valinit=0, valstep=1)

    # Функция для обновления графика при изменении слайдера
    def update(val):
        idx = int(slider.val)
        ax.set_xlim(idx - 5, idx + 5)  # Показываем 10 точек (5 до и 5 после)
        ax.set_xticks(range(max(0, idx - 5), min(len(dates), idx + 6)))
        ax.set_xticklabels(dates[max(0, idx - 5):min(len(dates), idx + 6)], rotation=45)
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()

def main():
    first_date = "01/08/2024"
    second_date = "10/10/2024"

    #print(show_valutes_name())
    valute_name = "Японских иен"

    rates = valute_interval(first_date, second_date, valute_name)
    
    plot_exchange_rates(rates, valute_name)

if __name__ == "__main__":
    main()