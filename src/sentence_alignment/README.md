How To Run The Sentence Alignment for Cabinet Speeches:
===========================================================================
OS Requirements:
----------------
-   Ubuntu 20.04
-   Ubuntu 22.04 does not support python 3.8 so do not use it.

Required Python Version:
------------------------
- Currently, only python 3.8 has successfully been able to run the sentence alignment without issues. 
- However feel free to test with other python versions.

Ubuntu Commands to Run:
-----------------------
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install build-essential
sudo apt-get install cmake
sudo apt-get install zip
```

Install Python Requirements:
----------------------------
After running the commands above, go to the root of the project and run the following command:      
```
pip install -r requirements.txt
```

Change Line Endings For ALl .sh Files:
-------------------------------------
- Change the the line break for every .sh in the src/sentence_alignment/LASER directory for `CRLF` to `LF`

How To Run the Script:
----------------------
- Go to the following directory `src/sentence_alignment/`
- Run the following command:  ```python3 main.py```

Author(s):
----------
- Isheanesu Joseph Dzingirai