class Report:
    def generate(self, data: dict) -> str:
        pass

class FinancialReport(Report):
    def generate(self, data: dict) -> str:
        revenue = data.get('revenue', 0)
        expenses = data.get('expenses', 0)
        profit = revenue - expenses
        return f"Financial Report:\n  Revenue: ${revenue:.2f}\n  Expenses: ${expenses:.2f}\n  Net Profit: ${profit:.2f}"

class StudentPerformanceReport(Report):
    def generate(self, data: dict) -> str:
        student_name = data.get('name', 'N/A')
        grade = data.get('grade', 'N/A')
        score = data.get('score', 0)
        return f"Student Performance Report for {student_name}:\n  Grade: {grade}\n  Score: {score}/100"

class InventoryReport(Report):
    def generate(self, data: dict) -> str:
        items = data.get('items', [])
        total_value = sum(item['price'] * item['quantity'] for item in items)
        return f"Inventory Report:\n  Total Items: {len(items)}\n  Total Inventory Value: ${total_value:.2f}"

class ReportFactory:
    def create_report(self, report_type: str) -> Report:
        if report_type == "financial":
            return FinancialReport()
        elif report_type == "student_performance":
            return StudentPerformanceReport()
        elif report_type == "inventory":
            return InventoryReport()
        else:
            raise ValueError(f"Unknown report type: {report_type}")

factory = ReportFactory()

fin_data = {'revenue': 150000.00, 'expenses': 85000.00}
student_data = {'name': 'Alice Smith', 'grade': 'A', 'score': 92}
inv_data = {'items': [{'name': 'Laptop', 'price': 1200, 'quantity': 10}, {'name': 'Mouse', 'price': 25, 'quantity': 50}]}

financial_report = factory.create_report("financial")
student_report = factory.create_report("student_performance")
inventory_report = factory.create_report("inventory")

print(financial_report.generate(fin_data))
print("\n" + student_report.generate(student_data))
print("\n" + inventory_report.generate(inv_data))

try:
    sales_report = factory.create_report("sales")
except ValueError as e:
    print(e)