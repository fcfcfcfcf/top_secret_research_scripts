#include "sink_file2.hpp"
#include "taint_file1.hpp"

sink_file2::sink_file2()
{
}

/* static */ int sink_file2::calculate_important_value()
{
        return ( 2 * taint_file1::get_tainted_value() );
}

