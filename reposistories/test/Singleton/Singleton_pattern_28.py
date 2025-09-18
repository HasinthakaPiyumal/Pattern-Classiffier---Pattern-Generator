class PrinterSpoolerRegistry:
    _instances = {}

    @classmethod
    def get_instance(cls, spooler_name="default_spooler"):
        if spooler_name not in cls._instances:
            cls._instances[spooler_name] = _PrinterSpooler(spooler_name)
        return cls._instances[spooler_name]

class _PrinterSpooler:
    def __init__(self, name):
        self.name = name
        self.print_queue = []
        self.printer_status = "idle"

    def add_job(self, document_name, copies=1):
        job_id = f"{self.name}-{document_name}-{len(self.print_queue)+1}"
        self.print_queue.append({"id": job_id, "document": document_name, "copies": copies})
        return job_id

    def process_next_job(self):
        if not self.print_queue:
            self.printer_status = "idle"
            return None
        self.printer_status = "printing"
        job = self.print_queue.pop(0)
        self.printer_status = "idle"
        return job

    def get_queue_size(self):
        return len(self.print_queue)

if __name__ == "__main__":
    spooler1 = PrinterSpoolerRegistry.get_instance("OfficePrinter")
    spooler2 = PrinterSpoolerRegistry.get_instance("OfficePrinter")

    spooler_dev = PrinterSpoolerRegistry.get_instance("DevPrinter")

    print(f"Are spooler1 and spooler2 the same instance? {spooler1 is spooler2}")
    print(f"Are spooler1 and spooler_dev the same instance? {spooler1 is spooler_dev}")

    spooler1.add_job("Report.pdf", 5)
    spooler2.add_job("Invoice.docx", 2)
    spooler_dev.add_job("TestCode.txt", 1)

    print(f"OfficePrinter queue size: {spooler1.get_queue_size()}")
    print(f"DevPrinter queue size: {spooler_dev.get_queue_size()}")

    spooler1.process_next_job()
    spooler_dev.process_next_job()
    spooler2.process_next_job()

    print(f"OfficePrinter queue size after processing: {spooler1.get_queue_size()}")