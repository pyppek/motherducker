import asyncio
from asyncio import Queue, StreamReader, StreamWriter, run
import struct
from typing import Tuple


async def _read(reader: StreamReader) -> bytes:

    expected_len = struct.unpack('<I', await reader.read(4))[0]
    response = b''
    while len(response) < expected_len:
        response += await reader.read(expected_len - len(response))
    return response


async def _send(writer: StreamWriter,
                cmd: bytes) -> None:

    writer.write(cmd)
    await writer.drain()


async def _handle(reader: StreamReader,
                  writer: StreamWriter) -> None:

    uuid = await _read(reader)

    print(f'{uuid.hex()} is quacking.')

    # Example
    # dd if=/dev/urandom of=test.file count=1024 bs=1024
    jobs = Queue()
    jobs.put_nowait(b'cat test.file')
    jobs.put_nowait(b'exit')

    # Send payloads as they are enqueued.
    while (cmd := await jobs.get()) != b'exit':

        await _send(writer, cmd)
        response = await _read(reader)

        print(response)

    await _send(writer, cmd)
    writer.close()


async def start_server(addr: Tuple[str, int]) -> None:

    server = await asyncio.start_server(
        _handle, *addr)

    async with server:
        await server.serve_forever()


try:
    run(start_server(('localhost', 5000)))
except KeyboardInterrupt:
    pass
