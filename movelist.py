"""
Movelist
"""

import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import NotationParser
import random
import requests
from shutil import copyfile
import re

from NotationParser import ParseMoveList

class MoveList:

    def __init__(self, char_id):
        self.directory = "TekkenData/Movelists/"
        self.CharXml = self.GetMovelistByCharID(char_id)
        self.CharName = self.CharXml.getroot().attrib['name']
        try:
            self.FullName = self.CharXml.getroot().attrib['fullname']
        except:
            self.FullName = ""
            
        self.allMoves = self.CharXml.getroot()[0]
#                    for move in char_root.findall("./moves/move"):
#                        print(move.findall("command")[0].text)
                    #self.CharXml = data_file
                    #self.allMoves = char_root[0]
        try:
            self.allMoves
        except:
            raise Exception("Character Movelist Not Found.")
#        try:
#            url = 'http://www.seattletekken.com/modules/academy/src/characters/'
#            char = self.CharXml.getroot().attrib['name']
#            print(char)
#            r = requests.get(url + char + '/movelist/movelist.xml')
#            if r.ok:
#                print("Retrieved updated movelist")
#        except:
#            raise Exception("Can't load xml from website")
        
        self.gameplan = []
        self.gameplanIndex = 0
        stances = self.GetStances()
        self.stances = {}
        for stance in stances:
            stanceName = stance.find("name").text
            self.stances[stanceName] = []
            moveNames = stance.findall(".//movename")
            for moveName in moveNames:
                self.stances[stanceName].append(moveName.text)


    def getMoveCommand(self, move, stanceEntry=None):
        if move == None:
            return
            
        stanceXml = move.find(".//stance")
        command = move.find(".//command").text
        if(stanceXml != None):
            stanceEntryXml = self.CharXml.findall(".//stances/stance[name='" + stanceXml.text + "']/entry")
            if(stanceEntry == None):
                entry = random.choice(stanceEntryXml)
            else:
                entry = stanceEntryXml[stanceEntry]
            command = entry.find('command').text + ", " + entry.find('entryDelay').text + ", " + command
        
        #inputs = []
        #for inputXml in inputsXml:
        #    inputs.append(inputXml.text)
        #s = ", "
        return command
        
    def updateMoveCommand(self, move, NewCommand):
        move.find(".//command").text = NewCommand

    def getParsedCommand(self, move):
        return ParseMoveList(self.getMoveCommand(move))
        
    def getRandomMove(self):
        #foundMoves = self.CharXml.findall("")
        #return random.choice(self.CharXml.findall(".//Punishable/../.."))
        return random.choice(self.gameplan)
            
    def shuffleGameplan(self):
        if len(self.gameplan) > 1:
            random.shuffle(self.gameplan)
            
    def getNextGameplanMove(self):
        if self.gameplanIndex >= len(self.gameplan):
            self.gameplanIndex = 0
        if self.gameplan:
            move = self.gameplan[self.gameplanIndex]
        else:
            move = None
        
        self.gameplanIndex = self.gameplanIndex + 1
        
        return move
        
    def getMoveById(self, id):
        return self.CharXml.find(".//moves/move[id='" + str(id) + "']")
    
    def setGameplan(self):
        #Just get punishable moves
        self.gameplan = self.CharXml.findall(".//Punishable/../..")
        #print(self.gameplan)
        
    def getMoveName(self, move):
        return move.find(".//name").text

    def getGameplan(self, id):
        gp = self.CharXml.find(".//gameplan[id='" + str(id) + "']/moves")
        moves = []
        for id in gp:
            moves.append(self.getMoveById(id.text))
        self.gameplan = moves
    
    def removeMoveFromGameplan(self, move):
        self.gameplan.remove(move)
    
    def getMoveId(self, move):
        return move.find(".//id").text
        
    def getMoveOnBlock(self, move):
        OnBlock = move.find(".//BlockFrame").text
        if OnBlock == None:
            return "N/A"
        else:
            return OnBlock
    
    def GetStances(self):
        return self.CharXml.findall(".//stances/stance")
        
    def GetStanceFromGameMove(self, moveName):
        for stance, names in self.stances.items():
            for name in names:
                if(name == moveName):
                    return stance
        return None

    def GetAllMoveIds(self):
        moves = self.CharXml.findall(".//moves/move")
        moveList = []
        for move in moves:
            moveList.append(self.getMoveId(move))
        return moveList

    def GetAllMoveIdsAndNames(self):
        moves = self.CharXml.findall(".//moves/move")
        moveList = []
        for move in moves:
            moveList.append(self.getMoveId(move) + ": " + self.getMoveName(move))
        return moveList
    
    def GetPunishers(self, frames, standing):
        if(standing):
            punishers = self.CharXml.findall(".//punishers/punish/standing/..")
        else:
            punishers = self.CharXml.findall(".//punishers/punish/whilerising/..")
        
        moves = []
        maxFrames = 0
        for punisher in punishers:
            pframes = int(punisher[0].text)
            if(pframes <= frames):
                if(pframes > maxFrames):
                    moves = [self.getMoveById(punisher[1].text)]
                    maxFrames = pframes
                elif(pframes == maxFrames):
                    moves.append(self.getMoveById(punisher[1].text))
        return moves

    def DidMoveJustHappen(self, MoveHistory, Move):
        found = False
        if not MoveHistory:
            print("Empty MoveHistory")
            return False

        gameIds = Move.findall(".//gameIds/gameId")

        #MoveHistory.reverse()
        #gameIds.reverse()
        Found = False
        index = -1
        newIndex = -1
        
        MoveState = 0
        
        for m in MoveHistory:
            if(m == gameIds[MoveState].text):
                MoveState += 1
                if(MoveState == len(gameIds)):
                    return True
                
        return False
        #print(MoveHistory)
