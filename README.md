@Name: Credit Card Tokenisation using Python
@Author: Noel Singh
@Date: 14th April 2025
@Description: The following application is used to create a unique token for credit cards which belong to different
policies / accounts. The credit cards need to be in a 16-digit format, and are generated using random values within
a given range.

--------------------------------------------------------------------------------------------------------------------
@version: 1.0
@date = 14th April 2025
@includes:
    > Creation of test data i.e. policy numbers, credit card numbers and expiration dates
    > Generation of bulk records for testing
    > Checks performed on data including:
        - special characters in data
        - data lengths and consistency
--------------------------------------------------------------------------------------------------------------------
@version: 2.0
@date: 21st April 2025
@includes:
    > separate module for creation of test data to use for tokenisation
    > logger_config.py creation to reuse across modules.
    > separate fpe and aes modules
    > update to main function
--------------------------------------------------------------------------------------------------------------------
logger_config.py
    > logging configuration that is imported and used by subsequent scripts.

simulated_data.py
    > simulates credit card numbers, expiration dates and policy numbers for the sample size of values the user defines.

fpe_encryption.py
    > Encryption algorithm used with the fpe_key to encrypt the credit card numbers preserving the length expected.

aes_encryption.py
----------------



----------------
# Comments
These are just my own comments and thoughts based on recent experience. You 
have to decide if they are appropriate for you. Happy to discuss

- as you know, I'm not a great fan of pip as the **dependency manager**, but 
  it's a personal choice. I used to advocate for Poetry, but I'm starting 
  to use UV now. I find both of them more consistent than pip and venv, but 
  whatever works for you.
- I think you need a **gitignore** file to ignore any of the files that will 
  junk up your repo. I've added one using the GitHub default template
- **README**: you have a read me file, but I'd recommend considering how a 
  user should install and use your software. Build out a README that
  covers the installation and usage of your software.
- **licence**: you should always have a licence of some sort that covers 
  your software. I personally default to the MIT licence, but you can 
  choose whatever you want. Just make sure that you have one.
- doc strings: every function should have a doc-string that describes 
  what the function does, what the inputs are and what the outputs are. Not 
  strictly necessary but good practice.
- **type hints**: i see that you currently dont' use type hints. I would 
  recommend using them. They are not strictly necessary, but they do help 
  with readability and understanding of the code.
- **tests**: I can't see any unit tests yet. I would strongly suggest 
  adding unit tests. once you have decent coverage, extend to include 
  integration tests and whatever other tests you need to ensure that your 
  software is behaving the way you expect it to.
- **pre-commit hooks**: tests are a pain to maintain, and i always find myself 
  falling behind because i forget to run them. so i use 
  pre-commit hooks to run 3 things before I commit any code: tests, linting 
  and formatting. I use Pytest, Black and MyPy, for this.
- **deployment**: how do you intend users to use your software? If they are 
  other coders and are going t run it from their own IDE then that's fine, 
  but if you want to deploy it to cloud or package as an .exe file, then we 
  need to build that out.
- **exception handling**: need more. I've added a little