add_test( NAME channel COMMAND $<TARGET_FILE:gotm_exe> WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} )
add_custom_target( test_channel )
