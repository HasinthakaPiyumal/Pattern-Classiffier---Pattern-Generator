class FileMonitor:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def simulate_change(self, filename, change_type):
        print(f"\nFileMonitor: Detected {change_type} on '{filename}'")
        self.notify(filename, change_type)

    def notify(self, filename, change_type):
        for observer in self._observers:
            observer.on_file_change(filename, change_type)

class Logger:
    def __init__(self, name):
        self.name = name

    def on_file_change(self, filename, change_type):
        print(f"Logger {self.name}: Logged '{filename}' - {change_type} event.")

class BackupSystem:
    def __init__(self, name):
        self.name = name

    def on_file_change(self, filename, change_type):
        if change_type in ["created", "modified"]:
            print(f"Backup System {self.name}: Initiating backup for '{filename}'.")
        else:
            print(f"Backup System {self.name}: Noting deletion of '{filename}'.")

if __name__ == '__main__':
    monitor = FileMonitor()
    system_logger = Logger("System")
    data_backup = BackupSystem("Data")

    monitor.attach(system_logger)
    monitor.attach(data_backup)

    monitor.simulate_change("report.txt", "created")
    monitor.simulate_change("config.ini", "modified")
    monitor.detach(data_backup)
    monitor.simulate_change("temp.log", "deleted")