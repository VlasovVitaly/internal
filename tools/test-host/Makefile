TARGET = testhost
PREFIX = /usr/local
WARNINGS = -Werror -Wall -Wextra
FLAGS = -O3
CFLAGS += $(WARNINGS) $(FLAGS)

default: $(TARGET)

test-host.o: test-host.c
	gcc $(CFLAGS) -c test-host.c

$(TARGET): test-host.o
	gcc $(CFLAGS) -o $(TARGET) test-host.o

clean:
	-rm -f test-host.o
	-rm -f $(TARGET)

install: $(TARGET)
	/usr/bin/install --strip --strip-program=/usr/bin/strip -m 755 \
			 $(TARGET) $(PREFIX)/bin

uninstall:
	-rm -f $(PREFIX)/bin/$(TARGET)

.PHONY: default clean install uninstall
