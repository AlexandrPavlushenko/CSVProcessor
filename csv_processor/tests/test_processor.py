import pytest
from csv_processor.processor import CSVProcessor


@pytest.fixture
def sample_csv(tmp_path):
    csv_data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(csv_data)
    return file_path


def test_read_csv(sample_csv):
    processor = CSVProcessor(sample_csv)
    assert len(processor.data) == 4
    assert processor.data[0]['name'] == 'iphone 15 pro'


def test_filter_equals(sample_csv):
    processor = CSVProcessor(sample_csv)
    filtered = processor.filter_data("brand=xiaomi")
    assert len(filtered) == 2
    assert all(item['brand'] == 'xiaomi' for item in filtered)


def test_filter_greater_than(sample_csv):
    processor = CSVProcessor(sample_csv)
    filtered = processor.filter_data("price>500")
    assert len(filtered) == 2
    assert all(float(item['price']) > 500 for item in filtered)


def test_aggregate_avg(sample_csv):
    processor = CSVProcessor(sample_csv)
    avg_price = processor.aggregate('price', 'avg')
    assert avg_price == pytest.approx((999 + 1199 + 199 + 299) / 4)


def test_aggregate_min(sample_csv):
    processor = CSVProcessor(sample_csv)
    min_price = processor.aggregate('price', 'min')
    assert min_price == 199


def test_aggregate_max(sample_csv):
    processor = CSVProcessor(sample_csv)
    max_price = processor.aggregate('price', 'max')
    assert max_price == 1199


def test_sort_asc(sample_csv):
    processor = CSVProcessor(sample_csv)
    sorted_data = processor.sort_data(processor.data, 'price', 'asc')
    prices = [float(item['price']) for item in sorted_data]
    assert prices == sorted(prices)


def test_sort_desc(sample_csv):
    processor = CSVProcessor(sample_csv)
    sorted_data = processor.sort_data(processor.data, 'price', 'desc')
    prices = [float(item['price']) for item in sorted_data]
    assert prices == sorted(prices, reverse=True)


def test_invalid_condition(sample_csv):
    processor = CSVProcessor(sample_csv)
    with pytest.raises(ValueError):
        processor.filter_data("Неверный формат условия")
