import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

from msi import *
import serial
import cherrypy
from cherrypy.lib.static import serve_file
	

print "****************************"
print "Starting Marantz Web Service"
print 'MSW: Python Version   : ' + platform.python_version()
print 'MSW: PySerial Version : ' + serial.VERSION

serialIn = serial.Serial('/dev/ttyS0', 9600, bytesize=8, parity='N', stopbits=1, timeout=0)
print 'MSW: Connection success - Port: ' + serialIn.portstr

marantzSerialInt = MarantzSerialInterface(serialIn)
marantzSerialInt.start()


class WebApp:
	def index(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		return open(os.path.join(current_dir, 'html', 'mobileInterface.html'))

	index.exposed = True
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def status(self, **kwargs):
		aStatus = marantzSerialInt.status()
		return {"power" : aStatus.pwr, "source" : aStatus.src, "volume": aStatus.vol, "mute" : aStatus.mute, "attenuate" : aStatus.att, "treble" : aStatus.treble, "bass" : aStatus.bass}
		
	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def powerOn(self, **kwargs):
		marantzSerialInt.cmdMeta('powerOn')
		return {"message" : "ACK"}

	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def powerOff(self, **kwargs):
		marantzSerialInt.cmdMeta('powerOff')
		return {"message" : "ACK"}
		
	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def volumeUp(self, **kwargs):
		marantzSerialInt.cmdMeta('volumeUp')
		return {"message" : "ACK"}
		
	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def volumeDown(self, **kwargs):
		marantzSerialInt.cmdMeta('volumeDown')
		return {"message" : "ACK"}

	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def muteOn(self, **kwargs):
		marantzSerialInt.cmdMeta('muteOn')
		return {"message" : "ACK"}

	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def muteOff(self, **kwargs):
		marantzSerialInt.cmdMeta('muteOff')
		return {"message" : "ACK"}


	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def changeSource(self, src):
		marantzSerialInt.cmd('SRC', src + "" + src)
		return {"message" : "ACK"}
		
	@cherrypy.expose
	@cherrypy.tools.json_out()		
	def listSources(self, **kwargs):
		return marantzSerialInt.sources()


#cherrypy.config.update('prod.conf')
#cherrypy.config.update({'server.socket_host': '0.0.0.0', 
                         #'server.socket_port': 9999, 
                        #})

cherrypy.quickstart(WebApp(), '/', 'webservice.cfg')
