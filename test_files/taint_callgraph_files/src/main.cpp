#include "sink_file1.hpp"
#include "sink_file2.hpp"
#include "sink_file3.hpp"

#include "taint_file1.hpp"

int main()
{
	sink_file1::calculate_important_value();
	sink_file2::calculate_important_value();
	sink_file3::calculate_important_value();

    int tainted_data = taint_file1::get_tainted_value();
    sink_file1::consume_tainted_value( tainted_data );

	return( 0 );
}
