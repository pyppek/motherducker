import asyncio
from asyncio import Queue, StreamReader, StreamWriter, TimeoutError, run, wait_for
import struct
from datetime import datetime
from typing import Tuple


DEFAULT_TIMEOUT = 60


def _largest_power_of_two(n: int) -> int:

    """ Return largest power of two less than or equal to <n>. """

    # Prevent negative shift.
    if n < 1:
        return None
    return 1 << (n.bit_length() - 1)


async def _recv_data(reader: StreamReader,
                     length: int,
                     timeout: float) -> bytes:

    """ Receive <length> amount of data from <reader>. """

    if length < 1:
        return None

    # Preallocate bytearray.
    data = bytearray(length)
    index = 0
    while index < length:
        diff = length - index

        # Retrieve data in power of two sized chunks capped at <reader> limit.
        buf_size = _largest_power_of_two(diff)
        if buf_size > reader._limit:
            buf_size = reader._limit

        # Wait at most <timeout> seconds, then return None.
        try:
            chunk = await wait_for(reader.read(buf_size), timeout)
        except TimeoutError:
            return None

        # Return None in case less data received than expected.
        if not chunk:
            return None

        data[index:index+buf_size] = chunk
        index += buf_size

    # Return None in case more data received than expected.
    if len(data) > length:
        return None

    return bytes(data)


async def _read(reader: StreamReader,
                timeout: float = DEFAULT_TIMEOUT) -> bytes:

    # Each message is prepended by 8 bytes representing
    # the remaining message length. Assuming little-endian?
    chunk = await _recv_data(reader, 8, timeout)
    expected_len = struct.unpack('<Q', chunk)[0]

    # Read stream until <expected_len> bytes.
    return await _recv_data(reader, expected_len, timeout)


async def _send(writer: StreamWriter,
                cmd: bytes) -> None:

    writer.write(cmd)
    await writer.drain()


async def _handle(reader: StreamReader,
                  writer: StreamWriter) -> None:

    # Initial message consists of only client UUID.
    uuid = await _read(reader)

    print(f'{uuid.hex()} is quacking.')

    # Example
    # dd if=/dev/urandom of=test.file count=1024 bs=1024
    jobs = Queue()
    jobs.put_nowait(b'cat test.file')
    jobs.put_nowait(b'exit')

    # Send payloads as they are enqueued until "exit" is issued.
    while (cmd := await jobs.get()) != b'exit':

        await _send(writer, cmd)
        response = await _read(reader)

    await _send(writer, cmd)
    writer.close()


async def start_server(addr: Tuple[str, int]) -> None:

    server = await asyncio.start_server(_handle, *addr)

    async with server:
        await server.serve_forever()


try:
    run(start_server(('localhost', 5000)))
except KeyboardInterrupt:
    pass
