#include <stdlib.h>
#include <stdio.h>

#define NUM_FREE_MAX 1024

void* chibicc_asan_malloc(size_t n) {
  return malloc(n);
}

int chibicc_asan_num_free = 0;
void* chibicc_asan_freed_pointers[NUM_FREE_MAX];

void chibicc_asan_free(void* p) {
  for (int i = 0; i < chibicc_asan_num_free; i++) {
    if (chibicc_asan_freed_pointers[i] == p) {
      fprintf(stderr, "[ASan] Double-Free detected: %p\n", p);
      exit(1);
    }
  }
  if (chibicc_asan_num_free < NUM_FREE_MAX) {
    chibicc_asan_freed_pointers[chibicc_asan_num_free++] = p;
  }

  // Intentionally skip free(): when freed it may be reused.
  // free(p);
}
