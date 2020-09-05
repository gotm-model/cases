cmake_minimum_required(VERSION 3.0)

project(gotm-cases VERSION 2.5.0 LANGUAGES Fortran)

enable_testing()

mark_as_advanced( FORCE GOTM_BASE )
find_path( GOTM_BASE CMakeLists.txt HINTS ENV GOTM_BASE PATHS extern/gotm DOC "Path to GOTM source directory." )
if ( ${GOTM_BASE} STREQUAL "GOTM_BASE-NOTFOUND" )
    message( " " )
    message( "The GOTM source code was not found - you must either:" ) 
    message( "  1) set the environmental variable GOTM_BASE to point to the GOTM source code" ) 
    message( "  2) checkout the GOTM source code as a submodule to the cases" ) 
    message( " " )
    message( " " )
    message( FATAL_ERROR )
else()
    message( "Using GOTM source code from: " ${GOTM_BASE} ) 
endif()

set( GOTM_EMBED_VERSION ON )

add_subdirectory( ${GOTM_BASE} gotm )

set( cases channel nns_annual entrainment )
foreach ( case ${cases} )
   add_test( NAME ${case} COMMAND $<TARGET_FILE:gotm_exe> WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${case} )
endforeach()


