import threading
import serial
import serial.tools.list_ports
from processors import GXProcessor, SunplusProcessor, ALiProcessor

class FlasherCore:
    def __init__(self, log_callback, progress_callback, finish_callback):
        self.log_cb = log_callback
        self.progress_cb = progress_callback
        self.finish_cb = finish_callback
        self.is_running = False

    @staticmethod
    def get_available_ports():
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def start_process(self, port, baudrate, chip_type, file_path, mode):
        if self.is_running: return
        self.is_running = True
        thread = threading.Thread(
            target=self._execute_flash, 
            args=(port, baudrate, chip_type, file_path, mode),
            daemon=True
        )
        thread.start()

    def _execute_flash(self, port, baudrate, chip_type, file_path, mode):
        try:
            ser = serial.Serial(port=port, baudrate=int(baudrate), timeout=2)
        except Exception as e:
            self.log_cb(f"[-] خطأ في فتح المنفذ: {e}")
            self.finish_cb(False)
            self.is_running = False
            return

        if "GX" in chip_type: processor = GXProcessor(ser, self.log_cb)
        elif "Sunplus" in chip_type: processor = SunplusProcessor(ser, self.log_cb)
        else: processor = ALiProcessor(ser, self.log_cb)

        success = False
        if mode == "تحديث السوفتوير (Flash)":
            if processor.init_boot(): success = processor.upload(file_path, self.progress_cb)
        ser.close()
        self.is_running = False
        self.finish_cb(success)
