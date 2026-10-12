
cmake_minimum_required(VERSION 3.16)

project(DUNE_TMS LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Geant4
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

# MARLEY installation directory
set(MARLEY_ROOT "$ENV{HOME}/software/marley"
    CACHE PATH "Path to MARLEY installation")

# Source files
file(GLOB SOURCES CONFIGURE_DEPENDS
    "${PROJECT_SOURCE_DIR}/src/*.cc"
)

file(GLOB HEADERS CONFIGURE_DEPENDS
    "${PROJECT_SOURCE_DIR}/include/*.hh"
)

# Executable
add_executable(exampleB4c
    exampleB4c.cc
    ${SOURCES}
    ${HEADERS}
)

# Include directories
target_include_directories(exampleB4c PRIVATE
    "${PROJECT_SOURCE_DIR}/include"
    "${PROJECT_SOURCE_DIR}/EcoMug"
    "${MARLEY_ROOT}/include"
    "${MARLEY_ROOT}/include/builtin"
)

# Libraries
target_link_libraries(exampleB4c PRIVATE
    ${Geant4_LIBRARIES}
    "${MARLEY_ROOT}/build/lib/libMARLEY.so"
    "${MARLEY_ROOT}/build/lib/libHepMC3.so"
)

# Copy simulation macros into the build directory
file(COPY
    "${PROJECT_SOURCE_DIR}/macros"
    DESTINATION "${PROJECT_BINARY_DIR}"
)
