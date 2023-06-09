include .mk.defs

BASEDIR = ./
X264_DIR = $(BASEDIR)../x264

BUILD_DIR = .
SUBDIRS = wrapper

CFLAGS += -I$(X264_DIR)/include

ifeq ($(OS_TYPE), Linux)
LDFLAGS = -shared '-Wl,-rpath,$$ORIGIN' -Wl,-z,origin -lpthread -stdlib=libc++
else
LDFLAGS = -dynamiclib
endif

TARGET = $(BINDIR)/x264_encoder_plugin.dvcp

LDFLAGS += -L$(X264_DIR)/lib -lx264 -lz

OBJDIR = $(BUILD_DIR)/build
BINDIR = $(BUILD_DIR)/bin

.PHONY: all

HEADERS = plugin.h x264_encoder.h audio_encoder.h
SRCS = plugin.cpp x264_encoder.cpp dummy_container.cpp audio_encoder.cpp
OBJS = $(SRCS:%.cpp=$(OBJDIR)/%.o)

all: prereq make-subdirs $(HEADERS) $(SRCS) $(OBJS) $(TARGET)

prereq:
	mkdir -p $(OBJDIR)
	mkdir -p $(BINDIR)

$(OBJDIR)/%.o: %.cpp
	$(CC) -c -o $@ $< $(CFLAGS)

$(TARGET):
	$(CC) $(OBJDIR)/*.o $(LDFLAGS) -o $(TARGET)

clean: clean-subdirs
	rm -rf $(OBJDIR)
	rm -rf $(BINDIR)

make-subdirs:
	@for subdir in $(SUBDIRS); do \
	echo "Making $$subdir"; \
	(cd $$subdir; make; cd ..) \
	done

clean-subdirs:
	@for subdir in $(SUBDIRS); do \
	echo "Making clean in $$subdir"; \
	(cd $$subdir; make clean; cd ..) \
	done
