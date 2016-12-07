import xml.etree.ElementTree as ET
import pickle

from utils import DATA,TRACKS

class TrackData:

	special_events = -1
	poss = -1

	def __init__(self,special_events,poss):
		self.special_events = special_events
		self.poss = poss

	def length(self):
		return sum([0 if pos == -1 else 1 for pos in self.poss])


class TracksPosition:

	s_pos = -1
	tracks = -1

	def __init__(self,tracks,s_pos):
		self.tracks = tracks
		self.s_pos = s_pos

	def __repr__(self):
		return self.s_pos+"| "+str(self.tracks)

def parsePosition(s_pos):
	C = 0.6449999809265137#pixel width and pixelheight
	
	try:
		tree = ET.parse(TRACKS+s_pos+'.xml')
	except:
		return -1
	root = tree.getroot()
	tracks = []
	for track in root.findall('.//AllTracks/Track'):
		track_id = track.get('TRACK_ID')
		spots_ids = []
		for k,edge in enumerate(track.findall('Edge')):
			spots_ids.append(edge.get('SPOT_SOURCE_ID'))
			spots_ids.append(edge.get('SPOT_TARGET_ID'))
		spots_ids = list(set(spots_ids))
		pos = [-1 for e in range(300)]
		special_events = {}
		for spot_id in spots_ids:
			query = ".//Spot[@ID='"+spot_id+"']"
			spot = root.findall(query)
			if len(spot) > 0:
				spot = spot[0]
				t = int(float(spot.get('POSITION_T')))
				r = float(spot.get('RADIUS'))/C
				x = float(spot.get('POSITION_X'))/C
				y = float(spot.get('POSITION_Y'))/C
				raw_name = spot.get('name')
				if not raw_name.startswith("ID"):
					special_events[t] = raw_name
				tuple_ = (x,y,r)
				pos[t] = tuple_
		track = TrackData(special_events,pos)
		tracks.append(track)
	return TracksPosition(tracks,s_pos)


def loadAll(cache):
	if cache:
		return pickle.load(open(DATA+"cache","r"))
	else:
		res = {}
		for pos in range(1,85):
			print pos
			if pos < 10:
				s_pos = "00"+str(pos)
			else:
				s_pos = "0"+str(pos)
			tps = parsePosition(s_pos)
			if not tps == -1:
				print s_pos
				res[s_pos] = tps
		pickle.dump(res,open(DATA+"cache","w"))
		return res
