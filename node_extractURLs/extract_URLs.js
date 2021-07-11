/*
The program should, given a list of HTTP and HTTPS URLs as arguments, retrieve each URL as a document
and return the number of UNIQUE external URLs referenced in the document.
Your program must parse HTML document responses, although you may optionally choose to also parse other
document types for external URLs.  
For example, an invocation with a list of URLs should look something like:
"program http://example.com http://www.columbia.edu/~fdc/sample.html". 
For each VALID URL, your program should print a line consisting of the URL and the number of external links
in the retrieved document, separated by a space, like "http://example.com 1". 
Each URL should be printed on its own line of the output. In a comment at the top of your main program file.
*/

const got = require('got');
const cheerio = require('cheerio');
const prompt = require('prompt-sync')();

const urls = prompt("Kindly input the list of URLs you wanna crawl:");
const urls_arr = urls.split(" ");
//const urls = "http://www.google.com"
function isValid(url){
    // console.log(`checking validity of ${url}`);
    let valid_url;
    try{
        vaild_url = new URL(url);
    }catch(_){
        return false;  
    }
    let validity = ((vaild_url.protocol === "http:" || vaild_url.protocol === "https:")
                    && Boolean(vaild_url.hostname));
    // console.log("+++++++++++++++"+validity+"\n");
    return validity;
}

const extract_URLs = async (url) => {
    try {
        // Fetching HTML
        const response = await got(url);
        const html = response.body;
        // Using cheerio to extract <a> tags
        const $ = cheerio.load(html);
        // this is a mass object, not an array
        const links_object = $('a');
        // Collect the "href" and "title" of each link and add them to an array
        const external_links = [];
        links_object.each((index, element) => {
            let href = $(element).attr('href');
            if(isValid(href)){
                let parsed_href = new URL(href);
                // console.log(`parsed_href = ${parsed_href}`);
                // console.log(`parsed_href.hostname =  ${parsed_href.hostname}`);
                let parsed_url = new URL(url);
                // console.log(`parsed_url = ${parsed_url}`);
                // console.log(`parsed_url.hostname =  ${parsed_url.hostname}`);
                // console.log(`external_links = ${external_links}`);
                href = parsed_href.protocol + "//" + parsed_href.hostname; 
                if((parsed_url.hostname != parsed_href.hostname )&& 
                            (!(external_links.includes(href)))){
                    external_links.push(href);
                } 
            }
    });
    console.log(`${url} -> ${external_links.length}`);
    // console.log(`external_links = ${external_links}`);
  }catch(error) {
    console.log(error.response.body);
  }
};


for(let url of urls_arr){
    if(isValid(url)){
        extract_URLs(url);
    }
}


