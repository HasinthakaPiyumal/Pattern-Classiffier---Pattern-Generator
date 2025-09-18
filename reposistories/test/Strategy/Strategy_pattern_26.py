import abc
import json
import csv
from io import StringIO

class DataExportStrategy(abc.ABC):
    @abc.abstractmethod
    def export(self, data):
        pass

class CSVExportStrategy(DataExportStrategy):
    def export(self, data):
        output = StringIO()
        if not data:
            print("CSV export: No data to export.")
            return ""

        fieldnames = list(data[0].keys()) if data else []
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        csv_string = output.getvalue()
        print("CSV Exported:\n", csv_string)
        return csv_string

class JSONExportStrategy(DataExportStrategy):
    def export(self, data):
        json_string = json.dumps(data, indent=2)
        print("JSON Exported:\n", json_string)
        return json_string

class XMLExportStrategy(DataExportStrategy):
    def export(self, data):
        if not data:
            print("XML export: No data to export.")
            return "<data/>"

        xml_parts = ["<data>"]
        for item in data:
            xml_parts.append(f"  <item>")
            for key, value in item.items():
                xml_parts.append(f"    <{key}>{value}</{key}>")
            xml_parts.append(f"  </item>")
        xml_parts.append("</data>")
        xml_string = "\n".join(xml_parts)
        print("XML Exported:\n", xml_string)
        return xml_string

class DataExporter:
    def __init__(self, export_strategy: DataExportStrategy):
        self._export_strategy = export_strategy
        self._data = []

    def set_export_strategy(self, strategy: DataExportStrategy):
        self._export_strategy = strategy

    def add_record(self, record):
        self._data.append(record)

    def export_data(self):
        print(f"\n--- Exporting data with {type(self._export_strategy).__name__} ---")
        return self._export_strategy.export(self._data)

if __name__ == "__main__":
    records = [
        {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 24, "city": "Los Angeles"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
    ]

    exporter = DataExporter(JSONExportStrategy())
    for record in records:
        exporter.add_record(record)
    exporter.export_data()

    exporter.set_export_strategy(CSVExportStrategy())
    exporter.export_data()

    exporter.set_export_strategy(XMLExportStrategy())
    exporter.export_data()

    empty_exporter = DataExporter(JSONExportStrategy())
    empty_exporter.export_data()