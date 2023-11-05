import asyncio
import multiprocessing
import random
import socket
import time


async def worker(worker_id, num_connections):
    # Create multiple connections for each worker
    connections = []
    for i in range(num_connections):
        reader, writer = await asyncio.open_connection(socket.gethostname(), 8000)
        connections.append((reader, writer))

    try:
        while True:
            # Send a message from each connection
            for reader, writer in connections:
                message = f"Worker {worker_id}: {time.time()}\n"
                writer.write(message.encode())
                await writer.drain()
                print(f"Worker {worker_id} sent a message")

                # Sleep for a random interval before sending messages again
                sleep_time = random.uniform(0.0, 1.0)
                await asyncio.sleep(sleep_time)

    finally:
        # Close all connections
        for reader, writer in connections:
            writer.close()
            await writer.wait_closed()


async def main(worker_id):
    num_connections_per_worker = 500
    await worker(worker_id, num_connections_per_worker)


def run_main(worker_id):
    asyncio.run(main(worker_id=worker_id))


if __name__ == '__main__':
    processes = []

    # Create and start 10 worker processes
    for _ in range(10):
        process = multiprocessing.Process(target=run_main, args=(_,))
        processes.append(process)
        process.start()

    # Wait for all worker processes to finish
    for process in processes:
        process.join()
