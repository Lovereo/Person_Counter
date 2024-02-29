import socket


def send_on_tcp_request():
    # 将十六进制字符串转换为字节
    turn_on_the_signal = bytes.fromhex("483A0170010100004544")

    # 创建 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect(("192.168.3.253", 1030))
        s.sendall(turn_on_the_signal)


def send_off_tcp_request():
    turn_off_the_signal = bytes.fromhex("483A0170010000004544")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect(("192.168.3.253", 1030))
        s.sendall(turn_off_the_signal)
