#!/bin/bash

# MAC address of the Bluetooth device
DEVICE="8C:DE:52:DD:84:FE"

# Use gatttool to discover characteristics and map UUIDs to handles
echo "Discovering services and characteristics..."
mapfile -t characteristics < <(timeout --foreground 10s gatttool -b $DEVICE --characteristics | awk -F 'handle = 0x|, char properties = 0x|, char value handle = 0x| uuid = ' '{print $3 " " $5}')

echo "Discovered characteristics with handles:"
printf "%s\n" "${characteristics[@]}"

# Loop over discovered characteristics
for line in "${characteristics[@]}"; do
    read -r handle uuid <<<"$line"
    
    # Check if handle and UUID are valid
    if [[ -n "$handle" && -n "$uuid" ]]; then
        echo "Attempting to write and read from UUID $uuid (handle $handle)..."
        
        # Write "ATZ" command to each handle and then read from it
        echo -n "ATZ\r" | gatttool -b $DEVICE --char-write-req --handle=$(printf "%d" "0x$handle") --value=$(xxd -ps) > /dev/null
        
        # Handling potential failures during write
        if [ $? -eq 0 ]; then
            echo "Written to handle $handle successfully."
            output=$(gatttool -b $DEVICE --char-read --handle=$(printf "%d" "0x$handle"))
            echo "Read from UUID $uuid (handle $handle): $output"
        else
            echo "Failed to write to handle $handle."
        fi
    fi
done


# #!/bin/bash

# # MAC address of the Bluetooth device
# DEVICE="8C:DE:52:DD:84:FE"

# # Discover all characteristics and their handles, capturing output
# echo "Discovering characteristics..."
# characteristics=$(timeout --foreground 10s gatttool -b $DEVICE --characteristics)

# echo "Attempting to write and read from each characteristic..."

# # Loop through the lines of characteristics output
# echo "$characteristics" | while IFS=, read -r a b; do
#     handle=$(echo "$a" | awk -F'handle = 0x' '{print $2}' | awk '{print $1}')
#     uuid=$(echo "$b" | awk -F'uuid = ' '{print $2}')
    
#     if [[ -n "$handle" && -n "$uuid" ]]; then
#         echo "-------------------------------------"
#         echo "Handle: $handle"
#         echo "0x$(echo $handle)"
#         echo "UUID: $uuid"

#         # Convert "ATZ\r" to hex and write to the handle
#         command_hex=$(echo -n "ATZ\r" | xxd -ps | tr -d '\n')
#         write_output=$(gatttool -b $DEVICE --char-write-req --handle="0x$(echo $handle)" --value="$command_hex" 2>&1)
        
#         # Check if the write was successful
#         if [[ "$write_output" == *"successfully"* ]]; then
#             echo "Write successful to handle $handle"
#             # Read from the handle
#             read_output=$(gatttool -b $DEVICE --char-read --handle="0x$(echo $handle)" 2>&1)
#             echo "Read from handle $handle: $read_output"
#         else
#             echo "Write to handle $handle failed: $write_output"
#         fi
#     fi
# done
