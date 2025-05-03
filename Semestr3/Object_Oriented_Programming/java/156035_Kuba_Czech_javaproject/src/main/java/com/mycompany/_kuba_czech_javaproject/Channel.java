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
import java.util.List;
import java.util.Random;
import java.time.*;

class Channel implements Runnable, Serializable {
    private final int idOfChannel;
    private Simulator simm;
    private final User owner;
    private final String name;
    private List<User> followingAccounts;
    private List<Media> uploadedMedia;
    
    private static final List<String> NAMES_OF_VIDEOS = List.of(
        "Top Gun", "Dune", "Spider-Man: No Way Home", "No Time to Die", "Pretty Woman", "The French Dispatch", "The Power of the Dog", "Licorice Pizza",
        "West Side Story", "The Matrix Resurrections", "The King's Man", "Indiana Jones and the Last Crucade", "Air Force One", "Fugitive", "Pirates Of The Carrabean 2",
        "Avengers Ultron's Age", "Ice Age 2", "Winnie The Pooh", "Private Ryan", "Potop", "Rush Hour 2", "Shanghai Noon", "The Transporter", "The Transporter 2", "The Transporter 3",
        "Die Hard", "Die Hard 2", "Pulp Fiction", "Pan Tadeusz", "Znachor"); 

    private static final Random someRandomNumber = new Random();
    
    public Channel(int someId, Simulator sim, User ownerOfTheChannel, String someName) {
        idOfChannel = someId;
        simm = sim;
        owner = ownerOfTheChannel;
        name = someName;
        followingAccounts = new ArrayList<>();
        uploadedMedia = new ArrayList<>();
    }
    
    //getters:
    public List<User> getFollowers() {
        return followingAccounts;
    }

    public List<Media> getUploadedVideos() {
        return uploadedMedia;
    }
    
    public String getName() {
        return name;
    }
    
    private List<Stream> getActiveStreams() {
        List<Stream> streams = new ArrayList<>();
        for (Media i : uploadedMedia) {
            if (i instanceof Stream stream) {
                if (stream.getEndTime() == null) {
                    streams.add(stream);
                }
            }
        }
        return streams;
    }
    
    //setters:
    public void setUploadedVideos(List<Media> someMedias) {
        uploadedMedia = someMedias;
    }
    
    //different  
    public void updateSimulation(Simulator sim) {
        simm = sim;
    }
    
    public void addFollowingAccount(User someUser) {
        if (!followingAccounts.contains(someUser)) {
            followingAccounts.add(someUser);
            someUser.subscribeToChannel(this);
        }
    }
    
    public void addFollowingAccoutns(List<User> someFollowers) {
        followingAccounts.addAll(someFollowers);
    }
    
    public void informFollowers(Media someMedia) {
        List<User> followingAccountsCopy;
        synchronized (followingAccounts) {
            followingAccountsCopy = new ArrayList<>(followingAccounts);
        }
        for (User i: followingAccountsCopy) {
            if (someMedia.getPremiumOrNot()) {
                if (i.getPremiumOrNot()) {
                    synchronized (i) {
                        i.addMediaToQueue(someMedia);
                    }
                }
            } else {
                synchronized (i) {
                    i.addMediaToQueue(someMedia);
                }
            }
        }
    }
    public void publishContent(int i) {
        if (Math.random()> 0.3) {
            int nameNumber = someRandomNumber.nextInt(30);
            int thumbnailNumber = (int) (Math.random()*(6 - 1) + 1);
            String createdVideoName = NAMES_OF_VIDEOS.get(nameNumber);
            String videoDescription = "Some very nice description" + nameNumber;
            Video createdVideo = new Video(this, "V"+thumbnailNumber+".jpg", createdVideoName + i + idOfChannel, videoDescription, someRandomNumber.nextInt(30) + 1, LocalDateTime.now(), Math.random() < 0.5);
            uploadedMedia.add(createdVideo);
            simm.addMedia(createdVideo);
            informFollowers(createdVideo); //Extra Credit
        } else {
            int nameNumber = someRandomNumber.nextInt(30);
            int thumbnailNumber = (int) (Math.random() * (2 - 1) + 1);
            String createdStreamName = "Stream"+nameNumber;
            String streamDescription = "Some super nice description of stream"  + nameNumber;
            Stream stream = new Stream(this, "s"+thumbnailNumber+".jpg", createdStreamName + i + idOfChannel, streamDescription, LocalDateTime.now());
            uploadedMedia.add(stream);
            simm.addMedia(stream);
            informFollowers(stream); //Extra Credit
        }
    }
    public List<String> getInfoAboutChannel() {
                List<String> someList = new ArrayList<>();
                someList.add(name);
                someList.add(owner.getUsersName());
                someList.add(Integer.toString(followingAccounts.size()));
                someList.add(Integer.toString(uploadedMedia.size()));
                return someList;
    }
    
     public List<String> uploadedVideosToString(){
        List<String> stringsOfMedia = new ArrayList<>();
        for (Media i : uploadedMedia) {
            stringsOfMedia.add(i.getName());
    }
        return stringsOfMedia;
    }
    @Override
    public String toString(){
        return  "\nName: " + name + "\nOwner: " + 
                owner.getUsersName() + 
                "\nNumber of Following Accounts " + followingAccounts.size() + 
                "Number of uploaded media: " + uploadedMedia.size() + "\n"; 
    }
     
    @Override
    public void run() {
        int counter = 0;
        synchronized(simm) {
            publishContent(counter);
        }
        while (simm.getIsSimulationRunning()) {
            try {
                if (Math.random()> 0.6) {
                    synchronized(simm) {
                        publishContent(counter);
                    }
                    counter += 1;
                    if (Math.random() > 0.6) {
                        List<Stream> activeStreams = getActiveStreams();
                        if (!activeStreams.isEmpty()) {
                            int randomIndex = someRandomNumber.nextInt(activeStreams.size());
                            Stream randomStream = activeStreams.get(randomIndex);
                            randomStream.setEndTime(LocalDateTime.now());
                        }
                    }
                }
                Thread.sleep(800);
            } catch (InterruptedException ex) {}
        }
    }
}
