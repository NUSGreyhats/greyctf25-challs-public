#!/usr/bin/python3
import os
import sys
import json
import subprocess
import base64

def process_data(source_path):
    """
    Run ljudge on the provided source file and return its JSON result.
    """
    # Load testcases
    with open('/testcases/testcases.json', 'r', encoding='utf-8') as tc_file:
        testcases = json.load(tc_file)

    # Build the ljudge command
    cmd = [
        'ljudge',
        '--max-cpu-time', '1.0',
        '--max-memory', '32m',
        '--user-code', source_path
    ]

    # Append each testcase
    for tc in testcases:
        inp = tc.get('input')
        out = tc.get('output')
        cmd.extend(['--testcase', '--input', inp, '--output', out])

    # Execute ljudge
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Parse or forward error
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            'error': 'Failed to parse JSON output',
            'stdout': proc.stdout,
            'stderr': proc.stderr
        }

def main():
    try:
        # Read base64-encoded user code from stdin
        b64_data = input()
        sfx = input()
        # print(f"b64: {b64_data}, sfx: {sfx}")
        
        if not b64_data:
            raise ValueError("No input received. Expected base64-encoded code.")

        # Decode Base64 to bytes
        try:
            code_bytes = base64.b64decode(b64_data)
            # print(f"b64 decoded: {code_bytes}")
        except (base64.binascii.Error, ValueError) as e:
            raise ValueError(f"Invalid base64 input: {e}")

        # Write decoded code to a temporary file
        tmp_dir = '/tmp'
        os.makedirs(tmp_dir, exist_ok=True)
        dest_path = ''
        if sfx == 'py':
            dest_path = 'code.py'
        elif sfx == 'cpp':
            dest_path = 'code.cpp'
        elif sfx == 'c':
            dest_path = 'code.c'
        elif sfx == 'java':
            dest_path = 'code.java'
        else:
            print("Unsupported suffix")
            exit()
        dest_path = os.path.join(tmp_dir, dest_path)
        with open(dest_path, 'wb') as dst:
            dst.write(code_bytes)

        # Process the code with ljudge
        result = process_data(dest_path)
        # Output JSON result to stdout
        print(json.dumps(result))
        solved = True 
        if not result.get('testcases'):
            exit()
        for res in result['testcases']:
            if res.get('result') and res.get('result') == 'ACCEPTED':
                continue
            else:
                solved = False
                break 
        if solved:
            print("grey{1m_s0m3whaT_oF_4_c0mp3tit1vE_pR0gramm3R_mYsELF}")

    except Exception as e:
        error_msg = {'error': str(e)}
        print(json.dumps(error_msg))

if __name__ == '__main__':
    main()
