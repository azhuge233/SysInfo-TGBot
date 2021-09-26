# SysInfo-TGBot

A python script let you control your server with telegram bot.

## Requirements

- python 3.5 +
    - psutil
    - pyTelegramBotAPI

## Usage

1. Clone repo

2. Install packages

   ```shell
   pip3 install -r requirements.txt
   ```

3. Fill in `TOKEN`, `ChatID`, `IPCAddress`, `IPCPassword` and `IPCBotList`, then change `Password` to your system user's password (systemd needs privilege).

   - Modify `WaitSec` if you want to wait longer/shorter before rebooting (default is 10 seconds).
   - Modify `BOT_INFO` to your own info message.
   - `IPCBotList` only contains multiple ASF bot nicknames hosted under your ASF client (e.g `IPCBotList = ["bot1", "bot2", "bot3"]`). When `/addlicense` command is called, the script will automatically add target Sub/App ID to these bots.

4. Then run

   ```shell
   python3 run.py
   ```

Tested on Debian 11 home server.

**Notice:**

1. This just a script for my personal use.
2. Since cloud platforms are using VMs to provide services, the CPU core temperature function may not working. This may leads to an exception and the script will sleep for 15s.
3. This script can't directly run on Windows since psutil can't detect sensors' temperature on Windows.
    - Prevent notice 2 and 3 by comment out the `res = get_CPU_Core_Temp()` line.
4. Services related functions require the `systemctl` command.
5. I added `while True` due to the unstable connection to *api.telegram.org* in my area, if you do not have this problem just delete it.

