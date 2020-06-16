
#include <stdio.h>
#include <time.h>

unsigned long long int ack(unsigned int n, unsigned long long int m)
{
    printf(" n=%d und m=%dt\n", n, m);
    if (n == 0){
        return m+1;
    }
    else if (m == 0){
        return ack(n-1,1);
    }
    else{
        return ack(n-1,ack(n,m-1));
    }
}

int main(int argc, int** argv){

    for(int n=4; n <= 4; ++n){
        for(int m=2; m <= 4; ++m){
            clock_t begin = clock();
            unsigned long long int ack_res = ack(n,m);
            clock_t end = clock();
            double time_spent = (double)(end - begin) / (CLOCKS_PER_SEC/1000.0);
            printf("ack von n=%d und m=%d ist: %d, mill_secs=%f\n", n, m, ack_res, time_spent);
        }
    }    

    return 0;
}