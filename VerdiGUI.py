# Verdi GUI is a small tool to interface with a Coherent Verdi laser through Serial
# Verdi GUI is distributed under the MIT Expat License

from PyQt4 import QtCore, QtGui
import os, serial, sys, time
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS

sys.path.insert(0, './forms')   # tell Python where to look for the next imports

# import the code for all the ui window classes
import icon_qrc
from verdiconnect import Ui_Form as Connect_Form
from verdidoc import Ui_Form as Doc_Form
from verdifault import Ui_Form as Fault_Form
from verdiname import Ui_Form as Name_Form
from verdiwindow import Ui_Form as Window_Form

# Verdi class contains information and methods that directly deal with the laser:
#    1. All methods that handle serial communication (establishing connection, sending, receiving)
#    2. It also contains information obtained from laser status updates
#    3. Finally, it contains static dictionaries of fault error codes and serial commands

class Verdi(object):

    # Fault dictionary, contains laser fault codes as keys and the corresponding fault message as values
    FAULTS = {
        "1": "Laser Head Interlock Fault",
        "2": "External Interlock Fault",
        "3": "PS Cover Interlock Fault",
        "4": "LBO Temperature Fault",
        "5": "LBO Not Locked at Set Temp",
        "6": "Vanadate Temp. Fault",
        "7": "Etalon Temp. Fault",
        "8": "Diode 1 Temp. Fault",
        "10": "Baseplate Temp. Fault",
        "11": "Heatsink 1 Temp. Fault",
        "16": "Diode 1 Over Current Fault",
        "18": "Over Current Fault",
        "19": "Diode 1 Under Volt Fault",
        "21": "Diode 1 Over Volt Fault",
        "25": "Diode 1 EEPROM Fault",
        "27": "Laser Head EEPROM Fault",
        "28": "Power Supply EEPROM Fault",
        "29": "PS-Head Mismatch Fault",
        "31": "Shutter State Mismatch",
        "40": "Head-Diode Mismatch Fault",
        "47": "Vanadate2 Temp Fault"
    }

    # STATS and HOURS tuples contain queries to get the desire laser health stats and operating hours

    STATS = ("C", "D1C", "D2C", "D1HST", "D2HST", "ET", "VT", "BT", "LBOT")

    HOURS = ("HH", "D1H", "D2H")

    def __init__(self):
        object.__init__(self)

        # populate laser initial values. These will change later.
        self.connected = False
        self.baud = 19200
        self.powerValue = 0
        self.fault = 0
        self.shutter = "0"

        # iterate over STATS and HOURS and populate initial values for each laser health stat
        for i in self.STATS:
            exec("".join(["self.", i, "= 'N/A'"]))

        for h in self.HOURS:
            exec("".join(["self.", h, "= 'N/A'"]))

        self.serSetup()        # call method to set up the serial port

    def serSetup(self):
        # Windows ports are named "COM1," "COM2", "COM3, ...
        # iterate through all of these to find a connection
        # once a connection is found, test to see if it is the laser
        # if it is the laser, flag the connection and escape the loop
        for i in range(0, 10):
            self.port = "COM" + str(i)
            try:
                self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=0.2)
            except serial.serialutil.SerialException:
                continue
            else:
                try:
                    # make sure that this is the laser's port
                    replies = ("PRINT SHUTTER", "Verdi>", "1", "0")
                    self.send("PRINT SHUTTER")
                    reply = self.read()
                    if reply in replies:
                        self.connected = True
                        break
                    else:
                        continue
                except:
                    continue

        if self.connected:
            # make sure Verdi is not in ECHO or PROMPT mode as that will mess with reading results
            self.send("ECHO = 0")
            self.send("PROMPT = 0")
            self.ser.flush()            # flush the buffer so there is no old data left

            # now that connection is ready, do the first round of updates
            self.updateStats()
            self.checkPower()
            self.checkShutter()

    def read(self):
        # read 1 line from serial buffer, stripping off termination characters automatically
        try:
            line = self.ser.readline().strip()
            return line
        except serial.serialutil.SerialTimeoutException:
            window.pred("ERROR: Readline timed out.")
        except:
            return "No response received."

    def send(self, cmd):
        # automatically add termination chars if none are given, then send command
        if cmd[-2:] != "\r\n":
            cmd += "\r\n"
        try:
            self.ser.write(cmd)
        except serial.serialutil.SerialTimeoutException:
            window.pred("ERROR: Send command timed out.")
        except serial.serialutil.SerialException as e:
            if "WriteFile failed" in str(e):
                self.connected = False
                window.serialDisconnected()
            else:
                raise

    def updateSer(self):
        # this function is called when serial port, baudrate or timeout are updated
        # program will close pre-existing serial port and open a new one
        try:
            self.ser.close()
        except:
            pass
        finally:
            try:
                self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=0.2)
            except serial.serialutil.SerialException:
                window.pred("Could not connect with these values.")
                self.connected = False
            else:
                self.connected = True

    def updateStats(self):
        # get updated values from the laser for currents and temperatures
        # but first make sure there are no faults
        if self.connected:
            self.checkFault()
            if not self.fault:
                for stat in self.STATS:
                    query = "?" + stat
                    self.send(query)
                    reply = self.read()
                    if reply == "No response received.":
                        reply = "N/A"
                    exec ("".join(["self.", stat, " = reply"]))
                self.checkPower()
            else:
                fault = self.fault
                window.triggerFault(fault, self.FAULTS[fault])

    def getHours(self):
        # get values for laser head, diode 1, diode 2 operating hours
        if self.connected:
            for item in self.HOURS:
                query = "?" + item
                self.send(query)
                reply = self.read()
                if reply == "No response received.":
                    reply = "???"
                exec("".join(["self.", item, " = reply + ' h'"]))

    def checkShutter(self):
        # check if shutter is open or closed
        if self.connected:
            self.send("?S")
            self.shutter = self.read()

    def checkFault(self):
        # query the laser for active faults
        # laser will return "SYSTEM OK" if no faults are active
        self.send("?F")
        fault = self.read()
        if fault == "SYSTEM OK":
            self.fault = 0
        elif fault == "No response received.":
            pass
        else:
            self.fault = fault

    def setPower(self, power):
        # set the laser's power to a new value
        if self.connected:
            power = round(power, 2)
            pstring = str(power)
            cmd = "P = " + pstring
            self.send(cmd)
            self.read()     # discard a line
            verdi.powerValue = power
            # window.pblue(" ".join(["Power has been set to", str(power), "watts."]))

    def checkPower(self):
        # get the laser's set power value
        if self.connected:
            self.send("?SP")
            power = self.read()
            if power != '':
                self.powerValue = float(power)

    def toggleShutter(self, open):
        # open or close the shutter
        if self.connected:
            if open:
                self.send("S = 1")
            else:
                self.send("S = 0")
        self.checkShutter()

