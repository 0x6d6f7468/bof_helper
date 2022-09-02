import re
import sys
import requests

def find(method):
    ms_uri = f"https://docs.microsoft.com/api/search?search={method}&scope=Desktop&locale=en-us&$filter=scopes/any(t: t eq 'Desktop')&facet=category&$top=1"
    ms_search = requests.get(ms_uri)
    if ms_search.json()["count"] == 0:
        print(f"[-] No API search results for {method}. Quitting.")
        return None

    options = re.search(method, ms_search.text, re.IGNORECASE)
    if options and options.group(0) != method:
        print(f"[!] Case of provided method name {method} does not match found method: {options.group(0)}. Using found method...")
        method = options.group(0)

    doc_uri = ms_search.json()["results"][0]["url"]
    doc_request = requests.get(doc_uri)
    doc_content = doc_request.text
    doc_stripped = re.sub('\r?\n|\t', '', doc_content)

    lib_pattern = re.compile(r'<tr><td><strong>Library</strong></td><td style="text-align: left;">(\w*)')
    dec_pattern = re.compile(f'<pre><code class="lang-cpp">((.*){method}(.*));</code></pre><h2 id="parameters">Parameters</h2>')

    try:
        library = re.search(lib_pattern, doc_stripped).group(1)

    except AttributeError:
        print("[-] Unable to parse library from webpage. Searching for relevant hyperlink...")
        lib_url = None

        for line in doc_content.split("\n"):

            if method in line:
                url_pattern = re.compile(f'<a href="(.*)" data-linktype="absolute-path">{method}</a>')

                try:
                    lib_url = re.search(url_pattern, line).group(1)
                except AttributeError:
                    print("[-] No hyperlinks found. Quitting.")
                    return None

                print(f"[+] Relevant hyperlink found pointing to {lib_url}! Parsing...")
                break

        if not lib_url:
            print("[-] No relevant hyperlink found! Quitting.")
            return None

        doc_request = requests.get(f"https://docs.microsoft.com{lib_url}")
        doc_content = doc_request.text
        doc_stripped = re.sub('\r?\n|\t', '', doc_content)

    finally:
        print("[+] All parsing successful. Continuing...")

    doc_content = ' '.join(doc_stripped.split())
    library = re.search(lib_pattern, doc_content).group(1)

    declaration = re.search(dec_pattern, doc_content).group(1)
    declaration = re.sub(r'\[in\]|\[out\]', '', declaration)
    declaration = ' '.join(declaration.split())
    declaration = declaration.replace('( ', '(')

    return (method, library, declaration)



def main():
    # banner: source: ascii.co.uk/text
    #         font: Ansi Shadow
    print("""
    ██████╗  ██████╗ ███████╗    ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔═══██╗██╔════╝    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║   ██║█████╗      ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝
    ██╔══██╗██║   ██║██╔══╝      ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗
    ██████╔╝╚██████╔╝██║         ██║  ██║███████╗███████╗██║     ███████╗██║  ██║
    ╚═════╝  ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
    [===============================================================]
    [=  Original BOF Helper code by @dtmsecurity                   =]
    [=  Cleaned, modified, and fixed BOF Helper code by moth@bhis  =]
    [===============================================================]
    """)

    if len(sys.argv) != 2:
        print(f"python3 {sys.argv[0]} <API Method>")
        return

    method = sys.argv[1]

    lib_dec = find(method)

    print()

    if not lib_dec:
        print(f"[-] Error: Unable to find reference to {method}")
        return

    method = lib_dec[0]

    if lib_dec[1]:
        print(f"[Library]     Function {method} is probably in library {lib_dec[1]}")

    if lib_dec[2]:
        chunks = lib_dec[2].partition(method)
        rtype = chunks[0]
        signature = ''.join(chunks[1:])
        print(f"[Declaration] DECLSPEC_IMPORT {rtype}{lib_dec[1].upper()}${signature}")



if __name__ == "__main__":
    main()
