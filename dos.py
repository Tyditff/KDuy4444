import aiohttp
import asyncio
import socket
import time
import os
from multiprocessing import Process, Value
from colorama import init, Fore, Style

init(autoreset=True)

def get_ip_from_url(url):
    hostname = url.replace("https://", "").replace("http://", "").split('/')[0]
    return socket.gethostbyname(hostname)

async def send_requests(session, url, counter, connections, process_index):
    sem = asyncio.Semaphore(connections)

    async def request():
        async with sem:
            try:
                async with session.get(url) as response:
                    await response.read()
                    with counter.get_lock():
                        counter.value += 1
            except:
                pass

    while True:
        await asyncio.gather(*[request() for _ in range(connections)])

def process_worker(url, counter, connections, index):
    asyncio.run(run(url, counter, connections, index))

async def run(url, counter, connections, index):
    timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        await send_requests(session, url, counter, connections, index)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    url = input(Fore.CYAN + "Nhập URL (ví dụ: https://example.com): " + Style.RESET_ALL).strip()
    try:
        ip = get_ip_from_url(url)
        print(Fore.YELLOW + f"IP của web: {ip}" + Style.RESET_ALL)
    except:
        print(Fore.RED + "Không lấy được IP." + Style.RESET_ALL)
        return

    connections = int(input(Fore.CYAN + "Số kết nối bất đồng bộ mỗi tiến trình: " + Style.RESET_ALL))
    num_processes = int(input(Fore.CYAN + "Số tiến trình: " + Style.RESET_ALL))

    counter = Value('i', 0)
    processes = []

    for i in range(num_processes):
        p = Process(target=process_worker, args=(url, counter, connections, i))
        p.start()
        processes.append(p)

    try:
        last = 0
        start_time = time.time()
        while True:
            time.sleep(1)
            with counter.get_lock():
                current = counter.value
            rps = current - last
            uptime = int(time.time() - start_time)
            print(Fore.GREEN + f"[{uptime:>4}s] [Tổng RPS] {rps} | Tổng: {current}" + Style.RESET_ALL)
            last = current
    except KeyboardInterrupt:
        print(Fore.RED + "Đang dừng..." + Style.RESET_ALL)
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
