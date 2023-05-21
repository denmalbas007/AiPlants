import pandas as pd


data = pd.read_excel('Plants.xlsx')


def calc_mean(x):
    try:
        a, b = list(map(int, x[1:].split('-')))
    except Exception:
        return 0
    return (a + b) / 2


data['meantime_plant'] = data['Период посева, мес'].apply(calc_mean)
data['meantime_collect'] = data['Период сбора урожая, мес'].apply(calc_mean)


def get_recs(query):
    top_5 = data[(data['Ареалы произрастания'].str.contains(query)) & (data['Если культура занесена в Красную книгу, то в каком регионе'] == ' -')].sort_values(['Ежегодная потребность лекарственного сырья, тонны', 'meantime_collect', 'meantime_plant'], ascending=False)
    ret = {i: top_5.iloc[i].to_dict() for i in range(min(5, len(top_5)))}
    if len(ret) < 5:
        top_n = data[(data['Ареалы произрастания'].str.contains('Все регионы России')) & (data['Если культура занесена в Красную книгу, то в каком регионе'] == ' -')].sort_values(['Ежегодная потребность лекарственного сырья, тонны', 'meantime_collect', 'meantime_plant'], ascending=False)
        for i in range(len(ret), 5):
            ret[i] = top_n.iloc[i].to_dict()
    return ret
