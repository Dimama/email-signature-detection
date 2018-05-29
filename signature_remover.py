from classifier import Classifier, ClassifierException
from const import CLASSIFIER_PATH
from email_extractor import EmailException, EmailWarning, EmailExtractor

class SignatureRemover():
    
    @staticmethod
    def delete_signature(address, password, index):
    
        try:
            email_lines, sender =  EmailExtractor.extract_email_lines_and_sender(address, password, index)
        except EmailException as e:
            raise e
        except EmailWarning as e:
            raise e

        try: 
            c = Classifier(CLASSIFIER_PATH)
        except ClassifierException as e:
            raise e

        without_sign_lines = []

        for line in email_lines:
            if not (len(line) > 0 and c.check_line_for_signature(line, sender)):
                without_sign_lines.append(line)

        return email_lines, without_sign_lines
            