#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file SpeechConsumer_idl_examplefile.py
 @brief Python example implementations generated from SpeechConsumer.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import Consumer, Consumer__POA

import csv

class SpeechConsumer_i (Consumer__POA.SpeechConsumer):
    """
    @class SpeechConsumer_i
    Example class implementing IDL interface Consumer.SpeechConsumer
    """

    def __init__(self):
        self.Flag = 0
        self.m_speechdata = ""
        self.m_bodylang = ""
        self.m_slide = 1
        self.index = 1
        """
        @brief standard constructor
        Initialise member variables here
        """
        pass

    # void write(in string speechstate)
    def write(self, speechstate):
        with open("data.csv") as f:
            reader = csv.reader(f)
            line = [row for row in reader]
        if (speechstate == "speechstart" or speechstate == "speechend"):
            if (line[self.index][0] == "" and line[self.index][1] == "" and line[self.index][2] == ""):
                self.Flag = 1
                self.index = 1
            elif (line[self.index][0] == ""):
                self.m_speechdata = line[self.index][1]
                self.m_bodylang = line[self.index][2]
                self.Flag = 2
                self.index += 1
            elif (int(line[self.index][0]) == self.m_slide):
                self.m_speechdata = line[self.index][1]
                self.m_bodylang = line[self.index][2]
                self.Flag = 2
                self.index += 1
            elif (int(line[self.index][0]) != self.m_slide):
                self.m_speechdata = line[self.index][1]
                self.m_bodylang = line[self.index][2]
                self.m_slide = self.m_slide + 1
                self.Flag = 3
                self.index += 1

        f.close()    
        #raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: None


if __name__ == "__main__":
    import sys
    
    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)
    
    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = SpeechConsumer_i()

    # Activate it in the Root POA
    poa.activate_object(servant)

    # Get the object reference to the object
    objref = servant._this()
    
    # Print a stringified IOR for it
    print orb.object_to_string(objref)

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()

