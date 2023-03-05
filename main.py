"""
Создать парсер excel файла (во вложении) на Python.

Создать таблицу согласно нормам реляционных баз данных (внести все значения в одну таблицу)
Добавить расчетный тотал по Qoil, Qliq, сгруппированный по датам (даты можете указать свои, добавив программно, не изменяя исходный файл, при условии, что дни будут разные, а месяц и год одинаковые)
"""

from parser import DefaultParser
from db_interface import SqLite

if __name__ == '__main__':
    excel_data = DefaultParser(filename='Приложение_к_заданию_бек_разработчика.xlsx', sheetname='Лист1').go_parse()

    # Генерируем скрипт загрузки данных
    data_load_script = 'insert into common_table ("data", company, fact_qliq, fact_qoil, forecast_qliq, forecast_qoil)  values ' + ','.join([f"('{row.date}', '{row.company}', {row.fact_qliq}, {row.fact_qoil}, {row.forecast_qliq}, {row.forecast_qoil})" for row in excel_data])

    with SqLite(db_name='simple.db') as db:
        # Создаем новую таблицу
        db.create_table(drop_if_exists=True)

        # Наполняем ее данными
        db.execute(data_load_script)

        # Создаем вью со сводной таблицей
        db.create_view()

        # Коммитим
        db.commit()
