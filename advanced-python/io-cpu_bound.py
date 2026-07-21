import time
import requests  # Yêu cầu phải cài requests bằng cách: pip install requests

# Ví dụ I/O bound: tải nội dung từ một URL (chờ I/O mạng)
def download_website(url):
    response = requests.get(url)
    return response.text

# Tính thời gian tải nhiều trang web
urls = ["https://example.com" for _ in range(10)]

start_time = time.time()

for url in urls:
    download_website(url)

end_time = time.time()

print(f"Tổng thời gian thực hiện (I/O bound): {end_time - start_time:.2f} giây")

import time

# Ví dụ CPU bound: tính toán với các số lớn
def intensive_computation(n):
    total = 0
    for i in range(1, n):
        total += i**2
    return total

# Tính thời gian thực hiện nhiều phép tính toán
start_time = time.time()

for _ in range(10):
    intensive_computation(10**6)

end_time = time.time()

print(f"Tổng thời gian thực hiện (CPU bound): {end_time - start_time:.2f} giây")