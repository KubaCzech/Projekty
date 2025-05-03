/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany._kuba_czech_javaproject;

/**
 *
 * @author Kuba
 */
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

class Simulator implements Serializable {
    private volatile transient List<Thread> allThreads;
    private List<User> users;
    private List<Channel> channels;
    private volatile List<Media> media;
    private boolean isSimulationRunning;
    
    public Simulator() {
        allThreads = new ArrayList<>();
        users = new ArrayList<>();
        channels = new ArrayList<>();
        media = new ArrayList<>();
        isSimulationRunning = false;
    }
    
    public List<User> getUsers() {
        return users;
    }
    public List<Channel> getChannels() {
        return channels;
    }
    public List<Media> getMedia() {
        return media;
    }
    
    public List<String> getNamesOfUsers() {
        List<String> namesOfUsersStrings = new ArrayList<>();
        for (User i : users) {
            namesOfUsersStrings.add(i.getUsersName());
        }
        return namesOfUsersStrings;
    }
    public List<String> getNamesOfMedia() {
        List<String> namesOfMediaStrings = new ArrayList<>();
        for (Media i : media) {
            namesOfMediaStrings.add(i.getName());
        }
        return namesOfMediaStrings;
    }
    
    public List<String> getNamesOfVideos(){
        List<String> namesOfVideosStrings = new ArrayList<>();
        for (Media i: media){
            if (i.getClass() == Video.class)
            {
                namesOfVideosStrings.add(i.getName());
            }
        }
        return namesOfVideosStrings;
    }
    
    public List<String> getNamesOfStreams(){
        List<String> namesOfStreamsStrings = new ArrayList<>();
        for (Media i: media){
            if(i.getClass() == Stream.class){
                namesOfStreamsStrings.add(i.getName());
            }
        }
        return namesOfStreamsStrings;
    }
    
    public User getUserByName(String someString){
        for (User i: users){
            if (i.getUsersName() == someString)
                return i;
        }
        return null;
    }
    
    public Channel getChannelByName(String someString){
        for (Channel i: channels){
            if (i.getName() == someString)
                return i;
        }
        return null;
    }
    
    public Media getVideoByName(String someString){
        for (Media i: media){
            if (i.getClass() == Video.class && i.getName() == someString){
                return i;
            }
        }
        return null;
    }
    
    public Media getStreamByName(String someString){
        for (Media i: media){
            if (i.getClass() == Stream.class && i.getName() == someString){
                return i;
            }
        }
        return null;
    }
    
    public List<String> getNamesOfChannels() {
        List<String> namesOfChannelsStrings = new ArrayList<>();
        for (Channel i : channels) {
            namesOfChannelsStrings.add(i.getName());
        }
        return namesOfChannelsStrings;
    }
     
    public String findEntityByName(String someName) {
        for (Media i: media) {
            //System.out.println(i.getName());
            if (i.getName().equals(someName)) {
                return i.toString();
            }
        }
        for (User i: users) {
            if (i.getUsersName().equals(someName)) {
                return i.toString();
            }
        }
        for (Channel i: channels) {
            if (i.getName().equals(someName)) {
                return i.toString();
            }
        }
        return "";
    }
    
    public String getThumbnail(String someName) {
        for (Media i: media) {
            if (i.getName().equals(someName)) {
                return i.getThumbnail();
            }
        }
        for (User i : users) {
            if (i.getUsersName().equals(someName)) {
                return i.getThumbnail();
            }
        }
        return null;
    }
    
    public boolean getIsSimulationRunning() {
        return isSimulationRunning;
    }
    
    private User getRandomUserWithoutChannel() {
        List<User> usersWithoutChannel = users.stream()
                .filter(user -> user.getChannel() == null)
                .collect(Collectors.toList());
        if (!usersWithoutChannel.isEmpty()) {
            return usersWithoutChannel.get((int) (Math.random()*(usersWithoutChannel.size()-1)));
        }
        return null;
    }
    
    public void addMedia(Media someMedia) {
        media.add(someMedia);
    }
        
    public void start() {
        isSimulationRunning = true;
        int numberOfUsers = 20;
        int numberOfChannels = 10;
        
        for (int i = 0; i < numberOfUsers; i++) {
            String userName = "User"+i;
            User createdUser = new User(this, "U"+(i%4 + 1)+".jpg", userName, LocalDateTime.now(), Math.random()<0.3);
            users.add(createdUser);
            Thread userThread = new Thread(createdUser);
            allThreads.add(userThread);
            userThread.start();
        }
        for (int i = 0; i < numberOfChannels; i++) {
            String channelName = "Channel"+i;
            User userWithoutChannel = getRandomUserWithoutChannel();
            if (userWithoutChannel != null) {
                Channel channel = new Channel(i, this, userWithoutChannel, channelName);
                userWithoutChannel.setChannel(channel); // assign the channel to user
                channels.add(channel);
                Thread channelThread = new Thread(channel);
                allThreads.add(channelThread);
                channelThread.start();  
            }
        }
        for (User j : users) {
            int channelsToFollow = (int) (Math.random()*(channels.size()-1) + 1);
            for (int i = 0; i < channelsToFollow; i++) {
                int channelIndex = (int) (Math.random()*(channels.size()-1) + 1);
                j.subscribeToChannel(channels.get(channelIndex));
            }
        }
    }
    public void resume() {
        if (isSimulationRunning == false) {
            isSimulationRunning = true;
            for (User i : users) {
                    i.updateSimulation(this);
            }
            for (User i: users) {
                Thread userThread = new Thread(i);
                allThreads.add(userThread);
                userThread.start();
            }
            for (Channel i: channels) {
                    i.updateSimulation(this);
            }
            for (Channel i: channels) {
                Thread channelThread = new Thread(i);
                allThreads.add(channelThread);
                channelThread.start();
            }
        }
    }
    public void stop() {
        isSimulationRunning = false;
        //System.out.println("Simulation paused");
    }
    public boolean save() {
        try (ObjectOutputStream objOutStr = new ObjectOutputStream(new FileOutputStream("simulator1.ser"))) {
            objOutStr.writeObject(this);
            return true;
        }
        catch (IOException ex) {
            //System.out.println("No serialization");
            return false;
        }
    }
    public void load() {
        Simulator loadedSimulator = null;
        try {
            ObjectInputStream objInStr = new ObjectInputStream(new FileInputStream("simulator1.ser"));
            loadedSimulator = (Simulator)objInStr.readObject();
            users = loadedSimulator.users;
            //System.out.println(users.size());
            channels = loadedSimulator.channels;
            //System.out.println(channels.size());
            media = loadedSimulator.media;
            //System.out.println(media.size());
            isSimulationRunning = false;
        } catch (IOException | ClassNotFoundException ex) {
            System.out.println("No file was found");
        }
    }
}
