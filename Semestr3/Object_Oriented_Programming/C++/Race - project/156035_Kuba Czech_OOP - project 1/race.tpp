#pragma once
#include <chrono>
#include <thread>
    template <typename V>
    Race<V>::Race(){}

    //Memory deallocation at the end
    template <typename V>
    Race<V>::~Race(){
        int index=vehicles.size() - 1;
        while(vehicles.size() > 0){
            *this -= index;
            index--;
        }
    }

    template <typename V>
    void
    Race<V>::operator+=(Vehicle* veh)
    {
        vehicles.push_back(veh);
    }

    template <typename V>
    void
    Race<V>::operator-=(int k)
    {
        vehicles.erase(vehicles.begin() + k);
    }

    template <typename V>
    void
    Race<V>::displayResults() const
    {
        for (int a=0; a<vehicles.size(); a++)
        {
            std::cout<<a+1<<". "<<vehicles[a]->toString()<<std::endl;
        }
    }

    template <typename V>
    void
    Race<V>::waitAndClear()
    {
        //std::this_thread::sleep_for(std::chrono::seconds(2)); //cross-platform - doesn't work
        long long i=0;
        while (i<=300000000)
            i++;
        system("cls"); //only windows
    }

    template <typename V>
    void
    Race<V>::Factory()
    {
        std::vector <std::string> allDrivers= {"Daniel Ricciardo", "Pierre Gasly", "Alex Albon", "Giancarlo Fisichella","Rober Kubica", "Lewis Hamilton", "Ayrton Senna", "Max Verstappen", "Kimi Raikkonen", "Fernando Alonso", "Sergio Perez", "George Russel", "Nico Rosberg", "Jenson Button", "Stoffel Vandorne", "Nick de Vries", "Lando Norris", "Oscar Piastri", "Mika Hakkinen", "Alain Prost"};
        std::vector <std::string> allFerrariDrivers = {"Jean Alesi" ,"Luca Badoer", "Gerherd Berger", "Eddie Ervine", "Charles Leclerc", "Felipe Massa", "Michael Schumacher", "Sebastian Vettel", "Carlos Sainz", "Niki Lauda", "Rubens Barichello", "Gilles Villenueve", "Mike Hawthorne", "Alberto Ascari"};
        std::vector <int>DriversIds = {3, 10, 23, 65, 88, 44, 3, 33, 7, 14, 11, 63, 13, 85, 6, 21, 4, 81, 91, 46};
        std::vector <int>FerrariIds = {32, 98, 66, 57, 16, 2, 1, 5, 55, 99, 85, 38, 53, 90};

        for (int i=0; i<numberOfVehicles; i++)
        {
            int prob = rand()%8;
            std::string driverToPut;
            float prob2 = (float)(rand())/(float)(RAND_MAX);
            bool spoilerOrNot;
            int idToPut;
            if (prob <2){
                int index = rand()% allFerrariDrivers.size();
                driverToPut = allFerrariDrivers[index];
                idToPut = FerrariIds[index];
                allFerrariDrivers.erase(allFerrariDrivers.begin()+index);
                FerrariIds.erase(FerrariIds.begin()+index);
            }
            else{
                int index = rand()%allDrivers.size();
                driverToPut = allDrivers[index];
                idToPut = DriversIds[index];
                allDrivers.erase(allDrivers.begin() + index);
                DriversIds.erase(DriversIds.begin() + index);
                if (prob2 <(float)(0.5))
                    spoilerOrNot = false;
                else
                    spoilerOrNot = true;
            }
            switch (prob){
            case 0:
                 *this += new ScuderiaFerrari(driverToPut, idToPut, 0.f, std::max(90.f, (float) 110.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.3, (float)(rand()/(float)(RAND_MAX))), std::min(15.f, 30 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 1:
                *this += new ScuderiaFerrari(driverToPut, idToPut, 0.f, std::max(90.f, (float) 90.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.2, (float)(rand()/(float)(RAND_MAX))), std::min(15.f, 35 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 2:
                *this += new RedBullRacing(driverToPut, idToPut, std::max((float) 0.01, (float) 0.08 * (float)(rand())/(float)(RAND_MAX)), std::max(75.f, (float) 90.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.4, (float)(rand()/(float)(RAND_MAX))), std::min(10.f, 20 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 3:
                *this += new Lamborghini(driverToPut, idToPut, 0.f, std::max(90.f, (float) 150*(float)(rand())/(float)(RAND_MAX)), spoilerOrNot);
                break;
            case 4:
                *this += new Bugatti(driverToPut, idToPut, 0.05, std::max(80.f, (float) 120*(float)(rand())/(float)(RAND_MAX)), spoilerOrNot);
                break;
            case 5:
                *this += new Jaguar(driverToPut, idToPut, 0.1, std::max(150.f, (float) 200*(float)(rand())/(float)(RAND_MAX)), std::max(0.15, 0.5 * (float)(rand())/(float)(RAND_MAX)));
                break;
            case 6:
                *this += new Porsche(driverToPut, idToPut, 0.03, std::max(130.f, (float) 170*(float)(rand())/(float)(RAND_MAX)), std::max(0.25, 0.9 * (float)(rand())/(float)(RAND_MAX)));
                break;
            case 7:
                *this += new MercedesAMGPetronas(driverToPut, idToPut, std::max(0.005, 0.01 * (float)(rand())/(float)(RAND_MAX)), std::max(80.f, 100*(float)(rand())/(float)(RAND_MAX)), std::min((float) 0.2, 2*(float)(rand())/(float)(RAND_MAX)), std::min(20.f, 35 * (float)(rand())/(float)(RAND_MAX)));
                break;
            }

        }
    }
    template <typename V>
    void
    Race<V>::sortVector()
    {
        std::sort(vehicles.begin(), vehicles.end(), [](const Vehicle* a, const Vehicle* b){
                  return a->getTravelledDistance() > b->getTravelledDistance();
            });
    }
    template <typename V>
    void
    Race<V>::Run()
    {
        std::cout<<"Insert number of turns"<<std::endl;
        Race<V>::numberOfLaps = 25;
        std::cout<<numberOfLaps<<std::endl;
        //std::cin>>numberOfLaps;
        std::cout<<"Insert number of vehicles participating"<<std::endl;
        //std::cin>>numberOfVehicles;
        Race<V>::numberOfVehicles = 20;
        std::cout<<numberOfVehicles<<std::endl;
        //waitAndClear();
        Race<V>::driversInRace = numberOfVehicles;
        std::cout<<"Factory time - vehicles to participate in a race are being constructed"<<std::endl;
        Race<V>::Factory();
        std::cout<<"All cars are constructed"<<std::endl;
        std::cout<<"Let's race"<<std::endl;
        waitAndClear();
        for (int i=0; i<numberOfLaps && driversInRace > 0; i++){
            driversInRace = numberOfVehicles;
            for (int j=vehicles.size(); j>0; j--){
                float someDistance;
                if (j == 0)
                    someDistance = 2* vehicles[j]->getTravelledDistance();
                else
                    someDistance = vehicles[j-1]->getTravelledDistance();
                if (vehicles[j]->getFuelOrEnergy() <=0 or vehicles[j]->getMalfunctionRate() == 1.0)
                    driversInRace--;
                vehicles[j]->takeTurn(someDistance);
                sortVector();
            }
            if (i+1 >= numberOfLaps)
                std::cout<<"Final Results: "<<std::endl;
            else
                std::cout<<"Lap "<<i+1<<std::endl;
            displayResults();
            if (i+1 < numberOfLaps)
                waitAndClear();
        }
        if (driversInRace < 1)
            std::cout<<"Race finished earlier because all drivers are out of Race"<<std::endl;
        std::cout<<"Thank You for participating in a race. Taht's it"<<std::endl;
    }
