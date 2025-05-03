#pragma once

#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <algorithm>

class Vehicle{
public:
    //constructor with parameters
    Vehicle(const std::string &Manufacturer, const std::string &Driver, const int IdOfCar,  float MalfunctionRate, float FuelOrEnergy);
    virtual std::string toString() const =0; //pure virtual function - class will be abstract
    virtual void takeTurn(float someDistance) =0; //pure virtual function - class will be abstract

    //Getters
    std::string getManufacturer() const;
    std::string getDriver() const;
    int getIdOfCar() const;
    float getMalfunctionRate()  const;
    float getTravelledDistance() const;
    float getFuelOrEnergy() const;

    //Setters
    void setTravelledDistance(float dist);
    void setFuelOrEnergy(float FuelConsumption);

protected:
    //fields
    std::string mManufacturer;
    std::string mDriver;
    int mIdOfCar;
    float mMalfunctionRate;
    float mTravelledDistance;
    float mFuelOrEnergy;

};
