#pragma once
#include "Vehicle.hpp"



class F1_car : public Vehicle
{
public:
    F1_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    virtual void takeTurn(float someDistance) =0; //pure virtual function
    virtual std::string toString() const =0; //pure virtual function
    //getters:
    float getDrs() const;
    float getTurbo() const;
    bool getDrsUsage() const;
    //setters:
    void setDrsUsage(float someDist);
protected:
    float mDrs;
    float mTurbo;
    bool mDrsUsage;
};
