import pandas as pd


my_num = 10.12
f'${my_num:,.2f}'

s = df.style.format({
    'Reservation Price':"${:,.2f}"
})
s

df = pd.DataFrame()


def set_color_to_white_on_black_centered(value):
    return 'color: white; background-color: black; text-align: center'

df.style.applymap(set_color_to_white_on_black_centered)