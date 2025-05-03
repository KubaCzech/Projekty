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
import java.util.List;

class Media implements Serializable {
    private final Channel channel;
    private final String thumbnail;
    private final String name;
    private final String description;
    private volatile int numberOfLikes;
    private final boolean premiumOrNot;

    public Media(Channel someChannel, String someThumbnail, String someName, String someDescription, boolean someBoolean) {
        channel = someChannel;
        thumbnail = someThumbnail;
        name = someName;
        description = someDescription;
        numberOfLikes = 0;
        premiumOrNot = someBoolean;
    }
    
    //getters:
    public boolean getPremiumOrNot() {
        return premiumOrNot;
    }
    public Channel getChannel() {
        return channel;
    }
    public String getThumbnail() {
        return thumbnail;
    }
    public String getName() {
        return name;
    }
    public String getDescription() {
        return description;
    }
    public int getNumberLikes() {
        return numberOfLikes;
    }
    //different
    public void like() {
        numberOfLikes += 1;
    }
    
    public List<String> getInfoAboutMedia(){
        return null;
    }
} 
