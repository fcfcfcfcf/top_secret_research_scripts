#include "test_file1.hpp"
#include "test_file3.hpp"
#include <iostream>

test_file1::test_file1()
{
	test_file3 testObj3;
	testObj3.test_function();
}

void test_file1::test_function()
{
	std::cout << "\n\nTEST FUNCTION 1\n\n" << std::endl;
}
