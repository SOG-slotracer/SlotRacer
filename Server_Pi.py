import socket
import datetime
import time


UDP_IP = ' 127.0.0.1'
#UDP_PORT = 4242
inner_track_p1 = ["376.332703,327.166351", "327.332703,327.166351", "283.332703,322.166351", "231.332703,329.166351",
               "183.332703,324.166351", "139.332703,319.166351", "105.332703,303.166351", "85.332703,270.166351",
               "73.332703,231.166351", "71.332703,191.166351", "78.332703,146.166351", "87.332703,121.166351",
               "106.332703,94.166351", "139.332703,72.166351", "172.332703,76.166351", "196.332703,96.166351",
               "216.332703,125.166351", "227.332703,157.166351", "244.332703,182.166351", "260.332703,196.166351",
               "274.332703,211.166351", "309.332703,223.166351", "348.332703,224.166351", "400.332703,222.166351",
               "431.332703,223.166351"]

inner_track_p2 = ["475.332703,222.166351", "519.332703,225.166351", "549.332703,219.166351", "596.332703,221.166351"]

inner_track_p3 = ["647.332703,224.166351", "684.332703,224.166351", "719.332703,237.166351", "745.332703,260.166351",
                  "756.332703,289.166351", "763.332703,318.166351", "769.332703,348.166351", "763.332703,379.166351",
                  "751.332703,420.166351", "723.332703,461.166351", "693.332703,474.166351", "651.332703,463.166351",
                  "624.332703,430.166351", "607.332703,391.166351", "586.332703,357.166351", "550.332703,331.166351",
                  "499.332703,324.166351", "458.332703,323.166351", "411.332703,324.166351"]

outer_track_p1 = ["396.332703,374.166351", "354.332703,373.166351", "309.332703,371.166351", "276.332703,372.166351",
                  "227.332703,372.166351", "173.332703,372.166351", "123.332703,365.166351", "86.332703,337.166351",
                  "66.332703,310.166351", "50.332703,272.166351", "40.332703,230.166351", "42.332703,188.166351",
                  "45.332703,154.166351", "53.332703,118.166351", "66.332703,82.166351", "94.332703,49.166351",
                  "121.332703,32.166351", "167.332703,27.166351", "197.332703,43.166351", "226.332703,70.166351",
                  "243.332703,103.166351", "259.332703,137.166351", "275.332703,156.166351", "309.332703,173.166351",
                  "353.332703,173.166351", "403.332703,175.166351", "433.332703,175.166351"]

outer_track_p2 = ["469.332703,171.166351", "510.332703,172.166351", "546.332703,170.166351", "590.332703,170.166351"]

outer_track_p3 = ["639.332703,173.166351", "673.332703,171.166351", "711.332703,180.166351", "742.332703,201.166351",
                  "764.332703,229.166351", "780.332703,256.166351", "787.332703,284.166351", "795.332703,312.166351",
                  "797.332703,359.166351", "793.332703,398.166351", "780.332703,431.166351", "772.332703,457.166351",
                  "756.332703,484.166351", "731.332703,508.166351", "699.332703,523.166382", "658.332703,518.166382",
                  "626.332703,495.166351", "603.332703,463.166351", "581.332703,423.166351", "556.332703,385.166351",
                  "514.332703,375.166351", "471.332703,373.166351", "430.332703,374.166351"]

inner_to_outer_track = ["470.332703,213.166351", "518.332703,205.166351", "561.332703,190.166351", "612.332703,181.166351"]

outer_to_inner_track = ["459.332703,179.166351", "496.332703,186.166351", "531.332703,197.166351", "568.332703,203.166351",
                        "608.332703,215.166351"]
final_track = inner_track_p1 + inner_track_p2 + inner_track_p3 + inner_track_p1 + inner_to_outer_track + \
              outer_track_p3 + outer_track_p1 + outer_to_inner_track + inner_track_p3

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#ry:
ip_port = ('127.0.0.1',4242)
sock.bind(ip_port)
print("Binding is complete")
print("waiting for client") 
i = 0
data, addr = sock.recvfrom(1024)
while True:
    print(data)
    text = final_track[i]
    try:
        sock.settimeout(0.0001)
        data2, addr2 = sock.recvfrom(1024)
        print(data2)
        sock.sendto(text.encode('utf-8'), addr)
        time.sleep(0.05)
        i += 1
        if i == len(final_track):
            i = 0
        continue
    except socket.timeout:
        time.sleep(0.1)
        print(text)
        sock.sendto(text.encode('utf-8'), addr)
        i += 1
        if i == len(final_track):
            i = 0
        print("gothere")
        continue