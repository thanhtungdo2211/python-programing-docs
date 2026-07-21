# Định nghĩa một callback function
def print_result(result):
    print(f"Kết quả: {result}")

# Hàm chính, thực hiện công việc và gọi callback sau khi xong
def process_data(data, callback):
    # Thực hiện một vài thao tác với dữ liệu
    processed_data = data ** 2
    # Gọi callback với kết quả đã xử lý
    callback(processed_data)

# Sử dụng hàm với callback
data = 10
process_data(data, print_result)

# Result
# 100