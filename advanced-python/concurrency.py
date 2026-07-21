import asyncio
import time

async def task(name, delay):
    print(f"Task {name} bắt đầu")
    await asyncio.sleep(delay)
    print(f"Task {name} hoàn thành sau {delay} giây")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )

start_time = time.time()
asyncio.run(main())
end_time = time.time()
print(f"Thời gian hoàn thành: {end_time - start_time} giây")