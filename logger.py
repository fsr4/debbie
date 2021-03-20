class Logger:
    log_file = None
    parent = None

    def __init__(self, log_path, parent):
        self.log_file = open(log_path, "a", encoding="utf-8")
        self.parent = parent

    def log(self, label, message):
        message = f"[{label}] {message}"
        print(message)
        self.log_file.write(f"{message}\n")
        self.log_file.flush()

    def info(self, message):
        self.log("Info", message)

    def error(self, message):
        self.log("Error", message)
