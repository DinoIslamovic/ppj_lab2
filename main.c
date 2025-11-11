#include <stdio.h>
#include <stdlib.h>

int main() {
    char* line;
    size_t len;
    while (getline(&line,&len,stdin)!=-1) {
        printf("<s>%s",line);
        free(line);
    }
    return EXIT_SUCCESS;
}
