from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys, select
import csv
import time
import threading
import Tkinter
import ttk

__author__ = 'brian.mcmillan@steeplesquare.co.uk'

										# Saved definitions 
ColoursSource = "Colours.rgb"
FixturesSource = "Fixtures."
GroupsSource = "Groups.Data"
PatternsSource = "Patterns.Data"
SequencesSource = "Sequences.Data"

# http://www.rentaliowa.com/pa_system_rentals/rgbcolorchart.htm
# http://www.blue-room.org.uk/wiki/RGB_Colours
# https://www.nlfxpro.com/ben-stowes-rgbaw-color-mixing-chart/


DMXData = array.array('B')
global StrideLength 								# Duration between steps through sequences


def DmxSent(status):
    if status.Succeeded():
#    print('Success!')
	    pass
    else:
        print('Error: %s' % status.message, file=sys.stderr)

    global wrapper
    if wrapper:
        wrapper.Stop()

class Signal:									# This tells the main DMX loop to keep running
	go = True

def getKey0(list):								# Need this to sort the Fixtures
	return(list[0])

class c_Patterns:
	def __init__(self):
		PatternsFile = open(PatternsSource, mode='r')
		PatternsData = csv.reader(PatternsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		self.Patterns_Count=0
		self.Patterns = []
		for Pattern in PatternsData:
			Members = list(Pattern[1].strip('[]').split(',') )
			Members = [Member.strip() for Member in Members]  			# Remove leading or trailing spaces
			Values = [int(Pattern[0]), Members]
			self.Patterns.append(Values)
			self.Patterns_Count += 1
		PatternsFile.close()				
		print ("Read ", self.Patterns_Count, " pattern definitions from file")

	def Get(self, ID):
		for Pattern in self.Patterns:
			if int(Pattern[0]) == ID:
				return Pattern[1]	

	def Print(self):
		for Pattern in self.Patterns:
			print ("Pattern {:03d}, {:40s}".format(Pattern[0],str(Pattern[1]) ))


class c_Sequences:
	def __init__(self):
		SequencesFile = open(SequencesSource)
		SequencesData = csv.reader(SequencesFile, delimiter=',', quotechar='"')
		self.Sequences_Count=0
		self.Sequences = []
		for Sequence in SequencesData:
			Values = [int(column) for column in Sequence]
			Values.append(0)					# Add a column to track where in the group
			Values.append(0)					# Add a column to track where in the pattern
			self.Sequences.append(Values)
			self.Sequences_Count += 1
		print ("Read ", self.Sequences_Count, " sequence definitions from file")
		SequencesFile.close()

	def Get(self):
		return self.Sequences

	def Update(self, Seq, GIndex, PIndex):					# Update the Increment which keeps track of where we are in the pattern
		for index, Sequence in enumerate(self.Sequences):
			if Sequence[0] == Seq:
				Sequence[4] = GIndex
				Sequence[5] = PIndex
				self.Sequences[index] = Sequence

	def Print(self):
		for Sequence in self.Sequences:
			print("Sequence ", Sequence[0], 
			      ", Group: ", Sequence[1], 
				  ", Pattern: ", Sequence[2],
				  ", Enabled: ", bool(Sequence[3]) )


class c_Groups:
	def __init__(self):
		self.Groups = []
		self.Groups_Count = 0
		GroupsFile = open(GroupsSource, mode='r')
		GroupsData = csv.reader(GroupsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for GroupInfo in GroupsData:
			Members = list(GroupInfo[2].strip('[]').split(','))
			Members = [int(Member) for Member in Members]
			Values = [int(GroupInfo[0]), int(GroupInfo[1]), Members]
			self.Groups.append(Values)
			self.Groups_Count += 1
		GroupsFile.close()				

	def Add(self,Fixtures):
		Values = [self.Groups_Count, len(Fixtures), Fixtures]
		self.Groups.append(Values)
		self.Groups_Count += 1

	def Get(self, ID):						# Return the members as a list
		for Group in self.Groups:
			if Group[0] == ID:
				return Group[2]		

	def Print(self):
		for Group in self.Groups:
			print(Group)

	def Save(self):
		GroupsFile = open(GroupsSource, mode='w')
		GroupsData = csv.writer(GroupsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for GroupInfo in self.Groups:
			GroupsData.writerow(GroupInfo)
		GroupsFile.close()			

class c_ColourTable:
	def __init__(self):
		ColoursFile = open(ColoursSource)
		ColoursData = csv.reader(ColoursFile, delimiter=',', quotechar='"')
		self.Colours_Count=0
		self.Colours = []
		for Colour in ColoursData:
			if self.Colours_Count == 0:
				self.Colours.insert(0,[Colour[0], 
						              int(Colour[1]),
									  int(Colour[2]),
									  int(Colour[3])] )
				self.Colours_Count += 1
			else:
				self.Colours.append([Colour[0], 
						            int(Colour[1]),
									int(Colour[2]),
									int(Colour[3])] )
				self.Colours_Count += 1
		ColoursFile.close()
		print ("Read ", self.Colours_Count, " colour definitions from file")

	def Get(self, ColourPick):
		for Colour in self.Colours:
			if Colour[0] == ColourPick:
				RGB = [Colour[1], Colour[2], Colour[3]]
		return RGB

	def Print(self):		
		for Colour in self.Colours:
			print ("{0:12s} DMXRGB: {1:4d},{2:4d},{3:4d}".format(Colour[0],
									     Colour[1],
									     Colour[2],
									     Colour[3]) )

class c_Fixtures:
	global ColourTable

	def __init__(self, CollectionName):
		FixturesFile = open(FixturesSource + CollectionName)
		FixturesData = csv.reader(FixturesFile, delimiter=',', quotechar='"')
		self.Fix_Count=0
		self.Fixtures = []
		for Fixture in FixturesData:
			Values = [int(column) for column in Fixture]
#			print(Values)
			if self.Fix_Count == 0:
				self.Fixtures.insert(0, Values)
				self.Fix_Count += 1
			else:
				self.Fixtures.append(Values)
				self.Fix_Count += 1
		self.CollectionName = CollectionName
		FixturesFile.close()
		sorted(self.Fixtures, key=getKey0)					# Sort on Column 0 
		print ("Read ", self.Fix_Count, " fixtures from file")

	def Add(self, ID, BaseAddr, Type):
		if Type == "StdRGB":
			self.Fixtures.append ([self.Fix_Count, BaseAddr, BaseAddr+1, BaseAddr+2, 0, 0, Type])
			print ("Added fixture ID:", self.Fix_Count)
			self.Fix_Count += 1

	def Get(self, ID):
		for Fixture in self.Fixtures:
			if Fixture[0] == ID:
				return Fixture

	def Print(self):		
		for Fixture in self.Fixtures:
			print ("ID: {0:04d} RGB LEDs: {1:3d},{2:3d},{3:3d}".format(Fixture[0],
										   Fixture[1],
										   Fixture[2],
										   Fixture[3]) )			

	def Save(self):
		FixturesFile = open(FixturesSource + self.CollectionName, mode='w')
		FixturesData = csv.writer(FixturesFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for Fixture in self.Fixtures:
			FixturesData.writerow(Fixture)
		FixturesFile.close()
		
	def SetColour(self, ID, Colour):
#		print("Fixtures.setcolour: {:3d} {:10s}".format(ID, Colour))
		RGB = ColourTable.Get(Colour)
		Fixture = self.Fixtures[ID]
		for i in range(1,4):
			DMXData[Fixture[i]] = RGB[i-1]
			

				



def Stride():						# Go through all the sequences and increment by one step
	global Fixtures
	global PatternList

	for Sequence in Sequences.Get():
		if Sequence[3] == True:
			Group = Groups.Get(Sequence[1])
#			NFix = len(Group)
			Pattern = PatternList.Get(Sequence[2])
			NColours = len(Pattern)
			GroupIndex = Sequence[4]
			PatternIndex = Sequence[5]
			for Fixture in Group:	
				Fixtures.SetColour(Fixture,Pattern[PatternIndex])
				PatternIndex += 1
				if PatternIndex == NColours:
					PatternIndex = 0
			Sequences.Update(Sequence[0], GroupIndex, PatternIndex)	

class DMXLooper:



	def __init__(self):
		global StrideLength		
		self._RunOK = True

		StrideLength = 1.0					# 1 second gap between strides

		for i in range(512):				# Create and initialise DMX Universe
			DMXData.insert(i, 0)


	def terminate(self):
		for i in range(512):				# Zero out the universe
			DMXData.insert(i, 0)
		self.client.SendDmx(Universe, DMXData, DmxSent)			
		self._RunOK = False

	def run(self, Universe, Count):
		global wrapper
		wrapper = None
		wrapper = ClientWrapper()
		self.client = wrapper.Client()  

		while self._RunOK:
			Stride()
			self.client.SendDmx(Universe, DMXData, DmxSent)
			wrapper.Run()					# send 1 dmx frame
	#		print(DMXData[:50])
			time.sleep(StrideLength)
			

if __name__ == '__main__':

	global PatternList
	global ColourTable
	global Fixtures
	

	ColourTable = c_ColourTable()
	ColourTable.Print()

	PatternList = c_Patterns()
	PatternList.Print()

	Fixtures = c_Fixtures("Promo")
	Fixtures.Print()

	Sequences = c_Sequences()
	Sequences.Print()

	Groups = c_Groups()
	Groups.Print()
	
	Universe = 1
	Count = 0
	dmxloop = DMXLooper()
	looper = threading.Thread(target=dmxloop.run, args=(Universe, Count))
	looper.start()

	while True:
		kbd_input = raw_input('\nCMD> ')
		if len(kbd_input) == 0:
			break
		try:
			print ("You want me to " + kbd_input)
			if kbd_input == 'P':
				PatternList.Print()
			if kbd_input == 'S':
				Sequences.Print()
		except:
			pass
		else:
			pass
		finally:
			pass

	dmxloop.terminate()
	looper.join()
	Fixtures.Save()
	Groups.Save()
