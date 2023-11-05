#!/usr/bin/env python3
#run with python3 -m http.server --bind localhost --cgi 8000
#goto http://localhost:8000/

import cgi
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


print("Content-type: text/html")
print("")
arguments = cgi.FieldStorage()
userInput = ""
for i in arguments.keys():
    #print(arguments[i].value)
    userInput += str(arguments[i].value)
    userInput += " "
    #eprint(arguments[i].value)
eprint(userInput)
#print("sad,happy")
try:
    from google.cloud import language_v2


    def analyze_sentiment(userString):
        keywords = ""

        client = language_v2.LanguageServiceClient()

        document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

        language_code = "en"
        document = {
            "content": userString,
            "type_": document_type_in_plain_text,
            "language_code": language_code,
        }

        encoding_type = language_v2.EncodingType.UTF8

        response = client.analyze_sentiment(
            request={"document": document, "encoding_type": encoding_type}
        )

        #print(f"Document sentiment score: {response.document_sentiment.score}")
        #print(f"Document sentiment magnitude: {response.document_sentiment.magnitude}")

        for sentence in response.sentences:
            if (sentence.sentiment.score > 0):
                keywords += "happy "
                keywords += "pleased "
                keywords += "overjoyed "
                keywords += "merry "
                keywords += "jubilant "
                keywords += "satisfied "
                keywords += "content "
                keywords += "upbeat "
            elif (sentence.sentiment.score > 0.9):
                keywords += "ecstatic "
                keywords += "elated "
                keywords += "thrilled "
                keywords += "exhilarated "
            elif sentence.sentiment.score > 0.7 and sentence.sentiment.score < 0.8:
                keywords += "euphoric "
                keywords += "upbeat "
                keywords += "merry "
                keywords += "jubilant "
            elif sentence.sentiment.score > 0.6 and sentence.sentiment.score < 0.7:
                keywords += "radiant "
                keywords += "blissful "
            elif sentence.sentiment.score > 0.5 and sentence.sentiment.score < 0.8:
                keywords += "euphoric "
                keywords += "pleased "
            elif sentence.sentiment.score > 0.4 and sentence.sentiment.score < 0.5:
                keywords += "radiant "
                keywords += "blissful "
                keywords += "satisfied "
                keywords += "content "


            elif (sentence.sentiment.score < -0.7):
                keywords += "sorrow "
                keywords += "melancholy "
                keywords += "woeful "
                keywords += "depressed "
            elif sentence.sentiment.score < -0.5 and sentence.sentiment.score > -0.7:
                keywords += "sad "
                keywords += "dismal "
                keywords += "despondent "
            elif sentence.sentiment.score < -0.3:
                keywords += "crestfallen "
                keywords += "glum "
                keywords += "grim "
            if sentence.sentiment.score < 0:
                keywords += "dejected "
                keywords += "glum "
                keywords += "sad "
                keywords += "disheartened "
                keywords += "forlorn "




            if "sad" in sentence.text.content:
                keywords += "sad "

            angry_words = ["angry", "mad", "irritated", "frustrated", "annoyed"]

            for word in angry_words:
                if word in sentence.text.content:
                    keywords += "angry, "

            if "love" in sentence.text.content:
                keywords += "love, "

            #print(f"Sentence text: {sentence.text.content}")
            #print(f"Sentence sentiment score: {sentence.sentiment.score}")
            #print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")

        # Get the language of the text, which will be the same as
        # the language specified in the request or, if not specified,
        # the automatically-detected language.
        #print(f"Language of the text: {response.language_code}")
        print(keywords)
        eprint(keywords)
        eprint(sentence.sentiment.score)

        #return keywords
    analyze_sentiment(userInput)
except Exception:
    pass

#if __name__ == "__main__":
    #userInput = input("How are you feeling today? ")
    #
