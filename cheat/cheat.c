#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>

// Parses an integer in the given base, rejecting empty input, trailing junk and
// values outside [min, max] (unlike atoi/sscanf, which accept bad input silently).
// Returns 0 on success and stores the result in *out, -1 otherwise.
static int parse_ll(const char *text, int base, long long min, long long max, long long *out) {
    char *end = NULL;
    errno = 0;
    long long value = strtoll(text, &end, base);
    if (errno != 0 || end == text || *end != '\0' || value < min || value > max) {
        return -1;
    }
    *out = value;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        (void)fprintf(stderr, "Usage: %s <pid> <address_hex> <new_value>\n", argv[0]);
        (void)fprintf(stderr, "Example: %s 12345 0x7ffd5a34bc10 9999\n", argv[0]);
        return 1;
    }
    
    long long parsed = 0;
    if (parse_ll(argv[1], 10, 1, INT_MAX, &parsed) != 0) {
        (void)fprintf(stderr, "Error: Invalid pid '%s'.\n", argv[1]);
        return 1;
    }
    pid_t pid = (pid_t)parsed;
    
    // Parse hex address (strtoll with base 16 accepts an optional 0x prefix)
    if (parse_ll(argv[2], 16, 0, LLONG_MAX, &parsed) != 0) {
        (void)fprintf(stderr, "Error: Invalid address format. Must be hexadecimal (e.g. 0x555555556010 or 555555556010).\n");
        return 1;
    }
    unsigned long long address = (unsigned long long)parsed;

    if (parse_ll(argv[3], 10, INT_MIN, INT_MAX, &parsed) != 0) {
        (void)fprintf(stderr, "Error: Invalid new value '%s'.\n", argv[3]);
        return 1;
    }
    int new_value = (int)parsed;
    
    // Open process memory
    char mem_path[64];
    (void)snprintf(mem_path, sizeof(mem_path), "/proc/%d/mem", pid);
    
    (void)printf("[CHEAT] Opening %s for writing...\n", mem_path);
    int fd = open(mem_path, O_RDWR);
    if (fd == -1) {
        perror("[CHEAT] Error: Failed to open /proc/PID/mem. Are you sure the PID is correct and you have permission?");
        (void)fprintf(stderr, "[CHEAT] Hint: The target process must permit debugging (prctl PR_SET_PTRACER) if Yama ptrace_scope is enabled.\n");
        return 1;
    }
    
    // Seek to the target address
    if (lseek(fd, (off_t)address, SEEK_SET) == (off_t)-1) {
        perror("[CHEAT] Error: Failed to seek to address");
        (void)close(fd);
        return 1;
    }
    
    // Write the new value (4 bytes integer)
    (void)printf("[CHEAT] Writing new value %d to address 0x%llX...\n", new_value, address);
    ssize_t bytes_written = write(fd, &new_value, sizeof(int));
    if (bytes_written != sizeof(int)) {
        perror("[CHEAT] Error: Failed to write to memory");
        (void)close(fd);
        return 1;
    }
    
    (void)printf("[CHEAT] SUCCESS! Wrote %zd bytes. Target variable updated.\n", bytes_written);
    
    (void)close(fd);
    return 0;
}
