
#include <errno.h>
#include <error.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

/*
 * path - path to file to read
 * buf - resulting data; will be allocated; caller should free it
 * result - 0 if everything OK; 1 if error
 */
int read_file(char *path, char **buf) {
    // get file size [file_info is on stack]
    struct stat file_info;
    if (stat(path, &file_info) == -1) {
        error(0, errno, "error stat'ing %s", path);
        return errno;
    }
    int64_t size = file_info.st_size;
    
    // allocate buffer initialized to zeroes [buf is on heap - any errors from here should free it & clear the pointer]
    if (!(*buf = calloc(size+1, 1))) {
        error(0, errno, "error allocating %ld bytes", size+1);
        return errno;
    }

    // open file for reading [fd is on stack, but it should be closed whatever happens]
    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        error(0, errno, "error opening %s for reading", path);
        return errno;
    }

    // read data into buffer
    char *offset = *buf;
    int count;
    do {
        count = read(fd, offset, size-(offset-*buf));
        offset += count;
    } while (count && ((offset-*buf) < size));
    // XXX: what if count < size at this point? bail out with error?

    // close file
    if (close(fd) == -1) {
        error(0, errno, "error closing %s", path);
        return errno;
    }
    // XXX: what if this fails? according to close(2), it's not wise to close it again

    return 0;

/*
error:
    if (*buf) {
        free(*buf);
        buf = NULL;
    }
    return errno;
*/
}

int count_lines(char *s) {
    int r = 0;
    while (*s != '\0') {
        r += *s++ == '\n';
    }
    return r;
}

int read_lines_2(char *path, char ***lines, int *count) {
    // read data into buffer
    char *data = NULL;
    if (read_file(path, &data)) {
        return 1;
    }

    // resize buffer big enough for list of pointers as well the data
    int nlines = count_lines(data);
    int szdata = strlen(data);
    int szptrs = (nlines + 1) * sizeof(char *);
    void *new_buf = realloc(data, szptrs + szdata);
    if (new_buf == NULL) {
        error(0, errno, "error reallocating buffer");
        return 1;
    }

    // move data to end of buffer
    {
        char *t = (char *)new_buf - 1 + szdata + szptrs;
        char *s = (char *)new_buf - 1 + szdata;
        while (s >= (char *)new_buf) {
            *t-- = *s--;
        }
    }

    // put pointers to lines into start of buffer
    data = (char *)new_buf + szptrs;
    char **pointers = (char **)new_buf;
    char *line_ptr = NULL;
    for (char *line = strtok_r(data, "\n", &line_ptr); line != NULL; line = strtok_r(NULL, "\n", &line_ptr)) {
        *pointers++ = line;
    }

    // put extra NULL pointer
    *pointers = NULL;

    // return result
    *lines = (char **)new_buf;
    *count = nlines;
    return 0;
}

int read_lines(char *path, char ***lines, int *count) {
    char *data = NULL;
    if (read_file(path, &data)) {
        return 1;
    }

    char *line_ptr = NULL;
    for (char *line = strtok_r(data, "\n", &line_ptr); line != NULL; line = strtok_r(NULL, "\n", &line_ptr)) {
    
        // resize array
        char **new_buf = *lines;
        if (!(new_buf = realloc(new_buf, sizeof(char *) * (*count + 1)))) {
            error(0, errno, "error reallocating array");
            return 1;
        }
        *lines = new_buf;
    
        // duplicate string
        char *str = strdup(line);
        if (!str) {
            error(0, errno, "error allocating string");
            return 1;
        }
    
        *(*lines + (*count)++) = str;
    }
    
    free(data);
    return 0;
}
