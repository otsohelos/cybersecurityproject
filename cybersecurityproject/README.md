This project is a course work for the University of Helsinki cybersecurity course. It is meant to show an insecure project, with the vulnerabilities and their possible fixes detailed below.

# Usage
Clone the project on your local computer. Navigate to the project folder and run the command
```python3 manage.py runserver```

Open the URL that your terminal application gives you. Three user accounts have already been created for testing purposes, with the following usernames and passwords:

admin - allyourbase
bonnie - totaleclipse
freddie - isthisthereallife

# Security issues
The following security issues are modeled by the [OWASP 2021 top ten list](https://owasp.org/www-project-top-ten/).

## Cryptographic Failures
### The problem
In the initial commit, settings.py was leaked to Github and can still be found in git history. It has since been removed, but a resourceful attacker might find it, since previous commits have not been edited. settings.py contains e.g. the secret key to the program, which is classified as sensitive information, as well as a list of installed apps, which could lead an attacker to possible vulnerabilities in the program. OWASP clearly states that it is a security flaw to store passwords or other sensitive information in clear text, and that sensitive data should be identified and classified. Any passwords or cryptographic keys should not be in version control.

### How it could be fixed
This flaw could have been fixed with more careful setting up of the gitignore file and monitoring what is committed in each commit, noticing the inclusion of settings on time and adding it to ignored files. After the mistake has already been made, [the Github docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) provide ways of removing the sensitive data from the repo.


## Injection
### The problem
The messages that users can send to each other are not sanitized. This allows for the users to send messages containing HTML and JavaScript code, which in turn exposes the program to many vulnerabilities, including cross site scripting. OWASP states that user-supplied data should be validated, filtered, or sanitized by the application.

### How it could be fixed
Django's built-in methods sanitize the data by default. So instead of using the rather clunky method that I have written for posting a new message, the function could be two simple lines:

```
  target = User.objects.get(username=request.POST.get('to'))
  Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
```

Beside being clener and nicer to read, this fixes the security vulnerability. This is a case where I had to go to extra lengths to make the application less secure, for the purposes of this exercise.


## Identification and Authentication Failures
### The problem
The repo is uploaded with a database that has an admin user and two other users already on the database. Granted, this is done for the ease of testing (as this database doesn't really include any sensitive data), but it still constitutes a security flaw. Additionally, password requirements are quite lax. The following password requirements are in effect:

* passwords can't be too similar to the user's other personal information
* passwords must contain at least 8 characters
* passwords can't be a commonly used password
* passwords can't be entirely numeric.

These are good requirements to have but insufficient. For example, the admin password listed above is all lowercase, and is a common enough expression.

### How it could be fixed
The database should not be uploaded in the repo, at least not with users already added. A more secure approach to passwords would be to require, in addition to the requirements already in effect, the following:

* passwords must contain both uppercase and lowercase letters
* passwords must contain at least one number
* passwords must contain at least one special character.

Admin password should be changed immediately to a more secure one that follows the above guidelines. OWASP states that weak passwords are a security flaw.


## Broken Access Control
### The problem
The index page and adding a message have a @login_required tag, but the latest messages page does not. This means that if an attacker knows or guesses a user's id, they can navigate to /latest/{id} and read the messages that user has received, all without being logged in, or while being logged in as another user. Viewing another user's account without being logged in should not be allowed; OWASP guidelines state that "(p)ermitting viewing or editing someone else's account, by providing its unique identifier" is an access control vulnerability.

### How it could be fixed
The latest messages page should have @login_required tag.


## Security Logging and Monitoring Failures
### The problem
OWASP suggests that, for example, logins, logouts, and failed logins should be logged for monitoring purposes. Relatedly, many subsequent failed login attempts should be monitored and a throttling mechanism should be in place to prevent brute force attacks. Currently, there is no logging mechanism and brute force attacks are not monitored for.

### How it could be fixed
The package django.contrib.auth.signals should be used to log logins, logouts, and failed logins. A callback function could receive information on these, and a table in the database should record information on logins. A good starting point for preventing brute force attacks would be the package django-defender.