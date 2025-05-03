/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany._kuba_czech_javaproject;

/**
 * 
 * @Kuba
*/

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

class Stream extends Media implements Serializable{
    private volatile int currentSpectators;
    private final LocalDateTime startTime;
    private volatile LocalDateTime endTime;

    public Stream(Channel someChannel, String someThumbnail, String someName, String someDescription, LocalDateTime dateOfStart) {
        super(someChannel, someThumbnail, someName, someDescription, false);
        currentSpectators = 0;
        startTime = dateOfStart;
        endTime = null;
    }
    //getters:
    public LocalDateTime getEndTime() {
        return endTime;
    }
    
    //setters:
    public void setEndTime(LocalDateTime dateOfFinish) {
        endTime = dateOfFinish;
    }
    
    //different
    @Override
    public List<String> getInfoAboutMedia(){
        List<String> someList = new ArrayList<>();
        someList.add(super.getThumbnail());
        someList.add(super.getName());
        someList.add(super.getChannel().getName());
        someList.add(startTime.toString());
        if (endTime == null){
            someList.add(Integer.toString(currentSpectators));
        }
        else{
            someList.add("Stream finished at "+endTime.toString());
        }
        someList.add(Integer.toString(super.getNumberLikes()));
        someList.add(super.getDescription());
        return someList;
    }
    
    @Override    
    public String toString() {
        if (endTime == null) {
            return super.getThumbnail() +  "\nName: " + super.getName() + 
                    "\nStreaming on: " + super.getChannel().getName() + 
                    "\nStarted at: " + startTime + 
                    "\nCurrently Watching: " +  currentSpectators + 
                    "\nLikes: " + super.getNumberLikes() +
                    "\nDescription: " + super.getDescription() + "\n";
        } else {
            return super.getThumbnail() + "\nName: " + super.getName() + 
                    "\nWas streaming on: " + super.getChannel().getName() + 
                    "\nStarted at: " + startTime + 
                    "\nFinished at: " + endTime + 
                    "\nLikes: " + super.getNumberLikes() +
                    "\nDescription: " + super.getDescription()+"\n"; 
        }
    }
    
    public void watchAndIncrementNumberOfSpectators() {
        currentSpectators += 1;
    }
    public void exitAndDecrementNumberOfSpectators() {
        currentSpectators -= 1;
    }
}
