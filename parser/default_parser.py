from collections import namedtuple
from typing import List

import openpyxl

from .IParser import IParser

data_row = namedtuple('DataRow', ['company', 'date', 'fact_qliq', 'fact_qoil', 'forecast_qliq', 'forecast_qoil'])


class DefaultParser(IParser):
    def go_parse(self) -> List[namedtuple]:
        wb = openpyxl.open(self.filename)
        ws = wb.get_sheet_by_name(self.sheetname)

        # Получаем уникальные даты
        dates = self.get_dates(ws)

        # Последовательность полей
        fields = ('fact_qliq', 'fact_qoil', 'forecast_qliq', 'forecast_qoil')

        # Так как одна строка в эксель преобразуется в n строк бд, где n - число дат, создаем сразу n записей,
        # после записываем их в общий список data_ready, преобразовывая в namedtuple
        data_ready = []
        for row in list(ws.values)[3:]:
            company = row[1]

            col = 2
            batch = {date: dict() for date in dates}
            for field in fields:
                for date in dates:
                    batch[date][field] = row[col]
                    col += 1

            data_ready += [data_row(company, date, **fields_data) for date, fields_data in batch.items()]
        wb.close()

        return data_ready

    @staticmethod
    def get_dates(ws) -> List[str]:
        dates = []
        col = 3
        while True:
            date = ws.cell(3, col).value
            if date in dates:
                break
            dates.append(date)
            col += 1

        return dates
