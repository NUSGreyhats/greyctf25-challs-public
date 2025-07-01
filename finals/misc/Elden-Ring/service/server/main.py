from flask import Flask, send_from_directory, request, render_template
from datetime import datetime
app = Flask(__name__)
FILE_DIR = "files"

import ctypes
import time
from ctypes import wintypes

# Get SYSTEMTIME structure from Windows API
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", wintypes.WORD),
        ("wMonth", wintypes.WORD),
        ("wDayOfWeek", wintypes.WORD),
        ("wDay", wintypes.WORD),
        ("wHour", wintypes.WORD),
        ("wMinute", wintypes.WORD),
        ("wSecond", wintypes.WORD),
        ("wMilliseconds", wintypes.WORD)
    ]

def get_key():
    _time = datetime.now()

    # Read and sanitize input values
    month = _time.month & 0xFFFFFFFF
    day = _time.day & 0xFFFFFFFF
    hour = (_time.hour + 8) & 0xFFFFFFFF

    result = []

    for i in range(32):
        h1 = (8 * hour) & 0xFFFFFFFF
        h2 = (hour ^ h1) & 0xFFFFFFFF
        h3 = (h2 >> 3) & 0xFFFFFFFF
        h4 = (hour & 0xFFFFFFFE) & 0xFFFFFFFF
        h5 = (h4 << 15) & 0xFFFFFFFF
        hour = (h3 ^ h5) & 0xFFFFFFFF

        m1 = (month << 10) & 0xFFFFFFFF
        m2 = (month ^ m1) & 0xFFFFFFFF
        m3 = (m2 >> 16) & 0xFFFFFFFF
        m4 = (month & 0xFFFFFFF8) & 0xFFFFFFFF
        m5 = (m4 << 11) & 0xFFFFFFFF
        m6 = (16 * m5) & 0xFFFFFFFF
        month = (m3 ^ m6) & 0xFFFFFFFF

        d1 = (day << 13) & 0xFFFFFFFF
        d2 = (day ^ d1) & 0xFFFFFFFF
        d3 = (d2 >> 19) & 0xFFFFFFFF
        d4 = (day & 0xFFFFFFFE) & 0xFFFFFFFF
        d5 = (d4 << 12) & 0xFFFFFFFF
        day = (d3 ^ d5) & 0xFFFFFFFF

        val = (hour ^ month ^ day) & 0xFFFFFFFF
        byte_val = val % 128
        result.append(byte_val)
    return bytes(result)

    

@app.route("/", methods=["GET"])
def root():
    sad = "grey{Y0KOS0_KIR4_KIR4_DOKI_D0KI_M0CH1_MOCH1_PuY0_PuY0_WAKU_WAKU_W4SH0II_NA_W0NDER_ST4GE_YE}"
    reee = b""
    reee += b"\x00"
    reee += int.to_bytes(len(sad), 4,byteorder="little")
    based = get_key()
    print(based)
    sad = sad.encode()
    cry = b""
    for i in range(len(sad)):
         cry += int.to_bytes(sad[i] ^ based[i % len(based)], 1, byteorder="little")
    reee += cry
    return reee 

@app.route("/get", methods=["GET"])
def get():
    return render_template("index.html")

@app.route("/download/<name>", methods=["GET"])
def download(name):
    return send_from_directory(FILE_DIR, name, as_attachment=True)

@app.route("/main", methods=["GET"])
def yeet():
    return send_from_directory(FILE_DIR, "notes.lnk", as_attachment=True)

if __name__  == "__main__":
    app.run("0.0.0.0", 35000)