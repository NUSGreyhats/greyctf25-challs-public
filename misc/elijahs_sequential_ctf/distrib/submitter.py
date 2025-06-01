# usage: python3 submitter.py <code_file> <ip> <port>
#!/usr/bin/env python3
import sys
import base64
import os
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 submitter.py <code_file> <ip> <port>")
        sys.exit(1)
    
    code_file = sys.argv[1]
    ip = sys.argv[2]
    port = sys.argv[3]
    
    # Check if code file exists
    if not os.path.exists(code_file):
        print(f"Error: Code file '{code_file}' not found")
        sys.exit(1)
    
    # Read the code file
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading code file: {e}")
        sys.exit(1)
    
    # Convert to base64
    code_bytes = code_content.encode('utf-8')
    base64_code = base64.b64encode(code_bytes).decode('ascii')
    
    # Get file extension
    file_extension = Path(code_file).suffix[1:]  # Remove the dot
    if not file_extension:
        print(f"Warning: No file extension found for '{code_file}'")
        file_extension = ""
    
    # Write to submission file
    try:
        with open('submission', 'w') as f:
            f.write(base64_code + '\n')
            f.write(file_extension + '\n')
            f.write('\n')  # Additional newline
    except Exception as e:
        print(f"Error writing submission file: {e}")
        sys.exit(1)
    
    # Execute cat submission | nc IP PORT
    try:
        cmd = f"cat submission | nc {ip} {port}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Print output if any
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        # Exit with the same code as nc
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"Error executing nc command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()