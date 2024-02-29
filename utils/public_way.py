import socket


def send_tcp_request(hex_data):
    # 将十六进制字符串转换为字节
    data = bytes.fromhex(hex_data)

    # 创建 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect(("192.168.3.253", 1030))
