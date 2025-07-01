import signal
import anubi.mdns as mdns
from  anubi.mdns.dnsrrecords import  DnsRRecordA

# Create the responder instance
responder = mdns.mDNS()

# Create a SIGINT handler
def sigint_handler(sig_num, stack):
    #just to be sure
    if sig_num == signal.SIGINT:
        #stop the responder on SIGINT signal
        responder.stop()
        print('mDSN responder stopped')

# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)
# Create records for DNS
responder.add_record(DnsRRecordA('camera.home.', 120, '192.168.1.12'))
# Start the responder
responder.start()
# Instruct the user how to stop the application
print('mDSN responder started.\nPress CTRL + C to stop it.')
#  Wait untill the responder terminates
responder.join()
