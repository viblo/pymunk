    #include "chipmunk.h"

    double mass_sum(size_t numof, cpBody ** body);
    double mass_sum(size_t numof, cpBody ** body){
        double totalmass = 0;  
        for (int i=0; i<numof; i++){    
             totalmass += cpBodyGetMass(body[i]);
        }
        return totalmass;
    }