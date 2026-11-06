#!/bin/bash

# Quark Anticheat - Test Script Without Quark Protection
# Verifies that the game refuses to start when the anticheat daemon is NOT
# running, so there is never an unprotected process for a cheat to attack.

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}=== Quark Anticheat: Starting Test WITHOUT Quark Protection ===${NC}"

# 1. Compile the project
echo "Compiling components..."
if ! make > /dev/null; then
    echo -e "${RED}Error: Compilation failed!${NC}"
    exit 1
fi
echo -e "${GREEN}Compilation successful.${NC}\n"

# 2. Make sure no daemon is reachable. Socket activation (quark.socket) would
# start one on connect, so this test cannot run while the socket unit is active.
if [ -S /tmp/quark.sock ]; then
    echo -e "${RED}Error: /tmp/quark.sock exists, so a Quark daemon is reachable.${NC}"
    echo "Stop it first (e.g. 'sudo systemctl stop quark.socket quark.service')."
    exit 1
fi

# 3. Start the Mock Game. It must exit on its own with a non-zero status.
echo "Starting Mock Game without the Quark daemon..."
rm -f game_no_quark.log
timeout 10 ./game_target/game < /dev/null > game_no_quark.log 2>&1
GAME_EXIT=$?

echo -e "\n${BOLD}--- Game Log ---${NC}"
cat game_no_quark.log
echo -e "----------------\n"

# 4. Verification
echo -e "${BOLD}=== Verification ===${NC}"
if [ $GAME_EXIT -eq 124 ]; then
    echo -e "${RED}FAIL: The Mock Game kept running without Quark protection.${NC}"
    exit 1
fi
if [ $GAME_EXIT -eq 0 ] || ! grep -q "Refusing to run unprotected" game_no_quark.log; then
    echo -e "${RED}FAIL: The Mock Game did not refuse to start (exit code $GAME_EXIT).${NC}"
    exit 1
fi
if grep -q "Health address:" game_no_quark.log; then
    echo -e "${RED}FAIL: The Mock Game reached its game loop before refusing.${NC}"
    exit 1
fi

echo -e "${GREEN}${BOLD}CONFIRMED: The Mock Game refused to start without Quark (exit code $GAME_EXIT); there is no unprotected process to cheat on.${NC}"
rm -f game_no_quark.log
exit 0
