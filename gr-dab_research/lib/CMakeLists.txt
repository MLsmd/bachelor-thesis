# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND dab_research_sources
    delayed_correlation_cc_impl.cc
    measure_freq_offset_cf_impl.cc
    qpsk_demod_vcvb_impl.cc
    crc16.cc
    measure_fib_error_rate_impl.cc 
    firecode-checker.cpp
    firecode_check_bb_impl.cc)

set(dab_research_sources "${dab_research_sources}" PARENT_SCOPE)
if(NOT dab_research_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT dab_research_sources)

add_library(gnuradio-dab_research SHARED ${dab_research_sources})
target_link_libraries(gnuradio-dab_research ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-dab_research PROPERTIES DEFINE_SYMBOL "gnuradio_dab_research_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-dab_research PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-dab_research
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_dab_research_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_dab_research.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_dab_research.cc
)

add_executable(test-dab_research ${test_dab_research_sources})

target_link_libraries(
  test-dab_research
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-dab_research
)

GR_ADD_TEST(test_dab_research test-dab_research)
