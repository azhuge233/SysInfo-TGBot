# coding:utf-8
# /usr/bin/python3
import psutil as ps
import telebot
import os
import subprocess

'''Configure Variables'''
# bot token and test chatid
TOKEN = ""
ChatID = ""

# sudo required
Password = ""

# reboot wait seconds
WaitSec = "10"

G = 1024 * 1024 * 1024
M = 1024 * 1024

tb = telebot.TeleBot(TOKEN)

'''Reply Messages'''
# /info reply message
BOT_INFO = "This is 's private tg bot."

#/help reply message
BOT_HELP = "Commands:\n" \
           "/info - show bot info\n" \
           "/serverinfo - return machine's status\n" \
           "/service - control system service using systemctl\n" \
           "/execute - run any commands on server" \
           "/reboot - reboot system"


'''Functions'''
def get_IP():
    ip = ""
    res = "From Machine IP: "
    net_info = ps.net_if_addrs()
    for each in net_info.keys():
        if each[0] == 'e':
            ip = str(net_info[each][0].address)
            break

    res += ip + "\n"
    return res + "\n"


def get_CPU_Core_Temp():
    res = "CPU Temperature\n"
    temp = ps.sensors_temperatures()['coretemp']
    for i in range(0, len(temp)):
        if (i % 2) == 1:
            res += " Core " + str(i + 1) + " : " + str(temp[i].current) + " ℃\n"
        else:
            res += "\tCore " + str(i + 1) + " : " + str(temp[i].current) + " ℃"

    return res + "\n"


def get_MEM_Info():
    res = "Memory Info\n"
    tol_swap = ps.swap_memory().total
    avail_swap = ps.swap_memory().free
    swap_percent = ps.swap_memory().percent
    tol_mem = ps.virtual_memory().total
    avail_mem = ps.virtual_memory().available
    mem_percent = ps.virtual_memory().percent

    res += "\tMemory Usage: " + str(mem_percent) + "%\t"
    if avail_mem >= G:
        res += "\tAvailable: " + str(round(avail_mem / G, 2)) + "G\t"
    else:
        res += "\tAvailable: " + str(round(avail_mem / M, 2)) + "M\t"
    res += "\tTotal: " + str(round(tol_mem / G, 2)) + "G\n"

    res += "\tSwap Usage: " + str(swap_percent) + "%\t"
    if avail_swap >= G:
        res += "\tAvailable: " + str(round(avail_swap / G, 2)) + "G\t"
    else:
        res += "\tAvailable: " + str(round(avail_swap / M, 2)) + "M\t"
    res += "\tTotal: " + str(round(tol_swap / G, 2)) + "G\n"

    return res + "\n"


def get_Disk_Info():
    res = "Disk Info\n"
    partitions = ps.disk_partitions()
    for each in partitions:
        if "sd" in each.device:
            usage = ps.disk_usage(each.mountpoint)
            res += "\t" + each.mountpoint + " Usage: "
            res += str(usage.percent) + "%\n"
            if usage.free > G:
                res += "\t\tFree: " + str(round(usage.free / G, 2)) + "G\t"
            else:
                res += "\t\tFree: " + str(round(usage.free / M, 2)) + "G\t"
            if usage.used > G:
                res += "\t\tUsed: " + str(round(usage.used / G, 2)) + "G\t"
            else:
                res += "\t\tUsed: " + str(round(usage.used / M, 2)) + "G\t"
            if usage.total > G:
                res += "\t\tTotal: " + str(round(usage.total / G, 2)) + "G\n"
            else:
                res += "\t\tTotal: " + str(round(usage.total / M, 2)) + "G\n"
    return res + "\n"


def reboot(query):
    chatid = query.message.chat.id
    tb.answer_callback_query(query.id)

    # print(query.data)

    if query.data.startswith('reboot-No'):
        tb.send_message(query.message.chat.id, "Aborting reboot call.")
        return

    try:
        tb.send_message(chatid, "Rebooting system in " + WaitSec + " second(s).")
        tb.send_message(chatid, "Bye~")

        command = "sleep %s && echo %s | sudo -S reboot"
        res = subprocess.getoutput(command % (WaitSec, Password))

        if res != 0:
            tb.send_message(query.message.chat.id, "Sorry, Bye Failed!\nError : " + res)
    finally:
        pass


'''Message Handler'''
@tb.message_handler(commands=['help'])
def send_help(msg):
    tb.reply_to(msg, BOT_HELP)


@tb.message_handler(commands=['info'])
def send_info(msg):
    tb.reply_to(msg, BOT_INFO)


@tb.message_handler(commands=['serverinfo'])
def send_server_info(msg):
    res = get_IP()
    res += get_CPU_Core_Temp()
    res += get_MEM_Info()
    res += get_Disk_Info()

    tb.reply_to(msg, res)


@tb.message_handler(commands=['service'])
def service_op(msg):
    args = msg.text.split()

    if len(args) != 3:
        tb.reply_to(msg, "2 arguments required!\nUsage: /service [start|stop|restart|...] [service name]")
        return

    command = "echo %s | sudo -S systemctl %s %s"
    try:
        if args[1] == "status":
            res = subprocess.getoutput(command % (Password, args[1], args[2]))
            if res.endswith('could not be found.'):
                tb.reply_to(msg, "Service " + args[2] + " could not be found.\n")
            else:
                tb.reply_to(msg, str(res.split('●')[1]))
            return
        else:
            res = os.system(command % (Password, args[1], args[2]))

        if res == 0:
            tb.reply_to(msg, "Service " + args[2] + " " + args[1] + " Successfully.")
        elif res == 256:
            tb.reply_to(msg, "Service " + args[2] + " " + args[1] + " Failed.\nService command " + args[1] +
                        " does not exist.")
        elif res == 1280:
            tb.reply_to(msg, "Service " + args[2] + " " + args[1] + " Failed.\nService " + args[2] + " does not exist.")
        else:
            tb.reply_to(msg, "Service " + args[2] + " " + args[1] + " Failed.\nError Code: " + str(res))
    finally:
        pass


@tb.message_handler(commands=['reboot'])
def reboot_confirm(msg):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Confirm', callback_data='reboot-Yes'),
        telebot.types.InlineKeyboardButton('Cancel', callback_data='reboot-No')
    )

    tb.send_message(msg.chat.id, "Are you sure to reboot the system?", reply_markup=keyboard)


@tb.message_handler(commands=['execute'])
def execute_commands(msg):
    args = msg.text.split()

    if len(args) == 1:
        tb.reply_to(msg, "Command required!\nUsage: /execute [your command: (cat file.txt) etc.]")
        return

    command = ""
    for i in range(1, len(args)):
        if args[i] == 'sudo' and args[i+1] != '-S':
            tb.reply_to(msg, "If you are using commands require sudo privilege, you need to pass the password with "
                             "'echo [your password] |' then add '-s' argument after 'sudo' command.")
        command += args[i] + " "
    command = command.rstrip()

    try:
        res = subprocess.getoutput(command)
        tb.reply_to(msg, "Execution result:\n" + res)
    finally:
        pass


'''Query Handler'''
@tb.callback_query_handler(func=lambda call: True)
def callback(query):
    data = query.data
    if data.startswith('reboot-'):
        reboot(query)


def main():
    tb.polling(none_stop=True)


if __name__ == "__main__":
    main()

