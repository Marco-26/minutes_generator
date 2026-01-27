import sys
import os
import argparse

from minutes_generator import MinutesGenerator

parser = argparse.ArgumentParser(description='Generate meeting minutes from a transcript file.')
parser.add_argument('path', type=str, help='Path to the transcript file')

if __name__ == "__main__":
  args = parser.parse_args()
  
  if not os.path.exists(args.path):
    print("File doesn't exist...")
    sys.exit()
    
  min_generator = MinutesGenerator(max_tokens=10000)
  min_generator.generate(args.path)