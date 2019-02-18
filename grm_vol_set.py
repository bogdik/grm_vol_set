#!/usr/bin/python
import socket,time,re,sys,getopt


def sett(ip,passwd,cap,play):
	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	new.connect((ip, 8091))

	password=passwd
	cap_vol=cap
	play_vol=play

	#auth main complite
	new.send('')
	time.sleep(0.1)
	data ='589158510f010000'.decode('hex')
	new.send(data)

	time.sleep(0.1)
	data='0a3c3f786d6c2076657273696f6e3d22312e302220656e636f64696e673d2247423233313222203f3e0a3c584d4c5f544f505345453e0a3c4d4553534147455f484541444552204d73675f747970653d22555345525f415554485f4d45535341474522204d73675f636f64653d22434d445f555345525f4155544822204d73675f666c61673d2230222053657373696f6e69643d222220202f3e0a3c4d4553534147455f424f44593e0a3c555345525f415554485f504152414d20557365726e616d653d2261646d696e222050617373776f72643d22'+password.encode('hex')
	data = data.decode('hex')+'2220417574684d6574686f643d223122202f3e0a3c2f4d4553534147455f424f44593e0a3c2f584d4c5f544f505345453e0a'.decode('hex')
	new.send(data)
	time.sleep(0.1)
	data = new.recv(300)
	sessid=repr(data)
	sessid=re.findall(r'Sessionid=".+"', sessid)[0].split('"')[1].encode('hex')
	time.sleep(0.1)
	data = '58915851d3000000'.decode('hex')
	new.send(data)
	#/auth main complite
	#get seetings general
	data = '0a3c3f786d6c2076657273696f6e3d22312e302220656e636f64696e673d2247423233313222203f3e0a3c584d4c5f544f505345453e0a3c4d4553534147455f484541444552204d73675f747970653d2253595354454d5f434f4e54524f4c5f4d45535341474522204d73675f636f64653d223130323022204d73675f666c61673d2230222053657373696f6e69643d22'+sessid
	data = data.decode('hex')+'2220202f3e0a3c4d4553534147455f424f44592f3e0a3c2f584d4c5f544f505345453e'.decode('hex')
	new.send(data)
	time.sleep(0.1)
	data = new.recv(1024)
	time.sleep(0.1)
	data = '58915851'.decode('hex')
	new.send(data)
	#/get seetings general complite
	#get seetings audio
	time.sleep(0.1)
	data = 'a50000003c3f786d6c2076657273696f6e3d22312e302220656e636f64696e673d2247423233313222203f3e3c584d4c5f544f505345453e0a3c4d4553534147455f4845414445520a4d73675f747970653d2253595354454d5f434f4e4649475f4745545f4d455353414745220a4d73675f636f64653d22353032220a4d73675f666c61673d2230220a2f3e3c4d4553534147455f424f44592f3e0a3c2f584d4c5f544f505345453e'.decode('hex')
	new.send(data)
	data = new.recv(300)
	time.sleep(0.1)
	data = '58915851'.decode('hex')
	new.send(data)
	#get seetings audio
	#set audio settings
	data = 'f60000003c3f786d6c2076657273696f6e3d22312e302220656e636f64696e673d2247423233313222203f3e3c584d4c5f544f505345453e0a3c4d4553534147455f4845414445520a4d73675f747970653d2253595354454d5f434f4e4649475f5345545f4d455353414745220a4d73675f636f64653d22353237220a4d73675f666c61673d2230220a2f3e3c4d4553534147455f424f44593e0a3c4361707475726520566f6c756d653d22'+cap_vol.encode('hex')+'2220566f6c756d65506c61793d22'+play_vol.encode('hex')
	data = data.decode('hex')+'2220616d706c6966793d2231222072615f616e737765723d223022202f3e0a3c2f4d4553534147455f424f44593e0a3c2f584d4c5f544f505345453e'.decode('hex')
	new.send(data)
	data = new.recv(1024)
	#/set audio settings complite
	if 'Volume="'+cap_vol+'"' in data and 'VolumePlay="'+play_vol+'"' in data:
		return True
	else:
		return False


def main(argv):
   ip=''
   passwd='admin'
   cap_vol='50'
   play_vol='50'
   try:
      opts, args =getopt.getopt(sys.argv[1:], 'i:p:v:c:', ['i=', 'p=', 'v=', 'c='])
   except getopt.GetoptError:
      print('grm_vol_set.py -i <ipaddress> -p <password> -v <Play Volume> -c <Capture Volume>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('grm_vol_set.py -i <ipaddress> -p <password> -v <Play Volume> -c <Capture Volume>')
         sys.exit()
      elif opt in ("-i", "--ip"):
         ip = arg
      elif opt in ("-p", "--pass"):
         passwd = arg
      elif opt in ("-v", "--vol"):
         play_vol = arg
      elif opt in ("-c", "--cap_vol"):
         cap_vol = arg
   if ip:
     if int(cap_vol)>100 or int(cap_vol)<1 or int(play_vol)>100 or int(play_vol)<1:
         print('Play Volume 1-100  Capture Volume 1-100')
         sys.exit()
     if sett(ip,passwd,cap_vol,play_vol)==False:
          if sett(ip,passwd,cap_vol,play_vol)==False:
             print ('error')
          else:
             print('success')
     else:
        print('success')
   else:
     print('grm_vol_set.py -i <ipaddress> -p <password> -v <Play Volume> -c <Capture Volume>')

if __name__ == "__main__":
   main(sys.argv[1:])
