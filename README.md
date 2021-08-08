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

3. Fill in `TOKEN`, `ChatID`, `IPCAddress` and `IPCPassword`, then change `Password` to your system user's password (systemd needs privilege).

   - Modify `WaitSec` if you want to wait longer/shorter before rebooting (default is 10 seconds).
   - Modify `BOT_INFO` to your own info message.

4. Then run

   ```shell
   python3 run.py
   ```

Tested on Debian 11 home server.

**Notice:**

1. This script can't directly run on Windows since psutil can't detect sensors' temperature on Windows. You need to comment out the `get_CPU_Core_Temp()` function.
2. Requires the `systemctl` command.
3. I added `while True` due to the unstable connection to *api.telegram.org* in my area, if you do not have this problem then delete it.
4. Since cloud platforms are using virtual machine to provide service, the CPU core temperature function may not working if you are using VPS. This may leads to an exception and the script will sleep for 15s.
   - Prevent this by comment out the `res = get_CPU_Core_Temp()` line.

