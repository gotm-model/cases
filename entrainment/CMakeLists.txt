set( configs generic kepsilon )
foreach ( config ${configs} ) 
   add_test( NAME entrainment_${config} COMMAND $<TARGET_FILE:gotm_exe> gotm_${config}.yaml --output_id _${config} WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} )
endforeach()
