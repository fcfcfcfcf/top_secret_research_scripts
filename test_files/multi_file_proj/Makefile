# --------------------------------------------------------------
# Output settings
# --------------------------------------------------------------
QUIET := @
ECHO := @echo
ifneq ($(QUIET),@)
ECHO := @true
endif

# --------------------------------------------------------------
# Compiler settings
# --------------------------------------------------------------
CXX = clang++
IR_PRE_FLAGS = -S -emit-llvm
BC_PRE_FLAGS = -c -emit-llvm
C_FLAGS = -std=c++11 -g -MP -MD -Wall
C_FLAGS += -Wextra -Wwrite-strings -Wno-parentheses

IR_LINKER = llvm-link
#BC_LINKER = ld
BC_LINKER = llvm-link

# --------------------------------------------------------------
# Directories
# --------------------------------------------------------------
SDIR = ./src
BDIR = ./build
IDIR = ./include
LDIR = -L ./lib

IRDIR = ./llvm_ir
BCDIR = ./llvm_bc

TDIR = ./test
TEST_BDIR = $(BDIR)/test
TEST_IDIR = $(IDIR)/test

# --------------------------------------------------------------
# Executables
# --------------------------------------------------------------
EXEC = runner
TARGET = ./bin/$(EXEC)
TESTER = ./bin/tester

IR_OUTPUT = ./bin/output.ll
BC_OUTPUT = ./bin/output.bc

# --------------------------------------------------------------
# Includes
# --------------------------------------------------------------
INC = $(patsubst %,-I%,$(IDIR))
TEST_INC = $(INC) $(patsubst %,-I%,$(TEST_IDIR))

# --------------------------------------------------------------
# Source extension
# --------------------------------------------------------------
SRCEXT = cpp
IREXT = ll
BCEXT = bc

