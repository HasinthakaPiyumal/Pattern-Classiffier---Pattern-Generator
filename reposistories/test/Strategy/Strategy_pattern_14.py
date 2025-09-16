import json
class ExportStrategy:
    def export(self, data):
        raise NotImplementedError
class CSVExportStrategy(ExportStrategy):
    def export(self, data):
        if not data: return ""
        headers = ",".join(data[0].keys())
        rows = [",".join(str(v) for v in item.values()) for item in data]
        return headers + "\n" + "\n".join(rows)
class JSONExportStrategy(ExportStrategy):
    def export(self, data):
        return json.dumps(data, indent=2)
class DataExporter:
    def __init__(self, strategy):
        self._strategy = strategy
    def set_strategy(self, strategy):
        self._strategy = strategy
    def export_data(self, data):
        return self._strategy.export(data)
data_to_export = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
exporter = DataExporter(CSVExportStrategy())
print("CSV Export:\n" + exporter.export_data(data_to_export))
exporter.set_strategy(JSONExportStrategy())
print("JSON Export:\n" + exporter.export_data(data_to_export))