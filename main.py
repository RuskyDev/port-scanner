import asyncio
import sys
import argparse
import socket

async def scanPort(target, port, sem, timeout, lock, openPorts, status, family):
    async with sem:
        try:
            conn = asyncio.open_connection(target, port, family=family)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            async with lock:
                openPorts.append(port)
            writer.close()
            await writer.wait_closed()
        except:
            pass
        finally:
            async with lock:
                status["scanned"] += 1
                if status["scanned"] % 500 == 0 or status["scanned"] == status["total"]:
                    percent = (status["scanned"] / status["total"]) * 100
                    sys.stdout.write(f"\rScanned {status['scanned']}/{status['total']} ({percent:.2f}%)")
                    sys.stdout.flush()

async def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("--end", type=int, default=65535, help="End port (default 65535)")
    parser.add_argument("--concurrency", type=int, default=1000, help="Number of concurrent scans (default 1000)")
    parser.add_argument("--timeout", type=float, default=0.3, help="Connection timeout in seconds (default 0.3)")
    parser.add_argument("--ipv6", action="store_true", help="Use IPv6 instead of IPv4")
    args = parser.parse_args()

    family = socket.AF_INET6 if args.ipv6 else socket.AF_INET
    ports = range(args.start, args.end + 1)
    openPorts = []
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(args.concurrency)
    status = {"scanned": 0, "total": len(ports)}

    tasks = [scanPort(args.target, port, sem, args.timeout, lock, openPorts, status, family) for port in ports]
    await asyncio.gather(*tasks)

    print("\nScan complete.")
    if openPorts:
        print("Open ports:", openPorts)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    asyncio.run(main())
