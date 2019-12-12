import asyncio
from asyncio import StreamReader, StreamWriter, TimeoutError, open_connection, run, wait_for
from typing import Tuple


async def _read(reader: StreamReader,
                timeout: float) -> bytes:

    """ Read stream from <reader> until idle for <timeout> seconds. """

    result = b''
    while True:
        try:
            result += await wait_for(reader.read(reader._limit), timeout)
        except TimeoutError:
            return result


async def send_payload(addr: Tuple[str, int],
                       cmd: bytes,
                       timeout: float = 1) -> bytes:

    reader, writer = await open_connection(*addr)

    writer.write(cmd)
    await writer.drain()

    response = await _read(reader, timeout)

    writer.close()
    await writer.wait_closed()

    return response


async def _handle(reader: StreamReader,
                  writer: StreamWriter) -> None:

    data = await _read(reader, 1)

    # If there was nothing to read, assume initial connection.
    if data == b'':
        # Send NOP to get nothing but client UUID.
        writer.write(b':')
        await writer.drain()

        uuid = await _read(reader, 1)
        print(uuid)

    writer.close()


async def start_server(addr: Tuple[str, int]) -> None:

    server = await asyncio.start_server(
        _handle, addr[0], addr[1])

    async with server:
        await server.serve_forever()


try:
    run(start_server(('localhost', 5000)))
except KeyboardInterrupt:
    pass
