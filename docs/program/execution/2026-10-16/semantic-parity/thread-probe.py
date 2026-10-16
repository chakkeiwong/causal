import anyio
async def main():
 print(await anyio.to_thread.run_sync(lambda: 7), flush=True)
anyio.run(main)
