# services-monitor

The project consists of 3 main parts:
Part A - Monitor mode that shows the services running on the computer at any given moment. The monitor also shows the services running at the given moment and also shows the changes that occurred at each point in time and exports this data into files we created.
Part B - manual monitor mode that allows you to set 2 different time points and receive all the changes that occurred in the services between these time points.
Part C - Encrypting our code classes against attackers.
And in addition, alerts when unverified changes were made to the files we created.

**Departments:**
Monitor.py - The program is mainly responsible for implementing part A.
We used built-in functions for windows and linux to get information about all the services running in the background and put the list in the serviceList file, after that we made a comparison between adjacent time points by dict each time to see what changes were made between them and every time we found such a change We added it to the status_Log file

manualMonitor.py - The class is mainly responsible for implementing part B.
We opened the files we created in the monitor class and used their information to create a manual monitor. We created a new auxiliary file called date.txt which actually saves all the dates that appear in the serviceList file and in addition indicates in which line they are mentioned there so that we access the dates that the user has chosen and compare their positions in the serviceList file so that we can know about any changes made between them, along the way we transferred to dict the The services in both times and thus compared between them.

Gui.py - the department is responsible for designing the graphical user interface. We linked it to all parts of the project so that it is linked both to the normal monitor status part, to the manually managed monitor and to the defensive part and the attack alerts that pop up in the interface panel.
secureSystem.py- responsible for the part related to encrypting the code files against an external attacker. The only one who will be able to access them in an unencrypted way is the one who will hold the key to them, thus preventing the attacker from accessing them.


**running:**
-run the gui.py file.
- Click on the "monitor" button in the panel that opens and define there the time that will pass between each check of the services and click on "ok".
- After the monitor returns the information about the services and the changes made to them, you can also switch to manual mode and for this you have to press the "monitor" button and set a start and end time to check the changes between them and press "ok" to confirm.
*To use our protection layer, you need to run the "secureSystem.py" class