#        indices = []
#        for i in range(len(gameIds)):
            #print(gameIds[i].text)
            
#            indices.append([index for index, value in enumerate(MoveHistory) if value == gameIds[i].text])
            
            
            #try:
            #    newIndex = MoveHistory.index(gameIds[i].text)
            #except:
            #    print("index: " + str(index) + "\t new index: " + str(newIndex) + "\t Length: " + str(len(MoveHistory)))
            #    #print("Move not in history")
            #    return False
            #
            #if (newIndex > index):
            ##if newIndex > index:
            #    Found = True
            #    index = newIndex
            #else:
            #    print("index: " + str(index) + "\t new index: " + str(newIndex) + "\t Length: " + str(len(MoveHistory)))
            #    return False
         
                
            
        print(indices)
        #print("Length of History: " + str(len(MoveHistory)))        
        return Found

    def Save(self):
        filename = os.path.join(self.directory, self.CharName + ".xml")
        if 'version' in self.CharXml.getroot().attrib.keys():
            version = self.CharXml.getroot().attrib['version']
        else:
            version = '0'
        copyfile(filename, os.path.join(self.directory, "xml backups", self.CharName + "-" + version + ".xml"))
        self.CharXml.getroot().attrib['version'] = str(int(time.time()))
        f = open(filename, "w")
        text = ET.tostring(self.CharXml.getroot(), 'utf-8') #Get character encoding of XML
        xmlFile = xml.dom.minidom.parseString(re.sub('\s+(?=<)', '', text.decode('utf-8'))) #Strip excess whitespace between tags and parse it back to XML
        f.write(xmlFile.toprettyxml()) #Print a human readable document
        f.close()

    def GetMovelistByCharID(self, char_id, version = None):
        
        for filename in os.listdir(self.directory):
            if filename.endswith(".xml"):
                #print(os.path.join(self.directory, filename))
                data_file = ET.parse(os.path.join(self.directory, filename))
                char_root = data_file.getroot()
                if int(char_id) == int(char_root.attrib['id']):
                    print('Move list located: ' + char_root.attrib['name'])
                    stancesFile = GetUniversalStances()
                    stances = stancesFile.findall(".//stance")
                    charStance = char_root.find("./stances")
                    #print(str(charStance))
                    if charStance == None:
                        charStance = ET.SubElement(char_root, "stances")
                    for stance in stances:
                        charStance.append(stance)
                    return data_file

def GetUniversalStances():
    file = "TekkenData/Movelists/Universal/DefaultStances.xml"
    stance_file = ET.parse(file)
    return stance_file
    
                
if __name__ == "__main__":
    a = MoveList(26)
    #print(a.getRandomMove("Punishable")[0].text)
    a.getGameplan(1)
    print(a.getMoveName(a.getRandomMove()))