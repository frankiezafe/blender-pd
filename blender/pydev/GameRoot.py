import bge
import math
import random
import mathutils
from mathutils import Vector, Matrix, Euler, Quaternion

class GameRoot():
	
	def __init__( self ):
		
		print("GameRoot __init__ start")

		# reconfiguration of the ESC key in keyboardEvents below
		bge.logic.setExitKey( bge.events.F12KEY )

		scene = bge.logic.getCurrentScene()
		self.root = scene.objects["root"]
		self.avatar= scene.objects["stdman"]
		self.runs = True

		self.rest = {}
		self.eulers = {}
		
		# ------------ collecting all matrices ---------------- #
		for c in self.avatar.channels:
			cn = c.name
			print( cn )
			#self.rest[ cn ] = c.pose_matrix
			self.rest[ cn ] = mathutils.Matrix( c.pose_matrix )
			self.eulers[ cn ] = [ 0,0,0 ]
		
		# ThreadOsc will read these 2 params
		self.rcvdata = []	   # array to hold data
		self.rcvmutex = False   # mutex, ThreadOsc will wait for it to be False before writting the data
		print( bge.threadosc )
		bge.threadosc.addListener( self )
		
		print("GameRoot __init__ end")
	
	def exists( self ):
		return True
	
	def exit( self ):
		print( "ESC" )
		try:
			bge.threadosc.stop()
			bge.threadosc.killall()
			del bge.threadosc
			self.runs = False
		except:
			print( "OSC thread not killed..." )
	
	def keyboardEvents( self ):
		kbe = bge.logic.keyboard.events
		
		if kbe[ bge.events.ESCKEY ] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			self.exit()

	def oscEvents( self ):
		
		self.rcvmutex = True
		tmp = list( self.rcvdata )
		self.rcvdata = []
		self.rcvmutex = False
		
		if len( tmp ) == 0:
			return

		# print( "received", len( tmp ), "message(s)" )
		for data in tmp:
			if data[0] == "/avatar/bone/rot" :
				for d in range( len( data ) ):
					if d < 2:
						continue
					dn = d - 2
					if dn % 4 == 0:
						bname = str( data[ d ] )
						try:
							agls = self.eulers[ bname ]
							agls[ 0 ] += (float( data[ d+1 ] ) - agls[ 0 ])  * 0.85
							agls[ 1 ] += (float( data[ d+2 ] ) - agls[ 1 ])  * 0.85
							agls[ 2 ] += (float( data[ d+3 ] ) - agls[ 2 ])  * 0.85
							d += 4
						except:
							print( "OSC format error, no bone named '", bname, "'!" )
			elif data[0] == "/avatar/reset" :
				for cn in self.rest:
					self.eulers[ cn ][ 0 ] = 0
					self.eulers[ cn ][ 1 ] = 0
					self.eulers[ cn ][ 2 ] = 0
			elif data[0] == "/avatar/print" :
				print( self.eulers )
			else:
				print( d )
	
	def update( self ):
		
		self.keyboardEvents()
		self.oscEvents()

		for cn in self.rest:
			channel = self.avatar.channels[ cn ]
			mat = mathutils.Matrix( self.rest[ cn ] )
			agls = self.eulers[ cn ]
			channel.joint_rotation = (0,0,0)
			channel.rotation_mode = bge.logic.ROT_MODE_XYZ
			channel.rotation_euler = agls
			#print( cn, self.eulers[ cn ], channel.rotation_euler )

		self.avatar.update()

		return self.runs

try:
	
	# dependencies
	bge.threadosc.exists()
	
	try:
		bge.gameroot.exists()
	except:
		bge.gameroot = GameRoot()
	
except:
	pass
