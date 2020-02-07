#include <iostream>
#include "test_file1.hpp"
#include "test_file2.hpp"

int main()
{
	test_file1* testObj1 = new test_file1();
	testObj1->test_function();

	test_file2::test_function();

	return( 0 );
}
