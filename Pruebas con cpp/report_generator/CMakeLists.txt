cmake_minimum_required(VERSION 3.12)

project(report_generator)

# find_package(ROOT REQUIRED)
find_package(wkhtmltopdf REQUIRED)

add_executable(root_analysis src/root_analysis.cpp)
target_link_libraries(root_analysis PUBLIC ROOT::Core)

add_executable(wkhtmltopdf_report src/wkhtmltopdf_report.cpp)
target_link_libraries(wkhtmltopdf_report PUBLIC wkhtmltopdf)