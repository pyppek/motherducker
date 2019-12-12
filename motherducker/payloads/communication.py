import asyncio
from asyncio import StreamReader, StreamWriter, TimeoutError, open_connection, run, wait_for
from typing import Tuple


async def start_server(addr: Tuple[str, int]) -> None:

    server = await asyncio.start_server(
        _handle, addr[0], addr[1])

    async with server:
        await server.serve_forever()


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


async def _read(reader: StreamReader,
                timeout: float) -> bytes:

    """ Read stream from <reader> until idle for <timeout> seconds. """

    result = b''
    while True:
        try:
            result += await wait_for(reader.read(reader._limit), timeout)
        except TimeoutError:
            return result


async def _handle(reader: StreamReader,
                  writer: StreamWriter) -> None:

    pass    
    # addr = writer.get_extra_info('peername')
    # print(f'{addr!r}')

    # writer.write(b'ls')
    # await writer.drain()

    # response = await _read(reader, 5)
    # print(response)
