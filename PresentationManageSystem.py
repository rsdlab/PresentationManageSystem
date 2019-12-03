#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file PresentationManageSystem.py
 @brief PresentationManageSystem
 @date $Date$


"""
import sys
import time
import math
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import SpeechConsumer_idl
import ActionManage_idl
import SpeechProvider_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from SpeechConsumer_idl_example import *

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import Consumer, Consumer__POA
import Action, Action__POA
import Provider, Provider__POA


# </rtc-template>

actionid = ""
speechcontents = ""

# This module's spesification
# <rtc-template block="module_spec">
presentationmanagesystem_spec = ["implementation_id", "PresentationManageSystem", 
		 "type_name",         "PresentationManageSystem", 
		 "description",       "PresentationManageSystem", 
		 "version",           "1.0.0", 
		 "vendor",            "hiroyasu_tsuji", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.PresentationMode", "OneSet",
		 "conf.default.PresemtationData", "data.csv",

		 "conf.__widget__.PresentationMode", "radio",
		 "conf.__widget__.PresemtationData", "text",
		 "conf.__constraints__.PresentationMode", "(OneSet,LoopSet)",

         "conf.__type__.PresentationMode", "string",
         "conf.__type__.PresemtationData", "string",

		 ""]
# </rtc-template>

##
# @class PresentationManageSystem
# @brief PresentationManageSystem
# 
# 
class PresentationManageSystem(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Facedetectionposition = RTC.TimedDoubleSeq(RTC.Time(0,0),"")
		"""
		"""
		self._FacedetectionpositionIn = OpenRTM_aist.InPort("Facedetectionposition", self._d_Facedetectionposition)
		self._d_presentationop = RTC.TimedShort(RTC.Time(0,0),"")
		"""
		"""
		self._presentationopOut = OpenRTM_aist.OutPort("presentationop", self._d_presentationop)
		self._d_waistmovement = RTC.TimedDouble(RTC.Time(0,0),"")
		"""
		"""
		self._waistmovementOut = OpenRTM_aist.OutPort("waistmovement", self._d_waistmovement)

		"""
		"""
		self._actionmanagePort = OpenRTM_aist.CorbaPort("actionmanage")
		"""
		"""
		self._speechconsumerPort = OpenRTM_aist.CorbaPort("speechconsumer")
		"""
		"""
		self._speechproviderPort = OpenRTM_aist.CorbaPort("speechprovider")

		"""
		"""
		self._SpeechConsumerProvider = SpeechConsumer_i()
		

		"""
		"""
		self._ActionManageRequire = OpenRTM_aist.CorbaConsumer(interfaceType=Action.ActionManage)
		"""
		"""
		self._SpeechProviderRequire = OpenRTM_aist.CorbaConsumer(interfaceType=Provider.SpeechProvider)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  PresentationMode
		 - DefaultValue: OneSet
		"""
		self._PresentationMode = ['OneSet']
		"""
		
		 - Name:  PresemtationData
		 - DefaultValue: data.csv
		"""
		self._PresemtationData = ['data.csv']
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("PresentationMode", self._PresentationMode, "OneSet")
		
		# Set InPort buffers
		self.addInPort("Facedetectionposition",self._FacedetectionpositionIn)
		
		# Set OutPort buffers
		self.addOutPort("presentationop",self._presentationopOut)
		self.addOutPort("waistmovement",self._waistmovementOut)
		
		# Set service provider to Ports
		self._speechproviderPort.registerProvider("SpeechConsumer", "Consumer::SpeechConsumer", self._SpeechConsumerProvider)
		
		# Set service consumers to Ports
		self._actionmanagePort.registerConsumer("ActionManage", "Action::ActionManage", self._ActionManageRequire)
		self._speechconsumerPort.registerConsumer("SpeechProvider", "Provider::SpeechProvider", self._SpeechProviderRequire)
		
		# Set CORBA Service Ports
		self.addPort(self._actionmanagePort)
		self.addPort(self._speechconsumerPort)
		self.addPort(self._speechproviderPort)

                data = ["","",""]
                with open(self._PresemtationData[0], "a") as f:
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerow(data)
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
                self._d_presentationop.data = -1 * self._SpeechConsumerProvider.m_slide
                self._presentationopOut.write()
                self._SpeechConsumerProvider.m_slide = 1
	        self._SpeechConsumerProvider.index = 1
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
                time.sleep(1)
                if (self._PresentationMode == ['OneSet']):
                        time.sleep(1)
                        if (self._SpeechConsumerProvider.Flag == 1):
                                print( "PresentationEND " )
                
                        elif (self._SpeechConsumerProvider.Flag == 2):
                                speechcontents = self._SpeechConsumerProvider.m_speechdata
	                        actionid = self._SpeechConsumerProvider.m_bodylang
                                print("Slide Number : " + str(self._SpeechConsumerProvider.m_slide))
	                        print("speechdata : " + speechcontents)
	                        print("actionid : " + actionid)
	                        self._SpeechProviderRequire._ptr().read(speechcontents)
	                        self._ActionManageRequire._ptr().read(actionid)
                                print( "SendData_OK " )
                                
                        elif (self._SpeechConsumerProvider.Flag == 3):                        
                                self._d_presentationop.data = 1
                                self._presentationopOut.write()
                                print( "Slide next" )
                                self._d_presentationop.data = 0
                                print("Slide Number : " + str(self._SpeechConsumerProvider.m_slide))
                                speechcontents = self._SpeechConsumerProvider.m_speechdata
	                        actionid = self._SpeechConsumerProvider.m_bodylang
	                        print("speechdata : " + speechcontents)
	                        print("actionid : " + actionid)
	                        self._SpeechProviderRequire._ptr().read(speechcontents)
	                        self._ActionManageRequire._ptr().read(actionid)
	                        print( "SendData_OK " )

                        if self._FacedetectionpositionIn.isNew():
                                facedetectionposition = self._FacedetectionpositionIn.read()
                                self._d_waistmovement.data = facedetectionposition.data[0] - 320
                                self._d_waistmovement.data = math.degrees(math.asin(self._d_waistmovement.data/500))
                                if -45 <= self._d_waistmovement.data <= 45:
                                        self._waistmovementOut.write()
                                
                        self._SpeechConsumerProvider.Flag = 0
                                
                if (self._PresentationMode == ['LoopSet']):
                                        
                        if (self._SpeechConsumerProvider.Flag == 1):
                                print( "PresentationEND " )
                                self._SpeechConsumerProvider.Flag = 0
                                self._d_presentationop.data = -1 * (self._SpeechConsumerProvider.m_slide -1)
                                self._presentationopOut.write()
                                self._d_presentationop.data = 0
                                self._SpeechConsumerProvider.m_slide = 1
	                        self._SpeechConsumerProvider.index = 1
                                speechcontents = ""
                                self._SpeechProviderRequire._ptr().read(speechcontents)
                                return RTC.RTC_OK
                
                        elif (self._SpeechConsumerProvider.Flag == 2):
                                speechcontents = self._SpeechConsumerProvider.m_speechdata
	                        actionid = self._SpeechConsumerProvider.m_bodylang
                                print("Slide Number : " + str(self._SpeechConsumerProvider.m_slide))
	                        print("speechdata : " + speechcontents)
	                        print("actionid : " + actionid)
	                        self._SpeechProviderRequire._ptr().read(speechcontents)
	                        self._ActionManageRequire._ptr().read(actionid)
                                print( "SendData_OK " )
                                
                        elif (self._SpeechConsumerProvider.Flag == 3):                        
                                self._d_presentationop.data = 1
                                self._presentationopOut.write()
                                print( "Slide next" )
                                self._d_presentationop.data = 0
                                print("Slide Number : " + str(self._SpeechConsumerProvider.m_slide))
                                speechcontents = self._SpeechConsumerProvider.m_speechdata
	                        actionid = self._SpeechConsumerProvider.m_bodylang
	                        print("speechdata : " + speechcontents)
	                        print("actionid : " + actionid)
	                        self._SpeechProviderRequire._ptr().read(speechcontents)
	                        self._ActionManageRequire._ptr().read(actionid)
	                        print( "SendData_OK " )

                        if self._FacedetectionpositionIn.isNew():
                                facedetectionposition = self._FacedetectionpositionIn.read()
                                self._d_waistmovement.data = facedetectionposition.data[0] - 320
                                self._d_waistmovement.data = math.degrees(math.asin(self._d_waistmovement.data/500))
                                self._waistmovementOut.write()

                        self._SpeechConsumerProvider.Flag = 0
                                
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def PresentationManageSystemInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=presentationmanagesystem_spec)
    manager.registerFactory(profile,
                            PresentationManageSystem,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    PresentationManageSystemInit(manager)

    # Create a component
    comp = manager.createComponent("PresentationManageSystem")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

