from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys, select
import csv
import time

__author__ = 'brian.mcmillan@steeplesquare.co.uk'

										# Saved definitions 
ColoursSource = "Colours.rgb"
FixturesSource = "Fixtures."
PatternsSource = "Patterns.Data"
SequencesSource = "Sequences.Data"

# http://www.rentaliowa.com/pa_system_rentals/rgbcolorchart.htm
# http://www.blue-room.org.uk/wiki/RGB_Colours
# https://www.nlfxpro.com/ben-stowes-rgbaw-color-mixing-chart/


class c_Patterns:
	def __init__(self):
		PatternsFile = open(PatternsSource)
		PatternsData = csv.reader(PatternsFile, delimiter=',', quotechar='"')
		self.Patterns_Count=0
		self.Patterns = []
		for Pattern in PatternsData:
			Values = [str.strip(column) for column in Pattern]
			print(Values)
			if self.Patterns_Count == 0:
				self.Patterns.insert(0,Values)
				self.Patterns_Count += 1
			else:
				self.Patterns.append(Values)
				self.Patterns_Count += 1
		print ("Read ", self.Patterns_Count, " pattern definitions from file")

	def Print(self):
		for Pattern in self.Patterns:
			TmpStr = "Pattern: " + Pattern[0] + " [" + Pattern[1]
			for i in range(2,len(Pattern)):
			 	TmpStr +=  ", " + Pattern[i]
			TmpStr += "]"
			print(TmpStr)

class c_Sequences:
	def __init__(self):
		SequencesFile = open(SequencesSource)
		SequencesData = csv.reader(SequencesFile, delimiter=',', quotechar='"')
		self.Sequences_Count=0
		self.Sequences = []
		for Sequence in SequencesData:
			Values = [int(column) for column in Sequence]
			self.Sequences.append(Values)
			self.Sequences_Count += 1
		print ("Read ", self.Sequences_Count, " sequence definitions from file")

	def Print(self):
		for Sequence in self.Sequences:
			print("Sequence ", Sequence[0], 
			      ", Group: ", Sequence[1], 
				  ", Pattern: ", Sequence[2])


class c_Group:
	def __init__(self):
		self.Group = []

	def Add(self,Fixture):
		self.Group.append(Fixture)

	def Print(self):
		print(self.Group)

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

	def Print(self):		
		for Colour in self.Colours:
			print ("{0:12s} DMXRGB: {1:4d},{2:4d},{3:4d}".format(Colour[0],
																 Colour[1],
																 Colour[2],
																 Colour[3]) )

class c_Fixtures:
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
		
	def Send(self, Universe):
		print("Sending")


if __name__ == '__main__':

	ColourTable = c_ColourTable()
	ColourTable.Print()

	PatternList = c_Patterns()
	PatternList.Print()

	Fixtures = c_Fixtures("Promo")
	Fixtures.Print()

	Sequences = c_Sequences()
	Sequences.Print()

	BarA = c_Group()
	BarA.Add(1)
	BarA.Add(3)
	BarA.Add(6)

	BarA.Print()


#	while True:
	for i in range(10):	
		Fixtures.Send(1)
		time.sleep(0.5)
		print("Awake")
# Check for enter pressed		
		i,o,e = select.select([sys.stdin],[],[],0.0001)
		if i == [sys.stdin]: break
	print ("BYE BYE")

	Fixtures.Save()
