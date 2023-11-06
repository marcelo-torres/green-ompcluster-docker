#include <cstdio>
#include <cstdlib>

#include <omp.h>
#include <unistd.h>

int producer() {
  int value =
 rand() % 11;
  //printf("[WORKER] value (initial) = %d\n", value);
  char hostname[1024];
  hostname[1023] = '\0';
  gethostname(hostname, 1023);
  //printf("[1][PRODUCER][PID=%d] Node: %s\n", getpid(), hostname);
  return value;
}

int square(int value) {
  char hostname[1024];
  hostname[1023] = '\0';
  gethostname(hostname, 1023);
  //printf("[2][SQUARE][PID=%d] Node: %s\n", getpid(), hostname);
  return value * value;
}

int add_one(int value) {
  char hostname[1024];
  hostname[1023] = '\0';
  gethostname(hostname, 1023);
  //printf("[3][ADD_ONE][PID=%d] Node: %s\n", getpid(), hostname);
  return value + 1;
}

void display(int value) {
  char hostname[1024];
  hostname[1023] = '\0';
  gethostname(hostname, 1023);
  //printf("[4][DISPLAY][PID=%d] Node: %s\n", getpid(), hostname);
  //printf("[WORKER] value (final) = %d\n", value);
}

int main(int argc, char **argv) {
  int value = 999;

  double t;
  t = omp_get_wtime();

  #pragma omp parallel
  #pragma omp single
  {
    #pragma omp target nowait depend(out : value) map(from : value)
    value = producer();

    #pragma omp target nowait depend(inout : value) map(tofrom : value)
    value = square(value);

    #pragma omp target nowait depend(inout : value) map(tofrom : value)
    value = add_one(value);

    #pragma omp target nowait depend(in : value) map(to : value)
    display(value);

    //printf("[=HOST=] value (inside region) = %d\n", value);
  }


  //printf("[=HOST=] value (outside region) = %d\n", value);
  t = omp_get_wtime() - t;
  fprintf(stdout, "Computation done in %0.6lfs\n", t);
  return 0;
}
