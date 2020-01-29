#include "sink_file1.hpp"
#include "taint_file1.hpp"
#include "taint_file2.hpp"

sink_file1::sink_file1()
{
}

/* static */ int sink_file1::calculate_important_value()
{
        return ( 5 * taint_file1::get_tainted_value() + taint_file2::get_tainted_value() );
}

/* static */ void sink_file1::consume_tainted_value( int tainted_value )
{
    int new_tainted_value = tainted_value + 5;
}
