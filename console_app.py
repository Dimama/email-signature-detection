"""python console_app.py email_body_filename [sender_filename]
"""

import sys
from os import path
from classifier import Classifier, ClassifierException
from const import CLASSIFIER_PATH, EXTRACTOR_PATH


def delete_signature(email_filename, sender_filename=None):
    """Возвращает текст письма и подпись, если подпись не найдена,
    то второе значение None
    """

    with open(email_filename, 'r') as f_email:
        email_lines = f_email.read().split('\n')

    if sender_filename:
        with open(sender_filename, 'r') as f_sender:
            sender = f_sender.readline()
    else:
        sender = ''

    try: 
        c = Classifier(CLASSIFIER_PATH, EXTRACTOR_PATH)
    except ClassifierException as e:
        raise e
    
    with_sign = c.check_email_for_signature(email_lines, sender)
    
    if with_sign:
        signature_lines = []
        other_lines = []

        email_lines = [l for l in email_lines if l.strip()]
        for line in email_lines:
            if c.check_line_for_signature(line, sender):
                signature_lines.append(line)
            else:
                other_lines.append(line)
        
        return other_lines, signature_lines
        
    else: 
        return email_lines, None

    
def main():
    try:
        email_filename = sys.argv[1]
    except IndexError:
        print("Set email filename")
        return

    try:
        sender_filename = sys.argv[2]
    except IndexError:
        sender_filename = None

    if not path.exists(email_filename):
        print("File '{}' not exist".format(email_filename))
        return

    if sender_filename and not path.exists(sender_filename):
        print("File '{}' not exist".format(sender_filename))
        sender_filename = None

    try:
        text, signature = delete_signature(email_filename, sender_filename)
    except ClassifierException as e:
        print("Exception:", str(e))
        return

    print("Text lines: ")
    for line in text:
        print(line)
    
    if signature:
        print("\nSiganture Lines")
        for line in signature:
            print(line)
    else:
        print("\nSignature not found in email")
        
if __name__ == '__main__':
    main()