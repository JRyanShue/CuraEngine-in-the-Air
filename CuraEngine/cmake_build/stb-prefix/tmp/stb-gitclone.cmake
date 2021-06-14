
if(NOT "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitinfo.txt" IS_NEWER_THAN "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: 'C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: 'C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "C:/Users/jryan/AppData/Local/GitHubDesktop/app-2.8.3/resources/app/git/cmd/git.exe"  clone --no-checkout --config "advice.detachedHead=false" "https://github.com/nothings/stb.git" "stb"
    WORKING_DIRECTORY "C:/dev/CuraEngine/cmake_build/stb-prefix/src"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://github.com/nothings/stb.git'")
endif()

execute_process(
  COMMAND "C:/Users/jryan/AppData/Local/GitHubDesktop/app-2.8.3/resources/app/git/cmd/git.exe"  checkout d5d052c806eee2ca1f858cb58b2f062d9fa25b90 --
  WORKING_DIRECTORY "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: 'd5d052c806eee2ca1f858cb58b2f062d9fa25b90'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "C:/Users/jryan/AppData/Local/GitHubDesktop/app-2.8.3/resources/app/git/cmd/git.exe"  submodule update --recursive --init 
    WORKING_DIRECTORY "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: 'C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitinfo.txt"
    "C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: 'C:/dev/CuraEngine/cmake_build/stb-prefix/src/stb-stamp/stb-gitclone-lastrun.txt'")
endif()

