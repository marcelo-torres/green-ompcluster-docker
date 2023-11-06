#include <omp.h>
#include <string>

struct Timer {
  Timer(const char *name) : begin_(0), end_(0), name_(name) {
    printf("===== STARTING '%s' ======\n", name);
    begin_ = omp_get_wtime();
  }

  ~Timer() {
    end_ = omp_get_wtime();
    printf("===== FINISHED in %lf s ======\n", end_ - begin_);
  }

private:
  double begin_;
  double end_;
  std::string name_;
};