# --------------------------------------------------------------
# Sources, Objects, and Libraries
# --------------------------------------------------------------
SOURCES = $(shell find $(SDIR) -type f -name *.$(SRCEXT))
OBJ = $(patsubst $(SDIR)/%,$(BDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
TEST_SOURCES = $(shell find $(TDIR) -type f -name *.$(SRCEXT))
TEST_OBJ = $(patsubst $(TDIR)/%,$(TEST_BDIR)/%,$(TEST_SOURCES:.$(SRCEXT)=.o)) $(filter-out $(BDIR)/main.o, $(OBJ))
LIBS = 

# --------------------------------------------------------------
# Archieve name for tar and zip
# --------------------------------------------------------------
ARCHIVE_NAME = $(EXEC)-$(shell date '+%F')

# --------------------------------------------------------------
# Make settings
# --------------------------------------------------------------
.SUFFIXES:
.DELETE_ON_ERROR:

# --------------------------------------------------------------

.PHONY: all tester link_ir link_bc
all: $(TARGET)
tester: $(TESTER)

$(BDIR)/%.o: $(SDIR)/%.$(SRCEXT)
	$(QUIET) @mkdir -p $(dir $@)
	$(ECHO) "=============";
	$(ECHO) "Emitting ll $<";
	$(ECHO) "=============";
	$(QUIET) $(CXX) $(IR_PRE_FLAGS) $(INC) $< $(LIBS)
	$(ECHO) "[OK] $<"
	$(ECHO) "=============";
	$(ECHO) "Emitting bc $<";
	$(ECHO) "=============";
	$(QUIET) $(CXX) $(BC_PRE_FLAGS) $(INC) $< $(LIBS)
	$(ECHO) "[OK] $<"
	$(ECHO) "=============";
	$(ECHO) "Compiling $<";
	$(ECHO) "=============";
	$(QUIET) $(CXX) $(C_FLAGS) $(INC) -c -o $@ $< $(LIBS)
	$(ECHO) "[OK]  $@"

$(TEST_BDIR)/%.o: $(TDIR)/%.$(SRCEXT)
	$(QUIET) @mkdir -p $(dir $@)
	$(ECHO) "=============";
	$(ECHO) "Compiling test file $<";
	$(ECHO) "=============";
	$(QUIET) $(CXX) $(C_FLAGS) $(TEST_INC) -c -o $@ $< $(LIBS)
	$(ECHO) "[OK]  $@"

$(TARGET): $(OBJ)
	$(ECHO) "=============";
	$(ECHO) "Linking the target $@"
	$(ECHO) "=============";
	$(QUIET) $(CXX)  $(LDIR) -o $@ $^ $(C_FLAGS) $(LIBS)
	$(ECHO) "[OK]  $@"
	$(ECHO) "-- Link finished --";
	$(QUIET) $(shell mv *.$(IREXT) $(IRDIR))
	$(QUIET) $(shell mv *.$(BCEXT) $(BCDIR))

$(TESTER): $(TEST_OBJ)
	$(ECHO) "=============";
	$(ECHO) "Linking the target $@"
	$(ECHO) "=============";
	$(QUIET) $(CXX) $(PRE_FLAGS) $(LDIR) -o $@ $^ $(C_FLAGS) $(LIBS)
	$(ECHO) "[OK]  $@"
	$(ECHO) "-- Link finished --";

link_ir: $(TARGET)
	$(ECHO) "=============";
	$(ECHO) "Linking all IR files"
	$(ECHO) "=============";	
	$(QUIET) $(IR_LINKER) -S -o $(IR_OUTPUT) $(IRDIR)/*.$(IREXT)
	$(ECHO) "[OK] $(IR_OUTPUT)"

link_bc: $(TARGET)
	$(ECHO) "=============";
	$(ECHO) "Linking all bc files"
	$(ECHO) "=============";	
	$(QUIET) $(BC_LINKER) -o $(BC_OUTPUT) $(BCDIR)/*.$(BCEXT)
	$(ECHO) "[OK] $(BC_OUTPUT)"

# --------------------------------------------------------------

.PHONY: test_memory
test_memory: $(TARGET)
	-valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all ./$(EXEC) $(INPUT_FILE) $(RUN_FLAGS)

# --------------------------------------------------------------

.PHONY: clean clean_test clean_all
clean:
	$(ECHO) "Cleaning...";
	$(ECHO) "[CL] $(TARGET)"
	$(ECHO) "[CL] $(BDIR)/*"
	$(ECHO) "[CL] $(IRDIR)/*"
	$(ECHO) "[CL] $(BCDIR)/*"
	$(QUIET) find $(BDIR) -name "*.o" -type f -delete
	$(QUIET) find $(BDIR) -name "*.d" -type f -delete
	$(QUIET) find $(IRDIR) -name "*.$(IREXT)" -type f -delete
	$(QUIET) find $(BCDIR) -name "*.$(BCEXT)" -type f -delete

clean_test:
	$(ECHO) "Cleaning tests...";
	$(ECHO) "[CL] $(TESTER)"
	$(ECHO) "[CL] $(BDIR)/*"
	$(QUIET) find $(BDIR) -name "*.o" -type f -delete
	$(QUIET) find $(BDIR) -name "*.d" -type f -delete

clean_all:
	$(ECHO) "Cleaning all...";
	$(ECHO) "[CL] $(TARGET)"
	$(ECHO) "[CL] $(TESTER)"	
	$(ECHO) "[CL] $(BDIR)/*"
	$(QUIET) find $(BDIR) -name "*.o" -type f -delete
	$(QUIET) find $(BDIR) -name "*.d" -type f -delete

# --------------------------------------------------------------

.PHONY: tar archive zip
tar: clean clean_test
	$(ECHO) "Tarring...";
	$(ECHO) "[OK]  bin/$(ARCHIVE_NAME).tar.gz"
	$(QUIET) tar -czf bin/$(ARCHIVE_NAME).tar.gz . --exclude='bin' --exclude='build'

archive zip: clean clean_test
	$(ECHO) "Zipping...";
	$(ECHO) "[OK]  bin/$(EXEC)-$(shell date '+%F').zip"
	$(QUIET) zip -q -r bin/$(ARCHIVE_NAME).zip . -x bin/* build/*

-include $(OBJ:%.o=%.d) $(TEST_OBJ:%.o=%.d)
