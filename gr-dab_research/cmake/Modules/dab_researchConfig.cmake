INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_DAB_RESEARCH dab_research)

FIND_PATH(
    DAB_RESEARCH_INCLUDE_DIRS
    NAMES dab_research/api.h
    HINTS $ENV{DAB_RESEARCH_DIR}/include
        ${PC_DAB_RESEARCH_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    DAB_RESEARCH_LIBRARIES
    NAMES gnuradio-dab_research
    HINTS $ENV{DAB_RESEARCH_DIR}/lib
        ${PC_DAB_RESEARCH_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(DAB_RESEARCH DEFAULT_MSG DAB_RESEARCH_LIBRARIES DAB_RESEARCH_INCLUDE_DIRS)
MARK_AS_ADVANCED(DAB_RESEARCH_LIBRARIES DAB_RESEARCH_INCLUDE_DIRS)

