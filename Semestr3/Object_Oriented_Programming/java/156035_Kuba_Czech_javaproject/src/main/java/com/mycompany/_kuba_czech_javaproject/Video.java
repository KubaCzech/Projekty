/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany._kuba_czech_javaproject;

import java.util.List;
import java.util.ArrayList;
/**
 *
 * @author Kuba
 */

import java.io.Serializable;
import java.time.LocalDateTime;

class Video extends Media implements Serializable {
    private final int duration; //once set, no changes
    private final LocalDateTime uploadDate;
    private volatile int numberOfViews;

    public Video(Channel someChannel, String someThumbnail, String someName, String someDescription, int someDuration, LocalDateTime someDate, boolean someBoolean) {
        super(someChannel, someThumbnail, someName, someDescription, someBoolean);
        duration = someDuration;
        uploadDate = someDate;
        numberOfViews = 0;
    }
    
    //different
    @Override
    public String toString() {
        return super.getThumbnail() + 
                "\nName: " + super.getName() + 
                "\nChannel: " + super.getChannel().getName() +
                "\nUpload date: " + uploadDate + 
                "\nDuration: " + duration + " minutes\nNumber Of Views: " + numberOfViews + 
                "\nNumber of Likes: " + super.getNumberLikes() + "\nIs premium? " + super.getPremiumOrNot() + 
                "\nDescription: " + super.getDescription() + "\n";
    }
    @Override
    public List<String> getInfoAboutMedia(){
        List<String> someList = new ArrayList<>();
        someList.add(super.getThumbnail());
        someList.add(super.getName());
        someList.add(super.getChannel().getName());
        someList.add(uploadDate.toString());
        someList.add(Integer.toString(duration));
        someList.add(Integer.toString(numberOfViews));
        someList.add(Integer.toString(super.getNumberLikes()));
        if (super.getPremiumOrNot()){
            someList.add("Yes");
        }
        else
            someList.add("No");
        someList.add(super.getDescription());
        return someList;
    }
    public void incrementNumberOfViews() {
        numberOfViews += 1;
    }
}