import asyncio
import aiohttp.server


class HelloServer(aiohttp.server.ServerHttpProtocol):

    @asyncio.coroutine
    def handle_request(self, message, payload):

        # Do some work...
        yield from asyncio.sleep(1)

        # Send the response
        response = aiohttp.Response(self.writer, 200,
                                    http_version=message.version)
        body = u'สวัสดีครับ\n'.encode('utf-8')
        response.add_header('Content-Type', 'text/plain')
        response.add_header('Content-Length', str(len(body)))
        response.send_headers()
        response.write(body)
        yield from response.write_eof()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    create_server = loop.create_server(HelloServer, '0.0.0.0', '8000')
    server = loop.run_until_complete(create_server)
    print('Serving on', server.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
