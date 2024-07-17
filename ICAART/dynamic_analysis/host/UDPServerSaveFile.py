# 2023/09/19
# auther:naru
# encoding=utf-8

import time
import socket
import multiprocessing as mp
from typing import Optional, Any, Type, Callable

from lib763.fs import ensure_path_exists, append_str_to_file
from lib763.multp import start_process, EventHandler

from CONST import ITER_FINISH_COMMAND, SAVE_FINISH_COMMAND, SERVER_READY_COMMAND

STOP_COMMAND = "\x02STOP\x03"


class UDPServer:
    """A server for handling UDP packets.

    Args:
        host (str): The host of the server.
        port (int): The port of the server.
        buffer_size (int): The maximum amount of data to be received at once.
        timeout (float, optional): The timeout in seconds. Defaults to None.
    """

    def __init__(
        self, host: str, port: int, buffer_size: int, timeout: Optional[float] = None
    ) -> None:
        """Initialize the server with host, port and buffer size.

        Args:
            host (str): The host of the server.
            port (int): The port of the server.
            buffer_size (int): The maximum amount of data to be received at once.
            timeout (float, optional): The timeout in seconds. Defaults to None.
        """
        self._sock = None
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        to = timeout if timeout is not None else 60
        if not self.init_server(to):
            raise TimeoutError("UDP server timeout to bind")

    def init_server(self, timeout: float = 60) -> bool:
        """Initialize the server socket.

        Args:
            timeout (float, optional): The timeout in seconds. Defaults to 60.

        Returns:
            bool: True if the server socket is initialized successfully, False otherwise.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._sock.bind((self._host, self._port))
                return True
            except OSError as e:
                if e.winerror == 10048:
                    time.sleep(1)
                    continue
                else:
                    raise e
        return False

    def receive_udp_packet(self, timeout: Optional[float] = None) -> Optional[bytes]:
        """Receive a UDP packet from the socket.

        Args:
            timeout (float, optional): The timeout in seconds. Defaults to None.

        Returns:
            Optional[bytes]: The received data, None if an error occurred.
        """
        try:
            self._sock.settimeout(timeout)
            rcv_data, _ = self._sock.recvfrom(self._buffer_size)
            return rcv_data
        except socket.timeout:
            return None
        except Exception as e:
            return None

    def __enter__(self) -> "UDPServer":
        """Enter the context of the server, allowing use with 'with' statement.

        Returns:
            UDPServer: The server instance.
        """
        return self

    def __exit__(
        self, exc_type: Type[BaseException], exc_value: BaseException, traceback: Any
    ) -> None:
        """Exit the context of the server, allowing use with 'with' statement.

        Args:
            exc_type (Type[BaseException]): The type of exception.
            exc_value (BaseException): The instance of exception.
            traceback (Any): A traceback object.
        """
        self._sock.close()


class UdpServerSaveFile(UDPServer):
    def __init__(
        self,
        host: str,
        port: int,
        udp_buffer_size: int,
        edit_msg_func: Callable,
        msg_buf_size: int,
    ) -> None:
        """Initialize the server with host, port, buffer size, edit function and message buffer size.

        Args:
            host (str): The host of the server.
            port (int): The port of the server.
            udp_buffer_size (int): The maximum amount of data to be received at once.
            edit_msg_func (Callable): A function to edit the received message.
            msg_buf_size (int): The maximum number of messages to be saved at once.
        """
        super().__init__(host, port, udp_buffer_size)
        self.edit_func = edit_msg_func
        self.msg_buf_size = msg_buf_size
        self.save_path_q = mp.Queue()
        self.save_msgs_q = None
        self.eventh = EventHandler()

    def set_iter_fin(self):
        self.eventh.set_event(ITER_FINISH_COMMAND)

    def clear_save_fin(self):
        self.eventh.clear_event(SAVE_FINISH_COMMAND)

    def clear_server_ready(self):
        self.eventh.clear_event(SERVER_READY_COMMAND)

    def main(self) -> None:
        """The main function of the server."""
        while self.save_path_q.empty():
            time.sleep(1)
        self.start_saving_proc()
        msgs_buf = []
        while True:
            try:
                if not self.save_path_q.empty():
                    self.start_saving_proc()
                    msgs_buf.clear()
                if self.eventh.get_current_event_type() == ITER_FINISH_COMMAND:
                    self.eventh.clear_event(ITER_FINISH_COMMAND)
                    # 現在のバッファを保存する
                    if len(msgs_buf) != 0:
                        self.save_msgs(msgs_buf.copy())
                    self.save_msgs_q.put(STOP_COMMAND)

                msg = self.receive_udp_packet(1)
                if msg is None:
                    continue
                msgs_buf.append(msg)
                if len(msgs_buf) >= self.msg_buf_size:
                    self.save_msgs(msgs_buf.copy())
                    msgs_buf.clear()
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Error in server-save-file-main loop: {str(e)}")

    def change_save_path(self, next_path):
        """Change the path to save the messages.

        Args:
            next_path (str): The path to save the messages.
        """
        self.save_path_q.put(next_path)

    def start_saving_proc(self):
        """Start the process of saving the messages."""
        # pathを更新する
        path = self.save_path_q.get()
        self.save_msgs_q = mp.Queue()
        start_process(
            save_proc, self.save_msgs_q, path, self.edit_func, self.eventh
        )
        self.eventh.set_event(SERVER_READY_COMMAND)

    def save_msgs(self, copied_buffer):
        """Save the messages to the queue.

        Args:
            copied_buffer (list): The buffer of messages to be saved.
        """
        self.save_msgs_q.put(copied_buffer)


def save_proc(
    queue: mp.Queue,
    save_path: str,
    edit_msg_func: Callable,
    eventh: EventHandler,
) -> None:
    """The process of saving the messages.

    Args:
        queue (Queue): The queue of messages to be saved.
        save_path (str): The path to save the messages.
        edit_msg_func (Callable): A function to edit the received message.
        event (Event): An event object.
    """
    ensure_path_exists(save_path)
    while True:
        item = queue.get()
        if item == STOP_COMMAND:
            eventh.set_event(SAVE_FINISH_COMMAND)
            return
        save_str = "\n".join([edit_msg_func(msg.decode()) for msg in item]) + "\n"
        append_str_to_file(save_str, save_path)
