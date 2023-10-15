add_executable(matmul
    matmul.cc)

target_link_libraries(matmul
    PRIVATE OMPC::Runtime)

add_executable(matmuldm
    matmuldm.cc)

target_link_libraries(matmuldm
    PRIVATE OMPC::Runtime)
