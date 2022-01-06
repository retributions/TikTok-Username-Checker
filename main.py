import asyncio
import ctypes
import functools
import os

import aiohttp

RESET = "\u001b[0m"
RED = "\u001b[31;1m"
CYAN = "\u001b[36;1m"


class Tiktok:
    def __init__(self) -> None:
        self.avaiable = []
        self.checked = 0
        self.unavaiable = 0

    def _title_updater(self) -> None:
        while self.checked != len(self.names):
            ctypes.windll.kernel32.SetConsoleTitleW(
                "[TikTok Username Checker] - github.com/xdecemberrr | "
                f"Checked: {self.checked}/{len(self.names)} "
                f"({round(((self.checked / len(self.names)) * 100), 2)}%) | "
                f"Avaiable: {len(self.avaiable)} | "
                f"Taken: {self.unavaiable}"
            )

    async def _check(self, session: aiohttp.ClientSession, name: str) -> None:
        async with session.head(f"https://www.tiktok.com/@{name}") as response:
            if response.status == 200:
                self.unavaiable += 1
                print(f"{RED}[{RESET}TAKEN{RED}]{RESET} @{name}")
            elif response.status == 404:
                print(f"{CYAN}[{RESET}AVAIABLE{CYAN}]{RESET} @{name}")
                self.avaiable.append(name)
            else:
                print(f"{RED}[{RESET}ERROR{RED}] Status code: {response.status}")

            self.checked += 1

    async def start(self) -> None:
        if not os.path.exists("usernames.txt"):
            open("usernames.txt", "w").close()
            print(f"{RED}[{RESET}!{RED}]{RESET} Put usernames in usernames.txt")
            os.system("pause >nul")
            os._exit(0)

        with open("usernames.txt", encoding="utf-8") as f:
            self.names = [i.strip() for i in f]

        loop.run_in_executor(None, functools.partial(self._title_updater))

        async with aiohttp.ClientSession() as s:
            await asyncio.gather(*[self._check(s, n) for n in self.names])

        if len(self.avaiable) > 1:
            with open("avaiable.txt", "w") as f:
                f.write("\n".join(self.avaiable))

        print(f"\n{CYAN}[{RESET}+{CYAN}]{RESET} Done checking {self.checked} usernames")
        os.system("pause >nul")


if __name__ == "__main__":
    os.system("cls")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tiktok().start())
