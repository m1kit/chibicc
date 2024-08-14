int printf();
int pthread_create(); 
int pthread_join(); 
int pthread_mutex_lock();
int pthread_mutex_unlock();
void* malloc();

int counter = 0;
void* lock;

long tid_0;
long tid_1;

void* func(void* arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(lock);
        counter++;
        pthread_mutex_unlock(lock); 
    }
} 

int main() {
    lock = malloc(1234);

    pthread_create(&tid_0, 0, &func, 0);
    pthread_create(&tid_1, 0, &func, 0);

    pthread_join(tid_0, 0);
    pthread_join(tid_1, 0);

    printf("counter = %d\n", counter); 
    return 0;
}
