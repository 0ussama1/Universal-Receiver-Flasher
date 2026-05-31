import time
from xmodem import XModem

class GXProcessor:
    def __init__(self, serial_conn, log_signal):
        self.ser = serial_conn
        self.log = log_signal

    def init_boot(self):
        self.log("[*] GX: جاري إرسال نبضات التحفيز...")
        timeout = time.time() + 8
        while time.time() < timeout:
            self.ser.write(b'\x20')
            if self.ser.in_waiting:
                res = self.ser.read(self.ser.in_waiting)
                if b'BOOT' in res or b'Gx' in res or b'\xaa' in res:
                    self.log("[+] GX: تم رصد استجابة المعالج بنجاح!")
                    return True
            time.sleep(0.05)
        return False

    def upload(self, file_path, progress_callback):
        self.log("[*] GX: جاري بدء نقل السوفتوير عبر XMODEM-1K...")
        def getc(size, timeout=1): return self.ser.read(size) or None
        def putc(data, timeout=1): return self.ser.write(data)
        modem = XModem(getc, putc, mode='xmodem1k')
        with open(file_path, 'rb') as f:
            success = modem.send(f, callback=lambda p, s, e: progress_callback(p, e))
        return success

class SunplusProcessor:
    def __init__(self, serial_conn, log_signal):
        self.ser = serial_conn
        self.log = log_signal

    def init_boot(self):
        self.log("[*] Sunplus: جاري محاولة إيقاف الإقلاع التلقائي (Ctrl+C)...")
        timeout = time.time() + 6
        while time.time() < timeout:
            self.ser.write(b'\x03')
            self.ser.write(b'uart\n')
            if self.ser.in_waiting:
                res = self.ser.read(self.ser.in_waiting)
                if b'Sunplus' in res or b'<' in res or b'Console' in res:
                    self.log("[+] Sunplus: تم الدخول إلى وضع المطورين.")
                    return True
            time.sleep(0.05)
        return False

    def upload(self, file_path, progress_callback):
        self.log("[*] Sunplus: جاري مسح الفلاشة وضخ السوفتوير...")
        self.ser.write(b"sf probe 0; sf erase 0 0x400000\n")
        time.sleep(2)
        with open(file_path, 'rb') as f:
            data = f.read()
            for i in range(0, len(data), 1024):
                self.ser.write(data[i:i+1024])
                progress_callback(i // 1024, 0)
                time.sleep(0.001)
        return True

class ALiProcessor:
    def __init__(self, serial_conn, log_signal):
        self.ser = serial_conn
        self.log = log_signal

    def init_boot(self):
        self.log("[*] ALi: جاري مزامنة التردد مع الكريستالة...")
        self.ser.write(b'\x48\x45\x4c\x4c\x4f')
        time.sleep(0.5)
        return True

    def upload(self, file_path, progress_callback):
        self.log("[*] ALi: جاري فحص ملف السوفتوير...")
        with open(file_path, 'rb') as f:
            data = f.read()
        total_chunks = len(data) // 128
        for i in range(total_chunks):
            self.ser.write(data[i*128 : (i+1)*128])
            progress_callback(i, 0)
            time.sleep(0.005)
        return True
