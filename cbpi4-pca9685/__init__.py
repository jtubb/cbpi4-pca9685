import asyncio
import logging
from unittest.mock import MagicMock, patch

from cbpi.api import *

import subprocess
import os
import smbus
from numpy import interp
from pca9685_driver import Device

logger = logging.getLogger(__name__)

def getI2CAddress(bus_number):
    try:
        arr = []
        logger.info("PCA9685 ACTOR CONNECTING TO BUS %s" % (bus_number))
        bus = smbus.SMBus(int(bus_number))
        for device in range(3, 128):
            try:
                bus.write_byte(device, 0)
                arr.append(format(hex(device)))
                logger.info("PCA9685 ACTOR DEVICE DETECTED %s" % (format(hex(device))))
            except Exception as e:
                pass
        bus.close()
        return arr
    except Exception as e:
        logger.info("PCA9685 ACTOR DETECT I2C BUS FAILED %s" % (e))
        return []
        
def getI2CBus():
    try:
        arr = []
        for dirname in os.listdir('/dev/'):
            if dirname.startswith('i2c-'):
                logger.info("PCA9685 ACTOR BUS DETECTED %s" % (dirname))
                addresses = getI2CAddress(dirname.replace('i2c-',''))
                for address in addresses:
                    arr.append(dirname+':'+address)
        return arr
    except Exception as e:
        logger.info("PCA9685 ACTOR DETECT I2C BUS FAILED %s" % (e))
        return []





@parameters([Property.Select(label="Address", options=getI2CBus()), Property.Select(label="Channel", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]), Property.Number(label="Frequency", configurable=True, default_value=50, unit="hz"), Property.Number(label="Servo_Min_Pulse_Width", configurable=True, default_value=0), Property.Number(label="Servo_Max_Pulse_Width", configurable=True, default_value=4095)])

class PCA9685Actor(CBPiActor):

    # Custom property which can be configured by the user
    @action("Set Power", parameters=[Property.Number(label="Power", configurable=True,description="Power Setting [0-100]")])
    async def setpower(self,Power = 100 ,**kwargs):
        print("test", kwargs)
        #self.dev.set_pwm(int(self.props.Channel), self.pulseWidth(power))
        await self.set_pulseWidth(Power);
    
    async def set_pulseWidth(self, power):
        if (power<0):
            power=0
        if (power>100):
            power=100
        logger.info("PCA9685 ACTOR %s ADDR: %s CHANNEL: %s SET TO POWER: %s" % (self.id, self.props.Address, self.props.Channel, power))
        pulse_width = int(interp(power, [0, 100], [int(self.props.Servo_Min_Pulse_Width), int(self.props.Servo_Max_Pulse_Width)]));
        logger.info("PCA9685 ACTOR %s ADDR: %s CHANNEL: %s RANGED TO: %s" % (self.id, self.props.Address, self.props.Channel, pulse_width))
        self.dev.set_pwm(int(self.props.Channel), pulse_width)
        await self.cbpi.actor.actor_update(self.id,power)
        pass
        
    async def on_start(self):
        self.state = False


    async def on(self, power=None):
        try:
            if power is not None:
                await self.set_pulseWidth(power);
            self.state = True
        except Exception as e:
            logger.info("PCA9685 ACTOR %s ERR: %s" % (self.id, e))
            pass

    async def off(self):
        logger.info("PCA9685 ACTOR %s ADDR: %s CHANNEL: %s OFF" % (self.id, self.props.Address, self.props.Channel))
        try:
            self.dev.set_pwm(int(self.props.Channel), 0x1000)
            self.state = False
        except Exception as e:
            logger.info("PCA9685 ACTOR %s ERR: %s" % (self.id, e))
            pass

    def get_state(self):
        return self.state
    
    async def run(self):
        try:
            self.props.GPIO = self.props.Address+":"+str(self.props.Channel)
            addrBus = self.props.Address.split(':')
            #self.dev=Device(address=0x40, bus_number=1)
            addressValue=int(addrBus[1],0)
            bus_numberValue=int(addrBus[0].replace('i2c-',''))
            logger.info("PCA9685 ACTOR %s CONNECTING TO ADDR: %s BUS: %s" % (self.id, format(hex(addressValue)), addrBus[0]))
            self.dev = Device(address=addressValue, bus_number=bus_numberValue)
            self.dev.ranges['led_value'] = (0, 4096)
            self.dev.set_pwm_frequency(int(self.props.Frequency))
        except Exception as e:
            logger.info("PCA9685 ACTOR %s ERR: %s" % (self.id, e))
            pass
            
        while self.running == True:
            
            await asyncio.sleep(1)

def setup(cbpi):

    '''
    This method is called by the server during startup 
    Here you need to register your plugins at the server
    
    :param cbpi: the cbpi core 
    :return: 
    '''
    try:
        subprocess.run(["modprobe","i2c-bcm2835"])
        subprocess.run(["modprobe","i2c-dev"])
    except Exception as e:
        logger.info("PCA9685 ACTOR MODPROBE FAILED %s" % (e))
        pass
        
    cbpi.plugin.register("PCA9685Actor", PCA9685Actor)