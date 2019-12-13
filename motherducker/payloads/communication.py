import asyncio
from asyncio import Queue, StreamReader, StreamWriter, run
import struct
from typing import Tuple


async def _read(reader: StreamReader) -> bytes:

    response_len = struct.unpack('<I', await reader.read(4))[0]
    return await reader.read(response_len)


async def _send(writer: StreamWriter,
                cmd: bytes) -> None:

    writer.write(cmd)
    await writer.drain()


async def _handle(reader: StreamReader,
                  writer: StreamWriter) -> None:

    # Send "NOP" to get client UUID.
    await _send(writer, b':')
    uuid = await _read(reader)

    print(f'{uuid.hex()} is quacking.')

    # Example
    jobs = Queue()
    jobs.put_nowait(b'exit')

    # Loop here to send payloads?
    while True:
        cmd = await jobs.get()
        await _send(writer, cmd)

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
