import socket


def send_tcp_request(hex_data, server_ip, server_port):
    # 将十六进制字符串转换为字节
    data = bytes.fromhex(hex_data)

    # 创建 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect((server_ip, server_port))

        # 发送数据
        s.sendall(data)
        print(f"Sent Hex Data: {hex_data}")

        # 接收数据
        received_data = s.recv(1024)
        print(f"Received Hex Data: {received_data.hex()}")


# 使用示例
if __name__ == "__main__":
    hex_data = "483A0170010000004544"  # 待发送的十六进制数据
    server_ip = "192.168.3.253"
    server_port = 1030  # 服务器端口
    send_tcp_request(hex_data, server_ip, server_port)