# Create the connection pop-up window class

class ConnectWindow(QtGui.QWidget, Connect_Form):
    def __init__(self, parent=None):
        super(ConnectWindow, self).__init__(parent)
        # try to tell Windows to keep this window on top
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.resize(200,100)
        self.setWindowIcon(QtGui.QIcon(':/icon/verdigui.ico'))
        # assign handlers for the two buttons
        self.retry_btn.clicked.connect(self.retryConnection)
        self.cancel_btn.clicked.connect(self.cancelConnection)

    def retryConnection(self):
        verdi.serSetup()
        if verdi.connected:
            window.pblue("Verdi GUI is now connected to port: " + verdi.port)
            window.updateAll()
            window.checkShutter()
            window.formatPower()
            window.timer.start()
            self.hide()
        else:
            self.label.setText("Still no connection.")
            self.label_2.setText("Are you sure your computer is connected to the laser?")

    def cancelConnection(self):
        window.warned = True
        window.pblue("Verdi GUI did not establish a connection to a laser.\n"
                 "To try again at a later time, use the command \"-scan\".")
        self.hide()

# Create the documentation pop-up window

class DocWindow(QtGui.QWidget, Doc_Form):
    def __init__(self, parent=None):
        super(DocWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icon/verdigui.ico'))

# Create the fault pop-up window

class FaultWindow(QtGui.QWidget, Fault_Form):
    def __init__(self, parent=None):
        super(FaultWindow, self).__init__(parent)
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icon/verdigui.ico'))
        self.pushButton.clicked.connect(self.clearFault)

    def clearFault(self):
        # tell the laser that the fault is (probably) cleared
        verdi.send("L = 1")
        verdi.read()
        window.timer.start(window.interval)
        window.checkShutter()
        self.hide()

# Create the export pop-up window
# This window request the user's name, then logs laser stats

class NameWindow(QtGui.QWidget, Name_Form):

    def __init__(self, parent=None):
        super(NameWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icon/verdigui.ico'))

        # assign handlers to the buttons
        self.okay_btn.clicked.connect(self.exportData)
        self.name_box.returnPressed.connect(self.exportData)
        self.cancel_btn.clicked.connect(self.hide)

    def exportData(self):
        # record user's name and log that name, along with all the stats, to the log file
        name = str(self.name_box.text()).strip()
        if len(name) == 0:      # catch empty strings
            return
        else:
            verdi.getHours()
            try:
                # try to open the file
                log = open("verdilog.csv")
            except IOError:
                # an IOError would mean that the file does not exist, so create one
                log = open("verdilog.csv", "a")
                cols = ("TIME,LOGGER,POWER,AVG CURRENT,D1 CURRENT,D2 CURRENT,D1 HEATSINK,D2 HEATSINK,"
                        "ETALON,VANADATE,LBO,HEAD HRS,D1 HRS, D2 HRS\n")
                log.write(cols)
            else:
                # if file already exists, switch to "append" mode
                log = open("verdilog.csv", "a")
            finally:
                # now that the file definitely exists and is open, format stats and append them to the file
                datetime = time.strftime("%Y-%m-%d %H:%M:%S")
                stats = (datetime, name, str(verdi.powerValue), verdi.C, verdi.D1C, verdi.D2C, verdi.D1HST, verdi.D2HST,
                         verdi.ET, verdi.VT, verdi.LBOT, verdi.HH, verdi.D1H, verdi.D2H)
                writestring = ",".join(stats)
                try:
                    log.write(writestring + "\n")
                except IOError as e:
                    # an IOError here would mean the program doesn't have permission to write
                    if str(e) == "File not open for writing":
                        window.pred("Verdi GUI doesn't have permission to write to the log.\n"
                                 "Make sure the log file is closed and you have permission to write "
                                 "in the folder in which Verdi GUI is installed.")
                        self.hide()
                        return
                log.close()
                # get Verdi GUI's folder's path
                path = os.path.realpath(sys.argv[0])
                if not os.path.isdir(path):
                    path = os.path.dirname(path)
                window.pblue("".join(["Current stats have been logged to ", path, "\\verdilog.csv"]))
            self.hide()

# Main UI window

class MainWindow(QtGui.QWidget, Window_Form):

    COLORS = {
        "black": "#000000",
        "green": "#508a59",
        "red": "#a83636",
        "blue": "#586890",
    }

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # resize the window based on user's screen resolution
        screen = app.desktop().screenGeometry()
        width = int(screen.width()*0.22)
        height = int(screen.height()*0.52)
        self.resize(width, height)

        # set a custom icon
        self.setWindowIcon(QtGui.QIcon(':/icon/verdigui.ico'))

        # initialize the Verdi class when the GUI is created
        global verdi
        verdi = Verdi()

        self.assignHandlers()
        self.createTooltips()
        self.updateAll()
        self.checkShutter()
        self.formatPower()

        # initialize the auto-update timer with default interval of 5 seconds
        self.interval = 2000
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateAll)
        self.timer.start(self.interval)

        # flag to remember whether the user has already been warned about connection issues
        # so that they are not repeatedly spammed with pop-up warning windows
        self.warned = False

        # say hello to the user
        self.pgreen("<b>Welcome to Verdi GUI!</b> ")
        if verdi.connected:
            self.pgreen("Verdi GUI is connected via Windows port: " + verdi.port)
        else:
            self.serialDisconnected()

    def assignHandlers(self):
        # connect buttons to handler functions so that they actually do something when clicked
        self.shutter_btn.clicked.connect(self.toggleShutter)
        self.export_btn.clicked.connect(self.exportButtonPushed)
        self.openLog_btn.clicked.connect(self.openLog)
        self.doc_btn.clicked.connect(self.openDocumentation)
        self.input_box.returnPressed.connect(self.inputEntered)
        self.power_up.clicked.connect(self.powerUp)
        self.power_down.clicked.connect(self.powerDown)

    def createTooltips(self):
        # add helpful tooltips to everything
        self.power_up.setToolTip("Increase the laser power by 10 mW.")
        self.power_down.setToolTip("Decrease the laser power by 10 mW.")
        self.shutter_btn.setToolTip("Shutter is currently CLOSED. Click to OPEN.")
        self.export_btn.setToolTip("Record currents, temperatures, and operating hours to log file.")
        self.C_box.setToolTip("Average measured current, in amperes, of the two diodes.")
        self.D1C_box.setToolTip("Measured current, in amperes, of Diode 1.")
        self.D2C_box.setToolTip("Measured current, in amperes, of Diode 2.")
        self.D1HST_box.setToolTip("Measured temperature, in degrees Celsius, of Diode 1's heatsink.")
        self.D2HST_box.setToolTip("Measured temperature, in degrees Celsius, of Diode 2's heatsink.")
        self.BT_box.setToolTip("Measured temperature, in degrees Celsius, of laser head baseplate.")
        self.ET_box.setToolTip("Measured temperature, in degrees Celsius, of the etalon.")
        self.VT_box.setToolTip("Measured temperature, in degrees Celsius, of the vanadate element.")
        self.LBOT_box.setToolTip("Measured temperature, in degrees Celsius, of the LBO crystal.")
        self.doc_btn.setToolTip("Open the full list of commands.")

    # print colorful messages for better visibility
    def pblack(self, msg):
        msg = "".join(["<span style=\"color: ", self.COLORS["black"], ";\">", msg, "</span>"])
        self.output_box.append(msg)
        self.output_box.moveCursor(QtGui.QTextCursor.End)

    def pgreen(self, msg):
        msg = "".join(["<span style=\"color: ", self.COLORS["green"], ";\">", msg, "</span>"])
        self.output_box.append(msg)
        self.output_box.moveCursor(QtGui.QTextCursor.End)

    def pblue(self, msg):
        msg = "".join(["<span style=\"color: ", self.COLORS["blue"], ";\">", msg, "</span>"])
        self.output_box.append(msg)
        self.output_box.moveCursor(QtGui.QTextCursor.End)

    def pred(self, msg):
        msg = "".join(["<span style=\"color: ", self.COLORS["red"], ";\">", msg, "</span>"])
        self.output_box.append(msg)
        self.output_box.moveCursor(QtGui.QTextCursor.End)

    def updateAll(self):
        # query the laser for the latest health stats, then update the display boxes to match
        verdi.updateStats()
        self.checkShutter()
        self.C_box.setText(verdi.C)
        self.D1C_box.setText(verdi.D1C)
        self.D2C_box.setText(verdi.D2C)
        self.D1HST_box.setText(verdi.D1HST)
        self.D2HST_box.setText(verdi.D2HST)
        self.ET_box.setText(verdi.ET)
        self.VT_box.setText(verdi.VT)
        self.BT_box.setText(verdi.BT)
        self.LBOT_box.setText(verdi.LBOT)

    def formatPower(self):
        power = "{:.2f}".format(verdi.powerValue)
        self.power_lcd.display(power)

    def powerUp(self):
        # increase the laser's power by 0.01 W, unless power is already too high
        power = verdi.powerValue + 0.01
        if power <= 5.001:
            verdi.setPower(power)
            self.formatPower()
        else:
            window.pred("Power cannot be higher than 5.00 W.")

    def powerDown(self):
        # decrease the laser's power by 0.01 W, unless power is already too low
        power = verdi.powerValue - 0.01
        if power >= 0.009:
            verdi.setPower(power)
            self.formatPower()
        else:
            window.pred("Power cannot be lower than 0.01 W.")

    def toggleShutter(self):
        # toggle laser's shutter when button is pushed
        if verdi.shutter == "1":
            verdi.toggleShutter(False)
        else:
            verdi.toggleShutter(True)
        self.checkShutter()

    def checkShutter(self):
        # make sure GUI's shutter status button matches laser's real shutter status
        btn = self.shutter_btn
        verdi.checkShutter()
        if verdi.shutter == "1":
            btn.setChecked(True)
            btn.setText("OPEN")
            btn.setToolTip("Shutter is currently OPEN. Click to CLOSE.")
        else:
            btn.setChecked(False)
            btn.setText("CLOSED")
            btn.setToolTip("Shutter is currently CLOSED. Click to OPEN.")

    def exportButtonPushed(self):
        # when the export button is pushed, launch the export window
        self.name_popup = NameWindow()
        self.name_popup.show()

    def openLog(self):
        try:
            os.startfile("verdilog.csv")
        except WindowsError:
            self.pred("No log found. Click \"Export\" to start a log.")

    def openDocumentation(self):
        # when documentation button is pushed, launch the documentation window
        self.doc_popup = DocWindow()
        self.doc_popup.show()

    def inputEntered(self):
        # take whatever the user has typed and parse it for commands
        # give the user help, if they are asking for help
        # if user types a GUI command that beings with a dash (-), figure out what it is
        # all other commands are sent straight to the laser

        cmd = str(self.input_box.text()).strip()
        HELP = ["help", "-", "-help", "HELP", "-HELP", "-h"]

        if len(cmd) == 0:       # catch accidental enter press
            return

        self.pblack("&raquo; " + cmd)
        if cmd in HELP:
            self.showHelp()
        elif cmd[0] == "-":
            self.dashCommand(cmd[1:].split(" ", 1))
        else:
            if verdi.connected:
                verdi.send(cmd)
                reply = verdi.read()
                self.pblue("Reply received: " + reply)
        self.input_box.setText("")

    def dashCommand(self, cmd):
        # find out what the user wants and do it
        CMDS = ("port", "baud", "update")
        if cmd[0] == "scan":
            verdi.serSetup()
            if verdi.connected:
                self.pblue("Verdi GUI is now connected to port: " + verdi.port)
                self.warned = False
            else:
                self.pblue("Verdi GUI could not establish a connection to a laser.")
        elif cmd[0] not in CMDS:
            self.pred("Not a value command.")
        else:
            try:
                val = int(cmd[1])       # try to convert the second word to an integer
            except ValueError:
                # if we get a ValueError, that means there is a second word, but it's not a number
                # so we can't do anything with it. In this case, give the user an appropriate error message.
                self.pred("ERROR: New setting must be an integer")
            except IndexError:
                # if we get an IndexError, that means there was only one word in the command, which is fine
                # we can execute that one word command
                if cmd[0] == "port":
                    self.pblue("Current port is: " + str(verdi.port))
                elif cmd[0] == "baud":
                    self.pblue("Current baudrate is: " + str(verdi.baud))
                elif cmd[0] == "update":
                    if verdi.connected:
                        self.updateAll()
                        self.pblue("Updated laser stats.")
                    else:
                        self.pred("Verdi GUI cannot update stats while laser is disconnected.")
            else:
                # if no errors are raised, that means the user issued a valid 2-word command
                # figure out what it is and execute it
                if cmd[0] == "port":
                    verdi.port = "COM" + cmd[1]
                    self.pblue("Switching to port: " + cmd[1])
                elif cmd[0] == "baud":
                    verdi.baud = val
                    self.pblue("Baudrate changed to: " + cmd[1])
                elif cmd[0] == "update":
                    if val > 0:
                        self.interval = val*1000
                        self.timer.setInterval(self.interval)
                        self.pblue(" ".join(["Update frequency changed to", cmd[1], "seconds"]))
                    else:
                        self.pred("Update interval must be an integer greater than 0.")

                if verdi.connected:
                    verdi.updateSer()

        # clear the input box
        self.input_box.setText("")

    def showHelp(self):
        # mini-documentation, accessed in the program by typing 'help', '-h', etc
        helpstring = ("VERDI GUI QUICK COMMANDS REFERENCE:<br>"
                      "&nbsp;&nbsp;&nbsp;&nbsp;-scan: sweep COM ports to try and find the laser<br>"
                      "&nbsp;&nbsp;&nbsp;&nbsp;-port n: switch to using COM port n<br>"
                      "&nbsp;&nbsp;&nbsp;&nbsp;-baud n: switch to baudrate n<br>"
                      "&nbsp;&nbsp;&nbsp;&nbsp;-update: force Verdi GUI to fetch new stat values<br>"
                      "&nbsp;&nbsp;&nbsp;&nbsp;-update n: change update frequency to every n seconds<br>"
                      "Commands that do not being with a dash (-) are sent directly to the laser.")
        self.pblue(helpstring)

    def serialDisconnected(self):
        # check warning flag to see if user has already been warned about the lack of connection
        # if not, make the warning pop up window
        self.timer.stop()
        if not self.warned:
            self.connection_popup = ConnectWindow()
            self.connection_popup.show()

    def triggerFault(self, fault, faultstring):
        # oh no there is a fault
        # better make a new window
        self.fault_popup = FaultWindow()
        self.fault_popup.errorCode_label.setText("Error code: " + fault)
        self.fault_popup.errorMsg_label.setText(faultstring)
        self.fault_popup.show()
        self.timer.stop()   # temporarily suspend the update timer

# prevent duplicate windows by registered a mutex
class Singleton:

    def __init__(self):
        self.mutex = CreateMutex(None, False, "Verdi_GUI_Windows_Registered_Mutex")
        self.lasterror = GetLastError()

    def isRunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)

if __name__ == "__main__":
    # check for pre-existing window immediately; kill new window if it is a duplicate
    instance = Singleton()
    if instance.isRunning():
        sys.exit(0)
    else:
        app = QtGui.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())