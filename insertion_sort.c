#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static void insertion_sort(int *values, size_t length) {
    for (size_t i = 1; i < length; i++) {
        int key = values[i];
        size_t j = i;

        while (j > 0 && values[j - 1] > key) {
            values[j] = values[j - 1];
            j--;
        }
        values[j] = key;
    }
}

static double elapsed_seconds(struct timespec start, struct timespec end) {
    return (double)(end.tv_sec - start.tv_sec) +
           (double)(end.tv_nsec - start.tv_nsec) / 1000000000.0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s DATA_FILE\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL) {
        fprintf(stderr, "Could not open %s: %s\n", argv[1], strerror(errno));
        return EXIT_FAILURE;
    }

    size_t capacity = 1024;
    size_t length = 0;
    int *values = malloc(capacity * sizeof(*values));
    if (values == NULL) {
        fclose(input);
        return EXIT_FAILURE;
    }

    int value;
    while (fscanf(input, "%d", &value) == 1) {
        if (length == capacity) {
            capacity *= 2;
            int *resized = realloc(values, capacity * sizeof(*values));
            if (resized == NULL) {
                free(values);
                fclose(input);
                return EXIT_FAILURE;
            }
            values = resized;
        }
        values[length++] = value;
    }
    fclose(input);

    struct timespec start;
    struct timespec end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    insertion_sort(values, length);
    clock_gettime(CLOCK_MONOTONIC, &end);

    for (size_t i = 1; i < length; i++) {
        if (values[i - 1] > values[i]) {
            fprintf(stderr, "Sort verification failed\n");
            free(values);
            return EXIT_FAILURE;
        }
    }

    long long checksum = 0;
    for (size_t i = 0; i < length; i++) {
        checksum += values[i];
    }

    printf("%.9f %lld\n", elapsed_seconds(start, end), checksum);
    free(values);
    return EXIT_SUCCESS;
}
