import abc

class ReportFormatStrategy(abc.ABC):
    @abc.abstractmethod
    def generate_report(self, data):
        pass

class PdfReportStrategy(ReportFormatStrategy):
    def generate_report(self, data):
        report_content = f"--- PDF Report ---\nTitle: Sales Report\nData: {data}\n--- End PDF ---"
        print(f"Generated PDF Report: '{report_content}'")
        return report_content

class CsvReportStrategy(ReportFormatStrategy):
    def generate_report(self, data):
        headers = ",".join(data[0].keys())
        rows = [",".join(str(item) for item in row.values()) for row in data]
        report_content = f"--- CSV Report ---\n{headers}\n" + "\n".join(rows) + "\n--- End CSV ---"
        print(f"Generated CSV Report: '{report_content}'")
        return report_content

class ReportGenerator:
    def __init__(self, strategy: ReportFormatStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy):
        self._strategy = strategy

    def create_report(self, data):
        return self._strategy.generate_report(data)

if __name__ == "__main__":
    sales_data = [{"product": "Laptop", "quantity": 5, "price": 1200},
                  {"product": "Mouse", "quantity": 10, "price": 25}]

    generator = ReportGenerator(PdfReportStrategy())
    generator.create_report(sales_data)

    generator.set_strategy(CsvReportStrategy())
    generator.create_report(sales_data)