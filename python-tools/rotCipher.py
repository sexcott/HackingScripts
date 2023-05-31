#!/usr/bin/env python3
import argparse

ALPHABET = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]

def banner():
	return """Hola"""

def generateKey(rotNum):
        key={}
        for i, ch in enumerate(ALPHABET):
            if (i + int(rotNum)) < len(ALPHABET):
                key[ch] = ALPHABET[i + int(rotNum)]
            else:
                key[ch] = ALPHABET[(i + int(rotNum)) % len(ALPHABET)]
        return(key)

def encrypt(normalStr, key):
        encryptedText = ''
        for word in normalStr.split(' '):
            encryptedText += ' '
            for ch in word:
                if ch in key:
                    encryptedText += key[ch]
                elif ch.lower() in key:
                    encryptedText += key[ch.lower()].upper()
                else:
                    encryptedText += ch
        return(encryptedText)

def guardar(fileName, encryptedText):
	with open(fileName, "a") as f:
		f.write(encryptedText)

def main(s, n, f):
	outputFile = ""
	outputFile += encrypt(s, generateKey(n))+'\n\n'
	print('========= Rotation {} =========='.format(n))
	print('\t'+encrypt(s, generateKey(n)))
	if f != 'no save':
		if f[-4:] != '.txt':f += '.txt'
		guardar(f, outputFile)
		print("saved as {}".format(f))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="a simple Rot cipher")
	parser.add_argument('-nb', '--noBanner', action='store_true', help='no print banner')
	parser.add_argument('-s', '--string', type=str, metavar='', help='string to encode/decode')
	parser.add_argument('-n', '--number', type=int, default=13, metavar='', help='numbers of rotations')
	parser.add_argument('-o', '--output', type=str, metavar='', help="save the output as .txt file", default="no save")

	args = parser.parse_args()

	if not args.noBanner: print(banner())
	try:
		main(args.string, args.number, args.output)
	except Exception as a:
		print("============ ERROR ============")
		print("\n======== {} ======== \n\n\tpls select the string tho encrypt whit -s or --string\n".format(a))
