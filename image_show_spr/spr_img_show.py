import cv2,snap7,time
dic={}
file = open('file.pbtxt', "r")
for line in file:
    data=line.strip().split("=")
    a=data[0]
    b=data[1]
    dic[a]=b
PLC_ipaddress=dic['plc_ipaddress']
db_number=int(dic['plc_db_number'])
sw=int(dic['show_width'])
sh=int(dic['show_height'])
# start
start_position=int(dic['start_position'])
max_size_of_string=int(dic['max_size_of_string'])
plc_delay=int(dic["plc_communication_delay_in_milliseconds"])/1000

while True:
    try:
        client=snap7.client.Client()
        client.connect(PLC_ipaddress,0,1,102)
        print(bool(client.get_connected))
        print("PLC connected")
        break
    except:
        print("PLC not connected")
        time.sleep(.1)
        # break
while True:
    # model="model1"
    plc_data=bytearray(client.db_read(db_number,start_position,max_size_of_string))
    # plc_data=b'model1\x00\x00'
    model=plc_data.decode().strip("\x00")
    print(model)
    try:
        frame =cv2.imread(dic[model])
    except:
        frame=cv2.imread(dic["dummy_image"])
        cv2.putText(frame, 'Kindly update model and image for part number : {}'.format(model), (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2,cv2.LINE_8)
    cv2.imshow('Frame', cv2.resize(frame,(sw,sh)))
        # # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(plc_delay)
# Closes all the frames
client.disconnect()
cv2.destroyAllWindows()
# cv2.COLOR_RGB2

