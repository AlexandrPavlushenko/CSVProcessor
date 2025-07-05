import csv
from tabulate import tabulate


class CSVProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._read_csv()

    def _read_csv(self):
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def filter_data(self, condition):
        if not condition:
            return self.data

        column, operator, value = self._parse_condition(condition)
        filtered = []

        for row in self.data:
            row_value = row[column]
            if self._compare(row_value, operator, value):
                filtered.append(row)

        return filtered

    def aggregate(self, column, operation):
        if not column or not operation:
            return None

        numeric_values = []
        for row in self.data:
            try:
                num = float(row[column])
                numeric_values.append(num)
            except (ValueError, KeyError):
                continue

        if not numeric_values:
            return None

        if operation == 'avg':
            return sum(numeric_values) / len(numeric_values)
        elif operation == 'min':
            return min(numeric_values)
        elif operation == 'max':
            return max(numeric_values)
        else:
            raise ValueError(f"Неизвестная операция: {operation}")

    def sort_data(self, data, column, direction='asc'):
        if not column or not data:
            return data

        reverse = direction.lower() == 'desc'

        def sort_key(item):
            value = item[column]
            try:
                return float(value)
            except ValueError:
                return value

        return sorted(
            data,
            key=sort_key,
            reverse=reverse
        )

    def _parse_condition(self, condition):
        operators = ['>=', '<=', '!=', '>', '<', '=']
        for op in operators:
            if op in condition:
                column, value = condition.split(op)
                return column.strip(), op, value.strip()
        raise ValueError(f"Неверный формат условия: {condition}")

    def _compare(self, row_value, operator, condition_value):
        try:
            row_num = float(row_value)
            cond_num = float(condition_value)
            if operator == '>':
                return row_num > cond_num
            elif operator == '<':
                return row_num < cond_num
            elif operator == '>=':
                return row_num >= cond_num
            elif operator == '<=':
                return row_num <= cond_num
            elif operator == '=' or operator == '==':
                return row_num == cond_num
            elif operator == '!=':
                return row_num != cond_num
        except ValueError:
            if operator == '=' or operator == '==':
                return row_value == condition_value
            elif operator == '!=':
                return row_value != condition_value
            else:
                raise ValueError(f"Невозможно сравнить строки с оператором: {operator}")

    def display(self, data):
        if not data:
            print("Нет данных для отображения")
            return
        print(tabulate(data, headers="keys", tablefmt="grid"))
