# A tool that counts unique external links referenced in a given URL document
- To run the js code: <br />
    $ node extract_URLs.js <br />
- You will be prompted to input the array of URLs you wanna crawl<br />
    (DO NOT use quotes to wrap the list)<br />
    ex: Kindly input the list of URLs you wanna crawl:http://www.google.com https://wikipedia.com"
    
The program, given a list of HTTP and HTTPS URLs as arguments, retrieves each URL as a document and returns the number of unique external URLs referenced in the document. It parses HTML document responses. For example, an invocation with a list of URLs should look something like "program http://example.com http://www.columbia.edu/~fdc/sample.html". For each valid URL, the program prints a line consisting of the URL and the number of external links in the retrieved document, separated by a space, like "http://example.com -> 1".