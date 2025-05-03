Simulation - description:
1. there are 5 tabs -> users, channels, videos, streams and search. Search is used to find entity by name
2. Five buttons -> start (create), stop(pause), resume (unpause), save (serialize state to file named "simulator1.ser,
user can't serialize it to chosen file, thus only one save at time is possible), load (deserializing from
"simulator1.ser"). However to run loaded simulation you need to load it and then click resume to unpause.
3. Lists and data refresh everytime you click on jLists situated on the left side of the GUI)
4. Rest is I think pretty much obvious ;)
5. There are uploaded photos to the simulation but they are visible only when are in the same directory as .jar file
6. Command to run .jar file:
In terminal:
java -cp 156035_Kuba_Czech_javaproject-1.0-SNAPSHOT.jar com.mycompany._kuba_czech_javaproject.App
Assuming that .jar file is in target directory because otherwise it may not work properly (we discussed
it during our last classes)