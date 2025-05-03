/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany._kuba_czech_javaproject;

/**
 *
 * @author Kuba
 */

import java.io.Serializable;
import java.util.ArrayList;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Queue;
import java.util.LinkedList;
import java.util.Random;

class User implements Runnable, Serializable {
    private Simulator simm;
    private final String thumbnail;
    private final String name;
    private final LocalDateTime dateOfJoining;
    private Channel usersChannel; //if there is - channel, if not - null
    private List<Channel> followingChannels;
    private final boolean isPremiumOrNot;
    private volatile Media nowWatching;
    private volatile Queue<Media> waitingMedia; //Queue >> List, in list we need to take 0th element and remove. Queue does it for us

    public User(Simulator sim, String someThumbnail, String someName, LocalDateTime someDate, boolean someBoolean) {
        simm = sim;
        thumbnail = someThumbnail;
        name = someName;
        dateOfJoining = someDate;
        followingChannels = new ArrayList<>();
        isPremiumOrNot = someBoolean;
        nowWatching = null;
        usersChannel = null;
        waitingMedia = new LinkedList<>();
    }

    public void updateSimulation(Simulator sim) {
        simm = sim;
    }
    public void subscribeToChannel(Channel someChannel) {
        if (!followingChannels.contains(someChannel)) {
            followingChannels.add(someChannel);
            someChannel.addFollowingAccount(this);
        }
    }
    //getters:
    public Channel getChannel() {
        return usersChannel;
    }
    
    public String getThumbnail() {
        return thumbnail;
    }
    
    public String getUsersName() { //getName() does not work for threads ???
        return name;
    }
    
    public LocalDateTime getJoinDate() {
        return dateOfJoining;
    }
    
    public List<Channel> getFollowingChannels() {
        return followingChannels;
    }
    
    public boolean getPremiumOrNot() {
        return isPremiumOrNot;
    }
    
    public Media getNowWatching() {
        return nowWatching;
    }
    
    public Queue<Media> getWaitingMedia() {
        return waitingMedia;
    }
    
    public List<String> getInfoAboutUser() {
        List<String> someList = new ArrayList<>();
        someList.add(thumbnail);
        someList.add(name);
        if (usersChannel != null) {
            someList.add("Yes, it's "+usersChannel.getName());
        }
        else
            someList.add("No");
        someList.add(dateOfJoining.toString());
        if (isPremiumOrNot){
            someList.add("Yes!");
        }
        else{
            someList.add("No :(");
        }
        if (nowWatching == null){
            someList.add("Nothing");
        }
        else{
            someList.add(nowWatching.getName());
        }
        return someList;
    }
    
    public List<String> getListOfFollowers(){
        List<String> someList = new ArrayList<>();
        for (Channel i: followingChannels) {
            someList.add(i.getName());
        }
        return someList;
    }
    
    public List<String> getListOfWaitingMedia(){
        List<String> someList = new ArrayList<>();
        for (Media i: waitingMedia) {
            someList.add(i.getName());
        }   
        return someList;
    }
        
    //Setters:
    public void setChannel(Channel someChannel) {
        usersChannel = someChannel;
    }
    
    public void setNowWatching(Media someMedia) {
        nowWatching = someMedia;
    }    
    
    public void setWaitingMedia(){
        List<Media> availableMedia = simm.getMedia();
        int someRandom = (int) Math.floor(Math.random()*availableMedia.size());
        for (int i =0; i<someRandom; i++){
            int index = (int) Math.floor(Math.random()*availableMedia.size());
            waitingMedia.add(availableMedia.get(index));
        }
        
    }
    
    //different
    @Override
    public void run() {
        Random random = new Random();
        try {
            Thread.sleep(1000);
            while (simm.getIsSimulationRunning()) {
                synchronized (waitingMedia) {
                    //System.out.println("Leci");
                    try {
                        while (waitingMedia.size() == 0) {
                            waitingMedia.wait(1000);
                            if (!simm.getIsSimulationRunning()) {
                                break;}
                            setWaitingMedia();
                        }
                        if (waitingMedia.size() != 0) {
                            synchronized (this) {
                                try {
                                    nowWatching = waitingMedia.poll();
                                    if (Math.random() > 0.7) {
                                        nowWatching.like();
                                    }
                                    if (nowWatching instanceof Stream stream) {
                                        stream.watchAndIncrementNumberOfSpectators();
                                        Thread.sleep(5000); //simulating watching a stream
                                        stream.exitAndDecrementNumberOfSpectators();
                                    }
                                    else {
                                        Video video = (Video) nowWatching;
                                        video.incrementNumberOfViews();
                                        Thread.sleep(3000); //simulating of watching a video
                                    }
                                    
                                } catch (InterruptedException ex) {}
                            }
                        }
                    } catch (InterruptedException e) {}
                }
            }
        } catch (InterruptedException e) {}
    }
    
    @Override
    public String toString(){
        String usersChannelName = "No channel";
        if(usersChannel != null){
            usersChannelName = usersChannel.getName();
        }
        return  "\nName: " + name + "\nDate Of Joining: " + 
                dateOfJoining.toString() + "\nChannel: " + usersChannelName + "\nPremium user?: " 
                + isPremiumOrNot + "\nNumber of Following Accounts " + followingChannels.size() + 
                "\nNow watching: " + nowWatching.getName() + "\n" +  
                "Number of videos in queue: " + waitingMedia.size() + "\n"; 
    }
    
    public void addMediaToQueue(Media someMedia) {
        synchronized(waitingMedia) {
           waitingMedia.add(someMedia);
           waitingMedia.notify(); 
        }
    }
}
