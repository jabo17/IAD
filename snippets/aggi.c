#include <stdio.h>

unsigned int ack(int n, int m){
    if (n == 0){
        return m+1;
    }
    else if (m == 0){
        return ack(n,1);
    }
    else{
        return ack(n-1,ack(n,m-1));
    }
}

int main(){
     for(int n=0; n < 4; ++n){
        for(int m=0; m < 4; ++m){
            printf("ack von n=$d und m=$d ist: $d", n, m, ack(n,m));
        }
    }    

    return 0;
}