# Beacon Object File (BOF) Creation Helper

Cobalt Strike has now introduced the concept of Beacon Object File (BOF) as a way to rapidly extend its Beacon agent. This involves making and compiling a C program. These programs are much like normal C programs but with a few tweaks to make it work with Beacon as described in this video: [https://youtu.be/gfYswA_Ronw](https://youtu.be/gfYswA_Ronw).

This script has been written to make the process of making BOFs slightly easier. It tries automatically do what is described in the above video, by identifying which library in which the method exists via Microsoft's [docs.microsoft.com](http://docs.microsoft.com) endpoint. It also searches the relevant web page for function declarations.

Note: The Microsoft endpoint and dorks used are liable to change which may break this script. Ensure that the full method name is supplied for best results.

**Updates**
- Fixed API reference (links weren't working)
- "Cleaned" code
- Removed `find_declaration` function
- Removed references to dead mingw Git link
- Implemented regex matches for specified method
- Implemented case-insensitivity for specified method
- Tweaked output
- Added error handling
- Updated README

**Dependencies**

- python3
- requests python library

**Usage**

`python3 bof_helper.py <API Method>`

**Example**

```
$ python3 bof_helper.py DsGetDcNameA

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
    
[!] Case of provided method name DsGetDcNameA does not match found method: DsGetDcNameA. Using found method...
[-] Unable to parse library from webpage. Searching for relevant hyperlink...
[+] Relevant hyperlink found pointing to /en-us/windows/win32/api/dsgetdc/nf-dsgetdc-dsgetdcnamea! Parsing...
[+] All parsing successful. Continuing...

[Library]     Function DsGetDcNameA is probably in library NetApi32
[Declaration] DECLSPEC_IMPORT DSGETDCAPI DWORD NETAPI32$DsGetDcNameA(LPCSTR ComputerName, LPCSTR DomainName, GUID *DomainGuid, LPCSTR SiteName, ULONG Flags, PDOMAIN_CONTROLLER_INFOA *DomainControllerInfo)
```

**References**

- [https://www.cobaltstrike.com/help-beacon-object-files](https://www.cobaltstrike.com/help-beacon-object-files)
- [https://youtu.be/gfYswA_Ronw](https://youtu.be/gfYswA_Ronw).

**Author**

[@dtmsecurity](https://twitter.com/dtmsecurity)
[moth](https://github.com/0x6d6f7468)
