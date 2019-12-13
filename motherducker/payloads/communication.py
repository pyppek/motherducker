import asyncio
from asyncio import Queue, StreamReader, StreamWriter, run
import struct
from typing import Tuple


async def _read(reader: StreamReader) -> bytes:

    # Each message is prepended by 8 bytes representing
    # the remaining message length. Assuming little-endian?
    try:
        expected_len = struct.unpack('<Q', await reader.read(8))[0]
    except struct.error:
        return None

    # Read stream until <expected_len> bytes.
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
