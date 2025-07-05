import argparse
from .processor import CSVProcessor


def parse_args():
    parser = argparse.ArgumentParser(description='Обработка CSV-файла с фильтрацией и агрегированием.')
    parser.add_argument('file', help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Условие фильтрации (например, "price>500")')
    parser.add_argument('--aggregate', help='Аггрегирующая операция (например, "price=avg")')
    parser.add_argument('--order_by', help='Столбец для сортировки')
    parser.add_argument('--order_dir', choices=['asc', 'desc'], default='asc',
                        help='Направление сортировки (asc/desc)')
    return parser.parse_args()


def main():
    args = parse_args()
    processor = CSVProcessor(args.file)

    filtered_data = processor.filter_data(args.where)

    if args.order_by:
        filtered_data = processor.sort_data(filtered_data, args.order_by, args.order_dir)

    if args.aggregate:
        column, operation = args.aggregate.split('=')
        result = processor.aggregate(column, operation)
        if result is not None:
            print(f"{operation}({column}): {result}")
    else:
        processor.display(filtered_data)


if __name__ == '__main__':
    main()
