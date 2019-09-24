# SysInfo-TGBot

A python script let you control your server using telegram bot.

## Requirements

- python 3.6
- psutil (5.6.3)
- pyTelegramBotAPI (3.6.6)

## Usage

1. Modify `TOKEN` and `ChatID` to your own bot‘s information, change `Password` to your system user's password (system service needs privilege).

   - Modify `WaitSec` if you want to wait longer/shorter before rebooting (default is 10 seconds).
   - Modify `BOT_INFO` to your own info message.

2. Then run

   ```shell
   python3 run.py
   ```

Tested on a Ubuntu 18.04 server.

**Notice:**

1. This script can't directly run on Windows since psutil can't detect sensors' temperature on Windows platform. You need to comment out the `get_CPU_Core_Temp()` function.
2. System service function requires the `systemctl` command.
3. Now it's recommended to use the script as system service instead of adding `&` in CLI, since it has the `while True` part.
   - I added `while True` due to the unstable connection to *api.telegram.org* in my area, if you do not have this problem then delete it.