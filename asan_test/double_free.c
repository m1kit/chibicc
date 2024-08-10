#include <stdlib.h>

int main() {
  void* ptr1 = malloc(1);
  free(ptr1);

  void* ptr2 = malloc(1);
  free(ptr1);

  exit(0);
}
