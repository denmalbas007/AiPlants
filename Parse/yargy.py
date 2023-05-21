import csv


def extract_information(text):
    from yargy import Parser, rule, and_, or_
    from yargy.predicates import gram, normalized, dictionary, custom
    from yargy.interpretation import fact
    from yargy.relations import gnc_relation

    # Создаем факты для извлечения информации
    Plant = fact('Plant', ['name', 'regions', 'soil_type', 'day_length_summer', 'day_length_winter',
                           'day_length_spring', 'day_length_autumn', 'light_days', 'in_pharmacopoeia',
                           'in_red_book', 'red_book_region', 'sowing_period', 'harvest_period',
                           'chemical_composition', 'medicinal_preparations', 'annual_demand'])

    # Создаем правила для извлечения информации
    PlantName = rule(gram('NOUN')).interpretation(Plant.name)
    Regions = rule(gram('NOUN')).interpretation(Plant.regions)
    SoilType = rule(normalized('тип') + normalized('почвы')).interpretation(Plant.soil_type)
    DayLengthSummer = rule(normalized('долгота') + normalized('день') + normalized('лето')).interpretation(Plant.day_length_summer)
    DayLengthWinter = rule(normalized('долгота') + normalized('день') + normalized('зима')).interpretation(Plant.day_length_winter)
    DayLengthSpring = rule(normalized('долгота') + normalized('день') + normalized('весна')).interpretation(Plant.day_length_spring)
    DayLengthAutumn = rule(normalized('долгота') + normalized('день') + normalized('осень')).interpretation(Plant.day_length_autumn)
    LightDays = rule(normalized('количество') + normalized('световой') + normalized('день')).interpretation(Plant.light_days)
    InPharmacopoeia = rule(normalized('входит') + normalized('государственный') + normalized('фармакопея')).interpretation(Plant.in_pharmacopoeia)
    InRedBook = rule(normalized('внесен') + normalized('красный') + normalized('книга')).interpretation(Plant.in_red_book)
    RedBookRegion = rule(normalized('в') + gram('NOUN')).interpretation(Plant.red_book_region)
    SowingPeriod = rule(normalized('период') + normalized('посев')).interpretation(Plant.sowing_period)
    HarvestPeriod = rule(normalized('период') + normalized('сбор')).interpretation(Plant.harvest_period)
    ChemicalComposition = rule(normalized('содержание') + gram('NOUN')).interpretation(Plant.chemical_composition)
    MedicinalPreparations = rule(normalized('медицинский') + normalized('препарат')).interpretation(Plant.medicinal_preparations)
    AnnualDemand = rule(normalized('ежегодный') + normalized('потребность') + gram('NOUN')).interpretation(Plant.annual_demand)

    # Объединяем правила
    pattern = or_(PlantName, Regions, SoilType, DayLengthSummer, DayLengthWinter, DayLengthSpring,
                  DayLengthAutumn, LightDays, InPharmacopoeia, InRedBook, RedBookRegion, SowingPeriod,
                  HarvestPeriod, ChemicalComposition, MedicinalPreparations, AnnualDemand)

    # Создаем парсер
    parser = Parser(pattern)

    # Извлечение информации из текста
    plants = []
    for match in parser.findall(text):
        plant = match.fact
        plants.append(plant)

    # Сгруппировать данные в таблицу CSV
    rows = []
    for plant in plants:
        row = {
            'Название лекарственной культуры': plant.name,
            'Ареалы произрастания': plant.regions,
            'Типы почв, наименование': plant.soil_type,
            'Долгота дня (лето) по региону, ч': plant.day_length_summer,
            'Долгота дня (зима) по региону, ч': plant.day_length_winter,
            'Долгота дня (весна) по региону, ч': plant.day_length_spring,
            'Долгота дня (осень) по региону, ч': plant.day_length_autumn,
            'Кол-во световых дней по региону': plant.light_days,
            'Культура входит в государственную фармакопейю': plant.in_pharmacopoeia,
            'Занесена ли культура в Красную книгу': plant.in_red_book,
            'Если культура занесена в Красную книгу, то в каком регионе': plant.red_book_region,
            'Период посева, мес': plant.sowing_period,
            'Период сбора урожая, мес': plant.harvest_period,
            'Содержание БАВ, хим состав': plant.chemical_composition,
            'В каких медицинских препаратах содержится, наименование': plant.medicinal_preparations,
            'Ежегодная потребность лекарственного сырья, тонны': plant.annual_demand,
        }
        rows.append(row)

    # Записать данные в CSV файл
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
