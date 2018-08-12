#include "humblelogging/api.h"
HUMBLE_LOGGER(L, "test");

int main() {
	HL_INFO(L, "testing");
}
