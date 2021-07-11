# A tool that counts unique external links referenced in a given URL document
- To run the python code: <br />
    $ pip3 install -r pythonCodeRequirements.txt <br />
    $ python3 extract_URLs.py "A GIVEN LIST OF URLS". <br />
        ex: $ python3 extract_URLs.py "https://github.com https://facebook.com"
    
The program, given a list of HTTP and HTTPS URLs as arguments, retrieves each URL as a document and return the number of unique external URLs referenced in the document. It parses HTML document responses. For example, an invocation with a list of URLs should look something like "program http://example.com http://www.columbia.edu/~fdc/sample.html". For each valid URL, the program prints a line consisting of the URL and the number of external links in the retrieved document, separated by a space, like "http://example.com -> 1".