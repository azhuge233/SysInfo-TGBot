#coding:utf-8
#/usr/bin/python3
import psutil as ps
import telebot, time, requests
TOKEN = ""
ChatID = ""
G = 1024*1024*1024
M = 1024*1024


def tg_push(msg):
    tb = telebot.TeleBot(TOKEN)
    tb.send_message(ChatID, msg)


def get_IP():
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
            res += " Core " + str(i+1) + " : " + str(temp[i].current) + " ℃\n"
        else:
            res += "\tCore " + str(i+1) + " : " + str(temp[i].current) + " ℃"
    
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


def main():
    msg = get_IP()
    msg += get_CPU_Core_Temp()
    msg += get_MEM_Info()
    msg += get_Disk_Info()

    tg_push(msg)


if __name__ == "__main__":
    main()

